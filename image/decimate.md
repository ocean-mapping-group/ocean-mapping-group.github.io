---
layout: default
title: decimate
parent: Image Tools
nav_order: 15
tool_name: decimate
source_path: code/image/decimate.c
category: Image & Raster Processing
input_formats: ["OMG1 8-bit array (JHC_header)"]
output_formats: ["Downsampled OMG1 8-bit array"]
related_tools: ["decr4", "expand", "changeAspect", "shoalBias"]
---

# decimate

## Description
`decimate` downsamples an 8-bit `OMG1` (`JHC_header`) raster by an integer factor `-count <n>` along both axes (or along a single axis via `-justx` or `-justy`). It supports either valid-pixel mean averaging (default) or minimum-value selection (`-lowest`), while excluding a user-specified background/no-data value (`-ignore`, default `255`).

## CLI Options & Usage
```bash
decimate -in <infile> -out <outfile> -count <n> \
  [-justx | -justy] [-ignore <val>] [-lowest]
```
* **`-in <infile>`**: Input 8-bit `OMG1` raster file.
* **`-out <outfile>`**: Output downsampled 8-bit `OMG1` raster file.
* **`-count <n>`**: Integer decimation factor (must be `>= 1`).
* **`-justx`**: Decimates horizontally (`X`) only, preserving `ymax` and `dy`.
* **`-justy`**: Decimates vertically (`Y`) only, preserving `xmax` and `dx`.
* **`-ignore <val>`**: Background pixel value ignored during averaging/minimum calculation (default: `255`).
* **`-lowest`**: Retains the lowest valid Digital Number within each `xcount × ycount` block instead of the arithmetic mean.

## Algorithm
1. Divides `xmax` by `xcount` and `ymax` by `ycount`, and multiplies `dx *= xcount` and `dy *= ycount` in the output `JHC_header`.
2. For each output pixel `(i, j)`, inspects the corresponding `xcount × ycount` block in the source image:
   * Accumulates all pixels `!= ignore` (rounding the mean `(sum + good/2) / good`, or tracking the minimum if `-lowest` is set).
   * Outputs `ignore` (`255`) if no valid pixels exist in the block.
