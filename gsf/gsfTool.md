---
layout: default
title: gsfTool
parent: Generic Sensor Format — GSF (gsf)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 6
tool_name: gsfTool
source_path: code/gsf/gsfTool.c
category: Diagnostics & Indexing
input_formats:
- .gsf
output_formats:
- stdout (ASCII record inventory & dumps)
related_tools:
- gsftest
- gsf2omg
- gsf2orientation
- gsf2param
- gsf2svp
---

# gsfTool

## Overview
`gsfTool` is a fast diagnostic utility based on the lightweight `omg_gsf` parser that scans a Generic Sensor Format (`.gsf`) file, validates 4-byte record alignment, prints the GSF version header, optionally dumps specific record types (`-vid`), and outputs a summary count of all record types encountered.

## Usage

```bash
gsfTool [-v] [-vid <ID>] -in <inputfile.gsf>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<inputfile.gsf>` | **Required** | Path to the input `.gsf` file. |
| `-v` | None | Off | Print the record name and byte size for every packet read. |
| `-vid` | `<ID>` | Off | Verbose dump of decoded fields for a specific GSF record ID (`2` Swath Bathymetry Ping, `3` Sound Velocity Profile, `4` Processing Parameters, `5` Sensor Parameters, `6` Attitude). May be specified multiple times. |

## How It Works
1. **Packet Peeking:** Iterates through the `.gsf` file calling `peek_GSF_packet(infile, &record_id, &record_size)` and warns if `record_size` is not a multiple of 4 bytes.
2. **Record Parsing:** Dynamically grows a `GSF_Buffer` as needed, reads the record payload, prints the 12-byte `GSF_HEADER` version string (`GSF-vXX.XX`), and dispatches record IDs `2..6` to their respective `parse_GSF_*` and `print_GSF_*` routines.
3. **Summary Output:** Prints `<record_id>, <record_name>: <count>` for each non-zero record type at EOF.

## Practical Examples

**1. Print a record inventory of a GSF file:**

```bash
gsfTool -in survey01.gsf
```

**2. Dump all Sensor Parameters (ID 5) and Sound Velocity Profiles (ID 3):**

```bash
gsfTool -vid 5 -vid 3 -in survey01.gsf
```
