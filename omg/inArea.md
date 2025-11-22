---
layout: default
title: inArea
parent: OMG Tools
nav_order: 35
---
# inArea

## Description
`inArea` is a command-line utility that checks whether one or more OMG-HDCS data files (merged files or GLORIA files) intersect with a specified geographic area of interest. It's a spatial filtering tool that helps in selecting relevant data files based on their geographic coverage.

## Usage
```bash
inArea <datafile(s)> [-array <imagefile>] [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<datafile(s)>` | **Required.** One or more OMG-HDCS merged files or GLORIA files to be checked for spatial intersection. |
| `-array <imagefile>` | Specifies a JHC image file (e.g., a map or mosaic) whose header defines the geographic area of interest. The tool reads the `xmin`, `xmax`, `ymin`, `ymax` from this header. |
| `-xyzlist <filename>` | Specifies an ASCII file containing a list of input filenames. |
| `-usebounds` | When used with merged files, this option leverages pre-computed "100-ping bounds" files (`.100ping_bounds`) to accelerate the intersection check. These files provide a spatial index for every 100 pings. |
| `-exact` | This flag is present in the `USAGE` string but its specific function in the current code's intersection logic is not explicitly defined. It might imply a more rigorous intersection test. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Define Area of Interest:** The tool first establishes the geographic boundaries of the area of interest, either by reading the header of a specified JHC image file (`-array`) or by prompting the user for coordinate input (though the interactive prompt is currently commented out in the source).
2.  **Check Intersection:** For each input data file:
    *   If it's an OMG-HDCS merged file, the tool reads its summary header to get the overall geographic bounds.
    *   If `-usebounds` is active, it further checks the more detailed 100-ping bounds files.
    *   If it's a GLORIA file, it extracts geographic information from its headers.
    *   It then determines if these data file bounds overlap with the defined area of interest.
3.  **Report:** The tool prints a message to standard output for each input file, indicating whether it intersects the specified area.
