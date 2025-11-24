---
layout: default
title: refoOptech
parent: Optech Tools
nav_order: 122
---
# refoOptech

## Description
`refoOptech` is a utility designed to convert raw Optech ASCII data into the OMG-HDCS merged file format. It processes these ASCII files, extracts individual laser shots (zaps) with their geographic coordinates, depths, and other parameters, organizes them into scan lines (swaths), and then writes each scan line as a profile into separate OMG-HDCS merged files.

The tool handles different ASCII formats (`-fmt`), determines scan direction, and creates auxiliary navigation (`.nav`) and debug (`.debug`) files for each generated merged line.

## Usage
```bash
refoOptech <infile> <outfile_prefix> [-fmt <val>] [-dont_break_lines] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<infile>` | **Required.** The path to the input raw ASCII Optech data file. |
| `<outfile_prefix>` | **Required.** The base name for the output files. The tool will generate multiple merged files (e.g., `<outfile_prefix>_0000.merged`), `.nav` files, and `.debug` files. |
| `-fmt <val>` | Specifies the format of the input ASCII file.
    *   `1`: Standard format.
    *   `2`: A different format with julian date.
    *   `3`: Missing waveform file format (uses `inter_shot_azi`). | `1` |
| `-dont_break_lines` | Prevents the tool from breaking continuous scan lines into multiple merged files based on time gaps or scan direction changes. |
| `-v` | Enable verbose output. | |

## Data Structures
*   `optech_ascii_beam`: A custom structure to hold parsed data for each LASer shot (zap), including geographic coordinates, depths, waveform parameters, and flightline information.

## How It Works
1.  **Initialization:** Initializes various global variables, file handles, and structures for storing Optech data (`optech_ascii_beam`).
2.  **Argument Parsing:** Parses command-line arguments to set input/output filenames, ASCII format (`-fmt`), and flags for line breaking.
3.  **File Opening:** Opens the input ASCII file for reading.
4.  **Merged File Structure Initialization:** Initializes an `OMG_HDCS_summary_header` structure with default values for `toolType` (Optech_Laser), `fileVersion`, and other parameters.
5.  **Record Processing Loop:** Reads the ASCII input file line by line:
    *   **Parsing:** Parses the current line of the ASCII file into an `optech_ascii_beam` structure (`ozap[zaps_in_scan]`) based on the specified `-fmt`.
    *   **Scan Line Segmentation:**
        *   **Scan Direction Detection:** It determines the scan direction (`SCAN_PLUS` or `SCAN_MINUS`) by comparing `ozap[zaps_in_scan].scan_azimuth` (for `fmt 1` and `2`) or `inter_shot_azi` (for `fmt 3`) with the previous scan's azimuth.
        *   **Scan Line Break:** When a change in scan direction is detected, or a time gap exceeds 10 seconds (if `dont_break_lines` is not set), it signals the end of a scan line and triggers the processing of the accumulated `zaps_in_scan` as a single scan line/swath.
    *   **Scan Line Processing (`calculate_scan_pseudo_swath`, `dump_swath`):**
        *   **`calculate_scan_pseudo_swath()`:**
            *   Calculates the geographic center (lat/lon) of the accumulated zaps for the current scan.
            *   Performs a least-squares fit on the projected X/Y coordinates to determine the `scan_heading` of the scan line.
            *   Transforms the geographic coordinates into across-track (`across`) and along-track (`along`) offsets relative to the scan line's heading.
        *   **`dump_swath()`:**
            *   Initializes `OMG_HDCS_profile_header` with scan line information (timestamp, lat/lon offsets, heading, heave, pitch, roll, tide, etc.).
            *   Populates `OMG_HDCS_beam` structures for each zap in the scan line, converting extracted Optech ASCII parameters into beam fields (depth, across, along, scan_azimuth, wave_height, Intensity).
            *   Writes the `summary`, `profile`, and `beams` data into a new merged file (e.g., `<outfile_prefix>_0000.merged`) and a corresponding `.nav` file. It also writes to a `.debug` file for debugging purposes.
6.  **Cleanup:** Closes all open files.

## Output Files
*   Multiple merged files (e.g., `<outfile_prefix>_0000.merged`), one for each scan line.
*   Corresponding `.nav` files for navigation.
*   Corresponding `.debug` files for debugging information.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `jcu_nav.h`: For JCU NAV data structures.

## Notes
`refoOptech` is a crucial tool for integrating raw Optech ASCII data into the OMG-HDCS processing pipeline. It handles the complex conversion from ASCII point data to multibeam profiles, including managing scan line segmentation and various data formats. The output merged files can then be processed by other OMG tools for DTM generation, quality control, and visualization. The tool creates multiple output files based on scan lines, preserving the integrity of individual flight lines.