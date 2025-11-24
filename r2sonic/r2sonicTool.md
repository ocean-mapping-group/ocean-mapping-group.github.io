---
layout: default
title: r2sonicTool
parent: R2Sonic Tools
nav_order: 162
---
# r2sonicTool

## Description
`r2sonicTool` is a diagnostic utility for R2Sonic multibeam sonar `.r2s` files. It reads an `.r2s` file, builds an index of its internal data packets, and then, based on user-specified verbose flags, prints the contents of various packet types (Bathy, Snippets/FTS, TruePix, Water Column Data) to standard output.

This tool is primarily used for inspecting the raw structure and content of `.r2s` files, verifying data integrity, and understanding the details of R2Sonic's proprietary data formats. It's a valuable tool for developers and advanced users needing to debug or gain insight into R2Sonic data.

## Usage
```bash
r2sonicTool -in <input.r2s> [-vb] [-vs] [-vt] [-vw] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-in <input.r2s>` | **Required.** Path to the input R2Sonic `.r2s` file. |
| `-vb` | Verbose output for Bathy packets. |
| `-vs` | Verbose output for Snippets (FTS) packets. |
| `-vt` | Verbose output for TruePix packets. |
| `-vw` | Verbose output for Water Column Data (WCD) packets. |
| `-v` | Global verbose flag (enables verbose output for indexing and other general messages). |

## How It Works
1.  **Initialization:** Parses command-line arguments to set the input `.r2s` filename and various verbose flags. Initializes R2Sonic data structures (`R2SONIC_INDEX`, `R2SONIC_FTS`, `R2SONIC_TRUEPIX`, `R2SONIC_BATHY`, `R2SONIC_WCD`).
2.  **File Opening:** Opens the input `.r2s` file for reading.
3.  **R2Sonic Indexing:** Calls `build_R2SONIC_INDEX()` (an external function) to create an index of all packet types (e.g., BTH0, SNI0, TPX0, WCD0) present in the `.r2s` file.
4.  **Packet Traversal and Printing:**
    *   Iterates through each identified packet type.
    *   For each packet type that has records:
        *   If the corresponding verbose flag is set (e.g., `-vb` for Bathy, `-vs` for Snippets):
            *   It iterates through each ping (record) of that packet type.
            *   Seeks to the `file_offset` of the record.
            *   Reads the packet data using the appropriate `read_R2SONIC_*()` function (`read_R2SONIC_BATHY`, `read_R2SONIC_FTS`, `read_R2SONIC_TRUEPIX`, `read_R2SONIC_WCD`).
            *   Prints the contents of the packet using the corresponding `print_R2SONIC_*()` function (e.g., `print_R2SONIC_BATHY`, `print_R2SONIC_FTS`, `print_R2SONIC_TRUEPIX`, `print_R2SONIC_WCD`) to standard output.
5.  **Cleanup:** Frees the R2Sonic index and closes the input file.

## Output Files
The tool prints structured information about the contents of the `.r2s` file to standard output, detailing the headers and data within selected packet types.

## Dependencies
*   `R2Sonic_parser.h`: For R2Sonic data structures and parsing functions (`build_R2SONIC_INDEX`, `read_R2SONIC_*`, `print_R2SONIC_*`).
*   `support.h`: For general utility functions and error handling.

## Notes
`r2sonicTool` is an essential debugging and diagnostic utility for anyone working with R2Sonic raw data. It allows low-level inspection of the `.r2s` file contents, which is crucial for understanding data integrity, verifying parsing implementations, or troubleshooting issues with specific data streams. The detailed verbose output provides developers with the necessary information to interpret the proprietary R2Sonic format.