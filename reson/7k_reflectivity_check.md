---
layout: default
title: 7k_reflectivity_check
parent: Reson Tools
nav_order: 174
---
# 7k_reflectivity_check

## Description
`7k_reflectivity_check` is a utility designed to extract and compare reflectivity (intensity) data from different Reson 7k data records. It reads a Reson 7k (`.s7k`) file, processes `7k_7000_Sonar_Settings`, `7k_7006_Bathymetry`, `7k_7007_Backscatter`, and `7k_7008_Generic_Data` (snippets) records, and then outputs selected intensity values for each beam.

The primary purpose of this tool is for quality control and detailed analysis of backscatter data, allowing users to assess the consistency of intensity measurements from different sources within the 7k data stream.

## Usage
```bash
7k_reflectivity_check -s7k <input_name> [-v] [-debug]
```

## Arguments

| Option | Description |
|---|---|
| `-s7k <input_name>` | **Required.** Path to the input Reson 7k `.s7k` file. |
| `-v` | Enable verbose output (prints DRF information). |
| `-debug` | Enable debug output (currently unused). |

## Output Files
*   `intensity.dat`: ASCII file containing bathymetry-derived intensity values for each beam.
*   `snippet.dat`: ASCII file containing a specific snippet sample (sample 74) for each beam.
*   `snippet_max.dat`: ASCII file containing the maximum snippet amplitude for each beam.
*   `snippet_min.dat`: ASCII file containing the minimum snippet amplitude for each beam.

## How It Works

1.  **Initialization:** Parses command-line arguments, sets the input `.s7k` filename, and initializes Reson 7k data structures (`Reson_7K_DRF`, `Reson_7K_7000_Sonar_Settings`, `Reson_7K_7006_Bathymetry`, `Reson_7K_7007_Backscatter`, `Reson_7K_7008_Generic_Data`).
2.  **File Opening:** Opens the input `.s7k` file for reading and creates four output ASCII files: `intensity.dat`, `snippet.dat`, `snippet_max.dat`, and `snippet_min.dat`.
3.  **Record Processing Loop:** Reads the `.s7k` file record by record:
    *   **Sync Search:** Calls `seek_next_7K_sync()` to find the next Reson 7k synchronization pattern.
    *   **DRF Reading:** Reads the `Reson_7K_DRF` (Data Record Format) to determine the record type and size.
    *   **Record Parsing:** Uses a `switch` statement to call the appropriate `read_Reson_7K_*()` function (`read_Reson_7K_7000_Sonar_Settings`, `read_Reson_7K_7006_Bathymetry`, `read_Reson_7K_7007_Backscatter`, `read_Reson_7K_7008_Generic_Data`) based on the `record_type_id`.
    *   **Ping Matching and Corruption Check:** It skips records if the `ping_number` does not match across all relevant record types (Sonar Settings, Bathymetry, Backscatter, Snippets) or if any record is marked as corrupt.
    *   **Data Extraction and Output:** If a consistent set of records for a ping is found:
        *   For each beam in the `bathymetry` record:
            *   Writes `bathymetry.beams[beam].intensity` to `intensity.dat`.
            *   Writes `snippets.records[beam].magnitude_16[74]` (a fixed sample index) to `snippet.dat`.
            *   Finds the `max` and `min` amplitude within the first 150 samples of the snippet record and writes them to `snippet_max.dat` and `snippet_min.dat`, respectively.
4.  **Cleanup:** Closes all open files.

## Output
*   Four ASCII files (`intensity.dat`, `snippet.dat`, `snippet_max.dat`, `snippet_min.dat`) containing extracted reflectivity values.
```
```