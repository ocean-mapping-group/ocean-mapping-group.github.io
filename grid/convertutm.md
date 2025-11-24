---
layout: default
title: convertutm
parent: Grid Tools
nav_order: 15
---
---
layout: default
title: convertutm
parent: Grid Tools
nav_order: 15
---
# convertutm

## Description
`convertutm` is a versatile command-line utility for converting geographical coordinates between different formats and projections. Primarily, it converts input data (read from `stdin`) from UTM (Universal Transverse Mercator) or other Cartesian-like coordinates to Latitude/Longitude, or vice-versa, and can also handle specific grid formats like USGS weird and Nbstereo. It supports various input data formats (e.g., DMS to DD, comma-separated, or standard space-separated XYZ). The output is written to `stdout`.

## Usage
```bash
convertutm [OPTIONS] < input > output
```
Input data is read from `stdin` and output is written to `stdout`.

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-usgsweird <cenmer> <scalelat>` | Interprets input data as USGS weird format, using `<cenmer>` (central meridian) and `<scalelat>` (scale latitude) for Mercator initialization. | `-usgsweird -69 45.83` |
| `-nad27` | Use the NAD27 ellipsoid for conversions instead of the default WGS84. | |
| `-geoutm` | Perform Latitude/Longitude to UTM conversion. Input is Lat Lon Z. Output is X Y Z. | |
| `-nbstereo` | Use the Nbstereo projection system for conversions. | |
| `-eastshift <value>` | Apply an eastward shift (in meters) to UTM X-coordinates before conversion. | `500000` |
| `-commas` | Expects comma-separated input values (X,Y,Depth) instead of space-separated. | |
| `-merid <value>` | Specifies the central meridian (longitude) for UTM conversions. | `-69` |
| `-dms_to_dd` | Convert Degrees, Minutes, Seconds input format (Lat Deg, Lat Min, Lat Sec, Lon Deg, Lon Min, Lon Sec, Label) to Decimal Degrees output. | |
| `-xyonly` | Process only X and Y coordinates (ignoring Depth) from input, outputting Lat Lon 0.0. | |
| `-xlen <value>` | (Internal/Legacy, not directly used for conversion logic in parsed section). | |
| `-ylen <value>` | (Internal/Legacy, not directly used for conversion logic in parsed section). | |
| `-christos` | (Internal/Legacy, specific input format handling, reads until a `|` character). | |
| `-spacing <value>` | (Internal/Legacy, spacing parameter, not directly used for conversion logic in parsed section). | |
| `-colorbar` | (Internal/Legacy, relates to colorbar generation, not directly used for conversion logic in parsed section). | |
| `-out <filename>` | (Internal/Legacy, directs output to a file instead of stdout, but primary usage is `> output`). | |

## How It Works
`convertutm` reads coordinate data from standard input, processes it based on the specified command-line options, and writes the converted coordinates to standard output.
1.  **Coordinate System Setup:** Initializes projection parameters (e.g., Mercator, UTM, Nbstereo) and ellipsoid (WGS84, NAD27) based on command-line flags.
2.  **Input Parsing:** Reads each line of input, interpreting the format based on flags like `-dms_to_dd` or `-commas`.
3.  **Conversion:**
    *   **UTM to Lat/Lon (default):** If input is UTM (X, Y) and output is Lat/Lon, it uses `inv_proj` to convert.
    *   **Lat/Lon to UTM (`-geoutm`):** If input is Lat/Lon and output is UTM, it uses `Project` to convert.
    *   **DMS to DD (`-dms_to_dd`):** Converts Degrees, Minutes, Seconds format to Decimal Degrees.
    *   Other conversions (USGS weird, Nbstereo) use specific internal logic.
4.  **Offset/Shift:** Applies `eastshift` to UTM X-coordinates before conversion if specified.
5.  **Output:** Writes the converted coordinates to standard output.

## Output Files
The tool writes converted coordinates to standard output. This output can be redirected to a file.

## Dependencies
*   `j_proj.h`: For coordinate projection functions (`Project`, `inv_proj`).
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is flexible but relies on an understanding of coordinate systems and projection parameters. It's best used in scripting workflows where coordinate transformations are needed between different data processing steps. Some options are legacy and might not be fully functional or documented in the latest code.
