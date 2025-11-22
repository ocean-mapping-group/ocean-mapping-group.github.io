---
layout: default
title: splitOMG
parent: OMG Tools
nav_order: 67
---
# splitOMG

## Description
`splitOMG` is a utility designed to extract a subset of profiles (pings) from an OMG-HDCS merged file into a new merged file. It can split files based on either a numerical range of profiles or a time-based range.

Additionally, it has a specialized mode (`-into_natural_lines`) to analyze the vessel's speed and change in heading between pings, which can be used to identify natural line breaks in survey data.

## Usage
```bash
splitOMG <OMG_HDCS_infile> <OMG_HDCS_outfile> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_infile>` | **Required.** The path to the input OMG-HDCS merged file. |
| `<OMG_HDCS_outfile>` | **Required.** The path for the new output OMG-HDCS merged file containing the subset of data. |

### Splitting Options (Choose one)
| Option | Description |
|---|---|
| `-first <ping_num>` / `-last <ping_num>` | Specifies the starting and ending ping numbers (inclusive) for the subset. |
| `-time_start <year> <jday> <hr> <min> <sec>` / `-time_end <year> <jday> <hr> <min> <sec>` | Specifies a date and time range for the subset. The tool will find the corresponding ping numbers. |

### Analysis Option
| Option | Description |
|---|---|
| `-into_natural_lines` | Instead of splitting, this mode calculates and outputs the vessel's speed (in knots) and change in heading (in degrees) between consecutive pings. The output is an ASCII file (`<OMG_HDCS_outfile>`) with ping number, speed, and dhead. This option overrides the splitting functionality. |

### Other Options
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-minknots` | (Present in `USAGE` but not implemented) Likely intended to filter based on minimum speed. |
| `-minturn` | (Present in `USAGE` but not implemented) Likely intended to filter based on minimum turn. |

## How It Works
1.  **Input Reading:** Opens the input merged file and reads its summary header.
2.  **`into_natural_lines` Mode:**
    *   If `-into_natural_lines` is specified, the tool allocates memory for `speed_knots` and `dhead` arrays.
    *   It iterates through each ping (from 1 to `numProfiles - 1`):
        *   It reads the current and previous profile headers.
        *   It locates the transducer position for both pings.
        *   Calculates the geographic distance and time difference between the two ping positions.
        *   Computes the vessel's speed in knots (`speed_knots`) and the change in heading (`dhead`) between the pings.
    *   It then writes these calculated speed and heading change values (ping number, speed_knots, dhead) to the specified `OMG_HDCS_outfile` as an ASCII listing.
3.  **Splitting Mode (Default):**
    *   If `into_natural_lines` is *not* specified, the tool determines the `first` and `last` ping numbers for the subset. This can be directly from `-first`/`-last` options or by performing a time-based search using `OMG_HDCS_time_search` if `-time_start`/`-time_end` are provided.
    *   It performs error checks to ensure the `first` and `last` ping numbers are valid.
    *   A new output merged file (`OMG_HDCS_outfile`) is created.
    *   The summary header from the input file is modified to reflect the new `numProfiles` (i.e., `last - first`) and then written to the output file.
    *   It then iterates from `first` to `last - 1` in the input file:
        *   Reads the profile header and raw beams for the current ping.
        *   Writes these profile and beam data to the new output merged file.
4.  **Cleanup:** Closes all open files.
