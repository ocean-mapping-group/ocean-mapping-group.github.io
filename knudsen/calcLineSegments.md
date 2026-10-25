---
layout: default
title: calcLineSegments
parent: Knudsen Tools
nav_order: 1
tool_name: calcLineSegments
source_path: knudsen/calcLineSegments.c
category: navigation_processing
input_formats: [OMG_HDCS]
output_formats: [ASCII_STDOUT]
related_tools: [knud2glo, makeSeisPlot]
---

# calcLineSegments

## Overview

`calcLineSegments` reads one or more OMG HDCS `.merged` files, computes the ping-to-ping Course Made Good (`CMG_azi`), smoothed gyro heading (`SMTH_GYRO_azi`), smoothed turn rate in degrees per second (`SMTH_GYRO_rate`), and a complementary-filtered heading (`NEW_GYRO_azi`) that blends low-frequency CMG with high-frequency gyro variations, printing the per-ping heading and turn-rate history to standard output to identify survey line start and stop turns.

## Usage

```
calcLineSegments (-v) (-filtlen 3) OMG_HDCS_datafile [OMG_HDCS_datafile ...]
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<OMG_HDCS_datafile>` | `<file1> [file2 ...]` | *required* | One or more OMG HDCS `.merged` files to analyze. |
| `-filtlen` | `<pings>` | `3` | Half-width of the boxcar smoothing window in pings (averages over `2 * filtlen` pings from `-filtlen` to `+filtlen - 1`). |
| `-v` | none | `0` | Enable verbose output (prints `GYRO`, `CMG`, and `NEW_GYRO` azimuths in degrees for every ping). |

## How It Works

1. **Vector Decomposition**: Reads `OMG_HDCS_summary_header` and iterates through all `summary.numProfiles` pings. Converts `profile.vesselHeading` into unit vector components `(GYRO_x, GYRO_y)` via `dget360offsets()` and computes step displacements `CMG_x = dLon * cos(refLat)` and `CMG_y = dLat` and azimuth `CMG_azi` via `get360azi()`.
2. **Boxcar Filtering & Turn Rate**: Averages `CMG_x`, `CMG_y`, `GYRO_x`, and `GYRO_y` over `[-filtlen, +filtlen)` pings, reconstructs smoothed azimuths (`low_cmg_azi`, `SMTH_GYRO_azi`), computes turn rate `SMTH_GYRO_rate[i] = ((SMTH_GYRO_azi[i] - SMTH_GYRO_azi[i-1]) * 180 / pi) / dtime`, and forms the blended heading vector `NEW_GYRO = low_cmg + (GYRO - low_gyro)`.
3. **Output**: Prints per-ping `GYRO`, `SMTH`, `dt`, and turn `rate` to `stdout`.

## Practical Examples

### Compute smoothed heading and turn rates with a 10-ping filter window

```bash
calcLineSegments -v -filtlen 10 knud_line01.merged > line01_turns.txt
```
