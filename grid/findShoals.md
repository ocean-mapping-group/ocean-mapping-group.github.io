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

## Output Format
The output is a simple three-column ASCII file:
`latitude longitude depth`

Each line represents a single detected shoal. The depth value is inverted to be positive, following standard oceanographic convention.
