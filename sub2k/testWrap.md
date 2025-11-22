---
layout: default
title: testWrap
parent: SUB2K Tools
grand_parent: code
nav_order: 8
---
# testWrap

## Description
`testWrap` is a utility designed to test and visualize phase wrap-around effects, typically encountered in multibeam sonar phase-difference bathymetry systems. It simulates phase differences based on a user-defined seafloor depth, transducer mount angle, and three different transducer spacings. The program then calculates various phase metrics (individual phase, differential phase, fractional parts) and writes them to an output file named "wraps" in a format suitable for plotting, allowing for analysis of phase ambiguity and wrap-around behavior.

## Usage
```bash
testWrap [-v] [-xplot] [-depth <value>]
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output (though not explicitly used in `main` or helper functions). |
| `-xplot` | If specified, the output format is simplified, printing only `dphas1` and `dphas2` for each step, suitable for X-Y plotting. |
| `-depth <value>` | Specifies the simulated seafloor depth (in units of `drange`, where `drange = 0.01`). | (Not explicitly used in the main loop for depth calculation, `depth` is internally set from `drange`) |

## How It Works
1.  **Input Spacings:** The program interactively prompts the user to enter three transducer spacings (`spac1`, `spac2`, `spac3`).
2.  **Output File Setup:** It opens a file named "wraps" for writing output. The header of this file is formatted based on whether `-xplot` is enabled, defining plot dimensions and ranges for a plotting tool.
3.  **Simulation Loop:** The tool iterates `i` from 0 to 4999, which represents a simulated slant range.
4.  **Angle Calculation:** For each `slant_range`:
    *   If `slant_range` is greater than the simulated `depth`, it calculates the `angle` (grazing angle) using `acos(depth / slant_range)`.
    *   This `angle` is then adjusted by `mount_angle` (hardcoded to 60.0 degrees) to simulate the transducer's physical mounting.
5.  **Phase Calculation:**
    *   For each of the three `spacings`, it calculates `phas1`, `phas2`, `phas3` using `calc_dphase(angle, spacing)`. The `calc_dphase` function (presumably from `j_SUB2K.h`) calculates the phase difference based on angle and spacing.
    *   The fractional parts of these phases (`dphas1`, `dphas2`, `dphas3`) are then extracted using `get_fraction`.
    *   A differential phase `ddp1_2` is calculated between `dphas1` and `dphas2` using `diff_pair`.
6.  **Output:**
    *   If `-xplot` is *not* specified, it prints the `angle`, `dphas1`, `dphas2`, `dphas3`, `dphas1_2`, `ddp1_2`, and another differential phase to the "wraps" file.
    *   If `-xplot` *is* specified, it prints only `dphas1` and `dphas2` to the "wraps" file.
    *   If `slant_range` is not greater than `depth`, it prints placeholder `0.0` values.
7.  **Helper Functions:**
    *   `get_fraction(val)`: Returns the fractional part of a float value (e.g., 3.75 -> 0.75, -2.25 -> 0.75).
    *   `diff_pair(p1, p2)`: Calculates the difference between two phase values, handling wrap-around (ensuring the difference is between 0 and 1).
8.  **File Closing:** The "wraps" file is closed.
