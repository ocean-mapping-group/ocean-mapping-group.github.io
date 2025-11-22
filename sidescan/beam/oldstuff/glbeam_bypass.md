---
layout: default
title: glbeam_bypass
parent: Beam Tools
grand_parent: sidescan
nav_order: 2
---
# glbeam_bypass

## Description
`glbeam_bypass` is a utility for beam pattern correction of a JCU GLORIA file. This tool has two primary modes of operation:
1.  **Calculate Beam Pattern:** If no beam pattern file is supplied, it calculates the average beam pattern parameters from the input GLORIA file.
2.  **Apply Beam Pattern:** If a beam pattern file is supplied, it applies the corrections from that file to the input GLORIA file.

## Usage
```bash
glbeam_bypass <infile> <outfile> <beamfile_or_null>
```

## Arguments

| Option | Description |
|---|---|
| `<infile>` | **Required.** The input JCU GLORIA file. |
| `<outfile>` | **Required.** The output JCU GLORIA file with beam pattern correction applied. |
| `<beamfile_or_null>` | **Required.** Either the path to a beam pattern file (`.beam_pattern` format) to apply, or the string "null" to instruct the tool to calculate the beam pattern from the `infile`. |

## How It Works
1.  **Mode Determination:**
    *   If `<beamfile_or_null>` is "null", the tool enters "calculate beam pattern" mode.
    *   Otherwise, it enters "apply beam pattern" mode and loads the supplied beam pattern parameters.
2.  **Calculate Beam Pattern Mode (`<beamfile_or_null>` is "null"):**
    *   Reads the input GLORIA file record by record.
    *   For each pixel in the sidescan data (port and starboard), it calculates the `theta` (angle) based on its distance from nadir and the altitude.
    *   It then accumulates the sum of pixel intensities and the count of pixels for each `itheta` (integer `theta` bin).
    *   After processing the entire file, it computes the average intensity (`stbd_ave`, `port_ave`) for each `itheta` bin.
    *   It calculates `stbd_par` and `port_par` by dividing the average intensity in each bin by the overall average intensity within a defined range (`min_use` to `max_use`). These `stbd_par` and `port_par` arrays represent the calculated beam pattern.
3.  **Apply Beam Pattern Mode (a `beamfile` is supplied):**
    *   Loads the beam pattern parameters (`stbd_par`, `port_par`, `stbd_ave`, `port_ave`) from the supplied beam pattern file.
    *   For each parameter, it calculates its reciprocal so that corrections can be done by multiplication.
4.  **Correction Application (both modes):**
    *   Reads the input GLORIA file record by record.
    *   For each pixel in the sidescan data (port and starboard):
        *   Calculates `theta` and `itheta` as described above.
        *   It interpolates `parameter` from `stbd_par`/`port_par` arrays based on `itheta` and weights (`weight1`, `weight2`).
        *   The raw pixel value is multiplied by `parameter` to get the `corrected` value.
        *   The `corrected` value is clamped to a maximum of 254.
    *   The corrected record is written to the output file.
