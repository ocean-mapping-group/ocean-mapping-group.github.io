"""
Pure-Python Binary Reader, JHC_header (edhead.c / make_blank.c) Interpreter & Writer,
GDAL Zero-Copy VRT Generator, and Workspace Scanner for UNB Ocean Mapping Group (OMG)
Multibeam Sonar Files.

Tested against real Kongsberg EM124 (.kmall / .kmwcd) Antarctica survey data
(02_Bransfield, RV Almirante Viel, Julian Days 74-81) and verified against
compiled OMG binaries (make_blank, tor4, weigh_grid, r4to8bit, addSUN, edhead).
"""

from datetime import datetime, timezone
import json
import math
import os
import struct
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


JHC_OMG_RECLEN = 1024
JCU_BINNAV_RECLEN = 48
OMG_HDCS_SUMMARY_HEADER_SIZE = 96
OMG_HDCS_SUMMARY_V4EXTRA_SIZE = 168
OMG_HDCS_BOUNDS_SIZE = 32
OMG_HDCS_ATTITUDE_SUMMARY_SIZE = 44

WGS84_A = 6378137.0
WGS84_E = 0.0818191908426215


@dataclass
class JhcHeaderInfo:
    filepath: str
    magic: str
    dx: int
    dy: int
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    xstep: float
    ystep: float
    data_type: int          # 1=8bit (uint8), 2=16bit (int16), 3=float (float32)
    rgb_bw: int             # 1=red, 2=green, 3=blue, 4=greyscale
    projection: int         # 0=None, 1=Mercator, 2=UTM, 3=Geographic, 4=RotUTM, 5=RotMerc, 6=NBStereo, 7=PolarStereo, 8=RotNBStereo, 9=RotPolarStereo, 10=LCC, 11=RotLCC
    ellipsoid: int          # 1=WGS84, 2=NAD27, 3=CLK66, 4=AGD84, 5=SPHER
    proj_merid: float
    sun_elev: float
    sun_azi: float
    sun_exag: float
    view_elev: float
    view_azi: float
    view_exag: float
    max_value: float
    min_value: float
    hemisphere: str         # "N" (0) or "S" (1)
    label_1: str
    proj_lat: float = 0.0
    lat_std1: float = 0.0
    lat_std2: float = 0.0
    false_easting: float = 0.0
    false_northing: float = 0.0

    @property
    def data_type_name(self) -> str:
        return {1: "Byte (8-bit)", 2: "Int16 (16-bit)", 3: "Float32 (32-bit)"}.get(
            self.data_type, f"Unknown({self.data_type})"
        )

    @property
    def gdal_data_type(self) -> str:
        return {1: "Byte", 2: "Int16", 3: "Float32"}.get(self.data_type, "Float32")

    @property
    def bytes_per_pixel(self) -> int:
        return {1: 1, 2: 2, 3: 4}.get(self.data_type, 4)

    @property
    def nodata_value(self) -> float:
        # In OMG make_blank / weigh_grid / r4to8bit / addSUN:
        #   - .8bit arrays from r4to8bit write 0 (*q = 0) for ungridded background pixels
        #   - .sun / .mos / 8-bit .blank arrays write 255 for ungridded background pixels
        #   - float32 arrays (data_type == 3, .r4 / .blank) write 0.0 for background (-ignore 0.0)
        if self.data_type == 1:
            if self.filepath.lower().endswith(".8bit") and self.sun_elev == 0.0:
                return 0.0
            return 255.0
        return 0.0

    @property
    def projection_name(self) -> str:
        return {
            0: "Unprojected / Curtain Grid",
            1: f"Mercator Orthogonal (Std Parallel {self.proj_merid:.4f}°)",
            2: f"UTM Orthogonal (CM {self.proj_merid:.1f}°, {self.hemisphere})",
            3: "Geographic (Decimal Degrees)",
            4: f"Rotated UTM (CM {self.proj_merid:.1f}°, Rot {self.ymax:.2f}°)",
            5: f"Rotated Mercator (Std Parallel {self.proj_merid:.4f}°, Rot {self.ymax:.2f}°)",
            6: "New Brunswick Stereographic (EPSG:2953)",
            7: f"Polar Stereographic ({self.hemisphere})",
            8: f"Rotated NB Stereographic (Rot {self.ymax:.2f}°)",
            9: f"Rotated Polar Stereographic ({self.hemisphere}, Rot {self.ymax:.2f}°)",
            10: f"Lambert Conformal Conic ({self.lat_std1:.1f}°/{self.lat_std2:.1f}°)",
            11: f"Rotated Lambert Conformal Conic (Rot {self.ymax:.2f}°)",
        }.get(self.projection, f"Projection({self.projection})")


@dataclass
class MergedSummaryInfo:
    filepath: str
    file_id: str
    file_version: int
    tool_type: int
    num_profiles: int
    num_depths: int
    time_scale_usec: int
    ref_time_100s: int
    min_time_epoch: float
    max_time_epoch: float
    min_lat_deg: float
    max_lat_deg: float
    min_lon_deg: float
    max_lon_deg: float
    min_obs_depth_m: float
    max_obs_depth_m: float
    status_flags: int
    total_profile_bytes: int = 0
    total_beam_bytes: int = 0


