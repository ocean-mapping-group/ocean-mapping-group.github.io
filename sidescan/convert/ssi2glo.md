---
layout: default
title: ssi2glo
parent: Convert Tools
grand_parent: sidescan
nav_order: 4
---
# ssi2glo

## Description
`ssi2glo` is a utility designed to convert SSI (Side Scan International) ASCII format sidescan data to JCU GLORIA format. It reads sidescan data along with navigation and altitude information from an ASCII input file and converts it into GLORIA records.

## Usage
```bash
ssi2glo -in <infile> -out <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `-in <infile>` | **Required.** The input SSI ASCII format sidescan file. |
| `-out <outfile>` | **Required.** The output JCU GLORIA format sidescan file. |

## How It Works
1.  **Read SSI Record:** The tool reads SSI format records from the input ASCII file. Each line contains:
    *   `nosams`: Number of samples.
    *   `pixwid`: Pixel width.
    *   `easting`, `northing`: Position.
    *   `heading`: Heading.
    *   `altitude`, `depth`: Altitude and depth.
    *   Followed by `nosams` integer values representing the sidescan data.
2.  **Populate GLORIA Header:** It populates the fields of the GLORIA record header:
    *   `lat`, `lon`: Set to `northing` and `easting`.
    *   `small_pixel`: Set to `pixwid`.
    *   `pixel_size`: Set to 0.
    *   `azi`: Converted from degrees to radians.
    *   `fishdepth`: Set to `depth`.
    *   `altitude`: Set to `altitude`.
3.  **Convert Sidescan Data:**
    *   It initializes `out_record.stbd_data` to 255 (for unassigned pixels).
    *   It then populates `out_record.port_data` and `out_record.stbd_data` using the `array` values, guessing which way round the data is (port data from the first half of `array`, starboard data from the second half).
4.  **Write GLORIA Record:** The fully populated GLORIA record (`out_record`) is written to the output file.
5.  **Loop:** This process repeats until the end of the input SSI file.
6.  **Report Bounds:** After conversion, it prints the minimum and maximum northing and easting encountered.
