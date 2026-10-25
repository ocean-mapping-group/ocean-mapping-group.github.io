---
layout: default
title: mask_ray
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 33
tool_name: mask_ray
source_path: code/image/mask_ray.c
category: Masking & Stenciling
input_formats:
- ASCII polygon vertex list (x, y)
output_formats:
- ACRES 8-bit filled polygon mask
related_tools:
- mask_make
- jb_mask_make
- stencil
---

# mask_ray

## Description
`mask_ray` (written by A. Y. / JCU, May 1990) creates an ACRES-format 8-bit polygon mask from an ASCII vertex file using a 4-directional ray-casting parity test (casting rays left, right, up, and down from every candidate pixel to count boundary intersections).

## CLI Options & Usage

```bash
mask_ray -infile <vertex_file> -outfile <acres_mask> -xlen <cols> -ylen <rows>
```
* **`-infile <vertex_file>`**: ASCII file of `(x, y)` polygon vertices.
* **`-outfile <acres_mask>`**: Output ACRES-format 8-bit mask file (with 90-byte header; `255` inside, `0` outside).
* **`-xlen <cols> -ylen <rows>`**: Image width and height in pixels.

## Algorithm
1. Rasterizes all polygon edges onto the `xlen × ylen` array (`value = 255`) while tracking the polygon's bounding box `[xmin..xmax, ymin..ymax]`.
2. For every non-boundary pixel `(i, j)` inside the bounding box, casts four orthogonal rays (`left`, `right`, `up`, `down`) to the bounding box edges, counting transitions across the `255` boundary. If the crossing count is odd (`count % 2 == 1`), marks the pixel as interior (`255`).
3. Writes a 90-byte ACRES header (`header[3] = xlen`, `header[4] = ylen`) followed by the mask array.
