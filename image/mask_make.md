---
layout: default
title: mask_make
parent: Image Tools
nav_order: 32
tool_name: mask_make
source_path: code/image/mask_make.c
category: Masking & Stenciling
input_formats: ["ASCII polygon vertex list (x, y)"]
output_formats: ["OMG1 8-bit filled polygon mask"]
related_tools: ["jb_mask_make", "mask_ray", "stencil", "stencilIPV"]
---

# mask_make

## Description
`mask_make` (written by A. Y. and J. E. H. C., May 1990) rasterizes one or more closed polygons from an ASCII vertex file into an 8-bit `OMG1` (`JHC_header`) mask image of arbitrary dimensions (`-xlen`, `-ylen`), filling polygon interiors with a specified Digital Number (`-val`).

## CLI Options & Usage
```bash
mask_make -infile <vertex_file> -outfile <mask.8bit> \
  [-xlen <cols>] [-ylen <rows>] [-val <0..255>] [-nmap <n>]
```
* **`-infile <vertex_file>`**: Input ASCII file containing `(x, y)` vertex coordinates (`999999 999999` separates multiple polygons when `-nmap > 1`).
* **`-outfile <mask.8bit>`**: Output 8-bit `OMG1` (`JHC_header`) mask file.
* **`-xlen <cols> -ylen <rows>`**: Mask width and height in pixels (default: `512 × 512`).
* **`-val <0..255>`**: Fill value assigned to polygon interior and boundary pixels (default: `128`).
* **`-nmap <n>`**: Number of distinct polygons to read from `<vertex_file>` (default: `1`).

## Algorithm
1. Allocates an `xlen × ylen` byte buffer initialized to `0`.
2. For each of the `nmap` polygons, connects consecutive vertices `(x1, y1) -> (x2, y2)` using integer line stepping (`255` for horizontal segments, `254` for non-horizontal edges, with double-crossing adjustment at local vertical extrema).
3. Performs a scanline parity fill across each row `j = 0 .. ylen-1`, toggling inside/outside state at `254` edge markers and writing `val` to all interior pixels before saving the `OMG1` file.
