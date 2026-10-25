---
layout: default
title: readheader
parent: Image Tools
nav_order: 40
tool_name: readheader
source_path: code/image/readheader.c
category: Satellite, SAR & Format Conversion
input_formats: ["landsat_rec scanline file"]
output_formats: ["ASCII scanline navigation table"]
related_tools: ["addheader", "control_points", "landsat2acres"]
---

# readheader

## Description
`readheader` (written by A. Y. / JCU, July 1990) inspects a `landsat_rec` scanline-headed Landsat file (created by [`addheader`](addheader.md) or calibrated by [`control_points`](control_points.md)) and dumps the scene metadata and per-scanline center coordinates (`scanline`, `latitude`, `longitude`) to an ASCII file.

## CLI Options & Usage
```bash
readheader -in <landsat_rec_file> -out <header_dump.txt>
```
* **`-in <landsat_rec_file>`**: Input `landsat_rec` file (`2340` scanlines).
* **`-out <header_dump.txt>`**: Output ASCII summary table.

## Output Format
Reads `landsat_rec` records (`0 .. 2339`). From the first scanline (`i == 0`), writes the scene-level orbital parameters:
* `row`, `path`, `blue` band indicator
* `scan_pixel_size` (m), `track_pixel_size` (m)
* `altitude` (km), `azimuth` (degrees, converted from radians)

Then prints a 2340-line table of `scanline_index`, `lat` (degrees), and `lon` (degrees) for every scanline in the scene.
