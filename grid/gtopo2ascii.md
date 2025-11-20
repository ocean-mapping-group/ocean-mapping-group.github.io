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

## Output
The tool prints space-separated `latitude longitude elevation` values to standard output, which can be redirected to a file.
