"""
Pure-Python Binary Reader, GDAL Zero-Copy VRT Generator, and Workspace Scanner
for UNB Ocean Mapping Group (OMG) Multibeam Sonar Files.

Tested against real Kongsberg EM124 (.kmall / .kmwcd) Antarctica survey data
(02_Bransfield, RV Almirante Viel, Julian Days 74-81).

Supports:
  - Both flat (merged/, decnav/, ss/) and Julian-Day subdirectory (merged/74/, decnav/74/, ss/74/) layouts
  - JHC_header ("OMG1") 1024-byte big-endian rasters (.r4, .8bit, .sun, .mos, .weight, .ran, .blank, .vert_prof)
  - OMG_HDCS (.merged) summary headers (v1-v4) and 32-byte .file_bounds / .100ping_bounds
  - JCU Binary Navigation (.nav, .decnav, .nav_1..3, .nav.strip) 48-byte big-endian records
  - OMG_HDCS Binary Attitude (.orientation, .net_att_1..2, .orientation_1..2) 44-byte header + records
  - OMG ASCII Ship Parameter (.param and Kongsberg .param_km) lever-arm files
  - OMG Sound Velocity Profiles (.sv_filtered, .svp_001, .ssp, .svTS)
  - Strict Read-Only Archive safety: all generated .vrt and .geojson files can be written to a separate
    local output/cache directory so master archive drives (e.g., /mnt/w) are never modified.
"""

from datetime import datetime, timezone
import json
import math
import os
import struct
import tempfile
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple


JHC_OMG_RECLEN = 1024
JCU_BINNAV_RECLEN = 48
OMG_HDCS_SUMMARY_HEADER_SIZE = 96
OMG_HDCS_SUMMARY_V4EXTRA_SIZE = 168
OMG_HDCS_BOUNDS_SIZE = 32
OMG_HDCS_ATTITUDE_SUMMARY_SIZE = 44


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
    rgb_bw: int
    projection: int         # 0=None, 1=Mercator, 2=UTM, 3=Geographic(min), 4=RotUTM, 5=RotMerc, 10=LCC
    ellipsoid: int          # 1=WGS84
    proj_merid: float
    sun_elev: float
    sun_azi: float
    sun_exag: float
    view_elev: float
    view_azi: float
    view_exag: float
    max_value: float
    min_value: float
    hemisphere: str
    label_1: str

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
        return 255.0 if self.data_type == 1 else 9999.0

    @property
    def projection_name(self) -> str:
        return {
            0: "Unprojected / Curtain Grid",
            1: "Mercator (WGS84)",
            2: f"UTM (Central Meridian {self.proj_merid:.1f}°)",
            3: "Geographic (Arc-Minutes)",
            4: "Rotated UTM",
            5: "Rotated Mercator",
            6: "New Brunswick Stereographic",
            7: "Polar Stereographic",
            10: "Lambert Conformal Conic",
            11: "Rotated Lambert Conformal Conic",
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
        """Returns a human-readable pipeline stage badge for Qimera/HIPS table."""
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
    (.r4, .8bit, .sun, .mos, .weight, .ran, .blank, .vert_prof).
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

    hemisphere_byte = buf[104:105]
    hemisphere = hemisphere_byte.decode("ascii", errors="replace") if hemisphere_byte != b"\x00" else "N"
    label_1 = buf[112:184].split(b"\x00", 1)[0].decode("ascii", errors="replace").strip()

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
    )


