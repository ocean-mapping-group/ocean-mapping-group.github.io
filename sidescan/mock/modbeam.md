---
layout: default
title: modbeam
parent: Mock Tools
grand_parent: sidescan
nav_order: 8
---
# modbeam

## Description
`modbeam` is a utility designed to modify the beam pattern by incorporating a vertical beam function. It uses existing beam-angle and aspherical spreading component files (in JHC image format) to compute new, modified beam patterns for both port and starboard transducers. The output consists of two new lookup array files (`.beam_port` and `.beam_stbd`) representing these modified beam patterns. This tool does not appear to incorporate beam focusing.

## Usage
```bash
modbeam -water <file_prefix> [-first <record>] [-last <record>]
```

## Arguments

| Option | Description |
|---|---|
| `-water <file_prefix>` | **Required.** Specifies a prefix for related water column files. The tool expects to find `<file_prefix>.beam_angle` and `<file_prefix>.aspherical`. It will output `<file_prefix>.beam_port` and `<file_prefix>.beam_stbd`. |
| `-first <record>` | Specifies the first record number to include in processing. |
| `-last <record>` | Specifies the last record number to include in processing. |

## How It Works
1.  **Input Loading:**
    *   The tool opens the specified beam-angle (`.beam_angle`) and aspherical component (`.aspherical`) files. These files are expected to be JHC image files containing `float` data.
    *   It reads their `JHC_header` to determine image dimensions and loads the entire image data into memory as arrays of `float` (`beams` and `aspherical`).
2.  **Output Initialization:**
    *   Two new output files, `.beam_port` and `.beam_stbd`, are created, each with a header copied from the input `beam_head`.
    *   A `newbeams` array is allocated to store the computed beam pattern.
3.  **Beam Pattern Calculation (for Port and Starboard):** The tool performs this calculation twice, once for port (k=0) and once for starboard (k=1).
    *   **Wavenumber Calculation:** `wave_number` is calculated based on the respective `PORT_FREQ` or `STBD_FREQ` and `SOUND_SPEED`.
    *   **Pixel Iteration:** It iterates through each pixel (`j`, `i`) of the input image data (skipping the edges for boundary conditions).
    *   For each pixel:
        *   `rbeam` is read from the `beams` array and converted from a scaled value to radians.
        *   `rasph` is read from the `aspherical` array (though it is not used in the provided calculation snippet for `D`).
        *   **Vertical Beam Function:** The core directivity `D` is calculated based on `rbeam` and the physical parameters `TRANSDUCER_SPACING`, `TRANSDUCER_RADIUS`, and `wave_number`. This calculation involves two terms:
            *   One term from `sin((2. * values)) / (2. * sin(values))` using `values = TRANSDUCER_SPACING * wave_number * sin(rbeam) / 2.0`. This models a two-element array pattern.
            *   Another term `2. * j1(x) / x` using `x = wave_number * TRANSDUCER_RADIUS * sin(rbeam)`. This models the directivity of a circular transducer.
        *   `D` is the product of these two terms.
        *   The squared magnitude (`pow((double)D, 2.0)`) is stored in the `newbeams` array.
4.  **Write Output:** The calculated `newbeams` array is written as `float` values to the respective `.beam_port` or `.beam_stbd` output file, preceded by its header.
