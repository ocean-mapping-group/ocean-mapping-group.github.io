---
layout: default
title: sdf2nav
parent: SDF Tools
nav_order: 1
tool_name: sdf2nav
source_path: code/sdf/sdf2nav.c
category: Navigation Extraction
input_formats: [".sdf"]
output_formats: [".nav"]
related_tools: ["sdf2omg", "sdf2orientation", "sdfTool", "mergeNav"]
---

# sdf2nav

## Overview
`sdf2nav` extracts Applanix POS/MV Group 102 navigation fixes embedded inside Klein Sonar Data Format (`.sdf`) records and writes them to a binary OMG `jcu_nav_rec` navigation file (`<nav_file_prefix>.nav`).

## Usage
```bash
sdf2nav [-v] [-debug] -sdf <input_name.sdf> -nav <nav_file_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-sdf` | `<input_name.sdf>` | **Required** | Path to the input Klein `.sdf` file. |
| `-nav` | `<nav_file_prefix>` | **Required** | Output prefix; creates `<nav_file_prefix>.nav`. |
| `-v` | None | Off | Enable verbose output. |
| `-debug` | None | Off | Enable debug flag. |

## How It Works
1. **Base Date Calculation:** Opens the `.sdf` file via `open_SDF_File()`, reads the first valid SDF record (`seek_SDF_Record` / `read_SDF_Record`), and computes `base_time` at `00:00:00` UTC of the header's calendar date (`year`, `month`, `day`).
2. **POS/MV Group 102 Extraction:** Iterates through all SDF records and loops over `reader->posmv_102[0..posmv_102_count-1]`. Verifies `common.time_select == 1`, computes UTC timestamp from `base_time + (time1 % 86400)`, and writes `latitude` and `longitude` to `<nav_file_prefix>.nav`.

## Practical Examples

**1. Extract POS/MV navigation from a Klein HydroChart `.sdf` file:**
```bash
sdf2nav -sdf line01.sdf -nav line01
```
