---
layout: default
title: new_speedtosalinity
parent: Ray Tools
nav_order: 166
---
# new_speedtosalinity

## Description
`new_speedtosalinity` is a utility that calculates salinity from sound velocity, temperature, and depth (converted to pressure) using empirical equations. It reads a file containing depth, sound velocity, and temperature data, then iterates through possible salinity values to find the best fit for the observed sound velocity using either the Wilson (1962) or Chen-Millero-Li (1977) equations.

This tool is essential for oceanographic applications where direct salinity measurements are unavailable, but sound velocity, temperature, and depth are known. It allows for the reconstruction of salinity profiles for use in various oceanographic models.

## Usage
```bash
new_speedtosalinity -in <infile> -out <outfile> (-wilson | -cml) [-v] [-test]
```

## Arguments

| Option | Description |
|---|---|
| `-in <infile>` | **Required.** Path to the input ASCII file containing `depth`, `sound_velocity`, `temperature` data. |
| `-out <outfile>` | **Required.** Path for the output ASCII file containing `depth`, `sound_velocity`, `temperature`, `salinity` data. |
| `-wilson` | **Required (choose one).** Uses the Wilson (1962) empirical equation to calculate sound velocity. |
| `-cml` | **Required (choose one).** Uses the Chen-Millero-Li (1977) empirical equation to calculate sound velocity. |
| `-v` | Enable verbose output. |
| `-test` | Runs a hardcoded test case for `vchemilli` and exits. |

## Input File Format (ASCII)
The input file (`-in`) is expected to be a comma-separated ASCII file with three columns:
`depth, sound_velocity, temperature`

## Output File Format (ASCII)
The output file (`-out`) will be a comma-separated ASCII file with four columns:
`depth, sound_velocity, temperature, best_guess_salinity`

## How It Works

1.  **Initialization:** Parses command-line arguments to get input/output filenames, select the empirical equation (`-wilson` or `-cml`), and set verbose/test modes.
2.  **File Opening:** Opens the input ASCII file (`-in`) for reading and the output ASCII file (`-out`) for writing.
3.  **Data Processing Loop:** Reads `depth`, `sound_velocity`, and `temperature` from each line of the input file:
    *   **Pressure Calculation:** Converts `depth` to `pressure` (in kg/cm²) by adding atmospheric pressure and accounting for density.
    *   **Salinity Iteration:**
        *   Initializes `salinity` to 0 and `minDiff` to a large value.
        *   Iterates `salinity` from 0 up to `max_salinity` (400, representing 0 to 40.0 ppt in 0.1 ppt increments).
        *   For each `salinity` value, it calculates `temp_velocity` using either `vsw()` (Wilson) or `vchemilli()` (Chen-Millero-Li) function.
        *   Compares `temp_velocity` with the observed `sound_velocity` to find the `best_guess_salinity` that minimizes the absolute difference.
    *   **Output:** Writes `depth`, `sound_velocity`, `temperature`, and `best_guess_salinity` to the output file.
4.  **`vsw(double t, double p, double s)` (Wilson 1962 Equation):**
    *   Calculates sound velocity based on temperature (`t`), pressure (`p`), and salinity (`s`) using Wilson's empirical formula.
5.  **`vchemilli(double t, double p, double s)` (Chen-Millero-Li 1977 Equation):**
    *   Calculates sound velocity based on temperature (`t`), pressure (`p`), and salinity (`s`) using the Chen-Millero-Li empirical formula, which is generally more accurate.
6.  **Cleanup:** Closes input and output files.

## Notes
*   Pressure is in kg/cm², Salinity is in parts per thousand (ppt).
*   The `salinity` iteration increments in 0.1 ppt steps implicitly (by dividing by 10.0 for calculations).
```
```