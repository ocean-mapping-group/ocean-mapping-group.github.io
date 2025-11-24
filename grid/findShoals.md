---
layout: default
title: findShoals
parent: Grid Tools
nav_order: 32
---
---
layout: default
title: findShoals
parent: Grid Tools
nav_order: 32
---
# findShoals

## Description
`findShoals` is a feature detection utility that scans a JHC-format 32-bit floating-point grid file (DTM/DEM) to identify all local maxima. In bathymetric terms, these local high points represent "shoals" or peaks on the seafloor.

The tool uses a 3x3 sliding window to examine each pixel. If a pixel's value is strictly greater than all eight of its immediate neighbors, it is classified as a shoal. The geographic coordinates (latitude, longitude) and depth of each identified shoal are then written to an ASCII output file.

## Usage
```bash
findShoals <depthfile.r4> <output_asciifile>
```

## Arguments

| Argument | Description | Example |
|---|---|---|
| `<depthfile.r4>` | **Required.** The input JHC-format 32-bit floating-point grid file to be analyzed. | `my_bathymetry.r4` |
| `<output_asciifile>` | **Required.** The name for the output ASCII file that will contain the list of detected shoals. | `shoal_list.txt` |

## How It Works
1.  **File Opening:** Opens the input `.r4` depth file and the output ASCII file.
2.  **Header Reading:** Reads the `JHC_header` from the input file to get grid dimensions and geographic information.
3.  **Data Loading:** Loads the entire input grid data into memory.
4.  **Local Maxima Detection:** Iterates through each pixel in the grid (excluding the outermost boundary):
    *   For each pixel, it compares its value with the values of its eight immediate neighbors in a 3x3 window.
    *   If the central pixel's value is strictly greater than all eight of its neighbors, it is identified as a local maximum (a shoal).
    *   The geographic coordinates (latitude, longitude) and depth of the shoal are calculated using the grid's geographic information.
5.  **Output:** Writes the `latitude`, `longitude`, and `depth` of each detected shoal to the output ASCII file.

## Output Files
*   `<output_asciifile>`: A three-column ASCII file (`latitude longitude depth`) listing all detected shoals.

## Dependencies
*   `array.h`: For `JHC_header` structure and DTM data handling.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.

## Notes
This tool is simple yet effective for identifying bathymetric high points that might be navigational hazards or features of geological interest. The definition of a "shoal" here is purely morphological (local maxima). Further analysis might be needed to determine significance. The depth values are inverted to be positive as is common in oceanographic conventions.
