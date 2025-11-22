---
layout: default
title: glbeam_spline
parent: Beam Tools
grand_parent: sidescan
nav_order: 3
---
# glbeam_spline

## Description
`glbeam_spline` is a program to accomplish beam pattern correction of a JCU GLORIA file. This tool uses spline interpolation to obtain a smooth correction, making it a more refined approach to beam pattern correction compared to simpler methods.

## Usage
```bash
glbeam_spline <infile> <outfile> <beamfile_or_null>
```

## Arguments

| Option | Description |
|---|---|
| `<infile>` | **Required.** The input JCU GLORIA file. |
| `<outfile>` | **Required.** The output JCU GLORIA file with beam pattern correction applied. |
| `<beamfile_or_null>` | **Required.** Either the path to a beam pattern file to apply, or the string "null" to instruct the tool to calculate the beam pattern from the `infile`. |

## How It Works
1.  **Mode Determination:**
    *   If `<beamfile_or_null>` is "null", the tool calculates the average beam pattern parameters from the input GLORIA file.
    *   Otherwise, it loads the beam pattern parameters from the supplied beam pattern file.
2.  **Calculate Beam Pattern Mode (`<beamfile_or_null>` is "null"):**
    *   Reads the input GLORIA file record by record.
    *   For each pixel in the sidescan data, it calculates the `theta` (angle) based on its distance from nadir and the altitude.
    *   It accumulates the sum of pixel intensities and the count of pixels for each `itheta` (integer `theta` bin).
    *   After processing the entire file, it computes the average intensity (`stbd_par`, `port_par`) for each `itheta` bin.
    *   It then normalizes these parameters by dividing them by the overall average intensity.
3.  **Apply Beam Pattern Mode (a `beamfile` is supplied):**
    *   Loads the beam pattern parameters (`stbd_par`, `port_par`) from the supplied beam pattern file. The file is expected to contain 91 pairs of `stbd_par` and `port_par` values.
4.  **Spline Interpolation:**
    *   The `stbd_par` and `port_par` arrays are then spline interpolated using the `zspl3` and `spl3` routines. This creates a smooth function from which correction factors can be derived for any `theta` value.
5.  **Correction Application (both modes):**
    *   The tool reads the input GLORIA file record by record.
    *   For each pixel in the sidescan data (port and starboard):
        *   Calculates `theta` as described above.
        *   It uses the spline interpolated function to obtain the `parameter` for `stbd` and `port` sides at the current `theta`.
        *   The raw pixel value is multiplied by this `parameter` to get the `corrected` value.
        *   The `corrected` value is clamped to a maximum of 255.
    *   The corrected record is written to the output file.
