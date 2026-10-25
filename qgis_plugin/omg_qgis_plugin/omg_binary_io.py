"""
Pure-Python Binary Reader, GDAL Zero-Copy VRT Generator, and Workspace Scanner
for UNB Ocean Mapping Group (OMG) Multibeam Sonar Files.

Supports:
  - JHC_header ("OMG1") 1024-byte big-endian rasters (.r4, .8bit, .sun, .mos, .weight, .ran, .blank)
  - OMG_HDCS (.merged) summary headers (v1-v4) and ping profile headers
  - JCU Binary Navigation (.nav, .nav_1..3) 48-byte big-endian records
  - OMG ASCII Ship Parameter (.param) lever-arm files
  - OMG ASCII Sound Velocity Profile (.sv_filtered) files
"""

import json
import math
import os
import struct
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple


JHC_OMG_RECLEN = 1024
JCU_BINNAV_RECLEN = 48
OMG_HDCS_SUMMARY_HEADER_SIZE = 96
OMG_HDCS_SUMMARY_V4EXTRA_SIZE = 168


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
            0: "Unprojected / Local Grid",
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
    has_raw_kmall: bool = False
    has_raw_kmwcd: bool = False
    has_raw_all: bool = False
    has_raw_wcd: bool = False
    has_merged: bool = False
    has_watercol: bool = False
    has_wc_phase1: bool = False
    has_param: bool = False
    has_nav_1: bool = False
    has_nav_active: bool = False
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
    bounds_wesn: Optional[Tuple[float, float, float, float]] = None
    merged_path: Optional[str] = None
    nav_path: Optional[str] = None
    param_path: Optional[str] = None
    ss_path: Optional[str] = None

    @property
    def stage_summary(self) -> str:
        """Returns a human-readable pipeline stage badge for Qimera/HIPS table."""
        if self.has_ss_gloria and self.has_merged and self.has_decnav and self.has_orientation_active:
            return "COMPLETE (Bathy + Nav + Att + SS)"
        if self.has_merged and self.has_decnav and self.has_orientation_active:
            return "BATHY READY (Nav + Att Merged)"
        if self.has_merged and self.has_nav_active:
            return "UNPACKED (Pending Att / Ray-Trace)"
        if self.has_merged:
            return "UNPACKED (Pending .nav / .orientation Copy)"
        if self.has_raw_kmall or self.has_raw_all:
            return "RAW ONLY (Not Unravelled)"
        return "PARTIAL"


