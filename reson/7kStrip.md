---
layout: default
title: 7kStrip
parent: Reson Tools
nav_order: 179
---
# 7kStrip

## Description
`7kStrip` is a utility designed to filter (or "strip") specific record types from a Reson 7k (`.s7k`) file. It reads through an input `.s7k` file, and for each record encountered, it decides whether to keep or discard it based on a user-provided list of record IDs to strip. All records that are kept are written to a new output `.s7k` file.

This tool is useful for reducing the size of `.s7k` files by removing unnecessary data (e.g., specific telemetry, unused sensor data) or for preparing specialized `.s7k` files containing only particular data types for specific processing steps.

## Usage
```bash
7kStrip -in <inputfile.s7k> -out <stripped_file.s7k> [-strip <ID>] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-in <inputfile.s7k>` | **Required.** Path to the input Reson 7k `.s7k` file. |
| `-out <stripped_file.s7k>` | **Required.** Path for the output stripped `.s7k` file. If not specified, it defaults to `<inputfile.s7k>.strip`. |
| `-strip <ID>` | **Required (at least one).** Specifies the record `ID` (e.g., `7000` for Sonar Settings, `7006` for Bathymetry) to be *stripped* (removed) from the output file. This option can be used multiple times to strip multiple record types. |
| `-v` | Enable verbose output (prints information about each record being processed). | |

## How It Works

1.  **Initialization:** Parses command-line arguments to get input/output filenames and a list of `ID`s to strip. Initializes `Reson_7K_NF` (Not Found) and `Reson_7K_DRF` (Data Record Format) structures, and an `OMG_Buffer` for reading/writing.
2.  **File Opening:** Opens the input `.s7k` file for reading and the output `.s7k` file for writing.
3.  **Record Processing Loop:** Reads the `.s7k` file record by record:
    *   **Sync Search:** Calls `seek_next_7K_sync()` (an external function) to find the next Reson 7k synchronization pattern.
    *   **DRF Reading:** Reads the `Reson_7K_DRF` to determine the `record_type_id` and `size`.
    *   **Strip Check:** Checks if the `record_type_id` is in the list of IDs to be stripped (`strip_id[drf.record_type_id]`).
    *   **Record Handling:**
        *   If the record is to be stripped: Skips the record's data in the input file.
        *   If the record is to be kept: Seeks back to the start of the record, reads its entire content into `inbuffer`, and writes it to the output file.
    *   Updates counters for records read (`count_in`) and records written (`count_out`).
4.  **Summary Output:** After processing the entire input file, it prints a summary of how many records of each type were processed and kept/stripped.
5.  **Cleanup:** Closes input and output files.

## Output Files
*   `<stripped_file.s7k>`: A new `.s7k` file containing all records from the input file *except* those specified with the `-strip` option.

## Dependencies
*   `Reson_7K_parser.h`: For Reson 7k data structures and `seek_next_7K_sync` function.
*   `support.h`: For general utility functions and error handling.

## Notes
`7kStrip` is a useful tool for data management and preprocessing. By removing unnecessary data, it can reduce file sizes, making data transfer and storage more efficient. It can also create specialized `.s7k` files containing only the data types required for specific processing steps, streamlining workflows. The tool creates a new file, preserving the original `.s7k` file.