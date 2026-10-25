---
layout: default
title: patchTA
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 38
tool_name: patchTA
source_path: code/image/patchTA.c
category: Multibeam Water Column & Acoustic Modeling
input_formats:
- OMG1 .wcim water-column Time-Angle files
output_formats:
- Composite time-windowed OMG1 water-column array
related_tools:
- comboTAs
- comboVPs
- TAtoXZ
- stackPIEs
- makeWC
---

# patchTA

## Description
`patchTA` composites and resamples a sequence of multibeam water-column `.wcim` Time-Angle files across a user-specified time window (`-time_start` to `-time_end`, or `-time_start_1970` + `-window_sec`) into a single uniform-time-stepped 8-bit `OMG1` (`JHC_header`) echogram.

## CLI Options & Usage

```bash
patchTA -out <outfile> -import <file1.wcim> [<file2.wcim> ...] \
  [-prime <template> | -time_start <yy/ddd/hh:mm:ss> -time_end <yy/ddd/hh:mm:ss> | \
   -time_start_1970 <sec> -window_sec <sec>] \
  [-norecs <cols>] [-back <val>] [-ignore <val>]
```
* **`-out <outfile>`**: Output composite 8-bit `OMG1` water-column file.
* **`-import <*.wcim>`**: List of input `.wcim` files (whose `JHC_header` stores `start_time` in `tlon` and `end_time` in `blon` as seconds since 1970).
* **`-time_start <str> -time_end <str>`**: Time window formatted as `yyyy/ddd/hh:mm:ss` (decoded via `decode_jultime()`).
* **`-time_start_1970 <sec> -window_sec <sec>`**: Time window specified as epoch seconds and duration in seconds (default duration: `3600 s`).
* **`-norecs <cols>`**: Horizontal column dimension (`xmax`) of a newly created output file (default: `3600`).
* **`-prime <template>`**: Uses an existing `OMG1` file's dimensions and time bounds to initialize `<outfile>`.
* **`-back <val>` / `-ignore <val>`**: Background fill (`255`) and ignored pixel value (`255`).

## Algorithm
1. Initializes or loads `<outfile>` with `tlon = start_time`, `blon = end_time`, and time step `dx = (end_time - start_time) / xmax`.
2. For each imported `.wcim` file whose `[tlon, blon]` overlaps the target time window:
   * If the `.wcim` file has higher temporal resolution than `<outfile>` by a factor $\ge 2$, downsamples it along the time axis via `downgrade_image()`.
   * Maps each target column's timestamp `out_time` into the `.wcim` column index `in_x` and copies valid vertical samples into `<outfile>`.