@dataclass
class LineProcessingStatus:
    line_name: str
    subdir: str = ""
    has_raw_kmall: bool = False
    has_raw_kmwcd: bool = False
    has_raw_all: bool = False
    has_raw_wcd: bool = False
    has_merged: bool = False
    has_watercol: bool = False
    has_wc_phase1: bool = False
    has_wc_phase2: bool = False
    has_vert_prof: bool = False
    has_param: bool = False
    has_param_km: bool = False
    has_nav_1: bool = False
    has_nav_active: bool = False
    has_nav_strip: bool = False
    has_decnav: bool = False
    has_net_att_1: bool = False
    has_net_att_2: bool = False
    has_orientation_1: bool = False
    has_orientation_active: bool = False
    has_sv_filtered: bool = False
    has_ss_data: bool = False
    has_ss_detvg: bool = False
    has_ss_gloria: bool = False
    num_pings: int = 0
    num_beams: int = 0
    min_depth_m: float = 0.0
    max_depth_m: float = 0.0
    start_time_utc: str = ""
    end_time_utc: str = ""
    mean_heading_deg: float = 0.0
    mean_speed_kts: float = 0.0
    bounds_wesn: Optional[Tuple[float, float, float, float]] = None
    merged_path: Optional[str] = None
    nav_path: Optional[str] = None
    decnav_path: Optional[str] = None
    param_path: Optional[str] = None
    param_km_path: Optional[str] = None
    svp_path: Optional[str] = None
    ss_path: Optional[str] = None
    vert_prof_path: Optional[str] = None

    @property
    def display_id(self) -> str:
        return f"{self.subdir}/{self.line_name}" if self.subdir else self.line_name

    @property
    def stage_summary(self) -> str:
        if self.has_ss_gloria and self.has_merged and (self.has_decnav or self.has_nav_active) and self.has_orientation_active:
            if self.has_watercol or self.has_vert_prof:
                return "COMPLETE (Bathy + WC + Nav + Att + SS)"
            return "COMPLETE (Bathy + Nav + Att + SS)"
        if self.has_merged and (self.has_decnav or self.has_nav_active) and self.has_orientation_active:
            return "BATHY READY (Nav + Att Merged)"
        if self.has_merged and (self.has_nav_active or self.has_decnav):
            return "UNPACKED (Pending Att / Ray-Trace)"
        if self.has_merged:
            return "UNPACKED (Pending .nav / .orientation)"
        if self.has_decnav:
            return "DECNAV ONLY (Track Overview)"
        if self.has_raw_kmall or self.has_raw_all:
            return "RAW ONLY (Not Unravelled)"
        return "PARTIAL"


def parse_jhc_header(filepath: str) -> JhcHeaderInfo:
    """
    Parse the 1024-byte big-endian JHC_header ("OMG1") from an OMG raster file
    (.r4, .8bit, .sun, .mos, .weight, .ran, .blank, .vert_prof) exactly as
    implemented in code/subr/array.c:read_JHC_header() and code/grid/edhead.c.
    """
    with open(filepath, "rb") as f:
        buf = f.read(JHC_OMG_RECLEN)

    if len(buf) < JHC_OMG_RECLEN:
        raise ValueError(f"File {filepath} is smaller than {JHC_OMG_RECLEN} bytes.")

    magic = buf[0:4].decode("ascii", errors="replace")
    if magic != "OMG1":
        raise ValueError(f"File {filepath} does not start with 'OMG1' magic bytes (got {magic!r}).")

    dx, dy = struct.unpack(">ii", buf[4:12])
    # 4 bytes alignment padding at buf[12:16] before 8-byte doubles
    xmin, xmax, ymin, ymax, xstep, ystep = struct.unpack(">6d", buf[16:64])
    data_type, rgb_bw, projection, ellipsoid = struct.unpack(">4B", buf[64:68])
    (
        proj_merid,
        sun_elev,
        sun_azi,
        sun_exag,
        view_elev,
        view_azi,
        view_exag,
        max_value,
        min_value,
    ) = struct.unpack(">9f", buf[68:104])

    # In edhead.c / j_area.c / j_proj.c, hemisphere is 0 (North) or 1 (South) (or ASCII 'N'/'S')
    hemi_val = buf[104]
    if hemi_val == 1 or hemi_val in (ord("S"), ord("s")):
        hemisphere = "S"
    elif hemi_val == 0 or hemi_val in (ord("N"), ord("n")):
        # Note: for Mercator or UTM in southern latitudes where hemisphere byte wasn't explicitly set to 1
        hemisphere = "S" if (projection in (1, 3, 5) and ymin < 0) else "N"
    else:
        hemisphere = "N"

    label_1 = buf[112:184].split(b"\x00", 1)[0].decode("ascii", errors="replace").strip()

    proj_lat = 0.0
    lat_std1 = 0.0
    lat_std2 = 0.0
    false_easting = 0.0
    false_northing = 0.0
    if projection in (10, 11):
        proj_lat, lat_std1, lat_std2, false_easting, false_northing = struct.unpack(">5f", buf[256:276])

    return JhcHeaderInfo(
        filepath=os.path.abspath(filepath),
        magic=magic,
        dx=dx,
        dy=dy,
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        xstep=xstep,
        ystep=ystep,
        data_type=data_type,
        rgb_bw=rgb_bw,
        projection=projection,
        ellipsoid=ellipsoid,
        proj_merid=proj_merid,
        sun_elev=sun_elev,
        sun_azi=sun_azi,
        sun_exag=sun_exag,
        view_elev=view_elev,
        view_azi=view_azi,
        view_exag=view_exag,
        max_value=max_value,
        min_value=min_value,
        hemisphere=hemisphere,
        label_1=label_1,
        proj_lat=proj_lat,
        lat_std1=lat_std1,
        lat_std2=lat_std2,
        false_easting=false_easting,
        false_northing=false_northing,
    )


def _omg_mercator_forward(lon_deg: float, lat_deg: float, proj_lat_deg: float, lon_0_deg: float = 0.0) -> Tuple[float, float]:
    """
    Exact Snyder ellipsoid Mercator forward projection matching code/subr/mercator.c
    and code/grid/edhead.c.
    """
    lat_ts = math.radians(proj_lat_deg)
    eqscale = math.sqrt(1.0 - (WGS84_E * math.sin(lat_ts)) ** 2) / math.cos(lat_ts)
    scaledrad = WGS84_A / eqscale

    dlon = lon_deg - lon_0_deg
    sin_lat = math.sin(math.radians(lat_deg))
    esin = WGS84_E * sin_lat

    x_m = scaledrad * math.radians(dlon)
    y_m = scaledrad * 0.5 * math.log(((1.0 + sin_lat) / (1.0 - sin_lat)) * (((1.0 - esin) / (1.0 + esin)) ** WGS84_E))
    return x_m, y_m


