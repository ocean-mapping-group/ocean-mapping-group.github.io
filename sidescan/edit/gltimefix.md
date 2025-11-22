---
layout: default
title: gltimefix
parent: Edit Tools
grand_parent: sidescan
nav_order: 2
---
# gltimefix

## Description
`gltimefix` is a utility designed to address time-related issues within JCU GLORIA record files. Its primary function is to constrain the Julian day of records to a specified range and to correct records where the year is not `1970`, which can be a base year for time calculations in some systems.

## Usage
```bash
gltimefix <filename>
```

## Arguments

| Option | Description |
|---|---|
| `<filename>` | **Required.** The path to the JCU GLORIA file to be time-fixed. |

## How It Works
1.  **File Opening:** The tool opens the specified GLORIA file in read-write mode.
2.  **File Length Determination:** It determines the total number of records in the file.
3.  **Record-by-Record Processing:** The tool iterates through each record in the GLORIA file:
    *   It reads each record into `glo_rec`.
    *   It calls the `constrain_day` function to perform time validation and correction.
    *   If `constrain_day` indicates a change was made, the modified `glo_rec` is written back to the file.
4.  **`constrain_day` Function:**
    *   This function takes `min` and `max` Julian day values (hardcoded as 311 and 312 in the provided source).
    *   It converts the `glo_rec.header.time` (Unix timestamp) to a `struct tm` using `gmtime`.
    *   **Julian Day Constraint:** If the record's Julian day (`tm1->tm_yday + 1`) falls outside the `min` and `max` range, it adjusts `tm1->tm_yday` to `last_day - 1` (where `last_day` is dynamically updated from valid records) and sets a `bad_day` flag.
    *   **Year Correction:** If the record's year (`tm1->tm_year`) is not `1970`, it sets a `bad_year` flag.
    *   **Apply Corrections:** If either `bad_day` or `bad_year` is set:
        *   It reconstructs the `glo_rec.header.time` using `stdtime_from_jul_day`, forcing the year to 1970 and using the potentially corrected Julian day.
        *   It returns `1` to indicate a modification was made.
    *   If no issues are found, it updates `last_day` and returns `0`.
5.  **Output:** Corrected records are written back to the input GLORIA file.
