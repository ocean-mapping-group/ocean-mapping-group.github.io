---
layout: default
title: compress_OMG_watercolumn
parent: OMG Tools
nav_order: 82
---
# compress_OMG_watercolumn

## Description
`compress_OMG_watercolumn` is a utility designed to compress water column (WC) data associated with OMG-HDCS merged files. It reads raw WC data, applies a user-specified compression factor (or lossless compression by default), and writes the compressed data to a new WC file. Concurrently, it updates the `watercol_offset` and `watercol_size` fields in the corresponding merged file to point to the newly compressed data.

The tool uses the JasPer library for JPEG2000 compression, offering a way to reduce storage size for large WC datasets.

## Usage
```bash
compress_OMG_watercolumn -in <filename.merged> [-compress <factor>] [-v]
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <filename.merged>` | **Required.** The path to the input OMG-HDCS merged file. This file will be modified to update water column offsets and sizes. | |
| `-compress <factor>` | Specifies the compression factor. A factor of `1` means lossless compression (default). Higher values generally mean more compression but potentially more loss. | `1` (lossless) |
| `-v` | Enable verbose output. | |

## How It Works
1.  **Initialization:** Initializes the JasPer library for JPEG2000 compression.
2.  **File Opening:**
    *   Opens the input merged file (`merged_name`) for reading and writing (to update WC offsets).
    *   Generates a `.jic` (JasPer Index Cache) filename and attempts to open it. If it doesn't exist, it creates one. This file is used to store original water column offsets, primarily to prevent overwriting during re-runs.
    *   Opens the original water column input file (`.watercol`) for reading.
    *   Creates a new water column output file (`.watercol2`) for writing the compressed data.
3.  **Summary Header Reading:** Reads the summary header from the merged file to get `summary.numProfiles` and `summary.toolType` (to determine the number of heads, e.g., EM3002D has 2 heads).
4.  **Profile Iteration:** Iterates through each profile (ping) in the merged file:
    *   Reads the profile header for the current ping.
    *   **Offset Tracking:** If a `.jic` file is being written, it stores the original `watercol_offset` and `watercol_offset_2nd` from the current profile.
    *   **Duplicate Offset Check:** It checks if the current profile's `watercol_offset` is the same as the `last_offset` encountered. If so, it flags this as a "doubly-pointed WC" and skips processing for this profile, effectively nullifying its WC data by setting `watercol_offset` and `watercol_size` to 0 in the merged file.
    *   **Head Iteration (for multi-head systems):** Loops through each head (e.g., 1 or 2 for EM3002D).
        *   Reads the raw water column data for the current head and ping from the input WC file into the `wc_in` structure using `j_EM_read_watercolumn`. If no WC data exists, the ping is skipped.
        *   **Compression:** Calls `j_EM_compress(&wc_in, compression_factor)` to compress the water column data.
        *   **Format Promotion:** Sets `wc_in.format_version = 2` to ensure the compressed data is written in a compatible format.
        *   **Write Compressed Data:** Writes the compressed water column data to the new WC output file (`.watercol2`) using `j_EM_write_watercolumn`. This function also updates the `watercol_offset` and `watercol_size` (or `watercol_offset_2nd` and `watercol_size_2nd` for the second head) in the `profile` structure within the merged file.
5.  **JIC File (Original Offset Backup):** If the `.jic` file was created, it writes the array of `old_offsets` to it and closes it.
6.  **Cleanup:** Closes all open files and frees allocated memory. The original `.watercol` file remains unchanged, and a new `.watercol2` file is created containing the compressed data. The `.merged` file is updated to point to this new `.watercol2` file.

## Output Files
*   The input merged file (`.merged`) is modified in-place to update water column offsets and sizes.
*   `<merged_filename_prefix>.watercol2`: A new water column file containing the compressed data.
*   `<merged_filename_prefix>.watercol.jic`: A JasPer Index Cache file.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `j_EM_watercol.h`: For water column data structures and functions (`j_EM_compress`, `j_EM_read_watercolumn`, `j_EM_write_watercolumn`).
*   `support.h`: For general utility functions and error handling.
*   `jasper/jasper.h`: For JPEG2000 compression.

## Notes
Compressing water column data can significantly reduce storage requirements, especially for long survey lines or high-resolution systems. Lossless compression (`-compress 1`) is recommended to preserve data fidelity, while higher compression factors can be used if some data loss is acceptable. This tool helps in managing the lifecycle of large water column datasets.