def _compute_crs_and_geotransform(hdr: JhcHeaderInfo) -> Tuple[str, Tuple[float, float, float, float, float, float]]:
    """
    Compute the WKT / PROJ.4 / EPSG string and 6-tuple GDAL GeoTransform
    (ulx, xres, xskew, uly, yskew, -yres) for a JhcHeaderInfo.
    Matches the georeferencing & world-file (.tfw / .geo_meta) logic in
    code/grid/edhead.c (lines 303-570 and 918-1045) and code/subr/j_proj.c.
    """
    # 1. Orthogonal UTM (projection == 2)
    if hdr.projection == 2:
        zone = int(round((hdr.proj_merid + 177.0) / 6.0 + 1.0))
        zone = max(1, min(60, zone))
        is_south = hdr.hemisphere.upper() == "S" or hdr.ymin < 0
        epsg = (32700 + zone) if is_south else (32600 + zone)
        srs = f"EPSG:{epsg}"
        ulx = hdr.xmin - 0.5 * hdr.xstep
        uly = hdr.ymax + 0.5 * hdr.ystep
        return srs, (ulx, hdr.xstep, 0.0, uly, 0.0, -hdr.ystep)

    # 2. Orthogonal Mercator (projection == 1)
    if hdr.projection == 1:
        lat_ts = hdr.proj_merid if abs(hdr.proj_merid) < 89.0 else 0.0
        srs = f"+proj=merc +lat_ts={lat_ts} +lon_0=0.0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
        x_m, y_m = _omg_mercator_forward(hdr.xmin, hdr.ymax, lat_ts, lon_0_deg=0.0)
        ulx = x_m - 0.5 * hdr.xstep
        uly = y_m + 0.5 * hdr.ystep
        return srs, (ulx, hdr.xstep, 0.0, uly, 0.0, -hdr.ystep)

    # 3. Rotated UTM (projection == 4)
    if hdr.projection == 4:
        zone = int(round((hdr.proj_merid + 177.0) / 6.0 + 1.0))
        zone = max(1, min(60, zone))
        is_south = hdr.hemisphere.upper() == "S"
        epsg = (32700 + zone) if is_south else (32600 + zone)
        srs = f"EPSG:{epsg}"
        # In j_proj.c:405, (xmin, ymin) is the UTM Easting/Northing of the center pixel (dx/2, dy/2),
        # and ymax is the anticlockwise rotation angle in degrees.
        angle_rad = math.radians(hdr.ymax)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        # Pixel (0, 0) is at xx = (-dx/2 - 0.5)*xstep, yy = (+dy/2 + 0.5)*ystep
        xx = (-0.5 * hdr.dx - 0.5) * hdr.xstep
        yy = (0.5 * hdr.dy + 0.5) * hdr.ystep
        corner_east = hdr.xmin + (xx * cos_a - yy * sin_a)
        corner_north = hdr.ymin + (xx * sin_a + yy * cos_a)
        return srs, (
            corner_east,
            hdr.xstep * cos_a,
            hdr.ystep * sin_a,
            corner_north,
            hdr.xstep * sin_a,
            -hdr.ystep * cos_a,
        )

    # 4. Rotated Mercator (projection == 5)
    if hdr.projection == 5:
        lat_ts = hdr.proj_merid if abs(hdr.proj_merid) < 89.0 else hdr.ymin
        srs = f"+proj=merc +lat_ts={lat_ts} +lon_0=0.0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
        # Center of map is at lon=xmin, lat=ymin; rotation angle is ymax (deg)
        cen_e, cen_n = _omg_mercator_forward(hdr.xmin, hdr.ymin, lat_ts, lon_0_deg=0.0)
        angle_rad = math.radians(hdr.ymax)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        xx = (-0.5 * hdr.dx - 0.5) * hdr.xstep
        yy = (0.5 * hdr.dy + 0.5) * hdr.ystep
        corner_east = cen_e + (xx * cos_a - yy * sin_a)
        corner_north = cen_n + (xx * sin_a + yy * cos_a)
        return srs, (
            corner_east,
            hdr.xstep * cos_a,
            hdr.ystep * sin_a,
            corner_north,
            hdr.xstep * sin_a,
            -hdr.ystep * cos_a,
        )

    # 5. NB Stereographic (projection == 6 or 8)
    if hdr.projection in (6, 8):
        srs = "EPSG:2953"
        if hdr.projection == 6:
            ulx = hdr.xmin - 0.5 * hdr.xstep
            uly = hdr.ymax + 0.5 * hdr.ystep
            return srs, (ulx, hdr.xstep, 0.0, uly, 0.0, -hdr.ystep)
        angle_rad = math.radians(hdr.ymax)
        cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
        xx = (-0.5 * hdr.dx - 0.5) * hdr.xstep
        yy = (0.5 * hdr.dy + 0.5) * hdr.ystep
        return srs, (
            hdr.xmin + (xx * cos_a - yy * sin_a),
            hdr.xstep * cos_a,
            hdr.ystep * sin_a,
            hdr.ymin + (xx * sin_a + yy * cos_a),
            hdr.xstep * sin_a,
            -hdr.ystep * cos_a,
        )

    # 6. Polar Stereographic (projection == 7 or 9)
    if hdr.projection in (7, 9):
        epsg = 3031 if hdr.hemisphere.upper() == "S" else 3995
        srs = f"EPSG:{epsg}"
        ulx = hdr.xmin - 0.5 * hdr.xstep
        uly = hdr.ymax + 0.5 * hdr.ystep
        return srs, (ulx, hdr.xstep, 0.0, uly, 0.0, -hdr.ystep)

    # 7. Lambert Conformal Conic (projection == 10 or 11)
    if hdr.projection in (10, 11):
        srs = (
            f"+proj=lcc +lat_1={hdr.lat_std1} +lat_2={hdr.lat_std2} "
            f"+lat_0={hdr.proj_lat} +lon_0={hdr.proj_merid} "
            f"+x_0={hdr.false_easting} +y_0={hdr.false_northing} +datum=WGS84 +units=m +no_defs"
        )
        ulx = hdr.xmin - 0.5 * hdr.xstep
        uly = hdr.ymax + 0.5 * hdr.ystep
        return srs, (ulx, hdr.xstep, 0.0, uly, 0.0, -hdr.ystep)

    # 8. Geographic Degrees (projection == 3)
    if hdr.projection == 3 or (
        hdr.projection == 0 and (-180.0 <= hdr.xmin <= 180.0 and -90.0 <= hdr.ymin <= 90.0 and hdr.xmin != 0.0 and hdr.xmax != -2500.0)
    ):
        srs = "EPSG:4326"
        xres = hdr.xstep
        yres = hdr.ystep
        ulx = hdr.xmin - 0.5 * xres
        uly = hdr.ymax + 0.5 * yres
        return srs, (ulx, xres, 0.0, uly, 0.0, -yres)

    # 9. Unprojected / Curtain Grid (projection == 0, e.g. .vert_prof)
    srs = ""
    xstep = hdr.xstep if hdr.xstep > 0 else 1.0
    ystep = hdr.ystep if hdr.ystep > 0 else 1.0
    ulx = hdr.xmin - 0.5 * xstep
    uly = (hdr.ymax if hdr.ymax != 0.0 else hdr.dy * ystep) + 0.5 * ystep
    return srs, (ulx, xstep, 0.0, uly, 0.0, -ystep)


