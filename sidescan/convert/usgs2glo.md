---
layout: default
title: usgs2glo
parent: Convert Tools
grand_parent: sidescan
nav_order: 5
---
# usgs2glo

## Description
`usgs2glo` is a utility designed to convert USGS merged GLORIA data to JCU GLORIA format. It is designed to work with ASCII header files and raw imagery, and can handle VAX byte order conversion to IEEE format.

## Usage
```bash
usgs2glo -in <infile_prefix> -out <outfile> [-ping_rate <value>]
```

## Arguments

| Option | Description |
|---|---|
| `-in <infile_prefix>` | **Required.** The prefix for the input USGS files. The tool expects to find an ASCII header file (`<infile_prefix>.hdr`) and a raw imagery file (`<infile_prefix>.img`). |
| `-out <outfile>` | **Required.** The output JCU GLORIA format sidescan file. |
| `-ping_rate <value>` | Specifies the ping rate. Default is `20`. |

## How It Works
1.  **Read Header and Imagery Data:** The tool reads an ASCII header file (`.hdr`) and a raw imagery file (`.img`). The header file contains ping-specific information such as time, position (latitude, longitude), heading, and depth. The imagery file contains the raw 8-bit sidescan data.
2.  **Populate GLORIA Header:** For each record, it populates the fields of the GLORIA record header:
    *   `time`, `centisecs`: Derived from the time information in the header file.
    *   `lat`, `lon`: From the header file.
    *   `ping_rate`: Set by the `-ping_rate` option.
    *   `small_pixel`, `pixel_size`: Calculated based on ping rate.
    *   `azi`: Converted from heading in the header file (degrees to radians).
    *   `fishdepth`: Set to `FISDEP` (80).
    *   `altitude`: Calculated from uncorrected depth minus `FISDEP`.
3.  **Convert Sidescan Data:** The raw 8-bit sidescan data from the imagery file is copied into `out_record.stbd_data` (specifically `out_record.stbd_data[16]` onwards).
4.  **Write GLORIA Record:** The fully populated GLORIA record (`out_record`) is written to the output file.
5.  **Loop:** This process repeats until the end of the input imagery file.
6.  **VAX to IEEE Conversion (Legacy):** The code includes functions (`swap_2bytes`, `swap_4bytes`, `vax2ieee`) for handling VAX byte order to IEEE format conversion, which were likely used for direct binary data reading in older versions.