def parse_jhc_header(filepath: str) -> JhcHeaderInfo:
    """
    Parse the 1024-byte big-endian JHC_header ("OMG1") from an OMG raster file
    (.r4, .8bit, .sun, .mos, .weight, .ran, .blank).
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
    # Default: pixel center convention nudged by half a pixel to upper-left corner (r4toESRI.c lines 242-246)
    if hdr.projection == 2:
        # UTM projection with central meridian hdr.proj_merid
        zone = int(round((hdr.proj_merid + 183.0) / 6.0))
        zone = max(1, min(60, zone))
        is_south = hdr.hemisphere.lower() == "s"
        epsg = (32700 + zone) if is_south else (32600 + zone)
        srs = f"EPSG:{epsg}"
        ulx = hdr.xmin - 0.5 * hdr.xstep
        uly = hdr.ymax + 0.5 * hdr.ystep
        return srs, (ulx, hdr.xstep, 0.0, uly, 0.0, -hdr.ystep)

    if hdr.projection == 1:
        # Mercator projection (WGS84) with standard parallel / scaling at proj_merid (which in OMG Mercator stores reference lat)
        lat_ts = hdr.proj_merid if abs(hdr.proj_merid) < 89.0 else 0.0
        srs = f"+proj=merc +lat_ts={lat_ts} +lon_0=0.0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
        # Convert geographic xmin, ymax (degrees) into Mercator meters
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

    if hdr.projection == 3 or (hdr.projection == 0 and (-180.0 <= hdr.xmin <= 180.0 and -90.0 <= hdr.ymin <= 90.0 and hdr.xmin != 0.0)):
        # Geographic coordinates (xmin/xmax/ymin/ymax in degrees, xstep/ystep in arc-minutes if projection==3)
        srs = "EPSG:4326"
        xres = (hdr.xstep / 60.0) if hdr.projection == 3 else hdr.xstep
        yres = (hdr.ystep / 60.0) if hdr.projection == 3 else hdr.ystep
        ulx = hdr.xmin - 0.5 * xres
        uly = hdr.ymax + 0.5 * yres
        return srs, (ulx, xres, 0.0, uly, 0.0, -yres)

    # Unprojected / Local Cartesian engineering grid (in meters)
    srs = ""
    xstep = hdr.xstep if hdr.xstep > 0 else 1.0
    ystep = hdr.ystep if hdr.ystep > 0 else 1.0
    ulx = hdr.xmin - 0.5 * xstep
    uly = (hdr.ymax if hdr.ymax != 0.0 else hdr.dy * ystep) + 0.5 * ystep
    return srs, (ulx, xstep, 0.0, uly, 0.0, -ystep)


def create_gdal_vrt_for_jhc(filepath: str, vrt_path: Optional[str] = None) -> str:
    """
    Create a zero-copy GDAL Raw Virtual Raster (.vrt) XML sidecar file for an OMG
    JHC_header raster (.r4, .sun, .8bit, .mos, .weight).

    Because OMG rasters store flat row-major big-endian (MSB) pixel arrays starting
    at byte offset 1024, GDAL/QGIS can read the binary file directly via VRTRawRasterBand
    without converting or duplicating data on disk.
    """
    hdr = parse_jhc_header(filepath)
    if vrt_path is None:
        vrt_path = filepath + ".vrt"

    srs, gt = _compute_crs_and_geotransform(hdr)
    pixel_offset = hdr.bytes_per_pixel
    line_offset = hdr.dx * hdr.bytes_per_pixel
    rel_filename = os.path.basename(filepath) if os.path.dirname( os.path.abspath(vrt_path) ) == os.path.dirname(hdr.filepath) else hdr.filepath
    rel_attr = "1" if rel_filename == os.path.basename(filepath) else "0"

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

    # Convert OMG_HDCS internal integer coordinates (100 nRad reference + nRad offset) to degrees
    # In OMG_HDCS_jversion.c: lat_rad = (refLat * 1e-7) + (offset * 1e-9 * positionScale)
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
    Read binary 48-byte big-endian jcu_nav_rec records from an OMG .nav file
    (code/subr/jcu_nav.c lines 62-125).
    """
    records = []
    file_size = os.path.getsize(filepath)
    num_recs = file_size // JCU_BINNAV_RECLEN
    step = max(1, stride)

    with open(filepath, "rb") as f:
        for idx in range(0, num_recs, step):
            f.seek(idx * JCU_BINNAV_RECLEN)
            raw = f.read(JCU_BINNAV_RECLEN)
            if len(raw) < JCU_BINNAV_RECLEN:
                break
            lat, lon, time_s, centisecs, _pad, azi, vel, depth, f0, f1, f2, f3 = struct.unpack(
                ">ddihhffhhhhh", raw
            )
            if -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0 and (lat != 0.0 or lon != 0.0):
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


def parse_omg_param(filepath: str) -> Dict[str, str]:
    """Parse key-value lever-arm parameters from an OMG .param file."""
    params: Dict[str, str] = {}
    if not os.path.isfile(filepath):
        return params
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                params[parts[0]] = " ".join(parts[1:])
    return params