def format_edhead_report(hdr: JhcHeaderInfo) -> str:
    """
    Generate a detailed header inspection report matching `edhead -show`,
    `edhead -dump_tfw`, and `edhead -dump_geotiff`.
    """
    srs, gt = _compute_crs_and_geotransform(hdr)
    lines = [
        f"=== OMG1 Header Report (edhead.c compatible): {os.path.basename(hdr.filepath)} ===",
        f"File Path       : {hdr.filepath}",
        f"Magic Tag       : {hdr.magic} (1024-byte big-endian JHC_header)",
        f"Dimensions      : dx = {hdr.dx} cols × dy = {hdr.dy} rows",
        f"Pixel Spacing   : xstep = {hdr.xstep:.4f} m, ystep = {hdr.ystep:.4f} m",
        f"Data Type       : {hdr.data_type} ({hdr.data_type_name}), NoData = {hdr.nodata_value}",
        f"Projection      : {hdr.projection} ({hdr.projection_name}), Ellipsoid = {hdr.ellipsoid} (WGS84)",
        f"Proj Meridian   : {hdr.proj_merid:.6f}° | Hemisphere = {hdr.hemisphere}",
    ]
    if hdr.projection in (4, 5, 8, 9, 11):
        lines.append(f"Rotated Center  : Lon/E = {hdr.xmin:.6f}, Lat/N = {hdr.ymin:.6f}, Rotation Angle = {hdr.ymax:.3f}°")
    else:
        lines.append(f"Bounds (X / Lon): [{hdr.xmin:.6f}, {hdr.xmax:.6f}]")
        lines.append(f"Bounds (Y / Lat): [{hdr.ymin:.6f}, {hdr.ymax:.6f}]")

    lines.extend([
        f"Value Range     : Min = {hdr.min_value:.3f}, Max = {hdr.max_value:.3f}",
        f"Sun Params      : Azimuth = {hdr.sun_azi:.1f}°, Elevation = {hdr.sun_elev:.1f}°, Exag = {hdr.sun_exag:.1f}",
        f"CRS / SRS       : {srs or 'Local / Curtain Coordinates'}",
        f"World File (TFW): dX={gt[1]:.4f}, rotY={gt[2]:.4f}, rotX={gt[4]:.4f}, dY={gt[5]:.4f}, ULX={gt[0]:.3f}, ULY={gt[3]:.3f}",
    ])
    if hdr.label_1:
        lines.append(f"Label 1         : {hdr.label_1}")
    return "\n".join(lines)


def write_jhc_header_bytes(hdr: JhcHeaderInfo) -> bytes:
    """
    Serialize a JhcHeaderInfo into a 1024-byte big-endian "OMG1" header buffer
    matching code/subr/array.c:write_JHC_header() byte-for-byte.
    """
    buf = bytearray(JHC_OMG_RECLEN)
    buf[0:4] = b"OMG1"
    struct.pack_into(">ii", buf, 4, hdr.dx, hdr.dy)
    struct.pack_into(">6d", buf, 16, hdr.xmin, hdr.xmax, hdr.ymin, hdr.ymax, hdr.xstep, hdr.ystep)
    struct.pack_into(">4B", buf, 64, hdr.data_type, hdr.rgb_bw, hdr.projection, hdr.ellipsoid)
    struct.pack_into(
        ">9f",
        buf,
        68,
        hdr.proj_merid,
        hdr.sun_elev,
        hdr.sun_azi,
        hdr.sun_exag,
        hdr.view_elev,
        hdr.view_azi,
        hdr.view_exag,
        hdr.max_value,
        hdr.min_value,
    )
    buf[104] = 1 if hdr.hemisphere.upper() == "S" else 0
    lbl_bytes = (hdr.label_1 or "").encode("ascii", errors="replace")[:71]
    buf[112 : 112 + len(lbl_bytes)] = lbl_bytes
    if hdr.projection in (10, 11):
        struct.pack_into(
            ">5f",
            buf,
            256,
            hdr.proj_lat,
            hdr.lat_std1,
            hdr.lat_std2,
            hdr.false_easting,
            hdr.false_northing,
        )
    return bytes(buf)


