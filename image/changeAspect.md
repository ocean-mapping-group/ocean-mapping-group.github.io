---
layout: default
title: changeAspect
parent: Image Tools
nav_order: 9
tool_name: changeAspect
source_path: code/image/changeAspect.c
category: Image & Raster Processing
input_formats: ["OMG1 8-bit or 32-bit float (.r4) array"]
output_formats: ["Rescaled OMG1 8-bit or 32-bit float (.r4) array"]
related_tools: ["expand", "expandr4", "decimate", "decr4", "stretchacres"]
---

# changeAspect

## Description
`changeAspect` independently rescales the horizontal (`X`) and vertical (`Y`) pixel dimensions of an 8-bit (`data_type = 1`) or 32-bit floating-point (`data_type = 3`, `.r4`) `OMG1` (`JHC_header`) array. It accepts either multiplicative scale factors (`-xfactor`, `-yfactor`) or explicit target pixel dimensions (`-xdim`, `-ydim`), updating the header's grid spacing (`dx`, `dy`) to preserve geographic scale.

## CLI Options & Usage
```bash
changeAspect -in <infile> -out <outfile> \
  [-xfactor <fx>] [-yfactor <fy>] [-xdim <nx>] [-ydim <ny>]
```
* **`-in <infile>`**: Input 8-bit or 32-bit float `OMG1` raster file.
* **`-out <outfile>`**: Output rescaled `OMG1` raster file.
* **`-xfactor <fx>` / `-yfactor <fy>`**: Floating-point multiplier for column count (`xmax`) and row count (`ymax`) (default: `1.0`).
* **`-xdim <nx>` / `-ydim <ny>`**: Explicit target column count and/or row count (overrides `-xfactor`/`-yfactor` by setting `xfactor = xdim / xmax`, `yfactor = ydim / ymax`).

## Algorithm
1. Reads the `JHC_header` from `<infile>`, computes new dimensions `new_x = xmax * xfactor` and `new_y = ymax * yfactor`, and scales pixel sizes `dx /= xfactor`, `dy /= yfactor`.
2. **For 8-bit images (`data_type == 1`)**: Performs inverse nearest-neighbor coordinate mapping (`old_i = i / xfactor`, `old_j = j / yfactor`) across the `new_x × new_y` grid.
3. **For 32-bit float grids (`data_type == 3`)**: Performs a two-stage separable resampling (`intermediate[xmax * new_y]` along Y, then `final[new_x * new_y]` along X). When downsampling (`factor < 1.0`), averages all valid (`!= 99999.0`) source cells falling within each output cell; when upsampling (`factor >= 1.0`), uses nearest-neighbor replication.
