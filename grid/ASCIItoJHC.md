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