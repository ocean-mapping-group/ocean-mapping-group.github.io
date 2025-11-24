---
layout: default
title: LPFbeams
parent: OMG Tools
nav_order: 36
---
# LPFbeams

## Description
`LPFbeams` is a command-line utility that applies a low-pass filter to the `observedDepth` values of selected beams within an OMG-HDCS merged file. Its primary purpose is to remove high-frequency noise or motion artifacts from the depth measurements, resulting in a smoother bathymetry.

The tool operates on a user-defined range of pings and beams, calculating a weighted average of depths within a specified window. The input merged file is modified in place.

## Usage
```bash
LPFbeams <merged_file> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `<merged_file>` | **Required.** The path to the OMG-HDCS merged file to be processed. This file is modified in place. | `survey_data.merged` |
| `-window <odd_num>` | Specifies the size of the filter window (in number of pings). It must be an odd number. | `11` |
| `-beams <first_beam> <last_beam>` | Specifies the range of beam numbers (inclusive, 0-indexed) to apply the filter to. | `0 59` |
| `-first <ping_num>` | Specifies the starting ping number (inclusive) to process. | `0` |
| `-last <ping_num>` | Specifies the ending ping number (inclusive) to process. | End of file |
| `-cos_square` | Uses a cosine-squared function to calculate the filter weights. By default, a simple cosine function is used. | (Cosine is default) |
| `-out <filename>` | Creates an ASCII file at the specified path, dumping the original and filtered depths for inspection. | `filtered_depths.ascii` |
| `-v` | Enable verbose output. | |

## How It Works
1.  **File Opening:** Opens the input merged file for reading and writing.
2.  **Summary Header Reading:** Reads the summary header to get `numProfiles` and `numDepths`.
3.  **Data Extraction:**
    *   Allocates memory for a 2D array (`depth_array`) to store `observedDepth` values for the specified ping and beam ranges.
    *   Reads `observedDepth` for the relevant beams and pings into `depth_array`.
4.  **Filter Application:**
    *   Iterates through each beam within the specified range.
    *   For each ping (`i`) within the processing range:
        *   Calculates a weighted average of `observedDepth` values from surrounding pings within the defined `window`.
        *   Weights are determined by either a cosine function (default) or a cosine-squared function (`-cos_square`), giving more importance to central samples.
        *   The calculated smoothed depth replaces the original `observedDepth` in the `depth_array`.
5.  **In-Place Update:** The modified `depth_array` is written back to the merged file, updating the `observedDepth` fields of the beams.
6.  **Output Dump (`-out`):** If specified, an ASCII file is created containing the original and filtered depths for diagnostic purposes.

## Output Files
*   The input merged file is modified in-place.
*   `<filename>`: An ASCII file with original and filtered depths (if `-out` is used).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `math.h`: For mathematical functions.

## Notes
Low-pass filtering is a common technique for noise reduction in bathymetric data. This tool provides a flexible way to apply such filters, with options for window size and weighting functions. The ability to filter specific beams or ping ranges allows for targeted noise removal. The tool modifies merged files in place, so backups are recommended before processing.