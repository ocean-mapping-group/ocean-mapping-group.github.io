---
layout: default
title: refoELAC
parent: ELAC BottomChart Multibeam (elac)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 2
tool_name: refoELAC
source_path: elac/refoELAC.c
category: format_conversion
input_formats:
- ELAC_FAU
output_formats:
- OMG_HDCS
- ASCII_HISTOGRAM
related_tools:
- qualityFlag
- elac2omg
- xse2omg
- SwathEd
---

# refoELAC

## Overview

`refoELAC` converts raw Honeywell ELAC BottomChart FAU (Fast Acquisition Unit) multibeam files into OMG HDCS `.merged` format (with image extensions) and outputs companion ASCII `.quality` and `.amplitudes` histogram files binned by grazing angle.

## Usage

```
refoELAC (-v) (-constant 0) (-merid -69.0) (-proj_lat 45.83333333) input_FAU_file output_merged_file
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<input_FAU_file>` | `<path>` | *required* | First positional argument: input Honeywell ELAC BottomChart FAU file. |
| `<output_merged_file>` | `<path>` | *required* | Second positional argument: output OMG HDCS `.merged` file (also generates `<output_merged_file>.quality` and `<output_merged_file>.amplitudes`). |
| `-v` | none | `0` | Enable verbose output. |
| `-constant` | `<meters>` | `0` | Constant northing offset added during Mercator projection conversion. |
| `-merid` | `<degrees>` | `-69.0` | Central meridian (longitude in decimal degrees) for the Mercator projection. |
| `-proj_lat` | `<degrees>` | `45.83333333` | Reference projection latitude (in decimal degrees) for the Mercator projection. |

## How It Works

1. **Mercator Projection Setup**: Initializes a Mercator projection using `-merid` and `-proj_lat` (and optional `-constant` northing offset) to convert FAU projected coordinates into geographic latitude and longitude.
2. **FAU Record Parsing**: Reads proprietary ELAC FAU records sequentially, extracting per-ping navigation, attitude (roll, pitch, heading), and per-beam bathymetry (depth, across-track distance, amplitude, and quality factor).
3. **OMG HDCS & Histogram Output**: Writes OMG HDCS profiles and beams to `<output_merged_file>`, while accumulating amplitude and quality factor distributions by grazing angle and writing them to `<output_merged_file>.amplitudes` and `<output_merged_file>.quality`.

## Practical Examples

### Convert an ELAC FAU file to OMG HDCS format

```bash
refoELAC -v -merid -66.5 -proj_lat 45.0 raw_line01.fau elac_line01.merged
```
