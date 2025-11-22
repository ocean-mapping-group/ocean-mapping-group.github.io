---
layout: default
title: profile
parent: Seabed Tools
grand_parent: sidescan
nav_order: 1
---
# profile

## Description
`profile` is a utility designed to build a depth profile from JCU GLORIA images, specifically focusing on the first returns in the nadir region. It processes the sidescan data, remaps pixel values (optionally), and marks the calculated nadir point on a generated output profile image. This tool can be useful for visualizing the seafloor depth across the swath.

## Usage
```bash
profile [-pingint <seconds>] [-first <record>] [-last <record>] [-noremap] <inname>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-pingint <seconds>` | Specifies the ping interval in seconds. Used in calculating the time per pixel. | `30.0` |
| `-first <record>` | Specifies the first record number to begin processing. | `0` |
| `-last <record>` | Specifies the last record number to end processing. | `-1` (end of file) |
| `-noremap` | If specified, pixel values will not be remapped (e.g., values 1-15 to 16). | Remap is `true` |
| `<inname>` | **Required.** The input JCU GLORIA merged file. | |

## How It Works
1.  **Input File Reading:** The tool opens the specified input JCU GLORIA file (`inname`).
2.  **Output File Creation:** It creates an output file with a `.pro` extension (e.g., `input.glo.pro`) for the generated profile data.
3.  **Colormap (Remapping):** An internal `colormap` array is initialized. By default, values 1-15 are remapped to 16. If `-noremap` is used, this remapping is skipped.
4.  **Record Processing Loop:** The tool reads each GLORIA record (`glrec`) from the input file:
    *   **Data Extraction and Remapping:** It extracts the port and starboard sidescan data from `glrec.port_data` and `glrec.stbd_data`. These values are then passed through the `colormap` (if remapping is enabled) and stored in `outbuf`.
    *   **Nadir Point Calculation:**
        *   It retrieves the `depth` from `glrec.header.altitude`.
        *   It calculates the expected pixel position (`pix`) corresponding to this depth based on `SOUND_SPEED` and `sec_per_pix` (seconds per pixel).
        *   This calculated `pix` position on the `outbuf` (which represents the across-track profile) is marked with a specific color (5, typically yellow).
    *   **Output:** The `outbuf` (representing the processed profile for the current record) is written to the output file.
5.  **Loop:** This process continues until all specified records have been processed.
