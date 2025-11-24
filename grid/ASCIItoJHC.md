---
layout: default
title: ASCIItoJHC
parent: Grid Tools
nav_order: 8
---
---
layout: default
title: ASCIItoJHC
parent: Grid Tools
nav_order: 8
---
# ASCIItoJHC

## Description
`ASCIItoJHC` is a versatile command-line utility for converting various ASCII (and some binary) gridded XYZ data formats into a JHC-format 32-bit floating-point (`.r4`) grid file. It supports numerous input formats including generic ASCII (Jarvis GSJ-like), NOAA, Larry's custom format, GMT-ish, Canadian 3D, and NTDB. It also has specific options for handling different data types (16-bit, 32-bit integers, or floats) within binary grid files. The tool can project coordinates (e.g., lat/lon to UTM), define grid dimensions and spacing, and handle invalid data values.

## Usage
```bash
ASCIItoJHC [OPTIONS] <input_ASCII_file> <output_JHC_file.r4>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `<input_ASCII_file>` | **Required.** The path to the input ASCII (or binary, depending on flags) grid file. | `data.txt` |
| `<output_JHC_file.r4>` | **Required.** The path for the output JHC-format 32-bit floating-point grid file. | `output_grid.r4` |
| `-lld` | Output Lat/Lon/Depth triplets (ASCII) instead of a JHC grid file. | |
| `-larry` | Input file is in Larry's custom ASCII format (Lat Lon Z). | |
| `-gmt_ish` | Input file is in a GMT-like ASCII format. | |
| `-int16` | Input data (for non-ASCII formats) is 16-bit signed integers. | |
| `-uint16` | Input data (for non-ASCII formats) is 16-bit unsigned integers (used with `-int16`). | |
| `-int32` | Input data (for non-ASCII formats) is 32-bit signed integers. | |
| `-float` | Input data (for non-ASCII formats) is 32-bit floats. | |
| `-extra_swap` | Perform an extra byte swap on input data (useful for cross-platform binary data). | |
| `-gpsh` | Input file is in a specific binary 16-bit GPS-H DTM format (Geodetic Survey of Canada). | |
| `-can3d` | Input file is in a Canada 3D DTM format. | |
| `-aschdr` | Input file is an ASC grid with a header. | |
| `-ntdb` | Input file is in NTDB DTM format. | |
| `-keep_zero` | If a grid value is 0.0, convert it to a very small positive number (0.000000001) instead of treating it as no data. | |
| `-flipdepth` | Invert the sign of the depth values. | |
| `-mirror_NS` | Mirror the grid data North-South (useful for GMT files). | |
| `-seek_bytes <value>` | Seek forward by `<value>` bytes in the input file before reading data. | `0` |
| `-invalid <value>` | Specifies a value in the input file to be treated as an "invalid" or "no data" value. These values will be converted to `0.0` in the output JHC grid. | `-32767` |
| `-noaa` | Input file is in NOAA DTM format. | |
| `-wcoast` | Input file is in West Coast DTM format. | |
| `-evspec` | Input file is in Evolutionary Spectra format. | |
| `-skipline <num_lines>` | Skip the first `<num_lines>` in the input file before processing data. | `0` |
| `-llon <value>` | Longitude of the left edge (western boundary) of the grid. | `0` |
| `-rlon <value>` | Longitude of the right edge (eastern boundary) of the grid. | `0` |
| `-tlat <value>` | Latitude of the top edge (northern boundary) of the grid. | `0` |
| `-blat <value>` | Latitude of the bottom edge (southern boundary) of the grid. | `0` |
| `-low <value>` | (Not implemented in the provided code snippet for clipping, likely a placeholder or legacy). | `0` |
| `-high <value>` | (Not implemented in the provided code snippet for clipping, likely a placeholder or legacy). | `0` |
| `-dx <value>` | Explicitly specify the X-dimension (number of columns) of the grid. Required if not implied by format flag. | |
| `-dy <value>` | Explicitly specify the Y-dimension (number of rows) of the grid. Required if not implied by format flag. | |
| `-xstep <value>` | Explicitly specify the X-axis grid spacing. | `0` |
| `-ystep <value>` | Explicitly specify the Y-axis grid spacing. | `0` |
| `-merid <value>` | Specify the central meridian for Mercator projection when converting lat/lon data. | `0` |
| `-v` | Enable verbose output during processing. | |

## How It Works
1.  **Argument Parsing:** Parses command-line arguments to determine input/output file names, format flags, coordinate projection parameters, and grid dimensions.
2.  **Input File Reading:** Opens the input ASCII (or binary) file.
3.  **Header Initialization:** Initializes an `JHC_header` structure for the output `.r4` grid, setting dimensions, geographic bounds, and data type based on command-line arguments or inferred from the input.
4.  **Data Conversion Loop:** Reads data from the input file based on the specified format:
    *   **ASCII Formats:** Parses space- or comma-separated XYZ values.
    *   **Binary Formats:** Reads 16-bit or 32-bit integer/float values, handling byte swapping as needed.
    *   **Coordinate Projection:** If input is lat/lon and output is a projected grid, it converts lat/lon to UTM or Mercator projected coordinates.
    *   **Data Manipulation:** Applies `flipdepth`, `mirror_NS`, and `keep_zero` as specified.
    *   **Invalid Data Handling:** Converts values matching `invalid_val` to `0.0` in the output.
5.  **Output Writing:** Writes the populated `JHC_header` and the processed float data to the output `.r4` file.
6.  **`lld` Mode:** If `-lld` is specified, it directly outputs Lat/Lon/Depth triplets to standard output, skipping grid generation.

## Output Files
*   `<output_JHC_file.r4>`: A JHC-format 32-bit floating-point grid file (`.r4`).
*   (If `-lld` is used): Standard output of `latitude longitude depth` triplets.

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions.
*   `support.h`: For general utility functions and error handling.
*   `jb_endian.h`: For byte swapping.
*   `j_proj.h`: For coordinate projection functions.

## Notes
This tool is crucial for preparing non-standard grid data for use within the JHC/OMG processing ecosystem. It provides flexibility in handling a wide variety of input formats and coordinate systems.
