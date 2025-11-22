---
layout: default
title: 7k2orientation
parent: Reson Tools
nav_order: 178
---
# 7k2orientation

## Description
`7k2orientation` is a utility designed to extract vessel orientation data (roll, pitch, heading, heave) from Reson 7k (`.s7k`) files and convert it into the OMG-HDCS attitude file format. It processes specific 7k records: `7k_1012_Orientation` (roll, pitch, heave), `7k_1013_Heading` (heading), and `7k_1016_Attitude` (roll, pitch, heading, heave time series).

This tool is essential for providing motion and heading data for various downstream processing steps within the OMG toolkit, such as motion compensation and data georeferencing.

## Usage
```bash
7k2orientation -s7k <input_name> -omg <omg_file_prefix> [-v] [-debug]
```

## Arguments

| Option | Description |
|---|---|
| `-s7k <input_name>` | **Required.** Path to the input Reson 7k `.s7k` file. |
| `-omg <omg_file_prefix>` | **Required.** Prefix for the output OMG-HDCS files. The tool will generate:
    *   `<omg_file_prefix>.orientation_1012` (if 7k_1012 records exist): OMG-HDCS attitude file for roll, pitch, heave.
    *   `<omg_file_prefix>.heading` (if 7k_1013 records exist): OMG-HDCS attitude file for heading.
    *   `<omg_file_prefix>.orientation_1016` (if 7k_1016 records exist): OMG-HDCS attitude file for roll, pitch, heading, heave time series. |
| `-v` | Enable verbose output. |
| `-debug` | Enable debug output. |

## How It Works

1.  **Initialization:** Parses command-line arguments to get input `.s7k` filename and output prefix. Initializes Reson 7k data structures (`Reson_7K_Index`, `Reson_7K_DRF`, `Reson_7K_1012_Orientation`, `Reson_7K_1013_Heading`, `Reson_7K_1016_Attitude`) and OMG-HDCS attitude structures (`OMG_HDCS_summary_attitude`, `OMG_HDCS_attitude`).
2.  **7k Indexing:** Calls `build_Reson_7K_Index()` (an external function) to create an index of all packet types within the `.s7k` file.
3.  **File Opening:** Opens the input `.s7k` file for reading.
4.  **Process 7k_1012_Orientation Records (Roll, Pitch, Heave):**
    *   If `7k_1012_Orientation` records are found in the index:
        *   Creates an output file named `<omg_file_prefix>.orientation_1012`.
        *   Initializes `OMG_HDCS_summary_attitude` for this file.
        *   Reads the first 7k_1012 record to determine `refTime` for the summary.
        *   Writes the summary to the output file.
        *   Iterates through each 7k_1012 record:
            *   Seeks to the record's file offset, reads DRF and `Reson_7K_1012_Orientation` data.
            *   Calls `convert_7K_orientation()` (an external function) to convert 7k orientation data to `OMG_HDCS_attitude`.
            *   Writes the `OMG_HDCS_attitude` record to the output file.
5.  **Process 7k_1013_Heading Records (Heading):**
    *   If `7k_1013_Heading` records are found in the index:
        *   Creates an output file named `<omg_file_prefix>.heading`.
        *   Initializes `OMG_HDCS_summary_attitude` for this file.
        *   Reads the first 7k_1013 record to determine `refTime` for the summary.
        *   Writes the summary to the output file.
        *   Iterates through each 7k_1013 record:
            *   Seeks to the record's file offset, reads DRF and `Reson_7K_1013_Heading` data.
            *   Calls `convert_7K_heading()` (an external function) to convert 7k heading data to `OMG_HDCS_attitude`.
            *   Writes the `OMG_HDCS_attitude` record to the output file.
6.  **Process 7k_1016_Attitude Records (Roll, Pitch, Heading, Heave time series):**
    *   If `7k_1016_Attitude` records are found in the index:
        *   Creates an output file named `<omg_file_prefix>.orientation_1016`.
        *   Initializes `OMG_HDCS_summary_attitude` for this file.
        *   Reads the first 7k_1016 record to determine `refTime` for the summary.
        *   Writes the summary to the output file.
        *   Iterates through each 7k_1016 record:
            *   Reads DRF and `Reson_7K_1016_Attitude` data.
            *   For each sample within the `7k_1016_Attitude` record (which can contain multiple samples per record):
                *   Calls `convert_7K_attitude()` (an external function) to convert 7k attitude sample data to `OMG_HDCS_attitude`.
                *   Writes the `OMG_HDCS_attitude` record to the output file.
7.  **Cleanup:** Closes all open files.

## Output Files
*   `<omg_file_prefix>.orientation_1012`: Binary attitude file (roll, pitch, heave) if `7k_1012` records exist.
*   `<omg_file_prefix>.heading`: Binary attitude file (heading) if `7k_1013` records exist.
*   `<omg_file_prefix>.orientation_1016`: Binary attitude file (roll, pitch, heading, heave time series) if `7k_1016` records exist.
```
```