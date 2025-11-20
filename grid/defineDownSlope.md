---
layout: default
title: defineDownSlope
parent: Grid Tools
nav_order: 18
---
# defineDownSlope

## Description
`defineDownSlope` is a command-line utility that analyzes a JHC-format 32-bit floating-point grid file (`.r4`), typically representing a Digital Terrain Model (DTM). For each pixel, it examines the eight neighboring pixels to determine the direction of the steepest descent. The output is an 8-bit JHC grid file where each pixel's value encodes the downslope direction, or indicates if it's a local minimum (a pit). This is useful for basic hydrological analysis and visualizing surface flow paths.

## Usage
```bash
defineDownSlope [-v] <floatfile_prefix>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `<floatfile_prefix>` | **Required.** The prefix for the input float file. The tool will automatically append `.r4` to this prefix to find the input grid. | `my_dtm` (looks for `my_dtm.r4`) |

## Output File
The tool generates an 8-bit JHC grid file named `<floatfile_prefix>.downSlope`.

### Output Value Encoding
The value of each pixel in the output `.downSlope` file represents the direction of the steepest descent from that location:

*   **20:** Downslope to North-West (NW)
*   **40:** Downslope to North (N)
*   **60:** Downslope to North-East (NE)
*   **80:** Downslope to East (E)
*   **100:** Downslope to South-East (SE)
*   **120:** Downslope to South (S)
*   **140:** Downslope to South-West (SW)
*   **160:** Downslope to West (W)
*   **RED (color constant):** The pixel is a local minimum (a pit or low point), meaning no neighbor is lower.
*   **YELLOW (color constant):** The pixel is in a flat area (a "lake"), where neighbors may be equal but none are lower.
*   **CYAN (color constant):** The pixel has no valid neighbors to compare against.
