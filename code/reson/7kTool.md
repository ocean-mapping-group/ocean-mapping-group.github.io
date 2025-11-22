---
layout: default
title: 7kTool
parent: Reson Tools
nav_order: 180
---
# 7kTool

## Description
`7kTool` is a diagnostic utility for Reson 7k (`.s7k`) files. Its primary function is to parse an `.s7k` file, identify all data records within it, and print a summary of their types, counts, and sizes. Optionally, it can provide verbose dumps of specific record types and perform timing checks.

This tool is invaluable for inspecting the contents and structure of `.s7k` files, debugging issues, and understanding the types and quantity of data stored within them. It supports a wide range of Reson 7k record types.

## Usage
```bash
7kTool -in <inputfile.s7k> [-v] [-vid <ID>] [-build_index] [-check_timing]
```

## Arguments

| Option | Description |
|---|---|
| `-in <inputfile.s7k>` | **Required.** Path to the input Reson 7k `.s7k` file. |
| `-v` | Enable general verbose output (e.g., DRF information). |
| `-vid <ID>` | Verbose output for specific record `ID` (e.g., `7000` for Sonar Settings, `1003` for Position). Can be used multiple times. |
| `-build_index` | Builds and prints a summary of the Reson 7k index. |
| `-check_timing` | Performs timing checks on specific record types (e.g., 1012 Orientation, 7027 Bathymetry). |

## How It Works

1.  **Initialization:** Parses command-line arguments to get the input `.s7k` filename and various verbose/check flags. Initializes numerous Reson 7k data structures for all supported record types.
2.  **File Opening:** Opens the input `.s7k` file for reading.
3.  **Index Building (`-build_index`):** If `build_index` is set, it calls `build_Reson_7K_Index()` (an external function) to create an in-memory index of all data records within the `.s7k` file. This index provides quick access to records by type and sequence.
4.  **Record Processing Loop:** Reads the `.s7k` file record by record:
    *   **Sync Search:** Calls `seek_next_7K_sync()` (an external function) to find the next Reson 7k synchronization pattern.
    *   **DRF Reading:** Reads the `Reson_7K_DRF` to determine the `record_type_id`, `size`, and timestamp.
    *   Updates internal counters (`count`, `sizes`) for each record type.
    *   **Verbose Dump (`-vid`):** If a `verbose_id[drf.record_type_id]` flag is set, it calls the appropriate `read_Reson_7K_*()` function and `print_Reson_7K_*()` function to dump the full content of that record type to standard output.
    *   **Timing Check (`-check_timing`):** If `check_timing` is set, it performs specific checks, like printing roll values for `1012_Orientation` records or beam angles for `7027_Bathymetry` records, along with their timestamps.
    *   If no specific verbose flags are set (`just_count` is true), it simply skips the data portion of the record to quickly count record types and sizes.
5.  **Summary Output:** After processing the entire input file, it prints a final summary table to standard output, showing:
    *   Record `ID`
    *   Record Name (e.g., `7000_Sonar_Settings`)
    *   Total count of records of that type
    *   Count of corrupt records of that type
    *   Total size (bytes) of data for that type
6.  **Cleanup:** Frees allocated memory and closes the input file.

## Output
*   A summary table of Reson 7k record types, counts, and sizes printed to standard output.
*   Optional verbose dumps of specified record types.
*   Optional timing checks for specific records.
```
```