---
layout: default
title: jgsf2omg
parent: gsf
---

# jgsf2omg

## Description
`jgsf2omg` is a utility program designed to convert GSF (Generalized Sonar Format) files to OMG (Ocean Mapping Group) format. It specifically handles HIPS dumps of 7125 data logged originally in HSX, reading GSF files and outputting OMG merged files. The program supports verbose and debug modes, and can process different sonar types like SeaBat 7125.

## Usage
```bash
jgsf2omg (-v) (-debug) (-7125) -gsf input_name -omg omg_file_prefix
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output |
| `-debug` | Enable debug output |
| `-7125` | Specify SeaBat 7125 sonar type |
| `-gsf input_name` | Specify the input GSF file name |
| `-omg omg_file_prefix` | Specify the output OMG file prefix |

## How It Works
1. **Argument Parsing:** Parses command-line arguments to set options, input file, and output prefix.
2. **File Opening:** Opens the specified GSF file for reading and creates output OMG merged file.
3. **Data Processing:** Reads GSF records and converts them to OMG format, writing to the output file.
4. **Record Counting:** Tracks various record types (headers, SVP, parameters, comments, pings, etc.) for processing statistics.

## Notes
- Originally modified from DUMP_GSF module by J. S. Byrne
- Designed for USNS Pathfinder data processing
- Supports GSF files without sonar ID included