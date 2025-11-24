---
layout: default
title: refoLAS
parent: Optech Tools
nav_order: 121
---
# refoLAS

## Description
`refoLAS` is a utility designed to convert Optech LAS (LASer) format data into the OMG-HDCS merged file format. It processes raw LAS binary files, extracts point cloud data (X, Y, Z, intensity, GPS time, etc.), organizes it into individual scan lines (swaths), and then writes these scan lines as profiles into OMG-HDCS merged files.

The tool also handles specific processing related to missing waveform data, scan direction changes, and the conversion of LAS-specific data into OMG-HDCS beam parameters.

## Usage
```bash
refoLAS <infile> <outfile_prefix> [-fmt <val>] [-dont_break_lines] [-miss <missing_zap_ascii_file>] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<infile>` | **Required.** The path to the input raw binary LAS file. |
| `<outfile_prefix>` | **Required.** The base name for the output OMG-HDCS merged files. The tool will generate multiple merged files, each representing a scan line, named like `<outfile_prefix>_0000.merged`, `<outfile_prefix>_0001.merged`, etc. |
| `-fmt <val>` | Specifies the format of the LAS file (e.g., `fmt 1` for a specific version). | `1` |
| `-dont_break_lines` | Prevents the tool from breaking continuous scan lines into multiple merged files based on time gaps or scan direction changes. |
| `-miss <missing_zap_ascii_file>` | Specifies an ASCII file containing timestamps of missing zaps (waveforms). This is used for handling gaps in the data. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Initializes various global variables, file handles, and structures for LAS data (`LAS_public_header`, `LAS_point_data_record_f1`, `optech_ascii_beam`).
2.  **Argument Parsing:** Parses command-line arguments to set input/output filenames, LAS format, and flags for handling missing data.
3.  **Missing Data Loading (`-miss`):** If a missing zaps file is provided, it reads the timestamps of missing zaps into `buf_miss_timestamp`, `buf_miss_lat`, `buf_miss_lon` arrays.
4.  **LAS File Header Reading:** Opens the input LAS file and reads the `LAS_public_header` (`phead`). It extracts scaling factors, offsets, and other metadata necessary for coordinate conversion.
5.  **Point Data Processing Loop:** Seeks to `phead.offset_to_point_data` in the input LAS file and then reads `LAS_point_data_record_f1` (`point_data`) records one by one:
    *   **Coordinate Conversion:** Converts raw integer X, Y, Z values from `point_data` into floating-point geographic coordinates (latitude, longitude) and depth, using the scaling factors and offsets from `phead`.
    *   **Timestamp Conversion:** Converts `point_data.GPS_Time` (GPS week seconds) to a Unix timestamp.
    *   **Scan Line Segmentation:**
        *   It continuously accumulates `ozap` structures (containing converted data for each LAS point) into a `zaps_in_scan` buffer.
        *   **Scan Direction Detection:** It detects changes in `scan_direction` (from `SCAN_PLUS` to `SCAN_MINUS` or vice-versa) based on `point_data.scan_angle_rank` (scan angle).
        *   **Scan Line Break:** When a scan direction changes or a significant time gap between zaps is detected (if `-dont_break_lines` is not set), it triggers the processing of the accumulated `zaps_in_scan` as a single scan line/swath.
    *   **Missing Waveform Handling (`-miss`):** This section includes logic to identify `zap_gap_count` and `continuous_zap_count` based on inter-zap time. If a gap is detected and falls within the loaded missing data timestamps, it attempts to insert missing zaps into the sequence (though the insertion logic is complex and involves referencing `buf_miss_timestamp`).
6.  **Scan Line Processing (`calculate_scan_pseudo_swath`, `dump_swath`):**
    *   **`calculate_scan_pseudo_swath()`:**
        *   Calculates the geographic center (lat/lon) of the accumulated zaps for the current scan.
        *   Performs a least-squares fit on the projected X/Y coordinates to determine the `scan_heading` of the scan line.
        *   Transforms the geographic coordinates into across-track (`across`) and along-track (`along`) offsets relative to the scan line's heading.
    *   **`dump_swath()`:**
        *   Initializes `OMG_HDCS_summary_header` for the new merged file (setting `toolType` to `Optech_Laser`).
        *   Populates `OMG_HDCS_profile_header` with scan line information (timestamp, lat/lon offsets, heading, heave, pitch, roll, tide, etc.).
        *   Populates `OMG_HDCS_beam` structures for each zap in the scan line, converting extracted LAS parameters (depth, across, along, intensity, scan_azimuth, wave_height) into beam fields.
        *   Writes the `summary`, `profile`, and `beams` data into a new merged file (e.g., `outfile_prefix_0000.merged`) and a corresponding `.nav` file.
7.  **Cleanup:** Closes all open files.

## Output Files
*   `<outfile_prefix>_0000.merged`, `<outfile_prefix>_0001.merged`, etc.: OMG-HDCS merged files, one for each scan line.
*   `<outfile_prefix>_0000.nav`, etc.: JCU NAV files corresponding to each merged file.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `jcu_nav.h`: For JCU NAV data structures.
*   `LAS_header.h`: For LAS file format structures.

## Notes
`refoLAS` is a critical tool for integrating Optech LASer scanner data into the OMG-HDCS processing pipeline. It handles the complex conversion from LAS point cloud format to multibeam profiles, including managing scan line segmentation and missing data. The output merged files can then be processed by other OMG tools for DTM generation, quality control, and visualization. The tool creates multiple output files based on scan lines, preserving the integrity of individual flight lines.