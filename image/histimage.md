---
layout: default
title: histimage
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 25
tool_name: histimage
source_path: code/image/histimage.c
category: Spectral & Backscatter Analysis
input_formats:
- ACRES 8-bit image
output_formats:
- Normalized 256-bin ASCII histogram table
related_tools:
- stretchacres
- classify
- MSpecBS_Xplot
---

# histimage

## Description
`histimage` (written by A. Y. / JCU, June 1990) interactively extracts and normalizes 256-bin greyscale intensity histograms from up to 10 user-defined rectangular sub-windows of an ACRES-format 8-bit image, writing a side-by-side comparison table to `<outfile>`.

## CLI Options & Usage

```bash
histimage -in <acres_file> -out <hist_table.txt>
```
* **`-in <acres_file>`**: Input ACRES-format 8-bit image (90-byte header).
* **`-out <hist_table.txt>`**: Output ASCII table containing normalized pixel counts (`0..1000` parts per thousand) for each grey level `0..255`.

## Interactive Prompts & Algorithm
1. Reads the 90-byte ACRES header (`row = header[4]`, `col = header[3]`) and loads the full image into memory.
2. Prompts the user for:
   * **`Number of histogram (max 10):`** — Number of sub-regions `nhist` to sample.
   * For each sub-region `k`: **`Input x_top, y_top, x_bot, y_bot :`** — Bounding pixel coordinates.
3. Accumulates the 256-bin histogram across each box `[x_top..x_bot, y_top..y_bot]`, normalizes bin counts by `1000 / ((x_bot - x_top) * (y_bot - y_top))`, and writes a formatted 256-row multi-column table to `<hist_table.txt>`.