def make_blank_grid_from_bounds(
    out_prefix: str,
    bounds_wesn: Tuple[float, float, float, float],
    mpp: float = 100.0,
    float_flag: bool = True,
    create_tor4_files: bool = True,
) -> JhcHeaderInfo:
    """
    Pure-Python implementation of `make_blank -float <prefix> -boundsof_nav ...`
    and `tor4 <prefix>` matching code/grid/make_blank.c and code/subr/j_area.c:gridsize().
    Creates `<out_prefix>.blank` (and optionally `.r4`, `.r4_weights`, `.r4_weight_depth`).
    """
    west, east, south, north = bounds_wesn
    proj_merid = 0.5 * (south + north)

    # Compute xlen, ylen in Mercator meters at standard parallel proj_merid (j_area.c:366)
    xleft, ybot = _omg_mercator_forward(west, south, proj_merid, lon_0_deg=west)
    xright, ytop = _omg_mercator_forward(east, north, proj_merid, lon_0_deg=west)
    xlen = abs(xright - xleft)
    ylen = abs(ytop - ybot)

    dx = int((xlen / mpp) + 0.5) + 1
    dy = int((ylen / mpp) + 0.5) + 1

    blank_path = out_prefix if out_prefix.endswith(".blank") else (out_prefix + ".blank")
    base_prefix = blank_path[:-6] if blank_path.endswith(".blank") else out_prefix

    hdr = JhcHeaderInfo(
        filepath=os.path.abspath(blank_path),
        magic="OMG1",
        dx=dx,
        dy=dy,
        xmin=west,
        xmax=east,
        ymin=south,
        ymax=north,
        xstep=float(mpp),
        ystep=float(mpp),
        data_type=3 if float_flag else 1,
        rgb_bw=0,
        projection=1,  # Mercator Orthogonal
        ellipsoid=1,   # WGS84
        proj_merid=float(proj_merid),
        sun_elev=0.0,
        sun_azi=0.0,
        sun_exag=0.0,
        view_elev=0.0,
        view_azi=0.0,
        view_exag=0.0,
        max_value=0.0,
        min_value=0.0,
        hemisphere="S" if south < 0 else "N",
        label_1="Created by OMG QGIS Plugin (make_blank)",
    )

    hdr_bytes = write_jhc_header_bytes(hdr)
    payload_bytes = dx * dy * (4 if float_flag else 1)
    fill_byte = b"\x00" if float_flag else b"\xff"

    with open(blank_path, "wb") as f:
        f.write(hdr_bytes)
        # Write payload in 1 MB chunks
        chunk = fill_byte * min(payload_bytes, 1048576)
        rem = payload_bytes
        while rem > 0:
            n = min(rem, len(chunk))
            f.write(chunk[:n])
            rem -= n

    if create_tor4_files and float_flag:
        import shutil
        for ext in (".r4", ".r4_weights", ".r4_weight_depth"):
            shutil.copy2(blank_path, base_prefix + ext)

    return hdr


def create_gdal_vrt_for_jhc(filepath: str, vrt_path: Optional[str] = None, output_dir: Optional[str] = None) -> str:
    """
    Create a zero-copy GDAL Raw Virtual Raster (.vrt) XML sidecar file for an OMG
    JHC_header raster (.r4, .sun, .8bit, .mos, .weight, .blank, .vert_prof).
    """
    hdr = parse_jhc_header(filepath)
    if vrt_path is None:
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            vrt_path = os.path.join(output_dir, os.path.basename(filepath) + ".vrt")
        else:
            vrt_path = filepath + ".vrt"

    srs, gt = _compute_crs_and_geotransform(hdr)
    pixel_offset = hdr.bytes_per_pixel
    line_offset = hdr.dx * hdr.bytes_per_pixel

    same_dir = os.path.dirname(os.path.abspath(vrt_path)) == os.path.dirname(hdr.filepath)
    rel_filename = os.path.basename(filepath) if same_dir else hdr.filepath
    rel_attr = "1" if same_dir else "0"

    srs_xml = f"  <SRS>{srs}</SRS>\n" if srs else ""
    gt_str = ", ".join(f"{v:.10f}" for v in gt)

    # Note: .vert_prof files produced by makeWC have a 2048-byte offset; standard JHC rasters use 1024
    img_offset = 2048 if filepath.endswith(".vert_prof") else JHC_OMG_RECLEN

    vrt_xml = f"""<VRTDataset rasterXSize="{hdr.dx}" rasterYSize="{hdr.dy}">
{srs_xml}  <GeoTransform>{gt_str}</GeoTransform>
  <Metadata>
    <MDI key="OMG_DATA_TYPE">{hdr.data_type_name}</MDI>
    <MDI key="OMG_PROJECTION">{hdr.projection_name}</MDI>
    <MDI key="OMG_MIN_VALUE">{hdr.min_value}</MDI>
    <MDI key="OMG_MAX_VALUE">{hdr.max_value}</MDI>
    <MDI key="OMG_SUN_AZI">{hdr.sun_azi}</MDI>
    <MDI key="OMG_SUN_ELEV">{hdr.sun_elev}</MDI>
  </Metadata>
  <VRTRasterBand dataType="{hdr.gdal_data_type}" band="1" subClass="VRTRawRasterBand">
    <SourceFilename relativeToVRT="{rel_attr}">{rel_filename}</SourceFilename>
    <ImageOffset>{img_offset}</ImageOffset>
    <PixelOffset>{pixel_offset}</PixelOffset>
    <LineOffset>{line_offset}</LineOffset>
    <ByteOrder>MSB</ByteOrder>
    <NoDataValue>{hdr.nodata_value}</NoDataValue>
  </VRTRasterBand>
</VRTDataset>
"""
    with open(vrt_path, "w", encoding="utf-8") as f:
        f.write(vrt_xml)
    return os.path.abspath(vrt_path)


