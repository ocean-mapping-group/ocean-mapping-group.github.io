---
layout: default
title: readOMG
parent: OMG Tools
nav_order: 52
---
# readOMG

## Description
`readOMG` is an interactive command-line utility for displaying the contents of an OMG-HDCS (Ocean Mapping Group - Hydrographic Data Collection System) data file. It provides a way to inspect the raw or processed data stored within these proprietary binary files, primarily focusing on the summary and individual profile information.

The tool offers an interactive interface to navigate through profiles, displaying details of each record.

## Usage
```bash
readOMG <OMG_HDCS_datafile> [-verbose]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile>` | **Required.** The path to the input OMG-HDCS data file. |
| `-verbose` | (Not explicitly used in the provided code but present in `USAGE`) Intended to provide more detailed output. |

## How It Works
1.  **File Opening:** Opens the specified OMG-HDCS data file for reading.
2.  **Summary Display:** It calls `OMG_HDCS_write_summary(infile)` (which, based on its name, likely reads the summary and writes it to standard output or a debug log, rather than modifying the file).
3.  **Interactive Profile Navigation:** The tool enters an infinite loop, prompting the user for navigation commands:
    *   **Input:** The user is asked to "imput record no:" (sic), and then presented with choices: `full (1)`, `next (2)`, `prev (0)`, `other (3)`.
    *   **Navigation:**
        *   If `2` (next) is chosen, `rec_no` is incremented.
        *   If `0` (previous) is chosen, `rec_no` is decremented.
        *   If `3` (other) is chosen, the user is prompted to enter a specific record number.
        *   The initial `rec_no` is set to `-1`, so the first `next` command makes it `0`.
    *   **Display:** For the current `rec_no`:
        *   It calls `OMG_HDCS_display_profile(infile, rec_no)`, which (based on its name) likely reads and prints the details of the specified profile.
        *   If `1` (full) is chosen, it also calls `OMG_HDCS_display(infile, rec_no)`, which presumably displays even more comprehensive information for that profile.
    *   The loop continues, allowing the user to browse through the profiles interactively.

## Limitations / Assumptions
*   The functions `OMG_HDCS_write_summary`, `OMG_HDCS_display_profile`, and `OMG_HDCS_display` are external to this file (likely defined in `OMG_HDCS_jversion.h` or linked libraries) and are assumed to handle the actual parsing and printing of the file's binary content.
*   The interactive input (`scanf`) expects integer inputs for navigation choices and record numbers.
