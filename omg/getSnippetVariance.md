---
layout: default
title: getSnippetVariance
parent: OMG Tools
nav_order: 108
---
# getSnippetVariance

## Description
`getSnippetVariance` is a utility designed to analyze the variance of backscatter snippet data from multibeam sonars, primarily focusing on Reson systems. It processes merged files, extracts snippet intensities, and calculates the mean and standard deviation of these intensities after applying a calibration.

The tool uses a Digital Terrain Model (DTM) to estimate grazing angles and calculate ensonified areas, which are crucial inputs for the `calibrate_reson` function. It outputs the mean and standard deviation for each beam.

## Usage
```bash
getSnippetVariance <filename.merged> -dtm <dtm.r4> [-debug]
```

## Arguments

| Option | Description |
|---|---|
| `<filename.merged>` | **Required.** The path to the input OMG-HDCS merged file (with associated `.ss_data` file). |
| `-dtm <dtm.r4>` | **Required.** Path to the DTM file in `.r4` (float grid) format. |
| `-debug` | Enable debug output. |

## How It Works
1.  **Initialization:** Initializes sum, sum_squares, and count arrays for statistical accumulation per beam. Sets debugging flags.
2.  **DTM Loading:** Opens the DTM file (`-dtm`), reads its header, and loads the DTM data into memory.
3.  **File Opening:** Opens the input merged file and its corresponding `.ss_data` file.
4.  **Summary Header Reading:** Reads the summary header and loads sonar parameters from the `.param` file.
5.  **Profile Iteration:** Loops through each profile (ping) in the merged file:
    *   Reads the current `profile` header and raw `beams`.
    *   **Grazing Angle and Ensonified Area Calculation:** Calls `get_dtm_grazing_angles` (to estimate grazing angles using the DTM) and `calc_ensonified_area` (to calculate ensonified areas). These are crucial for the backscatter calibration.
    *   **Snippet Calibration:** For each beam with valid data:
        *   Seeks to the beam's snippet data in the `.ss_data` file and reads `IScans` (raw snippet intensities).
        *   Calls `calibrate_reson` (an external function, likely from `Echo_calib.h`) to apply calibration to these `IScans`, producing `Scans` (calibrated snippet intensities). This function uses grazing angles, ensonified areas, and profile/beam data.
        *   Extracts the calibrated snippet intensity at the `beams[j].centre_no` (the central sample of the snippet).
        *   Accumulates the squared value of this snippet intensity in `sum_squares[j]` and the raw value in `sum[j]`, incrementing `count[j]`.
6.  **Statistical Output:** After processing all pings:
    *   For each beam, if `count[i]` is greater than 1, it calculates the `mean` and `std_dev` (standard deviation) of the snippet intensities using the accumulated `sum`, `sum_squares`, and `count` values.
    *   Prints `beam_index`, `mean`, and `std_dev` to standard output.
7.  **Cleanup:** Closes all open files and frees allocated memory.

## Output Files
The tool prints a three-column ASCII listing to standard output:
*   `beam_index`
*   `mean` of calibrated snippet intensity
*   `std_dev` of calibrated snippet intensity

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure and DTM data handling.
*   `support.h`: For general utility functions and error handling.
*   `grazing_angle.h`: For `get_dtm_grazing_angles` function.
*   `ensonification.h`: For `calc_ensonified_area` function.
*   `Echo_calib.h`: For `calibrate_reson` function.

## Notes
Analyzing snippet variance provides insight into the homogeneity of the seabed and the quality of the backscatter measurements. High variance might indicate a heterogeneous seafloor, noise, or an ineffective calibration. This tool is useful for quality control and seabed characterization, particularly for Reson multibeam systems. The calibration step uses a DTM to ensure accurate grazing angles and ensonified areas, which are critical for meaningful backscatter values.