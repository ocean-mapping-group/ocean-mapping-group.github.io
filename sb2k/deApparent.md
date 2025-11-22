---
layout: default
title: deApparent
parent: SB2K Tools
nav_order: 190
---
# deApparent

## Description
`deApparent` is a utility designed to "undo" the "apparent depth" correction often applied by SeaBeam sonar systems. SeaBeam systems typically present depths corrected to a constant sound velocity (e.g., 1500 m/s), even when the actual sound velocity profile (SVP) in the water column is different. This tool uses a provided SVP file to convert these "apparent depths" back to their true water depths, effectively removing the 1500 m/s assumption.

This process is critical for accurate hydrographic surveying, as it ensures that depths reflect the actual water column properties rather than a simplified model.

## Usage
```bash
deApparent -svp <SVP.file> <mergefile(s)> [-v] [-depscale <value>]
```

## Arguments

| Option | Description |
|---|---|
| `-svp <SVP.file>` | **Required.** Path to the Sound Velocity Profile (SVP) file. This file should contain depth and corresponding in-situ sound velocity pairs. |
| `<mergefile(s)>` | **Required.** One or more OMG-HDCS `.merged` files containing the SeaBeam depth data to be corrected. |
| `-v` | Enable verbose output. |
| `-depscale <value>` | (Optional) Manually set a depth scale factor. Defaults to `0.0105`. |

## How It Works

1.  **Initialization:** Parses command-line arguments to get the SVP file path, input merged files, and optional parameters (`verbose_flag`, `dep_scale`).
2.  **SVP File Reading:**
    *   Opens and reads the provided SVP file.
    *   Stores depth and in-situ sound velocity pairs into an internal `watercolumn` structure array.
3.  **Harmonic Mean Calculation:**
    *   Iterates through the read SVP data to calculate the harmonic mean sound velocity for each layer and the cumulative two-way travel time (TWTT) to each depth.
    *   From this, it calculates `harmonic_SSP` (harmonic mean sound speed to a given depth) and a corresponding scale factor (`harmonic_SSP / 1500.0`) that represents the ratio of the true average sound speed to the 1500 m/s assumed by the sonar.
4.  **Merged File Processing Loop:**
    *   For each input `.merged` file:
        *   Opens the file in read/write mode (`r+`).
        *   Reads the `OMG_HDCS_summary_header`.
        *   Iterates through each profile (ping) in the merged file:
            *   Reads the `OMG_HDCS_profile_header`.
            *   Reads the `OMG_HDCS_beam` array for the current profile.
            *   **Depth Correction:** For each beam that contains an observed depth:
                *   Determines the appropriate SVP layer based on the beam's observed depth.
                *   Calculates an interpolated `dep_scale` factor from the `harmonic_SSP` values, accounting for the depth range.
                *   Applies this `dep_scale` factor to the `beams[i].observedDepth`, effectively converting the 1500 m/s-corrected depth back to the true water depth.
            *   Writes the modified `OMG_HDCS_beam` array back to the `.merged` file.
        *   Closes the current `.merged` file.
5.  **Cleanup:** Exits.

## Output
The input `.merged` files are modified in-place, with the "apparent depths" converted to true water depths based on the provided SVP.
```
```