def scan_survey_workspace(workspace_dir: str) -> Tuple[List[LineProcessingStatus], List[JhcHeaderInfo]]:
    """
    Scan an OMG processing workspace directory (containing raw/, merged/, decnav/, ss/, and grids)
    and return:
      1. A list of LineProcessingStatus objects for every survey line.
      2. A list of JhcHeaderInfo objects for every OMG raster (.r4, .sun, .8bit, .mos, .weight, .blank).
    """
    workspace_dir = os.path.abspath(workspace_dir)
    raw_dir = os.path.join(workspace_dir, "raw")
    merged_dir = os.path.join(workspace_dir, "merged")
    decnav_dir = os.path.join(workspace_dir, "decnav")
    ss_dir = os.path.join(workspace_dir, "ss")

    lines_map: Dict[str, LineProcessingStatus] = {}

    def get_line(name: str) -> LineProcessingStatus:
        if name not in lines_map:
            lines_map[name] = LineProcessingStatus(line_name=name)
        return lines_map[name]

    # 1. Scan raw/
    if os.path.isdir(raw_dir):
        for fname in sorted(os.listdir(raw_dir)):
            base, ext = os.path.splitext(fname)
            ext_low = ext.lower()
            if ext_low == ".kmall":
                get_line(base).has_raw_kmall = True
            elif ext_low == ".kmwcd":
                get_line(base).has_raw_kmwcd = True
            elif ext_low == ".all":
                get_line(base).has_raw_all = True
            elif ext_low == ".wcd":
                get_line(base).has_raw_wcd = True

    # 2. Scan merged/
    if os.path.isdir(merged_dir):
        for fname in sorted(os.listdir(merged_dir)):
            if fname.startswith("justWC_"):
                continue
            fpath = os.path.join(merged_dir, fname)
            if not os.path.isfile(fpath) or os.path.getsize(fpath) == 0:
                continue
            base, ext = os.path.splitext(fname)
            if ext == ".merged":
                st = get_line(base)
                st.has_merged = True
                st.merged_path = fpath
                try:
                    summ = parse_omg_merged_summary(fpath)
                    st.num_pings = summ.num_profiles
                    st.num_beams = summ.num_depths
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
                get_line(base).has_watercol = True
            elif ext == ".WC_Phase1":
                get_line(base).has_wc_phase1 = True
            elif ext == ".param":
                st = get_line(base)
                st.has_param = True
                st.param_path = fpath
            elif ext == ".nav_1":
                st = get_line(base)
                st.has_nav_1 = True
                if not st.nav_path:
                    st.nav_path = fpath
            elif ext == ".nav":
                st = get_line(base)
                st.has_nav_active = True
                st.nav_path = fpath
            elif ext == ".net_att_1":
                get_line(base).has_net_att_1 = True
            elif ext == ".net_att_2":
                get_line(base).has_net_att_2 = True
            elif ext == ".orientation_1":
                get_line(base).has_orientation_1 = True
            elif ext == ".orientation":
                get_line(base).has_orientation_active = True
            elif ext == ".sv_filtered":
                get_line(base).has_sv_filtered = True
            elif ext == ".ss_data":
                get_line(base).has_ss_data = True
            elif ext == ".ss_data_deTVG":
                get_line(base).has_ss_detvg = True
            elif ext == ".ss":
                st = get_line(base)
                st.has_ss_gloria = True
                st.ss_path = fpath

    # 3. Scan decnav/
    if os.path.isdir(decnav_dir):
        for fname in sorted(os.listdir(decnav_dir)):
            if fname == "all_dec.nav":
                continue
            fpath = os.path.join(decnav_dir, fname)
            base, ext = os.path.splitext(fname)
            if ext == ".nav" and os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
                st = get_line(base)
                st.has_decnav = True
                st.nav_path = fpath

    # 4. Scan ss/
    if os.path.isdir(ss_dir):
        for fname in sorted(os.listdir(ss_dir)):
            fpath = os.path.join(ss_dir, fname)
            base, ext = os.path.splitext(fname)
            if ext == ".ss" and os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
                st = get_line(base)
                st.has_ss_gloria = True
                st.ss_path = fpath

    # 5. Scan for OMG1 rasters (.r4, .sun*, .8bit, .mos, .weight, .blank) in workspace root and subdirs
    rasters: List[JhcHeaderInfo] = []
    search_dirs = [workspace_dir]
    for sub in ("grids", "mosaic", "mosaics"):
        p = os.path.join(workspace_dir, sub)
        if os.path.isdir(p):
            search_dirs.append(p)

    for sdir in search_dirs:
        for fname in sorted(os.listdir(sdir)):
            if fname.endswith(".vrt"):
                continue
            fpath = os.path.join(sdir, fname)
            if not os.path.isfile(fpath) or os.path.getsize(fpath) < JHC_OMG_RECLEN:
                continue
            try:
                with open(fpath, "rb") as f:
                    magic = f.read(4)
                if magic == b"OMG1":
                    rasters.append(parse_jhc_header(fpath))
            except Exception:
                pass

    sorted_lines = [lines_map[k] for k in sorted(lines_map.keys())]
    return sorted_lines, rasters


def export_tracklines_geojson(lines: List[LineProcessingStatus], out_geojson_path: str, nav_stride: int = 10) -> str:
    """
    Export survey tracklines and per-line pipeline status flags as a GeoJSON FeatureCollection
    so QGIS can render color-coded survey lines by processing stage (like Qimera / CARIS HIPS).
    """
    features = []
    for st in lines:
        coords: List[List[float]] = []
        if st.nav_path and os.path.isfile(st.nav_path):
            try:
                recs = parse_omg_nav(st.nav_path, stride=nav_stride)
                coords = [[r["lon"], r["lat"]] for r in recs]
            except Exception:
                coords = []
        if len(coords) < 2 and st.bounds_wesn:
            w, e, s, n = st.bounds_wesn
            if -180.0 <= w <= 180.0 and -90.0 <= s <= 90.0 and (w != 0.0 or e != 0.0):
                coords = [[w, s], [e, n]]

        if len(coords) < 2:
            continue

        props = asdict(st)
        props["stage_summary"] = st.stage_summary
        if props.get("bounds_wesn"):
            props["bounds_wesn"] = list(props["bounds_wesn"])

        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": coords},
                "properties": props,
            }
        )

    fc = {"type": "FeatureCollection", "features": features}
    with open(out_geojson_path, "w", encoding="utf-8") as f:
        json.dump(fc, f, indent=2)
    return os.path.abspath(out_geojson_path)
