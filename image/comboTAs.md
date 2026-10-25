---
layout: default
title: comboTAs
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 11
tool_name: comboTAs
source_path: code/image/comboTAs.c
category: Multibeam Water Column & Acoustic Modeling
input_formats:
- OMG1 .time_angle water-column files
output_formats:
- Time-stepped .vert_prof vertical profile (OMG1)
related_tools:
- comboVPs
- patchTA
- TAtoXZ
- makeWC
- stretchacres
---

# comboTAs

## Description
`comboTAs` merges a sequence of single-beam or sector multibeam water-column time-series files (`*.time_angle`) into a single continuous, uniform time-stepped vertical profile (`<comboprefix>.vert_prof`) in `OMG1` (`JHC_header`) format, optionally overlaying red/black navigation fix tick marks (`-nav_fix`) along the bottom of the echogram.

## CLI Options & Usage

```bash
comboTAs [-v] [-time_step <sec>] [-nav_fix <sec>] -out <comboprefix> <file1.time_angle> [<file2.time_angle> ...]
```
* **`-out <comboprefix>`**: Output `.vert_prof` filename.
* **`-time_step <sec>`**: Uniform horizontal time bin width in seconds per output column (default: `1.0 s`).
* **`-nav_fix <sec>`**: Interval in seconds for drawing time/navigation tick marks (`10` or `20` pixels tall) along the bottom edge of the profile (`0.0` = disabled).
* **`-v`**: Verbose output printing header time windows (`start_time`, `end_time` stored in `tlon`/`blon`) for each input `.time_angle` file.

## Algorithm
1. Scans all input `.time_angle` headers (`tlon = start_time`, `blon = end_time` in seconds since 1970, `ymax` = vertical range samples) to find the overall survey time span `[min_time, max_time]` and maximum sample depth `max_y`.
2. Allocates an output array of `tot_x = (max_time - min_time) / time_step` columns by `max_y` rows, initialized to `255` (no data).
3. Maps each ping column `i` from every input `.time_angle` file into its corresponding time bin `out_x = (time - min_time) / time_step` and writes the combined `OMG1` `.vert_prof` file.
