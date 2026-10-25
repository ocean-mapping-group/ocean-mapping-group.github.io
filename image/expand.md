---
layout: default
title: expand
parent: Image Tools
nav_order: 20
tool_name: expand
source_path: code/image/expand.c
category: Image & Raster Processing
input_formats: ["OMG1 8-bit array (JHC_header)"]
output_formats: ["Upsampled (or downsampled) OMG1 8-bit array"]
related_tools: ["expandr4", "decimate", "changeAspect", "stretchacres"]
---

# expand

## Description
`expand` upsamples an 8-bit `OMG1` (`JHC_header`) raster by an integer factor (`-factor > 1`), or decimates it when given a negative factor (`-factor < -1`). When upsampling, it supports either pixel replication (default) or two-pass separable bilinear interpolation (`-interp`), optionally preserving masked background pixels (`-mask`, default `255`).

## CLI Options & Usage
```bash
expand -in <infile> -out <outfile> -factor <n> [-interp] [-mask]
```
* **`-in <infile>`**: Input 8-bit `OMG1` raster file.
* **`-out <outfile>`**: Output resampled 8-bit `OMG1` raster file.
* **`-factor <n>`**: Integer expansion factor (`> 1` multiplies `xmax` and `ymax` by `n` and divides `dx` and `dy` by `n`; `< -1` decimates dimensions by `|n|`).
* **`-interp`**: Linearly interpolates intermediate pixels first across rows and then down columns instead of replicating square pixel blocks.
* **`-mask`**: Excludes background pixels (`255`) from bilinear interpolation so edges do not bleed into no-data regions.

## Algorithm
1. Updates `JHC_header` dimensions (`xmax *= factor`, `ymax *= factor`, `dx /= factor`, `dy /= factor`).
2. **Replication mode (default)**: Copies each source pixel `(i, j)` into an `n × n` block `[i*n .. i*n+n-1, j*n .. j*n+n-1]`.
3. **Bilinear mode (`-interp`)**: Places source pixels at `i*n, j*n`, linearly interpolates intermediate columns along each key row `j*n`, and then linearly interpolates intermediate rows down every column `0 .. new_xmax-1` (honoring `-mask` if enabled).
