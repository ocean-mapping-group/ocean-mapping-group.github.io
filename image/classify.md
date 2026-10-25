---
layout: default
title: classify
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 10
tool_name: classify
source_path: code/image/classify.c
category: Spectral & Backscatter Analysis
input_formats:
- Three angular-sector OMG1 mosaics (<prefix>.nad, <prefix>.mea, <prefix>.tai)
output_formats:
- Intensity map (<prefix>.int)
- Slope map (<prefix>.slp)
- Classification map (<prefix>.cls)
- DumpLut
- DumpHist
related_tools:
- MSpecBS_Xplot
- build_back_mos
- back_char
- stretchacres
---

# classify

## Description
`classify` performs supervised/unsupervised acoustic seafloor classification from three co-registered angular-sector backscatter mosaics created by splitting a swath into near-nadir (`<prefix>.nad`), mid-range mean (`<prefix>.mea`), and outer-swath tail (`<prefix>.tai`) grazing-angle sectors. From these three inputs, it derives a weighted mean backscatter intensity image (`<prefix>.int`), an angular response slope image (`<prefix>.slp`), a 256×256 intensity-vs-slope 2D histogram (`DumpHist`), a 2D class lookup table (`DumpLut`), and a classified seafloor map (`<prefix>.cls`).

## CLI Options & Usage

```bash
classify -in <Prefix> [-show]
```
* **`-in <Prefix>`**: Input/output filename prefix. Reads `<Prefix>.nad`, `<Prefix>.mea`, and `<Prefix>.tai` (all 8-bit `OMG1` arrays of identical dimensions) and outputs `<Prefix>.int`, `<Prefix>.slp`, `<Prefix>.cls`, `DumpLut`, and `DumpHist`.
* **`-show`**: Prints progress diagnostics while building the lookup table and histograms.

## Algorithm
1. **Intensity & Angular Slope Calculation**:
   For every pixel where all three sector mosaics have valid data (`nad != 255`, `mea != 255`, `tai != 255`):
   * Computes weighted intensity: `intensity = (nad + 3 * mea + 2 * tai) / 6`.
   * Computes angular roll-off slope between near-nadir and outer swath: `slope = 128 + (nad - tai) / 2` (clamped `0..254`).
2. **2D Feature Space Lookup (`DumpLut` & `DumpHist`)**:
   * Constructs a 256×256 Intensity-vs-Slope lookup table (`lut[int][slp]`) partitioned into a 4×4 grid of 16 acoustic classes (centered around mean `128` and standard deviation `32`, mapping each class to a 3-3-2 RGB color byte) and accumulates the 2D feature-space density histogram (`DumpHist`, log-stretched to `0..254`).
3. **Spatial Classification**:
   * Maps each pixel's `(int, slp)` pair through `lut[int][slp]` to produce `<Prefix>.cls`.
