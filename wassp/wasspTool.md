---
layout: default
title: wasspTool
parent: WASSP Tools
nav_order: 2
tool_name: wasspTool
source_path: wassp/wasspTool.c
category: diagnostics
input_formats: [WASSP]
output_formats: [ASCII_STDOUT]
related_tools: [wassp2omg]
---

# wasspTool

## Overview

`wasspTool` is a diagnostic inspection utility for binary ENL WASSP (Wide Angle Sonar Seafloor Profiler) files. It scans through WASSP packet headers in a `.000` file and prints the decoded contents of `GENBATHY` (general bathymetry) and `GEN_SENS` (general sensor) packets to standard output, while reporting the type and byte size of any other skipped packet types.

## Usage

```
wasspTool (-v) -in input.000
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<input.000>` | *required* | Input WASSP binary file to inspect. |
| `-v` | none | `0` | Enable verbose output (prints packet header type and byte size before decoding each packet). |

## How It Works

1. **File Sizing & Packet Seeking**: Opens the input file in binary mode, determines the total file length, and iterates through packets using `seek_next_WASSP_Packet(infile, file_size, &header)`.
2. **Packet Dispatch**:
   - **`GENBATHY`**: Reads the bathymetry record via `read_WASSP_Gen_Bathy()` and prints the ping header and per-beam range, angle, and backscatter values using `print_WASSP_Gen_Bathy()`.
   - **`GEN_SENS`**: Reads the external sensor packet via `read_WASSP_Gen_Sensor()` and prints sensor strings and timestamps using `print_WASSP_Gen_Sensor()`.
   - **Other Packets**: Prints `"Skipping packet of type <header> (<size> bytes)"` and advances the file pointer by `header.size` bytes.

## Practical Examples

### Inspect all packets in a WASSP file with verbose header logging

```bash
wasspTool -v -in line01.000 | head -n 100
```
