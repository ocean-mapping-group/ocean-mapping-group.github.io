---
layout: default
title: decr4
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 16
tool_name: decr4
source_path: code/image/decr4.c
category: Image & Raster Processing
input_formats:
- OMG1 32-bit float grid (.r4)
output_formats:
- Downsampled OMG1 32-bit float grid (.r4)
related_tools:
- decimate
- expandr4
- shoalBias
- changeAspect
---

# decr4

## Description
`decr4` downsamples a 32-bit floating-point (`data_type = 3`, `.r4`) `OMG1` (`JHC_header`) bathymetric or backscatter grid by integer decimation factors (`-count`, or asymmetric `-xcount` / `-ycount`). It supports either valid-cell arithmetic averaging (default) or shoal-biased maximum selection (`-shoal_bias`), plus optional vertical datum offsetting (`-add`).

## CLI Options & Usage

```bash
decr4 -in <infile.r4> -out <outfile.r4> \
  [-count <n> | -xcount <nx> -ycount <ny>] \
  [-ignore <val>] [-shoal_bias] [-add <offset>]
```
* **`-in <infile.r4>`**: Input 32-bit float `OMG1` `.r4` grid.
* **`-out <outfile.r4>`**: Output decimated `.r4` grid.
* **`-count <n>`**: Symmetric integer decimation factor applied to both X and Y (`xcount = ycount = n`).
* **`-xcount <nx> -ycount <ny>`**: Independent integer decimation factors for X (columns) and Y (rows).
* **`-ignore <val>`**: No-data flag value excluded from calculations (default: `99999.0`; any cell `>= 9999.0` is also ignored).
* **`-shoal_bias`**: Selects the maximum (`shoalest`, in negative-down depth convention) valid value in each `xcount × ycount` block instead of the mean.
* **`-add <offset>`**: Constant floating-point offset added to every valid output cell (default: `0.0`).

## Algorithm
Updates `xmax /= xcount`, `ymax /= ycount`, `dx *= xcount`, and `dy *= ycount` in the `JHC_header`, then loops over each `xcount × ycount` window of source floats, computing either `sum / good + added_bit` or the shoalest value `lowest + added_bit` (writing `99999.0` when `good == 0`).