def _compute_crs_and_geotransform(hdr: JhcHeaderInfo) -> Tuple[str, Tuple[float, float, float, float, float, float]]:
    """
    Compute the WKT / PROJ.4 / EPSG string and 6-tuple GDAL GeoTransform
    (ulx, xres, xskew, uly, yskew, -yres) for a JhcHeaderInfo.
    Matches the georeferencing logic in code/grid/r4toESRI.c and code/subr/j_proj.c.
    """
    if hdr.projection == 2:
        zone = int(round((hdr.proj_merid + 183.0) / 6.0))
        zone = max(1, min(60, zone))
        is_south = hdr.hemisphere.lower() == "s" or hdr.ymin < 0
        epsg = (32700 + zone) if is_south else (32600 + zone)
        srs = f"EPSG:{epsg}"
        ulx = hdr.xmin - 0.5 * hdr.xstep
        uly = hdr.ymax + 0.5 * hdr.ystep
        return srs, (ulx, hdr.xstep, 0.0, uly, 0.0, -hdr.ystep)

    if hdr.projection == 1:
        lat_ts = hdr.proj_merid if abs(hdr.proj_merid) < 89.0 else 0.0
        srs = f"+proj=merc +lat_ts={lat_ts} +lon_0=0.0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
        a = 6378137.0
        e = 0.0818191908426215
        k0 = math.cos(math.radians(lat_ts)) / math.sqrt(1.0 - (e * math.sin(math.radians(lat_ts))) ** 2)
        lon_rad = math.radians(hdr.xmin)
        lat_rad = math.radians(hdr.ymax)
        x_m = a * k0 * lon_rad
        sin_lat = math.sin(lat_rad)
        y_m = a * k0 * math.log(
            math.tan(math.pi / 4.0 + lat_rad / 2.0) * (((1.0 - e * sin_lat) / (1.0 + e * sin_lat)) ** (e / 2.0))
        )
        ulx = x_m - 0.5 * hdr.xstep
        uly = y_m + 0.5 * hdr.ystep
        return srs, (ulx, hdr.xstep, 0.0, uly, 0.0, -hdr.ystep)

    if hdr.projection == 3 or (
        hdr.projection == 0 and (-180.0 <= hdr.xmin <= 180.0 and -90.0 <= hdr.ymin <= 90.0 and hdr.xmin != 0.0 and hdr.xmax != -2500.0)
    ):
        srs = "EPSG:4326"
        xres = (hdr.xstep / 60.0) if hdr.projection == 3 else hdr.xstep
        yres = (hdr.ystep / 60.0) if hdr.projection == 3 else hdr.ystep
        ulx = hdr.xmin - 0.5 * xres
        uly = hdr.ymax + 0.5 * yres
        return srs, (ulx, xres, 0.0, uly, 0.0, -yres)

    srs = ""
    xstep = hdr.xstep if hdr.xstep > 0 else 1.0
    ystep = hdr.ystep if hdr.ystep > 0 else 1.0
    ulx = hdr.xmin - 0.5 * xstep
    uly = (hdr.ymax if hdr.ymax != 0.0 else hdr.dy * ystep) + 0.5 * ystep
    return srs, (ulx, xstep, 0.0, uly, 0.0, -ystep)


