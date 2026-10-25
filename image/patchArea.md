---
layout: default
title: patchArea
parent: Image Tools
nav_order: 36
tool_name: patchArea
source_path: code/image/patchArea.c
category: Mosaicking & Patching
input_formats: ["Georeferenced OMG1 8-bit or 32-bit float (.r4, .r4.gz) mapsheets"]
output_formats: ["Merged/reprojected OMG1 8-bit or 32-bit float (.r4) mapsheet"]
related_tools: ["patchArea_MercOnly", "paster4", "pastemos", "subimage"]
---

# patchArea

## Description
`patchArea` is the Ocean Mapping Group's primary multi-projection raster merging and reprojection engine for georeferenced 8-bit (`data_type = 1`) and 32-bit floating-point (`data_type = 3`, `.r4`, including gzip-compressed `.gz` files) `OMG1` mapsheets. Given an existing or newly defined target mapsheet (`-out`), it reprojects and patches any number of input mapsheets (`-import` or interactive) across Geographic, Mercator, UTM, Transverse Mercator, Lambert Conformal Conic, Stereographic (`UNB`), Polar Stereographic, and Rectangular projections, automatically downsampling higher-resolution source grids (`downgrade_image`) to prevent spatial aliasing.

## CLI Options & Usage
```bash
patchArea -out <target_map> [-prime <template_map>] \
  [-import <in1> <in2> ...] [-back <val>] [-ignore <val>] \
  [-less_than <max>] [-greater_than <min>] [-no_interp] [-keep_edges] [-nudge] \
  [-float_offset <dz>] [-float_scale <scale>] [-grey_offset <dn>] \
  [-llshift <dlat> <dlon>] [-dont_check_bounds] [-custom_Salish <layer>]
```
* **`-out <target_map>`**: Target `OMG1` mapsheet to create or update.
* **`-prime <template_map>`**: Initializes a new `<target_map>` using the header geometry of `<template_map>` filled with background (`255` or `99999.0`).
* **`-import <files...>`**: Batch-imports all listed mapsheets into `<target_map>` without interactive prompts.
* **`-no_interp`**: Uses nearest-neighbor sampling instead of 4-neighbor distance-weighted bilinear interpolation.
* **`-keep_edges`**: Allows boundary interpolation even when fewer than 4 surrounding neighbors are valid.
* **`-less_than <max> -greater_than <min>`**: Clips source values outside `(min, max)` before patching.
* **`-float_offset <dz> -float_scale <scale>`**: Applies `val = (val + dz) * scale` to imported `.r4` grids (e.g., vertical datum shifts or feet/fathoms-to-meters conversion).
* **`-llshift <dlat> <dlon>`**: Applies a geographic datum shift to imported mapsheets.
* **`-custom_Salish <layer>`**: Extracts a specific depth layer from multi-layer NetCDF-derived `.r4` grids.

## Algorithm
For each imported mapsheet, `patchArea` compares its ground sample distance `(dx, dy)` against the target mapsheet. If the source grid is finer by a factor $\ge 2$, `downgrade_image()` boxcar-averages the source grid by `floor(target_dx / source_dx)` along X and Y. It then steps through every cell `(i, j)` in the target mapsheet, transforms its coordinates to `(lat, lon)` and into the source mapsheet's projection, and performs bilinear or nearest-neighbor resampling.
