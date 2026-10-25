---
layout: default
title: rotateimage
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 45
tool_name: rotateimage
source_path: code/image/rotateimage.c
category: Image & Raster Processing
input_formats:
- OMG1 8-bit array (JHC_header)
output_formats:
- Rotated or horizontally flipped OMG1 8-bit array
related_tools:
- distortImage
- changeAspect
- subimage
- 8bit2acres
---

# rotateimage

## Description
`rotateimage` rotates an 8-bit `OMG1` (`JHC_header`) image by 90° clockwise (default, swapping `xmax`/`ymax` and `dx`/`dy`), flips it horizontally left-to-right (`-hflip`), or rotates it by an arbitrary angle (`-rotate_angle <deg>`) about a specified pixel center (`-cen <x> <y>`) while keeping the original grid dimensions.

## CLI Options & Usage

```bash
rotateimage -in <infile> -out <outfile> \
  [-hflip | -rotate_angle <deg> [-cen <cx> <cy>]]
```
* **`-in <infile>`**: Input 8-bit `OMG1` (`JHC_header`) raster file.
* **`-out <outfile>`**: Output rotated/flipped 8-bit `OMG1` raster file.
* **`-hflip`**: Mirrors each scanline horizontally (`out[i, j] = in[xmax - 1 - i, j]`) without rotating.
* **`-rotate_angle <deg>`**: Rotates the image by `<deg>` degrees around `(cx, cy)`, filling out-of-bounds corners with `255` and preserving original `xmax × ymax` dimensions.
* **`-cen <cx> <cy>`**: Rotation pivot pixel coordinates for `-rotate_angle` (defaults to image center `(xmax/2, ymax/2)`).

## Algorithm
* **Default (90° Clockwise)**: Sets `out_head.xmax = in_head.ymax`, `out_head.ymax = in_head.xmax`, swaps `dx` and `dy`, and maps `out[in_ymax - 1 - j, i] = in[i, j]`.
* **Arbitrary Angle (`-rotate_angle`)**: For each output pixel `(i, j)`, computes polar offset `(range, dir)` from `(cx, cy)`, rotates by `dir -= rotate_angle`, and samples `in[cx + range*sin(dir), cy + range*cos(dir)]`.
