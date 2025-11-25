---
layout: default
title: readGenericADCP
parent: ADCP Tools
nav_order: 13
---

# readGenericADCP

## Description
`readGenericADCP` is a command-line utility designed to process a generic, pre-processed ADCP (Acoustic Doppler Current Profiler) dataset. Its primary function is to calculate a single depth-averaged current vector for each ADCP ensemble (ping) within a specified depth range.

The tool requires input data to be in a specific format: a JHC-formatted navigation file (`.nav`) accompanied by three JHC-formatted float-array files (`.r4`) that represent the vertical profiles of North, East, and Downward velocity components. The output is a new JHC navigation file where the velocity and azimuth fields are populated with the calculated depth-averaged current.

## Usage
```bash
readGenericADCP -out <outfile> -in <infile(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-out <outfile>` | **Required.** The name of the output file, which will contain the depth-averaged current vectors in JHC `.nav` format. |
| `-in <infile(s)>`| **Required.** One or more input navigation files (e.g., `survey1.dec3.nav`). The tool automatically searches for the corresponding `.N.r4`, `.E.r4`, and `.D.r4` files based on the input filename. |
| `-mindepth <meters>` | The minimum depth for the averaging window. Bins shallower than this depth will be excluded from the average. Default is `0`. |
| `-maxdepth <meters>`| The maximum depth for the averaging window. Bins deeper than this depth will be excluded. Default is `100`. |
| `-time_start <Y J H M S>`| Defines the start time for processing data (Year, Julian Day, Hour, Minute, Second). |
| `-time_end <Y J H M S>`| Defines the end time for processing data. |
| `-v` | Enable verbose output. |

## How It Works

1.  **File Handling:** For each input `.nav` file specified with `-in`, the tool constructs the filenames for the corresponding North, East, and Downward velocity component files (e.g., `survey1.dec3.N.r4`).
2.  **Data Reading:** It iterates through each record (ensemble) in the input files. For each record, it reads the navigation information from the `.nav` file and the corresponding vertical velocity profiles from the `.N.r4`, `.E.r4`, and `.D.r4` files.
3.  **Time Filtering:** If time bounds are set, it processes only the ensembles that fall within the specified start and end times.
4.  **Depth Averaging:** For each ensemble, it iterates through the depth bins of the velocity profiles. If a bin's depth is within the range defined by `-mindepth` and `-maxdepth`, its N, E, and D velocity values are added to a running sum.
5.  **Vector Calculation:** After processing all valid bins for an ensemble, it calculates the average North, East, and Downward velocities. From these averaged components, it computes the final magnitude and azimuth of the depth-averaged current vector.
6.  **Output:** A new navigation record is created where the original `velocity` and `azi` fields are replaced with the calculated depth-averaged magnitude and azimuth. This new record is written to the specified output file. This is repeated for every input ensemble, creating a new time-series of depth-averaged currents.

## Input File Requirements

This tool requires a specific set of input files for each dataset:
*   A JHC navigation file (e.g., `survey1.dec3.nav`).
*   Three corresponding JHC float-array files (`.r4`) with identical dimensions, containing the binned velocity data:
    *   `survey1.dec3.N.r4` (North velocity)
    *   `survey1.dec3.E.r4` (East velocity)
    *   `survey1.dec3.D.r4` (Downward velocity)