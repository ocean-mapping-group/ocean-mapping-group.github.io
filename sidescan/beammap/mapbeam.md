---
layout: default
title: mapbeam
parent: Beammap Tools
grand_parent: sidescan
nav_order: 3
---
# mapbeam

## Description
`mapbeam` is a utility that scans JCU GLORIA/MR1 format sidescan files to stack their across-track profiles. It organizes this data according to a series of depth bins, effectively computing a depth-dependent angular function or beammap. This tool is designed as a faster alternative to older beam pattern correction methods like `glbeam_bydepth.c`, providing an empirical representation of the beam pattern.

## Usage
```bash
mapbeam [-maxdep <depth>] [-mindep <depth>] [-depbin <count>] <basename> <datafile1> [datafile2 ...]
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-maxdep <depth>` | Set the maximum depth for binning. | `4000.0` |
| `-mindep <depth>` | Set the minimum depth for binning. | `200.0` |
| `-depbin <count>` | Set the number of depth bins. | `750` |
| `<basename>` | **Required.** A base name for the output files. Two files will be generated: `<basename>.mean` and `<basename>.count`. | |
| `<datafile1> [datafile2 ...]` | **Required.** One or more input sidescan files (GLORIA/MR1 format) to be processed. | |

## How It Works
1.  **Initialization:**
    *   The tool allocates memory for `sum` and `count` arrays, which are used to accumulate pixel intensity sums and pixel counts for each depth and across-track bin.
    *   It initializes `maxcount` to track the maximum number of pings contributing to any single bin.
2.  **Configuration:** Users can define the minimum depth (`-mindep`), maximum depth (`-maxdep`), and the number of depth bins (`-depbin`) for the mapping process.
3.  **Process Input Files (`scanfile` function):**
    *   The tool iterates through each provided `<datafile>`.
    *   For each GLORIA record in an input file:
        *   It extracts the `depth` (from `header.altitude`).
        *   It calculates the `row` (depth bin index) using the `DEPTHTOROW` macro.
        *   It iterates through all pixels (`SWATH_WIDTH`) in the record's sidescan data (`stbd_data`).
        *   For each valid pixel (not 255):
            *   Its intensity is added to `sum[index]` and `count[index]` is incremented, where `index` maps the current depth bin and across-track position.
4.  **Dump Data (`dump_data` function):** After processing all input files, the tool generates two output files:
    *   **`<basename>.mean` (Mean Beam Pattern):**
        *   For each depth bin, it calculates the average pixel intensity (`sum[index] / count[index]`).
        *   These average intensities are then written as GLORIA records to the `.mean` file. The `header.altitude` of each record in this file represents the mean depth of that bin.
    *   **`<basename>.count` (Coverage Count):**
        *   For each depth bin, it scales the `count[index]` by `255 / maxcount` to represent the pixel coverage as an 8-bit image.
        *   These scaled counts are written to the `.count` file.
