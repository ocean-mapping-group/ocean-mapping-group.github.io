---
layout: default
title: removeRadial
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 42
tool_name: removeRadial
source_path: code/image/removeRadial.c
category: Image & Raster Processing
input_formats:
- Raw or OMG1 8-bit image
output_formats:
- Radially compensated 8-bit image
related_tools:
- 8bit2acres
- stretchacres
- removecloud
---

# removeRadial

## Description
`removeRadial` compensates for radial illumination fall-off (vignetting or optical/acoustic hotspot shading) around a user-specified `(x, y)` center in an 8-bit greyscale image using either an additive power-law boost (`-add`) or a multiplicative radial gain function (`-gain`).

## CLI Options & Usage

```bash
removeRadial -in <rawimage> -out <outimage> \
  -rows <n> -cols <n> -centre <cx> <cy> \
  [-add | -gain] -constant <c> -power <p> [-calcheader]
```
* **`-in <rawimage> -out <outimage>`**: Input and output 8-bit image files.
* **`-rows <n> -cols <n>`**: Image height and width in pixels.
* **`-centre <cx> <cy>`**: Pixel coordinates `(cx, cy)` of the radial illumination center.
* **`-add` / `-gain`**: Selects additive compensation (`new = val + (range / constant)^power`) or multiplicative compensation (`new = val * (1.0 + (range / constant)^power)`).
* **`-constant <c>`**: Characteristic radial scale distance in pixels (default: `100.0`).
* **`-power <p>`**: Exponent of the radial correction curve (default: `1.0`).
* **`-calcheader`**: Skips a 1024-byte `OMG1` (`JHC_header`) header at the start of the file before processing pixel bytes.

## Algorithm
For every pixel `(i, j)` in the `cols × rows` raster, computes Euclidean radial distance `range = hypot(i - cx, j - cy)`, applies the chosen radial formula, clamps the result to `[0, 255]`, and writes the compensated byte to `<outimage>`.
