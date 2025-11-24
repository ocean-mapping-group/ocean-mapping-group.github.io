---
layout: default
title: moveOverWCinfo
parent: OMG Tools
nav_order: 42
---
# moveOverWCinfo

## Description
`moveOverWCinfo` is a utility designed to transfer water column (WC) information (size and offset) from a "WC info" merged file (typically generated from unraveling a `.wcd` file) to a "full" merged file (typically generated from unraveling a `.all` file). This is particularly useful when WC data is logged separately and needs to be linked to the main bathymetric merged file.

The tool attempts to match profiles between the two merged files. Historically, this was done primarily by time stamps. With the advent of formats like KMALL, which include more detailed indexing (ping number, RX fan index, swath position), `moveOverWCinfo` now offers a more robust matching mechanism.

## Usage
```bash
moveOverWCinfo [-v] [-tol <tolerance>] <dot_all_merged_file> <wcinfo_merged_file>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `<dot_all_merged_file>` | **Required.** The path to the main merged file (often derived from a `.all` raw file) where the water column information will be written. This file is modified in place. | |
| `<wcinfo_merged_file>` | **Required.** The path to the merged file (often derived from a `.wcd` raw file) containing the water column size and offset information. | |
| `-tol <tolerance>` | Specifies a time tolerance (in seconds) for matching profiles when exact time stamps don't align. | `0.0` (exact match) |
| `-v` | Enable verbose output. | |

## How It Works
1.  **File Loading:** Opens two merged files: the `dot_all_merged_file` (target) and the `wcinfo_merged_file` (source of WC info).
2.  **Header Check:** Verifies that both files have the same file version and warns if the number of profiles differs.
3.  **Matching Strategy (KMALL-aware):**
    *   **Ping Indexing (New in 2022):** If both merged files contain KMALL-specific ping indexing information (ping number, RX fan index, swath along position), the tool prioritizes matching profiles based on these indices in addition to time. It builds an index for both files and then attempts to find the best match for each profile in the target file.
    *   **Time-Based Matching (Old Way):** If KMALL ping indexing is not available or not used, the tool falls back to matching profiles primarily by their time stamps. It iterates through the target file, and for each profile, it searches the source file for a profile with a matching (or sufficiently close, given `-tol`) time stamp. It adjusts an internal `ping_offset` to speed up subsequent searches.
4.  **Information Transfer:**
    *   Once a match is found, the `watercol_size`, `watercol_offset`, and `watercol_offset_64` fields from the source profile are copied to the corresponding target profile.
    *   If no match is found, the water column information in the target profile is set to zero (effectively indicating no associated WC data).
5.  **In-Place Update:** The modified profiles in the `dot_all_merged_file` are written back to the file.

## Output Files
The input `dot_all_merged_file` is modified in-place to include water column information.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is essential for workflows where water column data is generated separately from the main bathymetry (e.g., from different raw data streams or processing paths). The improved KMALL-aware matching strategy enhances the reliability of linking WC data to bathymetric pings. As the tool modifies the merged file in place, backups are recommended.