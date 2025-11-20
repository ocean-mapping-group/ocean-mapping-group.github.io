---
layout: default
title: edhead
parent: Grid Tools
nav_order: 23
---
# edhead

## Description
`edhead` is a powerful and versatile utility for viewing, interactively editing, and exporting metadata from the headers of JHC-format grid files. It serves as a bridge between the OMG-HDCS grid formats and external GIS applications by generating standard georeferencing files (e.g., for GeoTIFF, ESRI, KML). It can also be used to manually inspect or correct corrupted or inaccurate header information.

## Usage
`edhead` can be run in several modes:

1.  **Show Header Info:**
    ```bash
    edhead -show <grid_file>
    ```
2.  **Export Georeferencing Data:**
    ```bash
    edhead <export_option> <grid_file>
    ```
3.  **Interactive Edit:**
    ```bash
    edhead <grid_file>
    ```

## Display and Export Options

These options run non-interactively to display information or generate metadata files.

| Option | Description |
|---|---|
| `-show` | Displays the full JHC header in a human-readable format and exits. |
| `-show_dm` | Similar to `-show`, but also prints the geographic corner coordinates in Degrees and Decimal Minutes. |
| `-show_meta` | Calculates and displays the geographic coordinates (Lat/Lon) of all four corners of the grid. |
| `-dump_tfw` | Creates a World File (`.tfw`) for the grid. This is a standard sidecar file for georeferencing raster images in GIS software. |
| `-dump_geotiff` | Creates a metadata file (`.geo_meta`) containing the tags and keys needed to georeference the grid as a proper GeoTIFF. |
| `-dump_esri_grid` | Creates an ASCII header file (`.esri_grid`) that is compatible with ESRI's grid format. |
| `-dump_kml_groundoverlay` | Creates a KML file (`.kml`) to display the grid as a ground overlay in Google Earth. Supports rotated grids. |
| `-clamptoseafloor` | Used with `-dump_kml_groundoverlay`. Sets the KML altitude mode to `clampToSeaFloor`, draping the image over the seafloor bathymetry in Google Earth. |
| `-addCentreMark` | Used with `-dump_kml_groundoverlay`. Adds a placemark at the center of the KML overlay. |
| `-center` | When dumping georeferencing info (e.g., `-dump_tfw`), this specifies that the origin coordinates should refer to the **center** of the top-left pixel. The default is the top-left **corner**, which is standard for most GIS software. |
| `-proj_long <longitude>` | Specifies the projection longitude to be used when exporting georeferencing for Mercator-projected grids. Essential for ensuring correct alignment in external programs. |

## File Manipulation Options

| Option | Description |
|---|---|
| `-replacehead <source_grid_file>` | Copies the header from `<source_grid_file>` and overwrites the header of the main input grid file. |
| `-fix_Y` | Recalculates the number of rows (`dy`) in the grid based on the file size and data type, then corrects the header. This is useful for fixing headers of truncated or corrupted files. |

## Interactive Mode
If `edhead` is run with only a filename as an argument, it enters an interactive menu-driven mode. This allows the user to manually change any field in the header, such as:
*   Grid dimensions (`dx`, `dy`)
*   Geographic boundaries (`ymax`, `ymin`, `xmax`, `xmin`)
*   Pixel size (`xstep`, `ystep`)
*   Data type (8-bit, 16-bit, float)
*   Projection information
*   Labels and descriptive text

This mode is intended for manual inspection and correction of grid metadata.
