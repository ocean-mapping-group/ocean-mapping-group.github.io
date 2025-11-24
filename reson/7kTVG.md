---
layout: default
title: 7kTVG
parent: Reson Tools
nav_order: 181
---
# 7kTVG

## Description
`7kTVG` is a utility designed to extract and process Time Varied Gain (TVG) data from Reson 7k (`.s7k`) files. It reads all `7k_7010_TVG` records from an `.s7k` file, aggregates the TVG gain values for each ping, and then outputs them as a 2D floating-point array (JHC `.r4` format). The output array represents ping number versus sample index, with each cell containing the TVG gain value.

This tool is useful for analyzing the TVG curves applied by the sonar, which is important for understanding backscatter measurements and for calibrating side-scan sonar data.

## Usage
```bash
7kTVG -in <inputfile.s7k> -out <outputfile.r4> [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-in <inputfile.s7k>` | **Required.** Path to the input Reson 7k `.s7k` file. |
| `-out <outputfile.r4>` | **Required.** Path for the output JHC `.r4` file containing the TVG array. |
| `-v` | Enable verbose output. | |

## How It Works

1.  **Initialization:** Parses command-line arguments to get input/output filenames. Initializes `Reson_7K_NF`, `Reson_7K_DRF`, and `Reson_7K_7010_TVG` structures.
2.  **File Opening:** Opens the input `.s7k` file for reading and the output `.r4` file for writing.
3.  **First Pass (Metadata Collection):**
    *   Reads through the entire input `.s7k` file once.
    *   Identifies all `7k_7010_TVG` records.
    *   Determines `max_num_samples` (the maximum number of samples found in any TVG record) and `num_pings` (total number of TVG records).
4.  **Buffer Allocation:** Allocates a 1D floating-point array `outbuffer` of size `max_num_samples * num_pings` to store all TVG gain values.
5.  **Second Pass (Data Extraction and Aggregation):**
    *   Resets the file pointer of the input `.s7k` file to the beginning.
    *   Reads through the input `.s7k` file a second time.
    *   For each `7k_7010_TVG` record:
        *   Copies the `tvg_gain` array from the `tvg` structure into the `outbuffer` at the appropriate offset (`this_ping * max_num_samples`).
    *   Increments `this_ping`.
6.  **Output to JHC `.r4` File:**
    *   Calls `writeJHC()` (an external function) to write a JHC header to the output `.r4` file. The header will reflect the dimensions of the TVG array (`max_num_samples` as `dx`, `num_pings` as `dy`, and data type as `JB_FLOAT`).
    *   Writes the aggregated `outbuffer` data to the `.r4` file.
7.  **Cleanup:** Frees allocated memory and closes all files.

## Output Files
*   `<outputfile.r4>`: A JHC `.r4` file (binary float array) where rows represent pings and columns represent sample indices, with each cell containing the TVG gain value.

## Dependencies
*   `Reson_7K_parser.h`: For Reson 7k data structures and parsing functions.
*   `array.h`: For `JHC_header` structure and `writeJHC` function.
*   `support.h`: For general utility functions and error handling.

## Notes
TVG curves are fundamental for correcting range-dependent intensity variations in sonar data. This tool provides a way to extract and visualize the TVG applied by the Reson 7k sonar, which is crucial for understanding backscatter measurements and for calibrating side-scan sonar data derived from multibeam systems. The output `.r4` format allows for easy integration with other gridded data.