---
layout: default
title: pastemos
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 34
tool_name: pastemos
source_path: code/image/pastemos.c
category: Mosaicking & Patching
input_formats:
- OMG1 8-bit rasters
- 2D FFT magnitude/azimuth grids (.mag.r4, .azi.r4)
- Temperature/Salinity grids
output_formats:
- Composite OMG1 8-bit raster or 24-bit Netpbm .ppm image
related_tools:
- paster4
- patchArea
- fft2dimage
- stretchacres
---

# pastemos

## Description
`pastemos` interactively composites multiple `OMG1` (`JHC_header`) sub-images onto a user-dimensioned 8-bit `OMG1` canvas or 24-bit RGB `.ppm` image (`-ppm`). In addition to standard greyscale pasting and grid-stepped tiling (`-xstep`, `-ystep`), `pastemos` includes specialized 24-bit RGB color encoders for plotting 2D FFT sandwave Magnitude + Azimuth pairs (from [`fft2dimage`](fft2dimage.html), complete with an embedded color-wheel compass rose) and ocean Temperature + Salinity cross-sections.

## CLI Options & Usage

```bash
pastemos -out <outfile> -rows <nrows> -cols <ncols> [-ppm] \
  [-back <val>] [-backrgb <r> <g> <b>] [-ignore <val>] \
  [-xstep <dx> -ystep <dy> [-xstart <x0> -ystart <y0>]]
```
* **`-out <outfile>`**: Output `OMG1` 8-bit raster or `P6` `.ppm` file.
* **`-rows <nrows> -cols <ncols>`**: Canvas height and width in pixels.
* **`-ppm`**: Outputs a 24-bit RGB Netpbm `.ppm` image and unlocks multi-variable color encoding modes (`1`: Greyscale, `2`: Mag/Azi, `3`: Mag/Azi Compass Rose, `4`: Temp/Sal).
* **`-back <val>` / `-backrgb <r> <g> <b>`**: Canvas background greyscale value (default `0`) or RGB triplet.
* **`-ignore <val>`**: Transparent source pixel value skipped when pasting (default `-1` = overwrite all).
* **`-xstep <dx> -ystep <dy>`**: Automatically advances the paste origin across a regular tiling grid instead of prompting for `(left_x, top_y)` on each file.

## Interactive Modes
When `-ppm` is active, `pastemos` prompts for the rendering mode on each paste operation:
* **Mode 1**: Standard 8-bit greyscale image pasted into `R = G = B`.
* **Mode 2 (`azi_to_rgb`)**: Reads a magnitude image and a `0°–180°` azimuth image, mapping orientation hue around a 3-phase cosine color wheel modulated by magnitude brightness.
* **Mode 3**: Renders a circular `Mag/Azi` reference compass rose at `(left_x, top_y)`.
* **Mode 4 (`TS_to_rgb`)**: Encodes Temperature (`Red/Green`) and Salinity (`Blue`) into RGB space.
