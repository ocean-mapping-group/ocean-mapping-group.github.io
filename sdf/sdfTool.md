---
layout: default
title: sdfTool
parent: SDF Tools
nav_order: 4
tool_name: sdfTool
source_path: code/sdf/sdfTool.c
category: Diagnostics & Indexing
input_formats: [".sdf"]
output_formats: ["stdout (ASCII summary & record dumps)"]
related_tools: ["sdf2omg", "sdf2nav", "sdf2orientation"]
---

# sdfTool

## Overview
`sdfTool` is a diagnostic utility for inspecting Klein Sonar Data Format (`.sdf`) files. It scans through all SDF ping records, optionally prints detailed header and sub-record structures when `-v` is enabled, and outputs a summary count of total records and specific Klein page versions (`5902`, `5911`, `5910`, `5920`).

## Usage
```bash
sdfTool [-v] -in <inputfile.sdf>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<inputfile.sdf>` | **Required** | Path to the input Klein `.sdf` file. |
| `-v` | None | Off | Increment `reader->verbose` to print detailed SDF record headers and sub-block structures during parsing. |

## How It Works
1. **Initialization:** Allocates and initializes an `SDF_Reader` structure (`init_SDF_Reader`) and opens the `.sdf` file with `open_SDF_File()`.
2. **Record Traversal:** Loops through the file calling `seek_SDF_Record()` and `read_SDF_Record()`, accumulating total record counts and page-version counters (`sdf_5902_count`, `sdf_5911_count`, `sdf_5910_count`, `sdf_5920_count`), and prints the summary totals at EOF.

## Practical Examples

**1. Inspect the record inventory of a Klein `.sdf` file:**
```bash
sdfTool -in survey_line01.sdf
```

**2. Dump detailed SDF headers for every record:**
```bash
sdfTool -v -in survey_line01.sdf
```
