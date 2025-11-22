---
layout: default
title: modarray
parent: Mock Tools
grand_parent: sidescan
nav_order: 7
---
# modarray

## Description
`modarray` is a utility designed to modify lookup arrays, specifically to calculate the "aspherical spreading component" derived from beam refraction. It processes input files representing time-lag and beam-angle (in JHC image format) to determine how the apparent angular change of a beam deviates from the normal angular change. This resulting "aspherical" component is then output as a new JHC image file.

## Usage
```bash
modarray -water <file_prefix> [-first <record>] [-last <record>]
```

## Arguments

| Option | Description |
|---|---|
| `-water <file_prefix>` | **Required.** Specifies a prefix for related water column files. The tool expects to find `<file_prefix>.time_lag` and `<file_prefix>.beam_angle`. It will output `<file_prefix>.aspherical`. |
| `-first <record>` | Specifies the first record number to include in processing. |
| `-last <record>` | Specifies the last record number to include in processing. |

## How It Works
1.  **Input Loading:**
    *   The tool opens three files: a time-lag file (`.time_lag`), a beam-angle file (`.beam_angle`), and creates an aspherical output file (`.aspherical`). These are expected to be JHC image files, typically containing `float` data.
    *   It reads the `JHC_header` from the time-lag and beam-angle files to get image dimensions (`dx`, `dy`).
    *   The entire image data for time-lag (`times`) and beam-angle (`beams`) is loaded into memory as arrays of `float`.
2.  **Aspherical Component Calculation:**
    *   The tool iterates through each pixel (`j`, `i`) of the image, from the inner regions (skipping the edges for derivative calculations).
    *   For each pixel:
        *   **Range Calculation:** It calculates the `range` using the time-lag value at that pixel (`*(times + j + (i * time_head.dx)) * 1500.0`, assuming speed of sound 1500 m/s).
        *   **Normal Angular Change (`normal_del_angle`):** This is calculated as the arctangent of `(2 * asph_head.xstep / range)`. This represents the expected angular change across a pixel given its range.
        *   **Apparent Angular Change (`del_angle`):** This is derived from the spatial derivatives of the `beams` array:
            *   `del_vert = top - bottom;` (vertical derivative of beam angles)
            *   `del_hori = right - left;` (horizontal derivative of beam angles)
            *   `del_angle = sqrt(del_hori^2 + del_vert^2);` (magnitude of the apparent angular change).
        *   **Ratio Calculation:** The `aspherical` component is calculated as the ratio `del_angle / normal_del_angle`. This ratio indicates how much the apparent angular change deviates from the expected normal angular change.
    *   If any input data is invalid (e.g., `range` is zero or neighboring beam-angle values are missing), the output `aspherical` value is set to -1.
3.  **Output File:** The calculated `aspherical` components are written as `float` values to the output file (`.aspherical`), preceded by a `JHC_header`.
