---
layout: default
title: addheader
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 8
tool_name: addheader
source_path: code/image/addheader.c
category: Satellite, SAR & Format Conversion
input_formats:
- ACRES 8-bit Landsat image
output_formats:
- Georeferenced landsat_rec scanline file
related_tools:
- readheader
- control_points
- landsat2acres
- lsfilter
---

# addheader (`image`)

## Description
`addheader` (written by A. Y. / JCU, July 1990) converts an ACRES-format Landsat MSS image into a scanline-headed `landsat_rec` file (`landsat.h`), attaching nominal WRS-1/WRS-2 orbital track parameters (path, row, scene center latitude/longitude, altitude, track azimuth, and across/along-track pixel dimensions) to every scanline.

## CLI Options & Usage

```bash
addheader -in <acres_file> -out <landsat_rec_file> \
  -path <n> -row <n> -cent_lat <deg> -cent_lon <deg> [-blue]
```
* **`-in <acres_file>`**: Input ACRES-format Landsat image (with 90-byte header).
* **`-out <landsat_rec_file>`**: Output `landsat_rec` scanline file.
* **`-path <n> -row <n>`**: Landsat World Reference System path and row numbers.
* **`-cent_lat <deg> -cent_lon <deg>`**: Scene center latitude and longitude in decimal degrees.
* **`-blue`**: Sets the `blue` band indicator flag (`1`) in the output scanline header.

## Algorithm
1. Reads the 90-byte ACRES header from `<acres_file>` and initializes default Landsat MSS orbital geometry: `scan_pixel_size = 56.0 m`, `track_pixel_size = 79.0 m`, `altitude = 918.0 km`, and nominal descending track azimuth `azi = 190.0°`.
2. Computes the geographic coordinates `(start_lat, start_lon)` of the top-center pixel (row 0) from `(cent_lat, cent_lon)` by projecting backward along `azi - 180°` over `1170` scanlines (`1170 × 79 m`) using `geog_posn()`.
3. Steps through all `2340` scanlines, advancing `(lat, lon)` along `azi` by `track_pixel_size` (`79 m`) per row and writing a `landsat_rec` structure (header + `3240` pixel bytes) for each line. Fine ground-control registration can then be applied using [`control_points`](control_points.html).
