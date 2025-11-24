---
layout: default
title: parseBIST
parent: Plot Tools
nav_order: 129
---
# parseBIST

## Description
`parseBIST` is a utility designed to parse output files from BIST (Built-In Self-Test) routines of multibeam sonars, specifically to extract noise spectrum data (either element-level or spectral noise). It processes these BIST reports, formats the extracted data, and outputs it to ASCII files for visualization or further analysis, often with `asciiplot`.

The tool supports parsing BIST reports for dual RX (receiver) systems like the EM2040 and can distinguish between port and starboard receivers.

## Usage
```bash
parseBIST <BIST_file(s)> (-rxspecnoise | -rxelemnoise) [-dualRx2040] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<BIST_file(s)>` | **Required.** One or more paths to input BIST report ASCII files. |
| `-rxspecnoise` | **Required (choose one).** Extracts receiver spectral noise data. |
| `-rxelemnoise` | **Required (choose one).** Extracts receiver element noise data. |
| `-dualRx2040` | Indicates that the BIST file is from a dual RX system (e.g., EM2040). This will generate separate output files for port and starboard RXs. |
| `-v` | Enable verbose output. | |

## How It Works
1.  **Initialization:** Parses command-line arguments to set input/output filenames, select the type of noise data to extract (`tofind`), and handle dual RX systems (`dualRx2040`).
2.  **Output File Setup:**
    *   If `dualRx2040` is enabled, it opens separate output files for port (`.port`) and starboard (`.stbd`) RX noise data.
    *   Otherwise, it opens a single output file (`parse.bist`) for writing the extracted noise data.
3.  **BIST File Processing:** Loops through each input BIST report file:
    *   Reads the BIST file line by line.
    *   **Noise Data Extraction:**
        *   If `tofind == RXELEMNOISE` and a line containing "Noise Test." is found:
            *   It skips a few lines to reach the data section.
            *   It then reads subsequent lines, extracting element numbers and noise levels (e.g., `lev55`, `lev85` for single RX, `lev200`, `lev300`, `lev380` for dual RX).
            *   It writes these values to the appropriate output file (`synfile`, `porfile`, or `stbfile`).
        *   If `tofind == RXSPECNOISE` and a line containing "Spectral noise test:" is found:
            *   It skips a few lines to reach the data section.
            *   It then reads subsequent lines, extracting frequency and noise levels (e.g., `lev1`, `lev2`, `aver` for single RX, `lev1`, `lev2`, `lev3`, `lev4`, `aver` for dual RX).
            *   It writes these values to the appropriate output file.
    *   **Dual RX Handling:** If `dualRx2040` is enabled, it detects "Port RX" and "Starboard RX" sections in the BIST report to direct data to the correct output file.
4.  **Helper Function `removebar()`:** This function replaces vertical bar characters (`|`) in a string with spaces, as these might be present in the BIST report formatting and interfere with `sscanf`.
5.  **Cleanup:** Closes all open files.

## Output Files
The output files (`.bist`, `.port`, `.stbd`) are ASCII files. The format depends on the `tofind` option:
*   **`RXELEMNOISE`:** Typically `element_number noise_level1 noise_level2 ...`
*   **`RXSPECNOISE`:** Typically `frequency noise_level1 noise_level2 ...`

## Dependencies
*   `support.h`: For general utility functions.

## Notes
BIST reports provide crucial diagnostic information about the sonar's internal electronics and noise characteristics. This tool helps to extract and organize this data into a usable format for quality control and system performance evaluation. The output ASCII format is compatible with external plotting tools for visual analysis.