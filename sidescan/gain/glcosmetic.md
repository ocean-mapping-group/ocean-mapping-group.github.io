---
layout: default
title: glcosmetic
parent: Gain Tools
grand_parent: sidescan
nav_order: 1
---
# glcosmetic

## Description
`glcosmetic` is a utility designed to apply cosmetic adjustments to JCU GLORIA sidescan files. Its primary function, as implemented, is to "smudge" or smooth out the nadir region of the imagery, particularly useful for data like Lake Ontario. It also includes options for applying independent gain factors to the port and starboard sides, although the current implementation focuses on the nadir smudging.

## Usage
```bash
glcosmetic [-smudge <start_smudge> <end_smudge>] [-port <gain>] [-stbd <gain>] [-fixsb] [-start <record>] [-end <record>] <infile> <outfile>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-smudge <start_smudge> <end_smudge>` | Specifies the inner and outer pixel indices for the nadir smudging zone. This defines the range within which pixels will be interpolated. | `30 60` |
| `-port <gain>` | Specifies a gain factor to apply to the port side data. | `1.0` |
| `-stbd <gain>` | Specifies a gain factor to apply to the starboard side data. | `1.0` |
| `-fixsb` | A flag indicating to "fix" something related to sidescan, but its functionality is not explicitly implemented in the provided source. | (None) |
| `-start <record>` | Specifies the starting record number for processing. | `0` |
| `-end <record>` | Specifies the ending record number for processing. | `5000` |
| `<infile>` | **Required.** The input JCU GLORIA file. |
| `<outfile>` | **Required.** The output JCU GLORIA file with cosmetic adjustments applied. |

## How It Works
1.  **Input/Output File Handling:** The tool opens the input GLORIA file for reading and the output file for writing.
2.  **Calculate Averages for Smudging:** For each record:
    *   It calculates `port_average` and `stbd_average` within the `start_smudge` to `end_smudge` range (excluding pixels with value 255). This establishes reference intensity levels outside the immediate nadir.
3.  **Nadir Smudging:**
    *   For pixels within the `start_smudge` range from the nadir on both port and starboard sides (e.g., `j` from `0` to `start_smudge-1`):
        *   It linearly interpolates the pixel value based on the `port_average` and `stbd_average`. The formula aims to create a smooth transition across the nadir, effectively blending the values from both sides.
        `value = port_average * (float)(j + start_smudge) / (float)(2 * start_smudge) + stbd_average * (float)(start_smudge - j) / (float)(2 * start_smudge);`
        (This formula is applied to both port and starboard sides, symmetric around the nadir).
    *   The smudged pixel values replace the original values in the `glo_rec.port_data` and `glo_rec.stbd_data` arrays.
4.  **Gain Application (Conceptual):** Although options `-port` and `-stbd` exist, the core loop's current implementation primarily focuses on the nadir smudging and doesn't explicitly show the multiplication by `port_gain` or `stbd_gain` within the `for` loop for pixel processing.
5.  **Write Output:** The modified `glo_rec` (with smudged nadir) is written to the output file.
6.  **Loop:** This process repeats for all records in the input file.