def create_gdal_vrt_for_jhc(filepath: str, vrt_path: Optional[str] = None, output_dir: Optional[str] = None) -> str:
    """
    Create a zero-copy GDAL Raw Virtual Raster (.vrt) XML sidecar file for an OMG
    JHC_header raster (.r4, .sun, .8bit, .mos, .weight, .vert_prof).

    If output_dir is provided (recommended for read-only master archives like W:),
    the .vrt file is written inside output_dir and points to the absolute filepath
    on the archive drive without modifying anything on the archive drive.
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
    <ImageOffset>{JHC_OMG_RECLEN}</ImageOffset>
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
    min_lon_deg = math.degrees(ref_long * 1.0e-7 + min_long * pos_scale_rad)
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
    Reads the file in a single sequential buffer for high performance over network/WSL mounts.
    """
    with open(filepath, "rb") as f:
        buf = f.read()

    num_recs = len(buf) // JCU_BINNAV_RECLEN
    step = max(1, stride)
    records = []

    for idx in range(0, num_recs, step):
        off = idx * JCU_BINNAV_RECLEN
        # First 42 bytes contain the big-endian fields; bytes 42..48 are trailing struct padding
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

    # Circular mean for heading
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
    Parse key-value lever-arm parameters from an OMG .param file (supports both
    'KEY=VALUE' as written by read_kmall and 'KEY VALUE' formats) or .param_km.
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
    and Julian-day subdirectory trees (e.g. decnav/74/*.decnav) using os.scandir()
    without expensive stat() calls on every file.
    """
    results: List[Tuple[str, str, str]] = []
    if not os.path.isdir(root_dir):
        return results

    try:
        with os.scandir(root_dir) as entries:
            for entry in entries:
                if entry.name.startswith("."):
                    continue
                if entry.is_dir(follow_symlinks=False):
                    sub = entry.name
                    try:
                        with os.scandir(entry.path) as sub_entries:
                            for se in sub_entries:
                                if not se.name.startswith(".") and se.is_file(follow_symlinks=False):
                                    results.append((sub, se.name, se.path))
                    except OSError:
                        pass
                elif entry.is_file(follow_symlinks=False):
                    results.append(("", entry.name, entry.path))
    except OSError:
        pass

    results.sort(key=lambda t: (t[0], t[1]))
    return results


def _split_line_and_compound_ext(filename: str) -> Tuple[str, str]:
    """
    Handle compound OMG extensions like:
      0029_..._Viel.merged.ss_data -> ('0029_..._Viel', '.merged.ss_data')
      0029_..._Viel.merged.16_data -> ('0029_..._Viel', '.merged.16_data')
      0029_..._Viel.nav.strip      -> ('0029_..._Viel', '.nav.strip')
      0029_..._Viel.vert_prof.gif  -> ('0029_..._Viel', '.vert_prof.gif')
    """
    for comp in (".merged.ss_data", ".merged.16_data", ".nav.strip", ".vert_prof.gif", ".kmall.gz"):
        if filename.endswith(comp):
            return filename[: -len(comp)], comp
    return os.path.splitext(filename)


def scan_survey_workspace(
    workspace_dir: str,
    read_merged_headers: bool = False,
    read_decnav_summaries: bool = True,
    filter_subdir: str = "",
) -> Tuple[List[LineProcessingStatus], List[JhcHeaderInfo]]:
    """
    Scan an OMG processing workspace directory (supporting both flat raw/, merged/, decnav/, ss/
    and Julian-Day subdirectories like raw/74/, merged/74/, decnav/74/, ss/74/) and return:
      1. A list of LineProcessingStatus objects for every survey line.
      2. A list of JhcHeaderInfo objects for discovered OMG1 rasters (.r4, .sun, .8bit, .mos, .vert_prof).

    By default, `read_decnav_summaries=True` and `read_merged_headers=False` so scanning hundreds of
    lines over a network/WSL mount (/mnt/w) is fast and extracts track bounds/times/depths from .decnav.
    """
    workspace_dir = os.path.abspath(workspace_dir)
    raw_dir = os.path.join(workspace_dir, "raw")
    merged_dir = os.path.join(workspace_dir, "merged")
    decnav_dir = os.path.join(workspace_dir, "decnav")
    ss_dir = os.path.join(workspace_dir, "ss")

    lines_map: Dict[Tuple[str, str], LineProcessingStatus] = {}

    def get_line(subdir: str, name: str) -> LineProcessingStatus:
        key = (subdir, name)
        if key not in lines_map:
            lines_map[key] = LineProcessingStatus(line_name=name, subdir=subdir)
        return lines_map[key]

    # 1. Scan raw/
    for sub, fname, _fpath in _iter_dir_files(raw_dir):
        if filter_subdir and sub != filter_subdir:
            continue
        base, ext = _split_line_and_compound_ext(fname)
        ext_low = ext.lower()
        if ext_low in (".kmall", ".kmall.gz"):
            get_line(sub, base).has_raw_kmall = True
        elif ext_low == ".kmwcd":
            get_line(sub, base).has_raw_kmwcd = True
        elif ext_low == ".all":
            get_line(sub, base).has_raw_all = True
        elif ext_low == ".wcd":
            get_line(sub, base).has_raw_wcd = True

    # 2. Scan decnav/ (both .decnav and .nav)
    for sub, fname, fpath in _iter_dir_files(decnav_dir):
        if filter_subdir and sub != filter_subdir:
            continue
        if fname in ("all_dec.nav",) or fname.endswith("_all.decnav"):
            continue
        base, ext = _split_line_and_compound_ext(fname)
        if ext in (".decnav", ".nav"):
            st = get_line(sub, base)
            st.has_decnav = True
            st.decnav_path = fpath
            st.nav_path = fpath

    # 3. Scan merged/
    rasters: List[JhcHeaderInfo] = []
    for sub, fname, fpath in _iter_dir_files(merged_dir):
        if filter_subdir and sub != filter_subdir:
            continue
        if fname.startswith("justWC_"):
            continue
        base, ext = _split_line_and_compound_ext(fname)
        st = get_line(sub, base)

        if ext == ".merged":
            st.has_merged = True
            st.merged_path = fpath
            if read_merged_headers:
                try:
                    summ = parse_omg_merged_summary(fpath)
                    st.num_pings = summ.num_profiles
                    st.num_beams = summ.num_depths
                    if summ.max_obs_depth_m > 0:
                        st.min_depth_m = summ.min_obs_depth_m
                        st.max_depth_m = summ.max_obs_depth_m
                    st.bounds_wesn = (
                        summ.min_lon_deg,
                        summ.max_lon_deg,
                        summ.min_lat_deg,
                        summ.max_lat_deg,
                    )
                except Exception:
                    pass
        elif ext == ".watercol":
            st.has_watercol = True
        elif ext == ".WC_Phase1":
            st.has_wc_phase1 = True
        elif ext == ".WC_Phase2":
            st.has_wc_phase2 = True
        elif ext == ".vert_prof":
            st.has_vert_prof = True
            st.vert_prof_path = fpath
        elif ext == ".param":
            st.has_param = True
            st.param_path = fpath
        elif ext == ".param_km":
            st.has_param_km = True
            st.param_km_path = fpath
            if not st.param_path:
                st.param_path = fpath
        elif ext == ".nav_1":
            st.has_nav_1 = True
            if not st.nav_path:
                st.nav_path = fpath
        elif ext == ".nav":
            st.has_nav_active = True
            if not st.decnav_path:
                st.nav_path = fpath
        elif ext == ".nav.strip":
            st.has_nav_strip = True
        elif ext == ".net_att_1":
            st.has_net_att_1 = True
        elif ext == ".net_att_2":
            st.has_net_att_2 = True
        elif ext == ".orientation_1":
            st.has_orientation_1 = True
        elif ext == ".orientation":
            st.has_orientation_active = True
        elif ext in (".sv_filtered", ".svp_001", ".ssp"):
            st.has_sv_filtered = True
            if ext in (".sv_filtered", ".svp_001") or not st.svp_path:
                st.svp_path = fpath
        elif ext in (".ss_data", ".merged.ss_data"):
            st.has_ss_data = True
        elif ext == ".ss_data_deTVG":
            st.has_ss_detvg = True
        elif ext == ".ss":
            st.has_ss_gloria = True
            st.ss_path = fpath

    # 4. Scan ss/
    for sub, fname, fpath in _iter_dir_files(ss_dir):
        if filter_subdir and sub != filter_subdir:
            continue
        base, ext = _split_line_and_compound_ext(fname)
        if ext == ".ss":
            st = get_line(sub, base)
            st.has_ss_gloria = True
            st.ss_path = fpath

    # 5. Populate fast navigation summaries (bounds, start/end UTC, depth, heading, speed) from .decnav
    if read_decnav_summaries:
        for st in lines_map.values():
            target_nav = st.decnav_path or st.nav_path
            if target_nav and os.path.isfile(target_nav):
                try:
                    info = summarize_nav_file(target_nav, stride=1)
                    if info:
                        if not st.bounds_wesn:
                            st.bounds_wesn = info["bounds_wesn"]
                        st.start_time_utc = info["start_time_utc"]
                        st.end_time_utc = info["end_time_utc"]
                        st.mean_heading_deg = info["mean_heading_deg"]
                        st.mean_speed_kts = info["mean_speed_kts"]
                        if st.max_depth_m == 0.0 and info["max_depth_m"] > 0:
                            st.min_depth_m = info["min_depth_m"]
                            st.max_depth_m = info["max_depth_m"]
                except Exception:
                    pass

    # 6. Scan for OMG1 rasters (.r4, .sun*, .8bit, .mos, .weight, .blank, .vert_prof) in workspace root and grids/
    search_dirs = [workspace_dir]
    for sub in ("grids", "mosaic", "mosaics"):
        p = os.path.join(workspace_dir, sub)
        if os.path.isdir(p):
            search_dirs.append(p)

    raster_exts = {".r4", ".8bit", ".sun", ".mos", ".weight", ".ran", ".blank", ".vert_prof"}
    for sdir in search_dirs:
        try:
            with os.scandir(sdir) as entries:
                for entry in entries:
                    if not entry.is_file(follow_symlinks=False) or entry.name.endswith(".vrt"):
                        continue
                    _, ext = os.path.splitext(entry.name)
                    if ext in raster_exts or ".sun" in entry.name or entry.name in ("Pseudo", "colorbar"):
                        try:
                            with open(entry.path, "rb") as f:
                                magic = f.read(4)
                            if magic == b"OMG1":
                                rasters.append(parse_jhc_header(entry.path))
                        except Exception:
                            pass
        except OSError:
            pass

    sorted_lines = [lines_map[k] for k in sorted(lines_map.keys())]
    return sorted_lines, rasters


def export_tracklines_geojson(
    lines: List[LineProcessingStatus], out_geojson_path: str, nav_stride: int = 1
) -> str:
    """
    Export survey tracklines and per-line pipeline status attributes as a GeoJSON FeatureCollection
    so QGIS can render color-coded survey lines by processing stage or Julian day (like Qimera / HIPS).
    """
    os.makedirs(os.path.dirname(os.path.abspath(out_geojson_path)), exist_ok=True)
    features = []
    for st in lines:
        coords: List[List[float]] = []
        target_nav = st.decnav_path or st.nav_path
        if target_nav and os.path.isfile(target_nav):
            try:
                recs = parse_omg_nav(target_nav, stride=nav_stride)
                coords = [[round(r["lon"], 6), round(r["lat"], 6)] for r in recs]
            except Exception:
                coords = []
        if len(coords) < 2 and st.bounds_wesn:
            w, e, s, n = st.bounds_wesn
            if -180.0 <= w <= 180.0 and -90.0 <= s <= 90.0 and (w != 0.0 or e != 0.0):
                coords = [[round(w, 6), round(s, 6)], [round(e, 6), round(n, 6)]]

        if len(coords) < 2:
            continue

        props = asdict(st)
        props["display_id"] = st.display_id
        props["stage_summary"] = st.stage_summary
        if props.get("bounds_wesn"):
            props["bounds_wesn"] = [round(x, 6) for x in props["bounds_wesn"]]

        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": coords},
                "properties": props,
            }
        )

    fc = {
        "type": "FeatureCollection",
        "name": "OMG_Multibeam_Tracklines",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": features,
    }
    with open(out_geojson_path, "w", encoding="utf-8") as f:
        json.dump(fc, f, indent=2)
    return os.path.abspath(out_geojson_path)
