---
layout: default
title: defineDownSlope
parent: Grid Tools
nav_order: 18
---
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

## How It Works
1.  **File Opening:** Opens the input `.r4` DTM file and creates the output `.downSlope` 8-bit grid file.
2.  **Header Reading:** Reads the `JHC_header` from the input file.
3.  **Slope Calculation:** Iterates through each pixel (`i`, `j`) in the input DTM (excluding the edges):
    *   For each pixel, it accesses its 8 immediate neighbors.
    *   It determines which neighbor has the lowest elevation relative to the current pixel.
    *   If a lower neighbor is found, the output pixel value is set to encode the direction (e.g., 40 for North, 80 for East).
    *   If no neighbor is lower (i.e., it's a local minimum), the pixel is marked as a pit (RED).
    *   If all valid neighbors have the same elevation, it's marked as a flat area (YELLOW).
    *   If there are no valid neighbors, it's marked as CYAn.
4.  **Output Header:** Creates a `JHC_header` for the output file (copied from the input, but with `data_type` set to 8-bit and min/max values reflecting the direction codes) and writes it.
5.  **Output Data:** Writes the processed 8-bit pixel data (representing downslope directions) to the output file.

## Output Files
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

## Dependencies
*   `array.h`: For `JHC_header` structure and DTM data handling.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is a fundamental component for hydrological modeling, enabling the visualization of water flow paths and the identification of drainage basins. The output can be further processed by tools like `defineWatershed`. The hardcoded color constants (RED, YELLOW, CYAN) are likely used for visualization in specialized image viewers.
