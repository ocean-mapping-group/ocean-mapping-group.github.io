---
layout: default
title: jb_mask_make
parent: Image Tools
nav_order: 26
tool_name: jb_mask_make
source_path: code/image/jb_mask_make.c
category: Masking & Stenciling
input_formats: ["ASCII polygon vertex list (x, y)"]
output_formats: ["OMG1 8-bit filled polygon mask"]
related_tools: ["mask_make", "mask_ray", "stencil", "stencilIPV"]
---

# jb_mask_make

## Description
`jb_mask_make` (written by A. Y. and J. E. H. C., May 1990, with JamesB parity-fill enhancements) generates an 8-bit `OMG1` (`JHC_header`) filled polygon mask from an ASCII file of polygon vertex coordinates. It uses Bresenham-style integer edge stepping combined with scanline interior parity toggling to fill arbitrary closed polygons with a user-specified mask value (`-val`).

## CLI Options & Usage
```bash
jb_mask_make -infile <vertex_file> -outfile <mask.8bit> [-val <0..255>]
```
* **`-infile <vertex_file>`**: ASCII file listing `(x, y)` vertex coordinates around a closed polygon (currently defaults to `512 × 512` grid dimensions).
* **`-outfile <mask.8bit>`**: Output 8-bit `OMG1` (`JHC_header`) mask file (`0` outside, `val` inside).
* **`-val <0..255>`**: Digital Number assigned to pixels on and inside the polygon boundary (default: `128`).

## Algorithm
1. **Boundary Rasterization**: Reads consecutive `(x, y)` vertex pairs from `<vertex_file>`, drawing each polygon edge onto the `xlen × ylen` canvas while distinguishing horizontal segments (`value = 255`) from non-horizontal crossing edges (`value = 254`) and accounting for local vertex extrema (peaks vs. monotonic crossings).
2. **Scanline Parity Fill**: Scans each row `j = 0 .. ylen-1` from left to right, toggling an `in` boolean state (`1` = inside, `0` = outside) whenever a `254` edge crossing is encountered and assigning `val` to all interior and boundary pixels.
3. Writes the resulting `OMG1` header and 8-bit mask array for use with [`stencil`](stencil.md).
