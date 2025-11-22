---
layout: default
title: mergeAltitude
parent: Optech Tools
nav_order: 116
---
# mergeAltitude

## Description
`mergeAltitude` is a utility designed to merge external ASCII altitude data (e.g., from an aerial survey or kinematic GPS) into OMG-HDCS merged files, specifically linking altitude measurements to the geographic positions of individual multibeam soundings.

The tool interpolates altitude values from the ASCII altitude file to match the timestamp of each beam's bottom strike in the merged file and outputs these merged geographic and altitude data to an ASCII file.

## Usage
```bash
mergeAltitude -in <merged_file(s)> -alt <altitude_file.ascii(s)> -out <ASCII_filename> [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-in <merged_file(s)>` | **Required.** One or more paths to input OMG-HDCS merged files. |
| `-alt <altitude_file.ascii(s)>` | **Required.** One or more paths to ASCII altitude files. Each file is expected to contain two columns: timestamp (double) and altitude (double). |
| `-out <ASCII_filename>` | **Required.** The path for the output ASCII file, which will contain merged geographic (lat/lon) and altitude data. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Initializes global variables, including `verbose_flag`, file handles, and counters.
2.  **Argument Parsing:** Parses command-line arguments to get input merged filenames, altitude filenames, and the output filename.
3.  **Altitude Data Reading:**
    *   Iterates through each specified ASCII altitude file (`-alt`).
    *   Reads `timestamp` and `altitude` values from each line and stores them into a 2D array `alt[2][...]`.
    *   Calculates the mean altitude (`mean_alt`) from all altitude data.
4.  **Merged File Processing:** Loops through each input merged file (`-in`):
    *   Opens the merged file for reading (`r+`).
    *   Reads the summary header.
    *   **Profile and Beam Iteration:** Loops through each profile (ping) in the merged file, and then through each beam within that profile:
        *   Reads the current profile header and raw beams.
        *   If `beams[k].observedDepth` is valid:
            *   **Timestamp Calculation:** Calculates a precise timestamp (`pasted`) for the current beam's bottom strike using `profile.laser_timestampRef` and `beams[k].timestampOffset`.
            *   **Geographic Positioning:** Locates the beam's geographic position (`lat`, `lon`) using `locate_beam`.
            *   **Altitude Interpolation/Lookup:** Iterates through the loaded altitude data (`alt` array) to find the two altitude records that bracket `pasted`.
            *   **Output to ASCII:** If bracketing altitude records are found, it prints the `lat`, `lon`, and interpolated/closest `altitude` (`alt[1][n]`) to the output ASCII file.
5.  **Cleanup:** Closes all open files.

## Output Format
The output ASCII file (`-out`) will contain three columns: `latitude`, `longitude`, and `altitude`, for each beam with a valid altitude lookup.
```
```
```