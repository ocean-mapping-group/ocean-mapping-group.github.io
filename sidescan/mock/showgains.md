---
layout: default
title: showgains
parent: Mock Tools
grand_parent: sidescan
nav_order: 12
---
# showgains

## Description
`showgains` is a utility designed to analyze and display the individual components of the backscatter strength equation as a function of range. It simulates a single swath of sidescan data at a given depth and calculates key acoustic parameters for each pixel, such as beam pattern, Time-Varying Gain (TVG), range decay, insonified area, and ultimately, the backscatter strength (`S_b`). The output is printed to standard output in a format suitable for plotting or further analysis.

## Usage
```bash
showgains [-verbose] [-min_beam <gain>] [-depth <seafloor_depth>]
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-verbose` | Enable verbose output, providing more detailed intermediate calculations. | (None) |
| `-min_beam <gain>` | Specifies the minimum beam gain factor to consider in the calculations. | `0.0` |
| `-depth <seafloor_depth>` | Specifies the simulated seafloor depth (in meters) for which the calculations are performed. | `3000` |

## How It Works
1.  **Initialization:**
    *   The tool initializes constants for acoustic parameters (e.g., `PORT_FREQ`, `STBD_FREQ`, `SOUND_SPEED`, `TRANSDUCER_SPACING`, `TRANSDUCER_RADIUS`, `PULSE_CORR_WIDTH`).
    *   It pre-calculates the TVG curve using `tvg_shading_loss`.
    *   It sets a default pixel size (`pixel_size = 30`).
2.  **Output Format Setup:** It prints header information to standard output, defining the plot dimensions, number of plots, x-axis range (range from 0 to 15000), and y-axis ranges for various acoustic parameters (in dB).
3.  **Swath Simulation and Calculation:** The tool iterates `j` from 5 to 495 (representing across-track pixels/samples):
    *   **Side Determination:** It assumes either port or starboard side (hardcoded to starboard in the main loop).
    *   **Acoustic Parameters:** Based on the chosen side, it sets `wave_number`, `beam_width`, `direct_index`, and `absorp_coeff`.
    *   **Geometry Calculation:**
        *   `range`: Calculated as `j * pixel_size`.
        *   `slant_range`: Calculated from `depth` and `range`.
        *   `rgraze`: Grazing angle from `depth` and `range`.
        *   `rbeam`: Beam angle, calculated as `rgraze - (20. * M_PI / 180.)` (a fixed offset from grazing angle, possibly representing a typical beam angle).
        *   The beam pattern directivity `D` is calculated using a model that includes both a two-point array pattern and a circular transducer pattern (similar to `beams.c` and `oldbeams.c`). `rbeam` is then set to `D^2`.
        *   If `rbeam` falls below `min_beam`, it's clipped to `min_beam`.
    *   **Backscatter Equation Components:**
        *   `r12_bit`: Converts an assumed 8-bit input (`old_8bit = 128`) to a 12-bit value.
        *   `I_b`: Calculates the received intensity, corrected for `rbeam`.
        *   `tvg[index]`: Retrieves the TVG value for the current range.
        *   `inson_area`: Calculates the insonified area.
        *   `range_decay`: Calculates the two-way range-dependent transmission loss.
        *   `S_b`: Finally, calculates the backscatter strength (`S_b`) using the full sonar equation, integrating all the above components.
4.  **Output:** For each `j` (range step), it prints the calculated values of `range`, `10*log10(rbeam)`, `10*log10(tvg[index])`, `10*log10(range_decay)`, `10*log10(S_b)`, and `10*log10(inson_area)` to standard output.
5.  **Loop:** This process repeats for all pixels across the simulated swath.
