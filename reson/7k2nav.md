---
layout: default
title: 7k2nav
parent: Reson Tools
nav_order: 176
---
# 7k2nav

## Description
`7k2nav` is a utility designed to extract position data from Reson 7k (`.s7k`) files and convert it into a generic binary navigation file format (`.nav`). It specifically targets `7k_1003_Position` records within the `.s7k` file, extracts the relevant timestamp, latitude, and longitude, and then writes them to a `.nav` file compatible with other OMG tools.

This tool is essential for providing position data for georeferencing multibeam sonar data when the `.s7k` file is the primary source of navigation.

## Usage
```bash
7k2nav -s7k <input_name> -omg <omg_file_prefix> [-v] [-debug]
```

## Arguments

| Option | Description |
|---|---|
| `-s7k <input_name>` | **Required.** Path to the input Reson 7k `.s7k` file. |
| `-omg <omg_file_prefix>` | **Required.** Prefix for the output OMG-HDCS files. The tool will generate:
    *   `<omg_file_prefix>.nav`: Binary navigation file. |
| `-v` | Enable verbose output. |
| `-debug` | Enable debug output. | |

## How It Works

1.  **Initialization:** Parses command-line arguments to get input `.s7k` filename and output prefix. Initializes Reson 7k data structures (`Reson_7K_Index`, `Reson_7K_DRF`, `Reson_7K_1003_Position`) and `jcu_nav_rec`.
2.  **File Opening:** Creates the output navigation file (`.nav`).
3.  **7k Indexing:** Calls `build_Reson_7K_Index()` (an external function) to create an index of all packet types within the `.s7k` file.
4.  **Position Data Extraction:** Iterates through each `7k_1003_Position` record found in the `.s7k` index:
    *   Seeks to the record's file offset.
    *   Reads the `Reson_7K_DRF` and `Reson_7K_1003_Position` data.
    *   Calls `convert_7K_position()` (an external function) to convert the 7k position data into a `jcu_nav_rec` structure (`nav_out`).
    *   Writes `nav_out` to the `.nav` file using `nav_write()` (an external function).
    *   Increments `num_nav_recs`.
5.  **Cleanup:** Closes all open files.

## Output Files
*   `<omg_file_prefix>.nav`: A binary file containing navigation records (`jcu_nav_rec`).

## Dependencies
*   `Reson_7K_parser.h`: For Reson 7k data structures and `build_Reson_7K_Index`, `convert_7K_position` functions.
*   `jcu_nav.h`: For `jcu_nav_rec` structure and `nav_write` function.
*   `support.h`: For general utility functions and error handling.

## Notes
`7k2nav` provides a standardized way to extract navigation information from Reson 7k files, making it compatible with other tools in the OMG ecosystem that require JCU NAV format for georeferencing and processing. The tool creates a new file, preserving the original `.s7k` file. Accurate navigation is fundamental for all subsequent multibeam data processing.