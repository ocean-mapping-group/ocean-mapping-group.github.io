---
layout: default
title: binPPK
parent: Optech Tools
nav_order: 110
---
# binPPK

## Description
`binPPK` is a utility designed to convert ASCII PPK (Post-Processed Kinematic) data, typically exported from software like TGO (Trimble Geomatics Office), into a custom binary format. This binarization streamlines the data for subsequent processing, such as merging with other datasets using tools like `merge_PPK`.

The tool reads date, time, latitude, longitude, and height from an ASCII input file and writes it to a binary file, performing byte-swapping for portability.

## Usage
```bash
binPPK <asciiPPKfile> <binaryPPKfile> [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<asciiPPKfile>` | **Required.** The path to the input ASCII PPK data file. |
| `<binaryPPKfile>` | **Required.** The path for the output binary PPK file. |
| `-v` | Enable verbose output. |

## How It Works
1.  **File Opening:** Opens the input ASCII file for reading and the output binary file for writing (`wb+`).
2.  **Data Structure:** Defines a `PPK_structure` to hold time (Unix timestamp), latitude, longitude, and height.
3.  **Line-by-Line Processing:** Iterates through each line of the ASCII input file:
    *   **Parsing:** Reads `hour`, `min`, `sec`, `day`, `mon`, `year`, `lat`, `lon`, and `height` from the current line using `fscanf`.
    *   **Timestamp Conversion:** Converts the date and time components into a Unix timestamp (seconds since 1970) using `stdtime_from_dmy`.
    *   **Data Validation:** Performs basic checks:
        *   If the absolute time difference between the current and previous record is greater than 20 seconds, it prints a warning.
        *   If the absolute height difference is greater than 1.0, it prints a warning.
        *   **Note:** These checks are for warnings only and do not stop processing the record.
    *   **Binary Writing (`ppk_write`):** If the data is deemed acceptable (not strictly filtered by the warnings), it writes the `PPK_structure` data to the binary output file at an offset determined by `recordnum * PPK_RECLEN`. The `ppk_write` function uses `put_swapped_int` and `put_swapped_float` to handle byte-swapping, ensuring platform compatibility.
4.  **Cleanup:** Closes both input and output files.

## Helper Functions
*   `interp_ppk()`: (Currently commented out in `main` but present) This function is designed to interpolate height values between two PPK records over a time gap, if a significant time gap and height difference exist.
*   `ppk_write()`: Writes a `PPK_structure` to the binary file at a specified record number, handling byte-swapping.
*   `show_date_calc()`: A debugging function to display date conversions.
```