---
layout: default
title: 8kTool
parent: Reson Tools
nav_order: 183
---
# 8kTool

## Description
`8kTool` is a diagnostic utility for older Reson SeaBat 8000 series (`.81x`) files. Its primary function is to parse an `.81x` file, identify and count bathymetry and snippet data records, and optionally print verbose dumps of their contents to standard output.

This tool is useful for inspecting the raw structure and content of `.81x` files, verifying data integrity, and understanding the types and quantity of data stored within them. It supports `RESON_BATHY` and `RESON_SNIPPET` (SNP0 and SNP1) records.

## Usage
```bash
8kTool -in <inputfile> [-v] [-vb] [-vs]
```

## Arguments

| Option | Description |
|---|---|
| `-in <inputfile>` | **Required.** Path to the input Reson SeaBat 8000 series (`.81x`) file. |
| `-v` | Enable general verbose output (e.g., sync header, packet type). |
| `-vb` | Verbose output for Bathymetry records. |
| `-vs` | Verbose output for Snippet records. |

## How It Works

1.  **Initialization:** Parses command-line arguments to get the input `.81x` filename and various verbose flags. Initializes `RESON_PEEKER`, `RESON_BATHY`, `RESON_SNIPPET`, and `SNP1` structures.
2.  **File Opening:** Opens the input `.81x` file for reading.
3.  **Record Processing Loop:** Reads the `.81x` file record by record:
    *   **Sync Search:** Calls `seek_next_8K_sync()` (an external function) to find the next Reson 8k synchronization pattern.
    *   **Peeker Reading:** Reads `RESON_PEEKER` to get the `synch_header` and `packet_type`.
    *   **Record Parsing and Printing:** Uses a `switch` statement based on `peeker.synch_header`:
        *   If `RESON_8K_SYNC_PATTERN`: Reads `RESON_BATHY` data. If `verbose_bathy` is set, calls `printRESON_BATHY()` (an external function). Increments `count_bathy`.
        *   If `SNIPPET_ID_SNP0`: Reads `RESON_SNIPPET` data. If `verbose_snippets` is set, calls `printRESON_SNIPPET()` (an external function). Increments `count_snippets`.
        *   If `SNIPPET_ID_SNP1`: Reads `SNP1` data. If `verbose_snippets` is set, calls `printSNP1()` (an external function). Seeks past the snippet sample data.
        *   For unsupported packet types, it prints a warning and seeks past the record.
    *   Updates `corrupt_bathy` counter if reading a bathy record fails.
4.  **Summary Output:** After processing the entire input file, it prints a summary of the total number of bathymetry and snippet records found, and the number of corrupt bathy datagrams.
5.  **Cleanup:** Closes the input file.

## Output Files
The tool prints a summary of bathymetry and snippet record counts, and optionally verbose dumps of selected record types, to standard output.

## Dependencies
*   `Reson_8K_parser.h`: For Reson 8k data structures and parsing functions.
*   `support.h`: For general utility functions and error handling.

## Notes
`8kTool` is an essential diagnostic utility for inspecting and troubleshooting older Reson SeaBat 8000 series data files. It provides raw insight into the binary format, which is invaluable for data validation, debugging conversion issues, and understanding the types and quantity of data present. The verbose output options allow for detailed examination of specific record types.