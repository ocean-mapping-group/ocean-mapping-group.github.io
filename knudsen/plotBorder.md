---
layout: default
title: plotBorder
parent: Knudsen Chirp Sub-Bottom (knudsen)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 12
tool_name: plotBorder
source_path: knudsen/plotBorder.c
category: seismic_plotting
input_formats:
- OMG_HDCS
output_formats:
- PLOTLIB_VECTOR
related_tools:
- makeSeisPlot
- knud2glo
---

# plotBorder

## Overview

`plotBorder` reads an OMG HDCS sub-bottom `.merged` file and generates a `plotlib` vector border file containing a rectangular frame, labeled horizontal depth grid lines (`-depths`), and vertical time/position annotation ticks (`-label_sec`) to surround hardcopy sub-bottom scroll plots.

## Usage

```
plotBorder (-v) (-size 100.0 20.0) (-first 100 -last 300) \
           (-depths 50 0 5) (-label_sec 60) -in infilename.merged -out outfilename.plt
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<infilename.merged>` | *required* | Input OMG HDCS `.merged` file. |
| `-out` | `<outfilename.plt>` | *required* | Output `plotlib` vector plot file. |
| `-size` | `<dx_cm> <dy_cm>` | `100.0 20.0` | Plot width and height in centimeters (note: `dx` is recomputed as `(last_ping - first_ping) / 25.0` cm at 25 pings/cm). |
| `-depths` | `<min> <max> <step>` | `0 0 1` | Minimum depth, maximum depth, and depth gridline interval in meters (automatically orders `mindepth <= maxdepth`). |
| `-label_sec` | `<seconds>` | `60` | Time interval in seconds between vertical timestamp and degrees/minutes latitude/longitude labels along the top border. |
| `-first` / `-last` | `<ping>` | `0` / `numProfiles` | First and last ping indices included in the scroll plot. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Frame & Depth Grid Drawing**: Opens a `plotlib` canvas of size `(dx + 10)` by `(dy + 10)` cm with a 5 cm margin (`xoff = 5.0`, `yoff = 5.0`), draws the outer rectangular box, and loops from `mindepth` to `maxdepth` in steps of `depthstep` to draw horizontal depth lines labeled in meters (`%.1fm`).
2. **Time & Position Tick Annotation**: Iterates from `first_ping + 1` to `last_ping`. Whenever the ping timestamp crosses a multiple of `label_sec`, formats the UTC date/time via `stdtime_nicetime()` (`JD%j %M %D %Y %T`) and transducer degrees/decimal-minutes coordinates via `locate_transducer()`, drawing a vertical tick mark and 90°-rotated text labels above the top border.

## Practical Examples

### Generate a vector border with 5 m depth lines and 60 s time ticks

```bash
plotBorder -depths 10 60 5 -label_sec 60 -in knud_line01.merged -out knud_line01_border.plt
```
