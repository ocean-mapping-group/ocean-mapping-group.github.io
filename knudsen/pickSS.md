---
layout: default
title: pickSS
parent: Knudsen Chirp Sub-Bottom (knudsen)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 11
tool_name: pickSS
source_path: knudsen/pickSS.c
category: bathymetry_processing
input_formats:
- OMG_HDCS
- OMG_SS_DATA
output_formats:
- ASCII_PICKS
- OMG_HDCS
related_tools:
- make_knudsen_ss
- makeSeisPlot
- knud2glo
---

# pickSS

## Overview

`pickSS` performs automated seabed first-break picking on 8-bit sub-bottom / echosounder traces stored in OMG HDCS `.merged` and `.merged.ss_data` files. It can pick on the high-frequency (`-hfpick`), low-frequency (`-lfpick`), or blended average of both channels (`-bothpick`), optionally smooth the resulting depth picks with a running median (`-median`) or mean (`-average`) filter, write the picks to `<prefix>.picks`, and overwrite the bottom-track depth in the `.merged` file in-place (`-replace`, `-replace_both`).

## Usage

```
pickSS (-v) (-log) (-first 100 -last 300) (-hfpick | -lfpick | -bothpick) \
       (-replace | -replace_both) (-median) (-average) \
       (-minpick 0.5) (-maxpick 20.0) (-pick_buffer 1.0) \
       (-pickthresh 50 | -autothresh) (-thresh_per_m 1) \
       (-pickwin 20 -ofwhich 15 -extrapix 25) -in infilename.merged
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<infilename.merged>` | *required* | Input OMG HDCS `.merged` file (reads companion `<infilename.merged>.ss_data` and writes `<prefix>.picks`). |
| `-lfpick` / `-hfpick` / `-bothpick` | none | `-lfpick` (`1`) | Pick on the LF channel (`1`), HF channel (`0`), or the 50/50 average of both channels (`2`). |
| `-replace` | none | `0` | Replace the observed depth and `centre_no` of the picked channel in `<infilename.merged>` in-place (saving original picks to `<prefix>.orig_picks`). |
| `-replace_both` | none | `0` | Replace the observed depth and `centre_no` of both HF and LF channels in `<infilename.merged>`. |
| `-minpick` / `-maxpick` | `<meters>` | `2.0` / `100.0` | Minimum and maximum depth gate in meters for searching the seabed arrival. |
| `-pick_buffer` | `<meters>` | none (`30.0`) | Search within `+-<meters>` of the existing bottom pick (`beams[chanpick].centre_no`) instead of `[minpick, maxpick]`. |
| `-pickthresh` | `<0..255>` | `50` | 8-bit amplitude threshold required to trigger a bottom pick. |
| `-autothresh` | none | `0` | Enable automatic threshold estimation flag. |
| `-thresh_per_m` | `<val>` | `0.0` | Linear threshold increase per meter of depth. |
| `-pickwin` / `-ofwhich` | `<samples>` | `20` / `15` | Confirmation window length (`pickwin`) and minimum number of samples exceeding threshold (`ofwhich`). |
| `-extrapix` | `<cm>` | `0` | Extra offset in centimeters added to the picked depth. |
| `-median` | none | `0` | Apply a running median filter (`jmedian`) to the picked depths before output/replacement. |
| `-average` | none | `0` | Apply a running mean filter (`javerage`) to the picked depths before output/replacement. |
| `-log` | none | `0` | Apply logarithmic lookup table enhancement (`loglut`) to 8-bit trace samples before picking. |
| `-first` / `-last` | `<ping>` | all | First and last ping indices to process. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Trace Window & Search Gate Calculation**: For each ping `i`, reads `OMG_HDCS_profile_header` and `OMG_HDCS_beam` from `.merged` and loads the corresponding 8-bit trace (`beams[chanpick].no_samples` bytes at `beams[chanpick].offset`) from `.merged.ss_data`. Converts the trace start delay (`trace_offset = range - centre_no`) and `[minpick, maxpick]` (or `+-pick_buffer`) into two-way travel time (`begTWTT`, `endTWTT`, `minTWTT`, `maxTWTT`).
2. **Sliding-Window Threshold Detector**: Scans samples within `[minTWTT, maxTWTT]` to find the first sample where at least `ofwhich` out of `pickwin` consecutive samples exceed `pickthresh + depth * thresh_per_m`.
3. **Filtering & In-Place Update**: Optionally smooths picks across pings using `jmedian()` or `javerage()`, writes `<prefix>.picks` (used by `makeSeisPlot -use_repick`), and if `-replace` or `-replace_both` is set, updates `beams[side].observedDepth` and `beams[side].centre_no` in `<infilename.merged>`.

## Practical Examples

### Re-pick seabed depths on the HF channel with median filtering and update `.merged` in-place

```bash
pickSS -hfpick -minpick 5.0 -maxpick 80.0 -pickthresh 65 \
       -pickwin 15 -ofwhich 12 -median -replace -in knud_line01.merged
```
