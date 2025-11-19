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