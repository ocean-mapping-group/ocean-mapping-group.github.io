---
layout: default
title: gtopo2ascii
parent: Grid Tools
nav_order: 35
---
---
layout: default
title: gtopo2ascii
parent: Grid Tools
nav_order: 35
---
# gtopo2ascii

## Description
`gtopo2ascii` is a command-line utility for converting binary Digital Elevation Model (DEM) data, specifically in the GTOPO30 format, into a simple three-column ASCII XYZ format (`latitude longitude elevation`).

The tool reads a binary `.DEM` file containing 16-bit integer elevation data and its corresponding ASCII `.HDR` header file. It uses the metadata from the header to correctly interpret the binary data, calculate the geographic coordinate for each pixel, and stream the results to standard output.

## Usage
```bash
gtopo2ascii -in <file_prefix> [OPTIONS] > output.xyz
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-in <file_prefix>` | **Required.** Specifies the prefix for the input files. The tool expects to find two files: `<file_prefix>.DEM` (the binary data) and `<file_prefix>.HDR` (the ASCII header). | `-in W140N90` |
| `-invalid <value>` | Specifies the integer value within the `.DEM` file that represents "no data". These pixels will be skipped. | `-99999` |
| `-maxlat <degrees>` | Defines the maximum latitude (northern boundary) of a geographic bounding box for extraction. | `-maxlat 48.0` |
| `-minlat <degrees>` | Defines the minimum latitude (southern boundary) of a geographic bounding box for extraction. | `-minlat 45.0` |
| `-maxlon <degrees>` | Defines the maximum longitude (eastern boundary) of a geographic bounding box for extraction. | `-maxlon -63.0` |
| `-minlon <degrees>` | Defines the minimum longitude (western boundary) of a geographic bounding box for extraction. | `-minlon -67.0` |
| `-v` | Enable verbose output. | |

## How It Works
1.  **File Opening:** Opens the binary `.DEM` file for reading and the ASCII `.HDR` file for reading.
2.  **Header Parsing:** Reads the `.HDR` file to extract metadata such as `ncols` (number of columns), `nrows` (number of rows), `latitude`, `longitude` (of the origin), and `cellsize` (pixel resolution in degrees).
3.  **Data Processing Loop:** Reads the `.DEM` file, which contains 16-bit signed integer elevation values, row by row and column by column:
    *   Reads a 16-bit `elevation` value.
    *   If `elevation` matches the `invalid_value`, it is skipped.
    *   Calculates the `latitude` and `longitude` for the current pixel using the origin coordinates and `cellsize`.
    *   If geographic bounding box options (`-maxlat`, `-minlat`, `-maxlon`, `-minlon`) are specified, it checks if the current pixel falls within these bounds.
    *   Prints `latitude`, `longitude`, and `elevation` to standard output.

## Output Files
The tool prints space-separated `latitude longitude elevation` values to standard output, which can be redirected to a file.

## Dependencies
*   `support.h`: For general utility functions and error handling.

## Notes
GTOPO30 is a global digital elevation model with a horizontal grid spacing of 30 arc seconds. This tool provides a way to extract subsets of this data in a simple, generic ASCII XYZ format suitable for further processing or visualization in other GIS or plotting software. It handles the binary 16-bit signed integer format specific to GTOPO30.

## Output
The tool prints space-separated `latitude longitude elevation` values to standard output, which can be redirected to a file.
