---
layout: default
title: expandr4
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 21
tool_name: expandr4
source_path: code/image/expandr4.c
category: Image & Raster Processing
input_formats:
- OMG1 32-bit float grid (.r4)
output_formats:
- Upsampled (or downsampled) OMG1 32-bit float grid (.r4)
related_tools:
- expand
- decr4
- changeAspect
- patchArea
---

# expandr4

## Description
`expandr4` is the 32-bit floating-point (`data_type = 3`, `.r4`) counterpart to [`expand`](expand.html). It upsamples (when `-factor > 1`) or downsamples (when `-factor < -1`) a georeferenced `OMG1` `.r4` bathymetric or backscatter grid using either nearest-neighbor block replication or two-pass bilinear interpolation (`-interp`) with optional no-data masking (`-mask`, `99999.0`).

## CLI Options & Usage

```bash
expandr4 -in <infile.r4> -out <outfile.r4> -factor <n> [-interp] [-mask]
```
* **`-in <infile.r4>`**: Input 32-bit float `OMG1` `.r4` file.
* **`-out <outfile.r4>`**: Output resampled 32-bit float `.r4` file.
* **`-factor <n>`**: Integer scale factor (`> 1` expands by `n`; `< -1` decimates by `|n|`).
* **`-interp`**: Performs bilinear interpolation between adjacent grid nodes.
* **`-mask`**: Prevents no-data values (`>= 9999.0` / `99999.0`) from being averaged into valid neighboring depth/backscatter cells during interpolation.

## Algorithm
1. Adjusts `xmax`, `ymax`, `dx`, and `dy` in the `JHC_header` by `factor`.
2. In `-interp` mode, populates grid nodes `(i * factor, j * factor)` with source floats, linearly interpolates horizontally between valid row nodes `(v1, v2)`, and then linearly interpolates vertically down all `new_xmax` columns, preserving `99999.0` whenever either endpoint is flagged and `-mask` is active.
