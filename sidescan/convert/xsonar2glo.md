---
layout: default
title: xsonar2glo
parent: Convert Tools
grand_parent: sidescan
nav_order: 6
---
# xsonar2glo

## Description
`xsonar2glo` is a utility designed to convert XSONAR merged GLORIA data to JCU GLORIA format. It handles XSONAR ping records, extracts navigation, attitude, and sidescan data, performs byte swapping if necessary, and converts it into GLORIA records.

## Usage
```bash
xsonar2glo [-merid <value>] [-timeseries] [-reverse] [-in <infile>] -out <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `-merid <value>` | Specifies the central meridian for UTM zone calculations. Default is automatically determined. | `-999.0` (default) |
| `-timeseries` | Process data as time series. |
| `-reverse` | If specified, the tool will attempt to convert from JCU GLORIA to XSONAR format (currently not fully implemented). |
| `-swapXS` | Perform byte swapping (default is determined by system endianness). |
| `-in <infile>` | **Required.** The input XSONAR GLORIA file. |
| `-out <outfile>` | **Required.** The output JCU GLORIA format sidescan file. |

## How It Works
1.  **Read XSONAR Record:** The tool reads XSONAR ping records from the input file. Each record contains a header (`PingHeader`) and raw sidescan data (port and starboard).
2.  **Byte Swapping:** It performs byte swapping on various fields of the `PingHeader` and data arrays if the byte order of the input file differs from the system's endianness.
3.  **Time Conversion:** Converts the XSONAR date and time fields into a Unix timestamp for the GLORIA record.
4.  **Coordinate Conversion:** Converts UTM coordinates (northing, easting) from the XSONAR header to latitude and longitude for the GLORIA record using Mercator projection.
5.  **Populate GLORIA Header:** Populates the fields of the GLORIA record header:
    *   `time`, `centisecs`: From converted XSONAR time.
    *   `lat`, `lon`: Converted from XSONAR UTM coordinates.
    *   `small_pixel`: Calculated based on swath width and number of samples.
    *   `pixel_size`: Set to 0.
    *   `azi`: From `fish_azi` in the XSONAR header.
    *   `fishdepth`: From `depth` in the XSONAR header.
    *   `altitude`: From `alt` in the XSONAR header.
6.  **Convert Sidescan Data:** The raw sidescan data from the XSONAR record (port and starboard channels) is copied into `out_rec.port_data` and `out_rec.stbd_data` fields of the GLORIA record. It handles different `no_samples_per_side` values.
7.  **Write GLORIA Record:** The fully populated GLORIA record (`out_rec`) is written to the output file.
8.  **Loop:** This process repeats until the end of the input XSONAR file.
