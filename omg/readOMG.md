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

## Interactive Mode
The tool enters an interactive loop, prompting the user for navigation commands:
*   **Input:** The user is asked to "imput record no:" (sic), and then presented with choices: `full (1)`, `next (2)`, `prev (0)`, `other (3)`.
*   **Navigation:**
    *   `2` (next): Increments `rec_no`.
    *   `0` (previous): Decrements `rec_no`.
    *   `3` (other): Prompts the user to enter a specific record number.
*   **Display:** For the current `rec_no`:
    *   Calls `OMG_HDCS_display_profile(infile, rec_no)`, which reads and prints profile details.
    *   If `1` (full) is chosen, it also calls `OMG_HDCS_display(infile, rec_no)` for more comprehensive information.

## How It Works
1.  **File Opening:** Opens the specified OMG-HDCS data file for reading.
2.  **Summary Display:** Calls `OMG_HDCS_write_summary(infile)` to read and print the file's summary header to standard output.
3.  **Interactive Profile Navigation:** Enters an infinite loop:
    *   Prompts the user for a command to navigate through the profiles.
    *   Based on user input, it updates the `rec_no` to point to the desired profile.
    *   It then calls external functions (`OMG_HDCS_display_profile`, `OMG_HDCS_display`) to read and display the details of the selected profile to the console.
    *   The loop continues, allowing the user to browse through the profiles interactively until an exit condition (e.g., specific user input, not explicitly shown in snippet) is met.

## Output Files
The tool primarily outputs data to the console during its interactive operation. No persistent output files are generated.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures and functions (`OMG_HDCS_write_summary`, `OMG_HDCS_display_profile`, `OMG_HDCS_display`).
*   `support.h`: For general utility functions.

## Notes
`readOMG` is a fundamental debugging and inspection tool for OMG-HDCS files, allowing developers and users to quickly view the contents of individual profiles and verify data integrity. Its interactive nature makes it suitable for exploratory data analysis. The functions responsible for the actual binary parsing and printing (`OMG_HDCS_write_summary`, etc.) are external to this file.