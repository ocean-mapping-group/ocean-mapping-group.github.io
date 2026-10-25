#!/usr/bin/env python3
"""
Standalone Command-Line Interface & Self-Test Utility for the OMG QGIS Plugin.

Can be used by graduate students or the LocalAI assistant outside of QGIS to:
  1. Inspect OMG1 raster headers (.r4, .sun, .8bit, .mos, .weight, .blank)
  2. Generate zero-copy GDAL Virtual Raster (.vrt) sidecars for QGIS
  3. Inspect OMG_HDCS (.merged) summary headers and .nav files
  4. Scan an OMG survey workspace and print a Qimera/HIPS-style processing status table
"""

import argparse
import os
import sys

from omg_qgis_plugin.omg_binary_io import (
    create_gdal_vrt_for_jhc,
    export_tracklines_geojson,
    parse_jhc_header,
    parse_omg_merged_summary,
    scan_survey_workspace,
)


def cmd_inspect_raster(filepath: str, make_vrt: bool = False):
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
        vrt_path = create_gdal_vrt_for_jhc(filepath)
        print(f"  Created Zero-Copy GDAL VRT: {vrt_path}")


def cmd_scan_workspace(workspace_dir: str, out_geojson: str = ""):
    lines, rasters = scan_survey_workspace(workspace_dir)
    print(f"=== OMG Workspace Scan: {os.path.abspath(workspace_dir)} ===")
    print(f"Discovered {len(lines)} survey line(s) and {len(rasters)} OMG1 raster(s).\n")

    if lines:
        print(f"{'Line Name':<32} {'Stage':<36} {'Pings':>7} {'Beams':>6} {'Depth (m)':>15}")
        print("-" * 100)
        for st in lines:
            d_str = f"{st.min_depth_m:.1f}-{st.max_depth_m:.1f}" if st.max_depth_m > 0 else "-"
            print(f"{st.line_name:<32} {st.stage_summary:<36} {st.num_pings:>7} {st.num_beams:>6} {d_str:>15}")
        print()

    if rasters:
        print(f"{'Raster File':<28} {'Type':<18} {'Size (dx x dy)':<16} {'Step':<14} {'Min..Max':<20}")
        print("-" * 100)
        for r in rasters:
            print(
                f"{os.path.basename(r.filepath):<28} {r.data_type_name:<18} "
                f"{f'{r.dx}x{r.dy}':<16} {f'{r.xstep:.2f}x{r.ystep:.2f}':<14} "
                f"{f'{r.min_value:.2f}..{r.max_value:.2f}':<20}"
            )

    if out_geojson and lines:
        gpath = export_tracklines_geojson(lines, out_geojson)
        print(f"\nExported tracklines GeoJSON to: {gpath}")


def main():
    parser = argparse.ArgumentParser(description="OMG QGIS Plugin CLI & Binary Inspector")
    sub = parser.add_subparsers(dest="cmd")

    p_ras = sub.add_parser("raster", help="Inspect an OMG1 raster (.r4, .sun, .8bit, .mos) and optionally create a .vrt")
    p_ras.add_argument("files", nargs="+", help="Input OMG1 raster file(s)")
    p_ras.add_argument("--vrt", action="store_true", help="Write zero-copy GDAL .vrt sidecar file(s)")

    p_mrg = sub.add_parser("merged", help="Inspect an OMG_HDCS .merged swath summary header")
    p_mrg.add_argument("files", nargs="+", help="Input .merged file(s)")

    p_scan = sub.add_parser("scan", help="Scan a survey workspace directory (raw/, merged/, decnav/, ss/)")
    p_scan.add_argument("workspace", help="Path to survey workspace directory")
    p_scan.add_argument("--geojson", default="", help="Optional output GeoJSON path for survey tracklines")

    args = parser.parse_args()
    if args.cmd == "raster":
        for f in args.files:
            cmd_inspect_raster(f, make_vrt=args.vrt)
    elif args.cmd == "merged":
        for f in args.files:
            summ = parse_omg_merged_summary(f)
            print(summ)
    elif args.cmd == "scan":
        cmd_scan_workspace(args.workspace, out_geojson=args.geojson)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
