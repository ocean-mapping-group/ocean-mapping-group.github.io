---
layout: default
title: glfudge
parent: Histogram Tools
grand_parent: sidescan
nav_order: 2
---
# glfudge

## Description
`glfudge` is a utility designed to fill in invalid data (typically pixels with a value of 255) in JCU GLORIA format files. It is similar to `glfill.c` but employs a more aggressive interpolation strategy, first filling gaps in the across-track direction within each ping, and then filling gaps in the along-track (ping-to-ping) direction. It allows for configurable maximum interpolation distances in both directions.

## Usage
```bash
glfudge [-invalid <value>] [-maxInterpAlong <pixels>] [-maxInterpAcross <pixels>] [-lower_level <value>] <rawfile> <fillfile>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-invalid <value>` | Specifies the pixel value that represents invalid data. | `255` |
| `-maxInterpAlong <pixels>` | Specifies the maximum number of pixels to interpolate along-track (ping-to-ping). | `10` |
| `-maxInterpAcross <pixels>` | Specifies the maximum number of pixels to interpolate across-track (within a single ping). | `10` |
| `-lower_level <value>` | Specifies a pixel intensity threshold. Pixels below this level are also considered invalid and candidates for filling. | `0` |
| `<rawfile>` | **Required.** The input JCU GLORIA file containing raw data to be fudged. |
| `<fillfile>` | **Required.** The output JCU GLORIA file with invalid data filled. |

## How It Works
1.  **Load Image Data:** The entire input GLORIA file (`rawfile`) is loaded into memory as a 2D array (`image`) of `unsigned char`, representing the pixel intensities for each record.
2.  **Across-Track Interpolation:** For each ping (`i`) in the `image` array:
    *   It identifies sequences of invalid pixels within the ping.
    *   If a sequence of invalid pixels is found between two valid pixels, and the length of this sequence is less than `maxInterpAcross`, the invalid pixels are filled by linear interpolation between the two surrounding valid pixels.
    *   This step addresses horizontal gaps within individual scan lines.
3.  **Along-Track Interpolation:** After across-track gaps are addressed, the tool proceeds to fill along-track gaps:
    *   It iterates through each pixel (`j`) that might still be invalid.
    *   If `image[i][j]` is `invalid` (or below `lower_level`):
        *   It searches forward along-track for a valid pixel (`image[i+k][j]`) within `maxInterpAlong` distance.
        *   If a valid pixel is found and `image[i-1][j]` is also valid, the invalid pixels between `image[i-1][j]` and `image[i+numToInterp][j]` are filled by linear interpolation.
        *   Special cases for `numToInterp == 1` (simple average of immediate neighbors) are handled.
4.  **Write Output File:** After all interpolation, the modified `image` data is copied back into `gloria_rec` structures and written to the `fillfile`.