def parse_omg_merged_summary(filepath: str) -> MergedSummaryInfo:
    """
    Read the big-endian OMG_HDCS_summary_header (96 bytes + 168 bytes v4 extension)
    from a .merged swath file (code/subr/OMG_HDCS_jversion.c lines 116-210).
    """
    with open(filepath, "rb") as f:
        data = f.read(OMG_HDCS_SUMMARY_HEADER_SIZE)
        if len(data) < OMG_HDCS_SUMMARY_HEADER_SIZE:
            raise ValueError(f"{filepath} is smaller than {OMG_HDCS_SUMMARY_HEADER_SIZE} bytes.")

        file_id = data[0:4].decode("ascii", errors="replace")
        ints = struct.unpack(">23i", data[4:96])
        (
            sensor_number,
            sub_file_id,
            file_version,
            tool_type,
            num_profiles,
            num_depths,
            time_scale,
            ref_time,
            min_time,
            max_time,
            position_type,
            position_scale,
            ref_lat,
            min_lat,
            max_lat,
            ref_long,
            min_long,
            max_long,
            min_obs_depth,
            max_obs_depth,
            min_proc_depth,
            max_proc_depth,
            status,
        ) = ints

        total_profile_bytes = 0
        total_beam_bytes = 0
        if file_version == 4:
            v4data = f.read(OMG_HDCS_SUMMARY_V4EXTRA_SIZE)
            if len(v4data) == OMG_HDCS_SUMMARY_V4EXTRA_SIZE:
                total_profile_bytes = struct.unpack(">i", v4data[0:4])[0]
                total_beam_bytes = struct.unpack(">i", v4data[84:88])[0]

    pos_scale_rad = (position_scale if position_scale > 0 else 100) * 1.0e-9
    min_lat_deg = math.degrees(ref_lat * 1.0e-7 + min_lat * pos_scale_rad)
    max_lat_deg = math.degrees(ref_lat * 1.0e-7 + max_lat * pos_scale_rad)
    min_lon_deg = math.degrees(ref_long * 1.0e-7 + min_lon * pos_scale_rad)
    max_lon_deg = math.degrees(ref_long * 1.0e-7 + max_long * pos_scale_rad)

    t_scale_sec = (time_scale if time_scale > 0 else 1000) * 1.0e-6
    min_time_epoch = ref_time * 100.0 + min_time * t_scale_sec
    max_time_epoch = ref_time * 100.0 + max_time * t_scale_sec

    return MergedSummaryInfo(
        filepath=os.path.abspath(filepath),
        file_id=file_id,
        file_version=file_version,
        tool_type=tool_type,
        num_profiles=num_profiles,
        num_depths=num_depths,
        time_scale_usec=time_scale,
        ref_time_100s=ref_time,
        min_time_epoch=min_time_epoch,
        max_time_epoch=max_time_epoch,
        min_lat_deg=min_lat_deg,
        max_lat_deg=max_lat_deg,
        min_lon_deg=min_lon_deg,
        max_lon_deg=max_lon_deg,
        min_obs_depth_m=min_obs_depth * 0.001,
        max_obs_depth_m=max_obs_depth * 0.001,
        status_flags=status,
        total_profile_bytes=total_profile_bytes,
        total_beam_bytes=total_beam_bytes,
    )


def parse_omg_nav(filepath: str, stride: int = 1) -> List[Dict]:
    """
    Read binary 48-byte big-endian jcu_nav_rec records from an OMG .nav or .decnav file
    (code/subr/jcu_nav.c lines 62-125).
    """
    with open(filepath, "rb") as f:
        buf = f.read()

    num_recs = len(buf) // JCU_BINNAV_RECLEN
    step = max(1, stride)
    records = []

    for idx in range(0, num_recs, step):
        off = idx * JCU_BINNAV_RECLEN
        lat, lon, time_s, centisecs, _pad, azi, vel, depth, f0, f1, f2, f3 = struct.unpack_from(
            ">ddihhffhhhhh", buf, off
        )
        if -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0 and (abs(lat) > 1e-5 or abs(lon) > 1e-5):
            records.append(
                {
                    "record": idx,
                    "lat": lat,
                    "lon": lon,
                    "timestamp": float(time_s) + centisecs * 0.01,
                    "azimuth_deg": azi,
                    "velocity_m_s": vel,
                    "depth_m": depth,
                }
            )
    return records


