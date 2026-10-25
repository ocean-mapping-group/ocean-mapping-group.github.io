---
layout: default
title: gsftest
parent: GSF Tools
nav_order: 7
tool_name: gsftest
source_path: code/gsf/gsftest.c
category: Diagnostics & Indexing
input_formats: [".gsf"]
output_formats: ["stdout (detailed sensor & snippet dumps)"]
related_tools: ["gsfTool", "omg2gsf", "gsf2omg_7101"]
---

# gsftest

## Overview
`gsftest` is a detailed GSF inspection and verification utility linked against the full `gsf_lib` library (`gsfOpen` / `gsfRead`). Originally written to verify GSF files produced by [`omg2gsf`](omg2gsf.md) and third-party hydrographic packages, it prints ping headers, scale factors, and full sensor-specific bathymetry and imagery subrecords for **R2Sonic (2022/2024)**, **Reson SeaBat 7125**, **Kongsberg EM4 (`EM710`, `EM302`, `EM122`)**, and **Kongsberg EM3002**, along with optional per-beam sounding arrays (`-print_beams`) and snippet time series (`-print_snippet_data`).

## Usage
```bash
gsftest [-print_beams] [-print_snippet_data] -in <filename.gsf>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<filename.gsf>` | **Required** | Path to the input `.gsf` file. |
| `-print_beams` | None | Off | Print per-beam flags, angles, two-way travel times, `(along, across, depth)` coordinates, relative/calibrated amplitudes, and snippet sample counts. |
| `-print_snippet_data` | None | Off | Print every individual snippet time-series sample (`raw`, `signed short`, and `0.1 dB` scaled float) for every beam in every ping. |

## How It Works
1. **Sequential GSF Reading:** Opens the `.gsf` file via `gsfOpen(inname, GSF_READONLY, &handle)` and iterates through all records using `gsfRead(handle, GSF_NEXT_RECORD, ...)`.
2. **Header, Comment, and Ping Inspection:** Prints `GSF_RECORD_HEADER` version strings and `GSF_RECORD_COMMENT` strings. For each `GSF_RECORD_SWATH_BATHYMETRY_PING`, prints ping time, attitude, navigation, beam count, sensor ID, depth/tide/GPS-tide correctors, and travel-time scale factor/offset.
3. **Sensor-Specific Subrecord Dumping:** Inspects `in_record.mb_ping.sensor_id` and prints all fields of `gsfR2SonicSpecific` / `gsfR2SonicImagerySpecific`, `gsfReson7100Specific`, `gsfEM4Specific` (including all transmit sectors and `gsfEM4ImagerySpecific`), or `gsfEM3ImagerySpecific`.
4. **Beam & Snippet Dumping:** If `-print_beams` or `-print_snippet_data` is enabled, loops through `0..number_beams-1` and prints beam arrays and `brb_inten->time_series[j]` snippet traces.

## Practical Examples

**1. Inspect ping headers and sensor-specific metadata in a GSF file:**
```bash
gsftest -in line01.gsf | head -n 60
```

**2. Dump all beam soundings and calibrated snippet samples:**
```bash
gsftest -print_beams -print_snippet_data -in line01.gsf > line01_dump.txt
```
