---
layout: default
title: traceBP
parent: OMG Tools
nav_order: 72
---
# traceBP

## Description
`traceBP` is a utility designed to analyze sidescan (SS) trace intensities as a function of incidence angle, primarily for EM710 and EM1000 multibeam sonars. It calculates the intensities for individual trace samples, bins them by incidence angle, and then performs a quadratic least-squares fit on the averaged backscatter response of the first and last beams.

The primary outputs are:
1.  A `tracepatt` file containing coefficients of quadratic equations to normalize outer traces (used by `makess -traceBP`).
2.  Optionally, a verbose output suitable for plotting traces intensities versus launch angles (for all beams or individual beams).

## Usage
```bash
traceBP <merged_file(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<merged_file(s)>` | **Required.** One or more paths to OMG-HDCS merged files (with associated `.ss_data` files). |
| `-v` | Enable verbose output. |
| `-draft <val>` | Specifies the draft (in meters) to subtract from observed depths. | Auto-calculated from `.param` or `VESSEL_DRAFT` (3.46m) |
| `-yoffset <val>` | Specifies the Y-offset (in meters) to subtract from across-track distances. | Auto-calculated from `.param` or `VESSEL_YOFFSET` (0.0m) |
| `-plot_log` | Output backscatter in logarithmic units (dB). |
| `-plot_linear` | Output backscatter in linear units. |
| `-plot_dn` | Output backscatter in raw Digital Number (DN) units. |
| `-depth_range <min_m> <max_m>` | Only process beams within this water depth range (in meters). | `0` to `1000` |

## Output
*   **`tracepatt` file:** An ASCII file (default name) containing 8 float values: `x_min`, `x_max`, `c`, `b`, `x_min_last`, `x_max_last`, `f`, `e`. These are coefficients of the quadratic equations fitted to the first and last beams.
*   **Standard Output (if plot flags are used):** Prints detailed information about beam numbers, launch angles, angle offsets, average backscatter, and counts, formatted for external plotting tools like `xmgrace`.

## How It Works
1.  **Initialization:** Initializes various parameters, including `draft`, `offset_y`, `min_depth`, `max_depth`, and arrays for accumulating backscatter and counts.
2.  **File Iteration:** Loops through each input merged file:
    *   Opens the merged file (`infile`) and its corresponding sidescan data file (`.ss_data`).
    *   Loads sonar parameters from the `.param` file to determine `draft` and `offset_y` if not overridden.
    *   Reads the summary header.
    *   **Ping Iteration:** Loops through each profile (ping) in the merged file:
        *   Reads the current profile header and raw beams.
        *   Calculates `sample_length` (pixel size in the sidescan trace).
        *   Adjusts depth for `draft` and `acrosstrack` for `offset_y`.
        *   **Beam and Sample Iteration:** For each valid beam within the current ping:
            *   Reads the raw sidescan `Scan` data for the beam from the `.ss_data` file.
            *   Calculates the `incAng_centre_trace[j]` (incidence angle of the center sample of the beam's trace).
            *   For each sample `k` within the beam's sidescan trace:
                *   Calculates the `incidence_angle` for that specific sample (Pythagorean theorem using depth and across-track offset, referencing the center sample's incidence angle).
                *   Determines `diff_incidence_angle` (difference from the center incidence angle) and a `division_index` to bin the sample's backscatter.
                *   Accumulates `dn_value` (Digital Number from the sidescan sample) into `sum[j][division_index]` and increments `count[j][division_index]`.
                *   Calculates `avg_BS[j][division_index]`.
3.  **Quadratic Least-Squares Fit:**
    *   After processing all pings, it identifies the `min_sector` and `max_sector` (angle bins with sufficient data) for the *first* and *last* valid beams.
    *   It then performs a least-squares fit to a quadratic equation (`y = c*x^2 + b*x + a`) using the `avg_BS` values as `y` and binned incidence angles as `x`. This is done separately for the first and last beams.
    *   The coefficients (`a`, `b`, `c`, `d`, `e`, `f`) are printed to standard output.
4.  **Output to `tracepatt`:** The calculated coefficients for the first and last beams are written to the `tracepatt` file.
5.  **Plotting Output (if plot flags are used):** Prints a formatted table to standard output for plotting, including beam number, file sequence, launch angle, angle offset, average backscatter (converted to log, linear, or DN as requested), and count.
