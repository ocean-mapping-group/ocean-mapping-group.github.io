---
layout: default
title: MSpecBS_Xplot
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 3
tool_name: MSpecBS_Xplot
source_path: code/image/MSpecBS_Xplot.c
category: Spectral & Backscatter Analysis
input_formats:
- Co-referenced OMG1 .mos backscatter mosaics
- OMG1 .r4 bathymetry DTM
- OMG1 8-bit class mask
output_formats:
- 2D cross-plot grid (.xplot.r4)
- Cross-plot parameters (.xplot.params)
- Classified raster (classification.map)
related_tools:
- classify
- stretchacres
- r4to8bit
- jview
---

# MSpecBS_Xplot

## Description
`MSpecBS_Xplot` (written by John Hughes Clarke, November 2015) cross-plots co-referenced pixels from two or three multi-frequency acoustic backscatter mosaics (`*.mos`, e.g., 100 kHz vs. 400 kHz R2Sonic or Kongsberg multispectral mosaics), optionally constrained to a specific water-depth range via a co-registered `.r4` bathymetric DTM (`-dep`). It generates a 300×300 floating-point 2D histogram density cross-plot (`<prefix>.xplot.r4`) covering `-40 dB` to `-10 dB` and, when supplied with a painted classification lookup table (`-class_mask`), maps acoustic classes back into geographic space (`classification.map`).

## CLI Options & Usage

```bash
MSpecBS_Xplot -out <prefix> [-av <halfwidth>] [-DN_shift <dB>] \
  [-dep <bathy.r4> -mindepth <m> -maxdepth <m>] \
  [-class_mask <mask.8bit>] <mos1.mos> <mos2.mos> [<mos3.mos>]
```
* **`-out <prefix>`**: Output prefix for `<prefix>.xplot.r4` and `<prefix>.xplot.params`.
* **`-av <n>`**: Spatial smoothing half-width (`2n+1 × 2n+1` boxcar average, requiring at least 75% valid pixels in the window; default `0`).
* **`-DN_shift <dB>`**: dB offset applied when converting 8-bit mosaic Digital Numbers to decibels (`dB = (DN * 0.5) - 127.0 + DN_shift`; default `40.0`).
* **`-dep <bathy.r4>`**: Co-registered 32-bit float bathymetry grid used to filter pixels by water depth.
* **`-mindepth <m> -maxdepth <m>`**: Minimum and maximum water depths included in the cross-plot when `-dep` is active.
* **`-class_mask <mask.8bit>`**: 300×300 8-bit `OMG1` image painted over the cross-plot space (`-40` to `-10 dB`) used to classify every co-registered geographic pixel into `classification.map`.

## Algorithm
1. Verifies that all input `.mos` files (and optional `-dep` `.r4` grid) have identical `xmax` and `ymax` dimensions.
2. Converts valid (`DN < 254`) pixels (or local `(2*av+1)²` neighborhood means) into decibels and maps pairs `(dB_0, dB_1)` into a 300×300 grid (`0.1 dB` bin resolution from `-40` to `-10 dB`).
3. Normalizes the 2D histogram counts (`0..100` scale, setting empty bins to `99999.0`) and writes `<prefix>.xplot.r4`.
4. If `-class_mask` is provided, looks up each pixel's `(bx, by)` cross-plot bin in the mask and writes the assigned class code (`255 - mval`) to `classification.map`.
