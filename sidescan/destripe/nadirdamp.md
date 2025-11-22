---
layout: default
title: nadirdamp
parent: Destripe Tools
grand_parent: sidescan
nav_order: 9
---
# nadirdamp

## Description
`nadirdamp` is a utility designed to dampen out low-frequency ridges that often appear in the nadir region of JCU GLORIA format sidescan files. It achieves this by applying a linear interpolation across a defined "widthzone" around the nadir, effectively smoothing out anomalies in that area. This tool is typically applied to the `.low` component resulting from a destriping operation.

## Usage
```bash
nadirdamp [-widthzone <pixels>] <infile_prefix>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-widthzone <pixels>` | Specifies the number of pixels on either side of the nadir to be affected by the damping. The total zone width will be `2 * <pixels>`. | `50` |
| `<infile_prefix>` | **Required.** The prefix for the input GLORIA low-pass file. The tool assumes the input file has a `.low` extension. The output file will have a `.low_damp` extension. |

## How It Works
1.  **Input Files:** The tool takes a single JCU GLORIA low-pass file (e.g., `<infile_prefix>.low`) as input.
2.  **Determine Nadir Zone:** The `widthzone` parameter defines the area around the nadir (center of the `all_data` array, typically `GLORIA_SIDESIZE`). For example, if `widthzone` is 50, the zone affected will be from `GLORIA_SIDESIZE - 50` to `GLORIA_SIDESIZE + 50`.
3.  **Read Reference Pixels:** For each record, it reads the pixel values at the left and right boundaries of the `widthzone`:
    *   `left = out_rec.all_data[GLORIA_SIDESIZE - widthzone];`
    *   `right = out_rec.all_data[GLORIA_SIDESIZE + widthzone];`
4.  **Linear Interpolation:** For each pixel (`j`) within the nadir `widthzone`:
    *   It calculates a new pixel value by linearly interpolating between the `left` and `right` reference pixel values. The formula used is:
        `new_value = (left * (widthzone - j)) / (widthzone * 2.) + (right * (widthzone + j)) / (widthzone * 2.);`
    *   This effectively creates a smoothed gradient across the nadir zone, from the `left` value to the `right` value.
5.  **Write Output:** The modified record (`out_rec`) is written to the output file (e.g., `<infile_prefix>.low_damp`).
6.  **Loop:** This process repeats for all records in the input file.