def summarize_nav_file(filepath: str, stride: int = 1) -> Optional[Dict]:
    """
    Read a .decnav or .nav file and return trackline coordinates, bounding box,
    start/end UTC timestamps, mean heading, mean speed (knots), and depth range.
    """
    recs = parse_omg_nav(filepath, stride=stride)
    if not recs:
        return None

    lats = [r["lat"] for r in recs]
    lons = [r["lon"] for r in recs]
    times = [r["timestamp"] for r in recs if r["timestamp"] > 0]
    depths = [r["depth_m"] for r in recs if r["depth_m"] > 0]
    vels = [r["velocity_m_s"] for r in recs if 0 <= r["velocity_m_s"] < 50]
    azis = [r["azimuth_deg"] for r in recs if 0 <= r["azimuth_deg"] <= 360]

    mean_hdg = 0.0
    if azis:
        sin_sum = sum(math.sin(math.radians(a)) for a in azis)
        cos_sum = sum(math.cos(math.radians(a)) for a in azis)
        mean_hdg = (math.degrees(math.atan2(sin_sum, cos_sum)) + 360.0) % 360.0

    mean_kts = (sum(vels) / len(vels)) * 1.94384 if vels else 0.0
    t0_str = datetime.fromtimestamp(min(times), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S") if times else ""
    t1_str = datetime.fromtimestamp(max(times), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S") if times else ""

    return {
        "num_records": len(recs),
        "coords": [[r["lon"], r["lat"]] for r in recs],
        "bounds_wesn": (min(lons), max(lons), min(lats), max(lats)),
        "start_time_utc": t0_str,
        "end_time_utc": t1_str,
        "min_depth_m": float(min(depths)) if depths else 0.0,
        "max_depth_m": float(max(depths)) if depths else 0.0,
        "mean_heading_deg": round(mean_hdg, 2),
        "mean_speed_kts": round(mean_kts, 2),
    }


def parse_omg_param(filepath: str) -> Dict[str, str]:
    """
    Parse key-value lever-arm parameters from an OMG .param file or .param_km.
    """
    params: Dict[str, str] = {}
    if not filepath or not os.path.isfile(filepath):
        return params
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line and "," not in line:
                k, v = line.split("=", 1)
                params[k.strip()] = v.strip()
            else:
                parts = line.split()
                if len(parts) >= 2:
                    params[parts[0]] = " ".join(parts[1:])
                else:
                    params[f"line_{len(params)+1}"] = line
    return params


def _iter_dir_files(root_dir: str) -> List[Tuple[str, str, str]]:
    """
    Yield (subdir_name, filename, full_path) for both flat directories (e.g. decnav/*.decnav)
    and Julian-day subdirectory trees (e.g. decnav/74/*.decnav).
    """
    results: List[Tuple[str, str, str]] = []
    if not os.path.isdir(root_dir):
        return results

    try:
        with os.scandir(root_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    results.append(("", entry.name, entry.path))
                elif entry.is_dir() and not entry.name.startswith("."):
                    sub = entry.name
                    try:
                        with os.scandir(entry.path) as sub_entries:
                            for se in sub_entries:
                                if se.is_file():
                                    results.append((sub, se.name, se.path))
                    except OSError:
                        pass
    except OSError:
        pass

    results.sort(key=lambda t: (t[0], t[1]))
    return results


def scan_survey_workspace(
    workspace_dir: str,
    read_merged_headers: bool = False,
    read_decnav_summaries: bool = True,
    extra_raster_dirs: Optional[List[str]] = None,
) -> Tuple[List[LineProcessingStatus], List[JhcHeaderInfo]]:
    """
    Scan an OMG processing workspace directory (supporting both flat and Julian-Day
    subdirectory layouts such as 02_Bransfield/decnav/74..81) and optional local
    output/cache directories for rasters (.blank, .r4, .8bit, .sun, .mos, .vert_prof).
    """
    lines_map: Dict[Tuple[str, str], LineProcessingStatus] = {}
    rasters: List[JhcHeaderInfo] = []
    seen_raster_paths = set()

    def get_line(subdir: str, name: str) -> LineProcessingStatus:
        key = (subdir, name)
        if key not in lines_map:
            lines_map[key] = LineProcessingStatus(line_name=name, subdir=subdir)
        return lines_map[key]

    # 1. Scan raw/
    for sub, fname, full in _iter_dir_files(os.path.join(workspace_dir, "raw")):
        if fname.startswith("._"):
            continue
        if fname.endswith(".kmall"):
            get_line(sub, fname[:-6]).has_raw_kmall = True
        elif fname.endswith(".kmwcd"):
            get_line(sub, fname[:-6]).has_raw_kmwcd = True
        elif fname.endswith(".all"):
            get_line(sub, fname[:-4]).has_raw_all = True
        elif fname.endswith(".wcd"):
            get_line(sub, fname[:-4]).has_raw_wcd = True

    # 2. Scan decnav/
    for sub, fname, full in _iter_dir_files(os.path.join(workspace_dir, "decnav")):
        if fname.startswith("._"):
            continue
        if fname.endswith(".decnav"):
            st = get_line(sub, fname[:-7])
            st.has_decnav = True
            st.decnav_path = full

    # 3. Scan merged/
    for sub, fname, full in _iter_dir_files(os.path.join(workspace_dir, "merged")):
        if fname.startswith("._") or fname.startswith("justWC_"):
            continue
        if fname.endswith(".merged"):
            st = get_line(sub, fname[:-7])
            st.has_merged = True
            st.merged_path = full
        elif fname.endswith(".watercol"):
            get_line(sub, fname[:-9]).has_watercol = True
        elif fname.endswith(".WC_Phase1"):
            get_line(sub, fname[:-10]).has_wc_phase1 = True
        elif fname.endswith(".WC_Phase2"):
            get_line(sub, fname[:-10]).has_wc_phase2 = True
        elif fname.endswith(".vert_prof"):
            st = get_line(sub, fname[:-10])
            st.has_vert_prof = True
            st.vert_prof_path = full
        elif fname.endswith(".param"):
            st = get_line(sub, fname[:-6])
            st.has_param = True
            st.param_path = full
        elif fname.endswith(".param_km"):
            st = get_line(sub, fname[:-9])
            st.has_param_km = True
            st.param_km_path = full
            if not st.param_path:
                st.param_path = full
        elif fname.endswith(".nav_1"):
            st = get_line(sub, fname[:-6])
            st.has_nav_1 = True
            if not st.nav_path:
                st.nav_path = full
        elif fname.endswith(".nav"):
            st = get_line(sub, fname[:-4])
            st.has_nav_active = True
            st.nav_path = full
        elif fname.endswith(".nav.strip"):
            st = get_line(sub, fname[:-10])
            st.has_nav_strip = True
            st.nav_path = full
        elif fname.endswith(".net_att_1"):
            get_line(sub, fname[:-10]).has_net_att_1 = True
        elif fname.endswith(".net_att_2"):
            get_line(sub, fname[:-10]).has_net_att_2 = True
        elif fname.endswith(".orientation_1"):
            get_line(sub, fname[:-14]).has_orientation_1 = True
        elif fname.endswith(".orientation"):
            get_line(sub, fname[:-12]).has_orientation_active = True
        elif fname.endswith(".sv_filtered") or fname.endswith(".svp_001") or fname.endswith(".ssp"):
            base = fname.rsplit(".", 1)[0]
            st = get_line(sub, base)
            st.has_sv_filtered = True
            if fname.endswith(".sv_filtered") or not st.svp_path:
                st.svp_path = full
        elif fname.endswith(".merged.ss_data"):
            get_line(sub, fname[:-15]).has_ss_data = True
        elif fname.endswith(".merged.ss_data_detvg"):
            get_line(sub, fname[:-21]).has_ss_detvg = True

    # 4. Scan ss/
    for sub, fname, full in _iter_dir_files(os.path.join(workspace_dir, "ss")):
        if fname.startswith("._"):
            continue
        if fname.endswith(".ss"):
            st = get_line(sub, fname[:-3])
            st.has_ss_gloria = True
            st.ss_path = full

    # 5. Populate trackline summaries from .decnav (preferred, fast) or .merged headers
    for st in lines_map.values():
        if read_decnav_summaries and st.decnav_path and os.path.isfile(st.decnav_path):
            try:
                info = summarize_nav_file(st.decnav_path, stride=1)
                if info:
                    st.bounds_wesn = info["bounds_wesn"]
                    st.start_time_utc = info["start_time_utc"]
                    st.end_time_utc = info["end_time_utc"]
                    st.min_depth_m = info["min_depth_m"]
                    st.max_depth_m = info["max_depth_m"]
                    st.mean_heading_deg = info["mean_heading_deg"]
                    st.mean_speed_kts = info["mean_speed_kts"]
                    st.num_pings = info["num_records"] * 10
            except Exception:
                pass

        if read_merged_headers and st.merged_path and os.path.isfile(st.merged_path):
            try:
                hdr = parse_omg_merged_summary(st.merged_path)
                st.num_pings = hdr.num_profiles
                st.num_beams = hdr.num_depths
                if hdr.min_obs_depth_m or hdr.max_obs_depth_m:
                    st.min_depth_m = hdr.min_obs_depth_m
                    st.max_depth_m = hdr.max_obs_depth_m
                if not st.bounds_wesn:
                    st.bounds_wesn = (hdr.min_lon_deg, hdr.max_lon_deg, hdr.min_lat_deg, hdr.max_lat_deg)
            except Exception:
                pass

    # 6. Scan workspace root, grids/, mosaics/, and any extra_raster_dirs (like local output cache dir) for OMG1 rasters
    raster_exts = (".r4", ".8bit", ".sun", ".mos", ".weight", ".ran", ".blank", ".vert_prof")
    candidate_dirs = [
        workspace_dir,
        os.path.join(workspace_dir, "grids"),
        os.path.join(workspace_dir, "mosaics"),
    ]
    if extra_raster_dirs:
        for ed in extra_raster_dirs:
            if ed and os.path.isdir(ed) and ed not in candidate_dirs:
                candidate_dirs.append(ed)

    for d in candidate_dirs:
        if not os.path.isdir(d):
            continue
        try:
            for fname in sorted(os.listdir(d)):
                if fname.startswith("._") or fname.endswith((".r4_weights", ".r4_weight_depth", ".r4_history", ".vrt")):
                    continue
                if fname.endswith(raster_exts) or ".sun" in fname:
                    fpath = os.path.abspath(os.path.join(d, fname))
                    if fpath in seen_raster_paths or not os.path.isfile(fpath):
                        continue
                    try:
                        rasters.append(parse_jhc_header(fpath))
                        seen_raster_paths.add(fpath)
                    except Exception:
                        pass
        except OSError:
            pass

    sorted_lines = sorted(lines_map.values(), key=lambda x: (x.subdir, x.line_name))
    return sorted_lines, rasters


def export_tracklines_geojson(
    lines: List[LineProcessingStatus],
    output_geojson_path: str,
    nav_stride: int = 1,
) -> str:
    """
    Export survey lines into a single GeoJSON FeatureCollection with full processing
    stage attributes so QGIS can style tracklines by Julian Day (`subdir`) or
    Processing Stage (`stage_summary`).
    """
    features = []
    for st in lines:
        coords = []
        nav_candidate = st.decnav_path or st.nav_path
        if nav_candidate and os.path.isfile(nav_candidate):
            stride = nav_stride if nav_candidate == st.decnav_path else max(1, nav_stride * 10)
            try:
                nav_pts = parse_omg_nav(nav_candidate, stride=stride)
                coords = [[pt["lon"], pt["lat"]] for pt in nav_pts]
            except Exception:
                coords = []

        if len(coords) < 2 and st.bounds_wesn:
            w, e, s, n = st.bounds_wesn
            if -180 <= w <= 180 and -180 <= e <= 180 and -90 <= s <= 90 and -90 <= n <= 90:
                coords = [[w, s], [e, n]]

        if len(coords) < 2:
            continue

        features.append(
            {
                "type": "Feature",
                "properties": {
                    "line_name": st.line_name,
                    "subdir": st.subdir,
                    "display_id": st.display_id,
                    "stage_summary": st.stage_summary,
                    "num_pings": st.num_pings,
                    "num_beams": st.num_beams,
                    "min_depth_m": round(st.min_depth_m, 2),
                    "max_depth_m": round(st.max_depth_m, 2),
                    "start_time_utc": st.start_time_utc,
                    "end_time_utc": st.end_time_utc,
                    "mean_heading_deg": st.mean_heading_deg,
                    "mean_speed_kts": st.mean_speed_kts,
                    "has_raw": int(st.has_raw_kmall or st.has_raw_all),
                    "has_wc": int(st.has_watercol or st.has_vert_prof),
                    "has_merged": int(st.has_merged),
                    "has_nav": int(st.has_nav_active or st.has_nav_1),
                    "has_decnav": int(st.has_decnav),
                    "has_orientation": int(st.has_orientation_active or st.has_net_att_2 or st.has_net_att_1),
                    "has_svp": int(st.has_sv_filtered),
                    "has_ss": int(st.has_ss_gloria),
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": coords,
                },
            }
        )

    fc = {"type": "FeatureCollection", "features": features}
    os.makedirs(os.path.dirname(os.path.abspath(output_geojson_path)), exist_ok=True)
    with open(output_geojson_path, "w", encoding="utf-8") as f:
        json.dump(fc, f)
    return os.path.abspath(output_geojson_path)
