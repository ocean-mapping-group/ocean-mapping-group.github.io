---
layout: default
title: makeSeisPlot
parent: Knudsen Chirp Sub-Bottom (knudsen)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 7
tool_name: makeSeisPlot
source_path: knudsen/makeSeisPlot.c
category: seismic_plotting
input_formats:
- OMG_HDCS
- OMG_SS_DATA
- JHC_MAPSHEET
output_formats:
- JHC_ARRAY
- ASCII_PERSPECT
- JCU_NAV
related_tools:
- collapseSeisStack
- makeSeisPlot_Op
- knud2glo
- k16to8
- pickSS
- plotBorder
---

# makeSeisPlot

## Overview

`makeSeisPlot` generates depth-phased, heave-compensated, along-track stacked, or 3D perspective map-projected seismic/sub-bottom scroll images (`JHC_header` 8-bit rasters) from Knudsen, Kongsberg SBP120/EA600/EK80, or SEG-Y sub-bottom profiler data stored in OMG HDCS `.merged` and `.merged.ss_data` files. When given a `.map` sheet (`-map`), it projects each vertical sub-bottom trace into the map's along-sheet or across-sheet coordinate frame and outputs a `.perspect` depth-order file for 3D fence-diagram compositing with [`collapseSeisPlot`](collapseSeisStack).

## Usage

