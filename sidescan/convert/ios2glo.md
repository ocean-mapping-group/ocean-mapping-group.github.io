---
layout: default
title: ios2glo
parent: Convert Tools
grand_parent: sidescan
nav_order: 1
---
# ios2glo

## Description
`ios2glo` is a utility designed to convert IOS (Institute of Ocean Sciences) format sidescan data to the JCU GLORIA format.

## Usage
```bash
ios2glo -in <infile> -out <outfile> [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-in <infile>` | **Required.** The input IOS format sidescan file. |
| `-out <outfile>` | **Required.** The output JCU GLORIA format sidescan file. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Read IOS Record:** The tool reads IOS format records from the input file, each record being 1024 bytes long.
2.  **Parse Header Information:** From the IOS record, it parses:
    *   `heading`: Vessel heading.
    *   `year`, `jday`, `hour`, `min`, `secs`: Time information.
3.  **Convert Sidescan Data:** It extracts the port and starboard sidescan data from the IOS record and rearranges it to fit the GLORIA format (`out_record.stbd_data` and `out_record.port_data`).
4.  **Populate GLORIA Header:** The tool populates the fields of the GLORIA record header:
    *   `time`: Converted from year, jday, hour, min, secs to a Unix timestamp.
    *   `lat`, `lon`: Set to 0.0 (as IOS format doesn't seem to provide these in this context).
    *   `ping_rate`: Set to 20.
    *   `small_pixel`, `pixel_size`: Set to 0.
    *   `azi`: Converted from degrees to radians.
    *   `fishdepth`: Set to 80.0.
    *   `altitude`: Set to 0.0.
5.  **Write GLORIA Record:** The fully populated GLORIA record (`out_record`) is written to the output file.
6.  **Loop:** This process repeats until the end of the input IOS file.
