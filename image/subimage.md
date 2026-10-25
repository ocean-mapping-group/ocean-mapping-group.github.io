---
layout: default
title: subimage
parent: Image Tools
nav_order: 51
tool_name: subimage
source_path: code/image/subimage.c
category: Image & Raster Processing
input_formats: ["OMG1 8-bit or 32-bit float (.r4) array", "Raw 8-bit raster (-raw)"]
output_formats: ["Cropped OMG1 8-bit or 32-bit float (.r4) sub-image"]
related_tools: ["8bit2acres", "pastemos", "paster4", "patchArea", "fft2dimage"]
---

# subimage

## Description
`subimage` extracts a rectangular sub-window (`-cols` × `-rows`) from an 8-bit (`data_type = 1`), 32-bit floating-point (`-float`, `data_type = 3`), or raw headerless (`-raw`) raster. The crop window can be specified either by upper-left pixel coordinates (`-left_x`, `-top_y`) or centered on a geographic coordinate (`-geocentre <lat> <lon>`), with automatic recalculation of the `OMG1` (`JHC_header`) geographic bounding box.

## CLI Options & Usage
```bash
subimage -in <infile> -out <outfile> -rows <nrows> -cols <ncols> \
  [-left_x <x0> -top_y <y0> | -geocentre <lat> <lon>] \
  [-float] [-georef] [-raw -in_rows <nr> -in_cols <nc>]
```
* **`-in <infile> -out <outfile>`**: Input and output `OMG1` raster files.
* **`-rows <nrows> -cols <ncols>`**: Height (`ymax`) and width (`xmax`) of the extracted sub-image in pixels.
* **`-left_x <x0> -top_y <y0>`**: Upper-left pixel coordinates of the crop window (default: `0, 0`).
* **`-geocentre <lat> <lon>`**: Centers the `cols × rows` crop window on `(lat, lon)` using `resolve_pixel_from_pos()` (`x0 = px - cols/2`, `y0 = py - rows/2`).
* **`-float`**: Extracts 4-byte floating-point (`data_type = 3`, `.r4`) cells (filling out-of-bounds padding with `99999.0` instead of `255`).
* **`-georef`**: Forces Mercator bounding-box recalculation (`merc_to_geog`) from `left_x`, `top_y`, `dx`, and `dy`.
* **`-raw -in_rows <nr> -in_cols <nc>`**: Reads a headerless raw 8-bit raster of dimensions `nc × nr` and wraps the extracted sub-window in an `OMG1` header.

## Algorithm
1. Reads the input `JHC_header` (or initializes one if `-raw` is set) and resolves `(left_x, top_y)`.
2. Calls `resolve_pos_from_pixel()` at `(left_x, top_y)` and `(left_x + cols, top_y + rows)` to update `(tlat, tlon)` and `(blat, blon)` in the output `JHC_header`.
3. Copies pixels inside `[left_x .. left_x + cols - 1, top_y .. top_y + rows - 1]` into the output buffer (padding any overhang beyond the source borders with `255` or `99999.0`) and writes `<outfile>`.