```
makeSeisPlot (-v) (-log) (-heave_already_applied) (-flip_heave) (-apply_diffheave) \
             (-RP_to_sonar X Y Z -test) (-first 100 -last 300) \
             (-time_start YYYY JJJ HH MM SS -time_end YYYY JJJ HH MM SS) \
             (-time_start_file XXX.merged -time_end_file YYY.merged) (-time_map 300) \
             (-above | -below | -pre_m 2.0 -above_m 10 -below_m 50) (-other_bpick) \
             (-stack 3 (-least_stack | -most_stack)) (-orthomap | -alongmap) (-lr_flip | -no_flip) \
             (-antialias) (-velocity 1480 -draft 7.0 -get_AUV_depth) (-nosam 500) \
             (-allow_non1600) (-nozerotrace) (-use_repick) \
             (-map whatever.map) (-pixel 1.0) (-reducedY 4000 4500) (-fill_map_gap -fix_zero_depth) \
             (-mindepth 20 -maxdepth 60 (-Zpixel 0.2) | -depth_range 100 | -m_less_than_maxdepth 10) \
             (-azirange 200 300) (-speedrange 0.5 10) (-m_per_m 10.0) (-contour 100) \
             (-hf | -lf) (-dump_16bit_ascii) -out outfilename -in infilename(s)
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-out` | `<outfilename>` | *required* | Output `JHC_header` 8-bit seismic scroll image file (plus `<out>.perspect` when `-map` is used). |
| `-in` | `<file1> [file2 ...]` | *required* | One or more input OMG HDCS `.merged` files (with companion `.merged.ss_data`). |
| `-hf` / `-lf` | none | `-lf` (`1`) | Select the high-frequency (`beam[0]`, `-hf`/`-HF`) or low-frequency (`beam[1]`, `-lf`/`-LF`) channel. |
| `-mindepth` / `-maxdepth` | `<meters>` | auto | Fixed minimum and maximum plot depth window in meters. |
| `-depth_range` | `<meters>` | `0.0` | Vertical depth window height in meters that auto-phases (shifts vertically in `10%` steps) based on the bottom track. |
| `-m_less_than_maxdepth` | `<meters>` | `0.0` | Set minimum plot depth to `<meters>` above the automatic maximum depth. |
| `-nosam` | `<pixels>` | `1000` | Vertical height of the output image in pixels (`nosamples`). |
| `-Zpixel` | `<meters>` | `0.0` | Vertical pixel size in meters (overrides `-nosam` when `-mindepth` and `-maxdepth` are set). |
| `-velocity` | `<m/s>` | `1500.0` | Sound speed in m/s used to convert two-way travel time to depth. |
| `-draft` | `<meters>` | `0.0` | Transducer draft in meters added to trace depths. |
| `-get_AUV_depth` | none | `0` | Add vehicle depth stored in the profile header for AUV sub-bottom surveys. |
| `-heave_already_applied` | none | `0` | Do not apply `profile.vesselHeave` vertical trace shift. |
| `-flip_heave` | none | `0` | Invert the sign of heave compensation. |
| `-apply_diffheave` | none | `0` | Apply differential heave correction. |
| `-RP_to_sonar` | `<X> <Y> <Z>` | `0 0 0` | Compute and apply lever-arm induced heave from roll/pitch and `[X, Y, Z]` offsets. |
| `-above` / `-below` | none | `ALL` | Plot only the water column above bottom (`-above`) or only the sub-bottom below the seabed pick (`-below`). |
| `-above_m` / `-below_m` / `-pre_m` | `<meters>` | `12000` / `0` | Restrict trace rendering to `<above_m>` meters above and `<below_m>` meters below the bottom pick. |
| `-use_repick` | none | `0` | Read re-picked seabed arrival depths from `<prefix>.picks` (created by [`pickSS`](pickSS)). |
| `-other_bpick` | none | `0` | Use the bottom pick from the opposite channel (`HF` pick for `LF` trace or vice versa). |
| `-fix_zero_depth` | none | `0` | Hold the last valid bottom track across zero-depth dropouts. |
| `-stack` | `<N>` | `0` | Stack `<N>` adjacent traces along-track. |
| `-least_stack` / `-most_stack` | none | average | Use minimum or maximum intensity instead of mean when stacking traces. |
| `-map` | `<file.map>` | none | Project traces into the coordinate system of `<file.map>` and write `<out>.perspect`. |
| `-orthomap` / `-alongmap` | none | `-alongmap` | Project traces onto the across-map (`-orthomap`) or along-map (`-alongmap`) axis. |
| `-pixel` | `<meters>` | map pixel size | Override horizontal pixel size in meters when mapping. |
| `-fill_map_gap` | none | `0` | Interpolate across empty horizontal map columns (`notraces_tofill = 15`). |
| `-lr_flip` / `-no_flip` | none | `-no_flip` | Flip the horizontal plot direction left-to-right. |
| `-time_start` / `-time_end` | `<Y> <J> <H> <M> <S>` | all | Filter pings to a UTC time window (`year jday hour min sec`). |
| `-time_start_file` / `-time_end_file` | `<file.merged>` | none | Derive time window start/end from the summary headers of reference `.merged` files. |
| `-time_map` | `<sec_per_pix>` | `0.0` | Map horizontal axis linearly by time at `<sec_per_pix>` seconds per pixel. |
| `-first` / `-last` | `<ping>` | all | First and last ping indices to plot (when processing a single file). |
| `-azirange` | `<low> <high>` | `0 360` | Only plot pings whose course made good falls within `[low, high]` degrees. |
| `-speedrange` | `<min> <max>` | `0 1000` | Only plot pings whose vessel speed in m/s falls within `[min, max]`. |
| `-contour` | `<meters>` | `0` | Draw horizontal depth grid lines every `<meters>` meters. |
| `-allow_non1600` | none | `0` | Support variable-length trace records (`!= 1600` samples). |
| `-log` | none | `0` | Apply logarithmic lookup table enhancement to 8-bit trace intensities. |
| `-dump_16bit_ascii` | none | `0` | Dump 16-bit trace values to an ASCII file. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Spatial & Temporal Indexing**: Scans all input `.merged` files (using `.100` decimated navigation index files when available via `check_in_area()`) to determine the geographic/map bounds, time range, and minimum/maximum trace depths.
2. **Trace Extraction & Vertical Alignment (`get_trace`)**: Reads each 8-bit trace from `<infile>.ss_data`, applies heave, draft, AUV depth, and lever-arm induced heave corrections, optionally masks samples above or below the seabed pick (`-above`, `-below`, `-above_m`, `-below_m`), and resamples the trace into the target `[mindepth, maxdepth]` vertical pixel array (`nosamples`).
3. **Scroll / Map Projection Output**: Writes the `JHC_header` image (`-out`) either sequentially by ping, linearly by time (`-time_map`), or binned into a `.map` sheet's horizontal pixels along with `<out>.perspect` for [`collapseSeisStack`](collapseSeisStack).

## Practical Examples

### Create a heave-compensated LF sub-bottom scroll image with 10 m depth contours

```bash
makeSeisPlot -lf -allow_non1600 -mindepth 20 -maxdepth 120 -nosam 1000 \
             -contour 10 -out line01_lf.seis -in line01.merged
```
