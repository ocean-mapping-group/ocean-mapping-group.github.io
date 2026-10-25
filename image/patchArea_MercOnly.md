---
layout: default
title: patchArea_MercOnly
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 37
tool_name: patchArea_MercOnly
source_path: code/image/patchArea_MercOnly.c
category: Mosaicking & Patching
input_formats:
- Mercator/UTM OMG1 8-bit or 32-bit float (.r4) mapsheets
output_formats:
- Merged Mercator OMG1 8-bit or 32-bit float (.r4) mapsheet
related_tools:
- patchArea
- paster4
- pastemos
---

# patchArea_MercOnly

## Description
`patchArea_MercOnly` is the earlier Mercator/UTM-focused predecessor to [`patchArea`](patchArea.html) (written by John Hughes Clarke, May 1995). It interactively patches georeferenced 8-bit or 32-bit floating-point (`-float`) `OMG1` (`JHC_header`) mapsheets into a target Mercator mapsheet (`-out`).

## CLI Options & Usage

```bash
patchArea_MercOnly -out <target_map> [-prime] [-float] \
  [-back <val>] [-ignore <val>] [-interp]
```
* **`-out <target_map>`**: Target Mercator `OMG1` mapsheet.
* **`-prime`**: Initializes the target mapsheet canvas to background (`-back`, default `255`) before patching.
* **`-float`**: Operates on 32-bit floating-point (`data_type = 3`, `.r4`) bathymetry grids (background `99999.0`) instead of 8-bit rasters.
* **`-back <val>`**: Background value when priming an 8-bit canvas (default: `255`).
* **`-ignore <val>`**: Transparent pixel value in imported 8-bit mapsheets (default: `255`).
* **`-interp`**: Enables 4-neighbor inverse-distance bilinear interpolation when resampling imported mapsheets.

## Algorithm
Prompts interactively for input mapsheet filenames (`Another file? (y/n)`), converts target pixel coordinates `(i, j)` to latitude/longitude via `merc_to_geog()` and into the input mapsheet's coordinate system (`MERCATOR` or `UTM`), and copies or bilinearly interpolates valid pixels into `<target_map>`. For batch scripting and full multi-projection support, use **[`patchArea`](patchArea.html)**.
