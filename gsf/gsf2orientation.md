---
layout: default
title: gsf2orientation
parent: Generic Sensor Format — GSF (gsf)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 3
tool_name: gsf2orientation
source_path: code/gsf/gsf2orientation.c
category: Attitude Extraction
input_formats:
- .gsf
output_formats:
- .orientation
related_tools:
- gsf2omg
- gsf2param
- gsf2svp
- gsfTool
- mergeAtt
---

# gsf2orientation

## Overview
`gsf2orientation` extracts full time-series attitude packets (`GSF_ATTITUDE`, record ID 6) from a Generic Sensor Format (`.gsf`) file and writes them to a binary OMG-HDCS v3 `.orientation` file.

## Usage

```bash
gsf2orientation [-v] -gsf <input_name.gsf> -omg <omgfile.orientation>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-gsf` | `<input_name.gsf>` | **Required** | Path to the input `.gsf` file. |
| `-omg` | `<omgfile.orientation>` | **Required** | Path to the output OMG `.orientation` file. |
| `-v` | None | Off | Print every parsed `GSF_Attitude` packet and individual attitude measurements (`time`, `roll`, `pitch`, `heading`, `heave`). |

## How It Works
1. **Summary Header Initialization:** Scans the `.gsf` file for the first `GSF_ATTITUDE` packet (`seek_GSF_packet`), extracts `basetime.seconds` and `basetime.nanoseconds`, rewinds the file, and writes an `OMG_HDCS_summary_attitude` header (`fileVersion = 3`, `status = 15` for RPH+heave).
2. **Bundle Unpacking:** Because each `GSF_ATTITUDE` packet stores a bundle of `num_points` measurements with millisecond offsets (`time_offset[i]`) relative to `recordBaseTime`, `gsf2orientation` loops over all `num_points` in each packet, preserves the native GSF integer scaling (hundredths of degrees for roll/pitch/heading, centimeters for heave), and writes each sample to `<omgfile.orientation>`.

## Practical Examples

**1. Extract high-rate attitude from a GSF file:**

```bash
gsf2orientation -v -gsf line01.gsf -omg line01.orientation
```
