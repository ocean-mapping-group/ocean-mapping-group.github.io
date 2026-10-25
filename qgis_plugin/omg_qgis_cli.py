#!/usr/bin/env python3
"""
Standalone Command-Line Interface & Self-Test Utility for the OMG QGIS Plugin.

Can be used by graduate students or the LocalAI assistant outside of QGIS to:
  1. Inspect OMG1 raster headers (.r4, .sun, .8bit, .mos, .vert_prof, .weight, .blank)
  2. Generate zero-copy GDAL Virtual Raster (.vrt) sidecars in a local output folder
  3. Inspect OMG_HDCS (.merged) summary headers and .nav / .decnav files
  4. Scan an entire multi-day OMG survey workspace (e.g. 02_Bransfield) and export
     QGIS-ready GeoJSON tracklines without modifying any files on the source archive.
"""

import argparse
from collections import Counter
import os
import sys

from omg_qgis_plugin.omg_binary_io import (
    create_gdal_vrt_for_jhc,
    export_tracklines_geojson,
    parse_jhc_header,
    parse_omg_merged_summary,
    scan_survey_workspace,
)


def cmd_inspect_raster(filepath: str, make_vrt: bool = False, output_dir: str = ""):
    hdr = parse_jhc_header(filepath)
    print(f"=== OMG1 Raster Header: {os.path.basename(hdr.filepath)} ===")
    print(f"  Path       : {hdr.filepath}")
    print(f"  Dimensions : {hdr.dx} x {hdr.dy} pixels")
    print(f"  Data Type  : {hdr.data_type_name} (GDAL: {hdr.gdal_data_type})")
    print(f"  Bounds     : W={hdr.xmin:.6f}, E={hdr.xmax:.6f}, S={hdr.ymin:.6f}, N={hdr.ymax:.6f}")
    print(f"  Step Size  : dx={hdr.xstep:.4f}, dy={hdr.ystep:.4f}")
    print(f"  Projection : {hdr.projection_name}")
    print(f"  Value Range: min={hdr.min_value:.4f}, max={hdr.max_value:.4f}")
    if hdr.sun_elev > 0 or hdr.sun_azi > 0:
        print(f"  Sun Params : azimuth={hdr.sun_azi:.1f}°, elevation={hdr.sun_elev:.1f}°, exag={hdr.sun_exag:.1f}x")
    if make_vrt:
        vrt_path = create_gdal_vrt_for_jhc(filepath, output_dir=output_dir or None)
        print(f"  Created Zero-Copy GDAL VRT: {vrt_path}")


def cmd_scan_workspace(
    workspace_dir: str,
    out_geojson: str = "",
    day_filter: str = "",
    read_merged: bool = False,
    limit_print: int = 30,
):
    lines, rasters = scan_survey_workspace(
        workspace_dir,
        read_merged_headers=read_merged,
        read_decnav_summaries=True,
        filter_subdir=day_filter,
    )
    print(f"=== OMG Workspace Scan: {os.path.abspath(workspace_dir)} ===")
    print(f"Discovered {len(lines)} survey line(s) and {len(rasters)} top-level OMG1 raster(s).")

    by_day = Counter(l.subdir or "root" for l in lines)
    by_stage = Counter(l.stage_summary for l in lines)
    print("Lines per Julian Day:", dict(sorted(by_day.items())))
    print("Lines per Stage     :", dict(by_stage))

    all_lons = [ b[0] for l in lines if l.bounds_wesn for b in [l.bounds_wesn] ] + [
        b[1] for l in lines if l.bounds_wesn for b in [l.bounds_wesn]
    ]
    all_lats = [ b[2] for l in lines if l.bounds_wesn for b in [l.bounds_wesn] ] + [
        b[3] for l in lines if l.bounds_wesn for b in [l.bounds_wesn]
    ]
    if all_lons and all_lats:
        print(
            f"Overall Survey Bounds: West={min(all_lons):.5f}°, East={max(all_lons):.5f}°, "
            f"South={min(all_lats):.5f}°, North={max(all_lats):.5f}°\n"
        )

    if lines:
        print(
            f"{'Day':<5} {'Line Name':<38} {'Stage':<38} {'Start UTC':<20} {'Hdg':>6} {'Kts':>5} {'Depth(m)':>10}"
        )
        print("-" * 128)
        for st in lines[:limit_print]:
            d_str = f"{st.min_depth_m:.0f}-{st.max_depth_m:.0f}" if st.max_depth_m > 0 else "-"
            print(
                f"{st.subdir:<5} {st.line_name:<38} {st.stage_summary:<38} "
                f"{st.start_time_utc:<20} {st.mean_heading_deg:>5.1f}° {st.mean_speed_kts:>5.1f} {d_str:>10}"
            )
        if len(lines) > limit_print:
            print(f"... ({len(lines) - limit_print} additional lines omitted from table) ...")
        print()

    if out_geojson and lines:
        gpath = export_tracklines_geojson(lines, out_geojson, nav_stride=1)
        print(f"Exported {len(lines)} survey tracklines to GeoJSON: {gpath}")


def main():
    parser = argparse.ArgumentParser(description="OMG QGIS Plugin CLI & Binary Inspector")
    sub = parser.add_subparsers(dest="cmd")

    p_ras = sub.add_parser("raster", help="Inspect an OMG1 raster (.r4, .sun, .8bit, .mos, .vert_prof)")
    p_ras.add_argument("files", nargs="+", help="Input OMG1 raster file(s)")
    p_ras.add_argument("--vrt", action="store_true", help="Write zero-copy GDAL .vrt sidecar file(s)")
    p_ras.add_argument("--output-dir", default="", help="Directory to write .vrt files (keeps source archive untouched)")

    p_mrg = sub.add_parser("merged", help="Inspect an OMG_HDCS .merged swath summary header")
    p_mrg.add_argument("files", nargs="+", help="Input .merged file(s)")

    p_scan = sub.add_parser("scan", help="Scan a survey workspace directory (raw/, merged/, decnav/, ss/)")
    p_scan.add_argument("workspace", help="Path to survey workspace directory")
    p_scan.add_argument("--day", default="", help="Optional Julian day / subdirectory filter (e.g. 74)")
    p_scan.add_argument("--merged-headers", action="store_true", help="Also read .merged binary headers")
    p_scan.add_argument("--geojson", default="", help="Output GeoJSON path for survey tracklines")
    p_scan.add_argument("--limit", type=int, default=30, help="Max lines to print in terminal table")

    args = parser.parse_args()
    if args.cmd == "raster":
        for f in args.files:
            cmd_inspect_raster(f, make_vrt=args.vrt, output_dir=args.output_dir)
    elif args.cmd == "merged":
        for f in args.files:
            summ = parse_omg_merged_summary(f)
            print(summ)
    elif args.cmd == "scan":
        cmd_scan_workspace(
            args.workspace,
            out_geojson=args.geojson,
            day_filter=args.day,
            read_merged=args.merged_headers,
            limit_print=args.limit,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
