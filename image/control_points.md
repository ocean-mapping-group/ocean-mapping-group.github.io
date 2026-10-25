---
layout: default
title: control_points
parent: Image Tools
nav_order: 13
tool_name: control_points
source_path: code/image/control_points.c
category: Satellite, SAR & Format Conversion
input_formats: ["landsat_rec scanline file", "ASCII control point file (2 GCPs)"]
output_formats: ["Geometrically calibrated landsat_rec file"]
related_tools: ["addheader", "readheader", "distortImage", "landsat2acres"]
---

# control_points

## Description
`control_points` (written by A. Y. / JCU, July 1990) refines the orbital navigation geometry stored in a `landsat_rec` scanline file (created by [`addheader`](addheader.md)) using two Ground Control Points (GCPs) with known pixel `(x, y)` and geographic `(latitude, longitude)` coordinates. It solves for the true satellite track heading (`track_angle`), along-track line spacing (`track_pixel_size`), across-track sample spacing (`scan_pixel_size`), and per-scanline center coordinates.

## CLI Options & Usage
```bash
control_points -in <in_landsat> -control <gcp_file> -out <out_landsat> [-scan_pixel <m>]
```
* **`-in <in_landsat>`**: Input `landsat_rec` file (`2340` rows × `3240` columns).
* **`-control <gcp_file>`**: ASCII file containing two lines: `x1 y1 lat1 lon1` and `x2 y2 lat2 lon2`.
* **`-out <out_landsat>`**: Output `landsat_rec` file with updated per-scanline headers.
* **`-scan_pixel <m>`**: Fixes the across-track pixel size to `<m>` meters instead of solving for both `scan_pixel_size` and `track_pixel_size` simultaneously.

## Algorithm
1. Computes the true geodetic distance `dist` and forward azimuth `angle` between GCP 1 `(lat1, lon1)` and GCP 2 `(lat2, lon2)` using `geog_dist()`.
2. Solves the 2D transformation between scanline/pixel offsets `(x2 - x1, y2 - y1)` and geodetic vector `(dist, angle)` to determine `track_angle`, `track_pixel_size`, and `scan_pixel_size`.
3. Projects from GCP 1 to the top-center pixel `(x = 1620, y = 0)` via `geog_posn()`, then steps down all `2340` scanlines along `track_angle`, writing updated `(lat, lon, azi, scan_pixel_size, track_pixel_size)` headers into `<out_landsat>`.
