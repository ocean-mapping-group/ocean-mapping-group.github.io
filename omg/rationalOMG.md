---
layout: default
title: rationalOMG
parent: OMG Tools
nav_order: 50
---
# rationalOMG

## Description
`rationalOMG` is an interactive command-line utility for exploring the contents of an OMG-HDCS merged data file in a "rationalized" format. It allows users to view summary information, and then interactively query specific profile (ping) records and their associated beam data. It can also display raw sidescan traces if available.

The "rationalized" format means that the data is presented in a more human-readable and processed form, as opposed to the raw binary storage format.

## Usage
```bash
rationalOMG <OMG_HDCS_datafile> <ASCII_listing> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile>` | **Required.** The path to the input OMG-HDCS merged data file. |
| `<ASCII_listing>` | **Required.** The path to the ASCII output file where information will be written. |
| `-coeffs` | (Not implemented in the provided code) This option is present in the `USAGE` string but its functionality is not seen in the `main` function. It might be intended to display coefficients. |
| `-tidecor` | Enables the use of tide correction (sets `use_tide_corr_flag`). |
| `-traces` | Enables the retrieval and display of raw sidescan traces associated with each beam. This requires a `.ss_data` file alongside the merged file. |
| `-v` | Enable verbose output (not explicitly used in `main` for display, but often a general verbose flag). |

## How It Works
1.  **File Opening:** Opens the specified OMG-HDCS merged data file and an ASCII output file. If `-traces` is enabled, it also attempts to open an associated `.ss_data` file.
2.  **Summary Display:** Reads and prints a "rationalized" summary of the merged file, including the number of profiles and the geographic extents (min/max latitude/longitude).
3.  **Interactive Profile Query:** Enters an infinite loop, prompting the user to "give profile no#":
    *   The user enters a profile number.
    *   The tool reads the "rationalized" profile header for that profile number, including ping latitude/longitude, heading, tide, and sample rate, and prints it to the console.
    *   It then retrieves the "rationalized" beam data for all beams within that profile.
    *   For each beam, it prints detailed information including status, position (latitude/longitude), depth, across-track, TWTT (Two-Way Travel Time), beam angle, and beam azimuth.
    *   If `-traces` is enabled, it also prints the number of samples, center number, and then the raw 8-bit sidescan data values for each sample in the beam.
    *   After displaying the information for the requested profile, it loops back to prompt for another profile number.

## Rationalized Data
The "rationalized" data means that the values are converted from their internal storage format (e.g., scaled integers) into standard engineering units (e.g., degrees, meters, seconds) and are directly related to physical measurements. This makes the output easier to interpret for analysis and debugging.
