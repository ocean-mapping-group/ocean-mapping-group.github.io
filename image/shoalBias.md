---
layout: default
title: shoalBias
parent: Image Tools
nav_order: 46
tool_name: shoalBias
source_path: code/image/shoalBias.c
category: Image & Raster Processing
input_formats: ["Georeferenced OMG1 32-bit float bathymetry DTM (.r4)"]
output_formats: ["Shoal-biased .r4 DTM (<out>)", "Sub-bin coordinate offset grids (<out>.lat, <out>.lon)"]
related_tools: ["decr4", "removeOverplot", "patchArea"]
---

# shoalBias

## Description
`shoalBias` (written by John Hughes Clarke, November 1995) downsamples a high-resolution 32-bit floating-point (`.r4`) `OMG1` bathymetric DTM into larger hydrographic shoal-biased cells of size `-binsize <meters>`. Within each output bin, it retains the shoalest depth while recording the exact sub-bin latitude and longitude offsets of that shoal sounding in companion `<outfile>.lat` and `<outfile>.lon` grids so hydrographic fair sheets can plot the sounding at its true geographic position.

## CLI Options & Usage
```bash
shoalBias -binsize <meters> -in <highres.r4> -out <shoal.r4>
```
* **`-binsize <meters>`**: Target ground cell size in meters (`count = binsize / head.dx`).
* **`-in <highres.r4>`**: Input georeferenced 32-bit float `OMG1` `.r4` bathymetric DTM.
* **`-out <shoal.r4>`**: Output shoal-biased `.r4` DTM (also generates `<shoal.r4>.lat` and `<shoal.r4>.lon`).

## Algorithm
1. Computes the integer decimation factor `count = binsize / dx`, sets `out_xmax = xmax / count`, `out_ymax = ymax / count`, and updates `out_head.dx = out_head.dy = count * dx`.
2. For each `count × count` block of input cells, finds the minimum positive depth value (`lowest < 9999.0`), computes the exact geographic coordinates `(real_lat, real_lon)` of the winning source pixel `(low_i, low_j)` and the bin center `(bin_lat, bin_lon)` via `resolve_pos_from_pixel()`, and stores:
   * `<out>`: `lowest` depth
   * `<out>.lat`: `real_lat - bin_lat`
   * `<out>.lon`: `real_lon - bin_lon`
