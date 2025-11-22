---
layout: default
title: mapmos
parent: Mapmos Tools
grand_parent: sidescan
nav_order: 1
---
# mapmos

## Description
`mapmos` is a utility for creating mosaics and visualizing the navigation tracks of JCU GLORIA/MR1 format sidescan files. It allows for various map projections, scaling, and the ability to highlight discontinuities (jumps) in azimuth, time, and distance between consecutive records. It can also overlay coastlines and grid lines.

## Usage
```bash
mapmos -merc <lat> -ll <lon> <lat> -ur <lon> <lat> -scale <value> [-grid <align>] [-azi <offset>] [-notime] [-nolabel] [-noflag] [-title <string>] [-first <nnnn>] [-last <mmmm>] [-coast <filename> <pen#>] <file1> [file2 ...]
```

## Arguments

| Option | Description |
|---|---|
| `-merc <lat>` | **Required.** Use a Mercator projection with the specified decimal projection latitude. |
| `-ll <lon> <lat>` | **Required.** Define the lower-left coordinates (longitude and latitude) of the map area. |
| `-ur <lon> <lat>` | **Required.** Define the upper-right coordinates (longitude and latitude) of the map area. |
| `-scale <value>` | **Required.** Set the overall scaling factor for the plot. |
| `-grid <align>` | Draw a grid with the specified decimal alignment interval. |
| `-azi <offset>` | Add an offset to the azimuth values (in degrees). |
| `-notime` | Suppress time labels on the plot. |
| `-nolabel` | Suppress file name labels on the plot. |
| `-noflag` | Suppress flags indicating jumps (azimuth, time, distance). |
| `-title <string>` | Add a title to the map. |
| `-first <nnnn>` | Specify the first record number to use from each input file. |
| `-last <mmmm>` | Specify the last record number to use from each input file. |
| `-coast <filename> <pen#>` | Include coastlines from the specified file, drawn with the given pen number. |
| `<file1> [file2 ...]` | **Required.** One or more input JCU GLORIA files whose tracks will be plotted. |

## How It Works
1.  **Initialization and Argument Parsing:** The tool parses command-line arguments to set up projection parameters, map boundaries, scaling, and various plotting options.
2.  **Mercator Projection Setup:** It initializes the Mercator projection using `merc_init` based on the provided reference latitude and scale.
3.  **Plot Setup:** It opens a plot device (`plot_open`) with dimensions derived from the map boundaries, generating a Metafile output (e.g., `mosaicmap.meta`). It draws a bounding box and adds an optional title.
4.  **Coastline Overlay (Optional):** If a coastline file is provided, it calls `add_coastline` to draw geographical features within the specified map area.
5.  **Process Sidescan Files (`markregion` function):**
    *   The tool iterates through each input GLORIA file provided.
    *   For each file, it reads all records, extracting navigation (latitude, longitude, azimuth, time) and calculating the swath width.
    *   It converts latitude and longitude to projected X, Y coordinates using the Mercator projection.
    *   For each record, it calculates the coordinates of the port and starboard edges of the swath.
    *   **Jump Detection:** It compares consecutive records to detect "jumps" or discontinuities based on:
        *   `AZI_THRESH`: Azimuth difference threshold.
        *   `TIME_THRESH`: Time difference threshold.
        *   `DIST_THRESH`: Distance difference threshold.
        *   These jumps are stored as `skip` flags for each record.
    *   **Plotting Tracks:** It then iterates through the records again, drawing the sidescan swath as a filled polygon.
        *   When a jump is detected, the current polygon segment ends, and a new one begins, effectively separating continuous tracks.
        *   Labels indicating the type of jump (Time, Azimuth, Distance) can be plotted.
6.  **Labels and Annotations:**
    *   Time labels are placed at the start and end of each continuous segment of the track (if `timelabel` is true).
    *   File names are labeled on the track (if `filelabel` is true).
7.  **Grid Overlay (Optional):** If a grid alignment is specified, `grid` function draws latitude and longitude lines.
8.  **Output:** The generated plot is saved as a Metafile.
