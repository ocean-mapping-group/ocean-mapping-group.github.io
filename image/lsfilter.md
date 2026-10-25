---
layout: default
title: lsfilter
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 30
tool_name: lsfilter
source_path: code/image/lsfilter.c
category: Satellite, SAR & Format Conversion
input_formats:
- ACRES 8-bit Landsat image
output_formats:
- Low-pass (<in>.low) or high-pass (<in>.high) ACRES 8-bit image
related_tools:
- add_hilo
- limit_change
- removecloud
- replacecloud
- destripe
---

# lsfilter

## Description
`lsfilter` (written by A. Y. / JCU, May 1990) implements 2D spatial boxcar low-pass (`-low`) and high-pass (`-high`) filtering on ACRES-format 8-bit Landsat imagery following the Chavez (1986) destriping methodology. By combining a narrow along-track low-pass kernel with an wide across-track high-pass kernel via [`add_hilo`](add_hilo.html), periodic detector striping is suppressed while preserving scene structure.

## CLI Options & Usage

```bash
lsfilter -in <acres_file> [-low | -high] \
  -filtlen <odd_cols> -filtwidth <odd_rows> [-skip <0..255>] [-edge]
```
* **`-in <acres_file>`**: Input ACRES 8-bit image (90-byte header). Outputs `<acres_file>.low` or `<acres_file>.high`.
* **`-low` / `-high`**: Selects low-pass boxcar smoothing (`<in>.low`) or high-pass residual extraction (`128 + pixel - mean` -> `<in>.high`).
* **`-filtlen <odd_cols>`**: Horizontal (across-track) filter length in pixels (must be odd).
* **`-filtwidth <odd_rows>`**: Vertical (along-track) filter height in scanlines (must be odd).
* **`-skip <val>`**: Pixel value to exclude from boxcar window averaging (e.g., `0` for masked clouds/background).
* **`-edge`**: Retains unfiltered original pixels along the image borders where the kernel overhangs the edge (default: sets border pixels to `0`).

## Algorithm
Maintains a sliding ring buffer of `filtwidth` scanlines and updates running horizontal column sums (`rowsum[j]`) to evaluate the `filtlen × filtwidth` boxcar mean in $O(\text{filtwidth})$ operations per pixel, excluding any pixel equal to `skip`.
