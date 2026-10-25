---
layout: default
title: makeSeisPlot_Op
parent: Knudsen Tools
nav_order: 8
tool_name: makeSeisPlot_Op
source_path: knudsen/makeSeisPlot_Op.c
category: seismic_plotting
input_formats: [OMG_HDCS, OMG_SS_DATA, JHC_MAPSHEET]
output_formats: [JHC_ARRAY, ASCII_PERSPECT]
related_tools: [makeSeisPlot, collapseSeisStack]
---

# makeSeisPlot_Op

## Overview

`makeSeisPlot_Op` is a multi-beam / swath-capable variant of [`makeSeisPlot`](makeSeisPlot) that tracks up to 200 beams per swath (`whole_swath` / `ebeam[200]`) when projecting sub-bottom or water-column trace data from OMG HDCS `.merged` and `.merged.ss_data` files onto a `JHC_header` scroll image or `.map` sheet.

## Usage

```
makeSeisPlot_Op (-v) (-log) (-first 100 -last 300) (-above | -below) \
                (-stack 3 (-least_stack | -most_stack)) (-orthomap) (-lr_flip) \
                (-antialias) (-velocity 1480 -draft 7.0) (-nosam 500) \
                (-allow_non1600) (-use_repick) (-map whatever.map) (-pixel 1.0) \
                (-fill_map_gap -fix_zero_depth) \
                (-mindepth 20 -maxdepth 60 | -depth_range 100) \
                (-m_per_m 10.0) (-hf | -lf) -out outfilename -in infilename(s)
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-out` | `<outfilename>` | *required* | Output `JHC_header` 8-bit image file. |
| `-in` | `<file1> [file2 ...]` | *required* | Input OMG HDCS `.merged` file(s). |
| `-hf` / `-lf` | none | `-lf` (`1`) | Select high-frequency (`0`) or low-frequency (`1`) channel. |
| `-mindepth` / `-maxdepth` | `<meters>` | auto | Fixed minimum and maximum depth window in meters. |
| `-depth_range` | `<meters>` | `0.0` | Auto-phasing depth window height in meters. |
| `-nosam` | `<pixels>` | `1000` | Vertical image height in pixels (`nosamples`). |
| `-velocity` | `<m/s>` | `1500.0` | Sound speed in m/s. |
| `-draft` | `<meters>` | `0.0` | Transducer draft in meters. |
| `-above` / `-below` | none | `ALL` | Plot only samples above or below the seabed pick. |
| `-use_repick` | none | `0` | Use re-picked seabed arrival depths from `<prefix>.picks`. |
| `-allow_non1600` | none | `0` | Support variable-length trace records (`!= 1600` samples). |
| `-stack` | `<N>` | `0` | Along-track trace stacking factor. |
| `-least_stack` / `-most_stack` | none | average | Stack using minimum or maximum value instead of average. |
| `-map` | `<file.map>` | none | Project traces onto `<file.map>` and output `<out>.perspect`. |
| `-orthomap` | none | `0` | Project onto the orthogonal axis of the map sheet. |
| `-pixel` | `<meters>` | map default | Horizontal pixel size in meters. |
| `-fill_map_gap` | none | `0` | Fill small horizontal gaps in mapped curtains. |
| `-fix_zero_depth` | none | `0` | Carry forward the last valid depth across zero-depth dropouts. |
| `-lr_flip` | none | `0` | Flip image horizontally left-to-right. |
| `-antialias` | none | `0` | Enable vertical antialiasing during resampling. |
| `-m_per_m` | `<value>` | `0.0` | Horizontal scale factor. |
| `-first` / `-last` | `<ping>` | all | First and last ping indices to plot. |
| `-log` | none | `0` | Apply logarithmic greyscale lookup table. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Swath Coordinate Projection**: Allocates `whole_swath` structures (`ebeam[200]`) and projects beam positions (`locate_beam`) into the map sheet's coordinate frame (`AcrossPos`, `AlongPos`).
2. **Trace Resampling (`get_trace(i, j, ...)`)**: Extracts the trace for ping `i` and channel/beam `j`, resamples it into `nosamples` vertical bins across `[mindepth, maxdepth]`, and accumulates it into the output `JHC_header` image along with perspective depth weights (`closestPerspect`).

## Practical Examples

### Project sub-bottom traces onto a map sheet for perspective stacking

```bash
makeSeisPlot_Op -lf -allow_non1600 -map area01.map -mindepth 10 -maxdepth 80 \
                -fill_map_gap -out line01_map.seis -in line01.merged
```
