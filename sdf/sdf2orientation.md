---
layout: default
title: sdf2orientation
parent: SDF Tools
nav_order: 3
tool_name: sdf2orientation
source_path: code/sdf/sdf2orientation.c
category: Attitude Extraction
input_formats: [".sdf"]
output_formats: [".orientation"]
related_tools: ["sdf2omg", "sdf2nav", "sdfTool", "mergeAtt", "newMergeAtt"]
---

# sdf2orientation

## Overview
`sdf2orientation` extracts Applanix POS/MV Group 102 attitude records (roll, pitch, heave, and heading) embedded inside Klein Sonar Data Format (`.sdf`) files and writes them to a binary OMG-HDCS v3 `.orientation` file (`<orientation_prefix>.orientation`).

## Usage
```bash
sdf2orientation [-v] [-debug] -sdf <input_name.sdf> -orientation <orientation_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-sdf` | `<input_name.sdf>` | **Required** | Path to the input Klein `.sdf` file. |
| `-orientation` | `<orientation_prefix>` | **Required** | Output prefix; creates `<orientation_prefix>.orientation`. |
| `-v` | None | Off | Enable verbose output. |
| `-debug` | None | Off | Enable debug flag. |

## How It Works
1. **Header & Base Time Initialization:** Reads the first valid SDF record to determine the UTC date (`year`, `month`, `day`), computes `base_time` at midnight UTC, and writes an `OMG_HDCS_summary_attitude` header (`status = 15` for roll, pitch, heave, and heading) to `<orientation_prefix>.orientation`.
2. **POS/MV Group 102 Extraction:** Iterates through all SDF records and loops over `reader->posmv_102[0..posmv_102_count-1]`. Converts `roll`, `pitch`, `heave`, and `heading` to hundredths of degrees/meters (`* 100.0 + 0.5`) and writes each `OMG_HDCS_attitude` record via `OMG_HDCS_write_attitude()`.

## Practical Examples

**1. Extract POS/MV orientation from a Klein `.sdf` file:**
```bash
sdf2orientation -sdf line01.sdf -orientation line01
```
