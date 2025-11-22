---
layout: default
title: jwn2glo
parent: Convert Tools
grand_parent: sidescan
nav_order: 2
---
# jwn2glo

## Description
`jwn2glo` is a utility designed to convert Jacques Whitford Nortech sidescan format data to JCU GLORIA format. It handles various time and position data sources within the Nortech format, allowing for flexible conversion.

## Usage
```bash
jwn2glo [-v] [-log] [-leapyear] [-usezdatime | -usenavtime] [-usezdaDMY] [-maxpingsperfile <value>] [-range <min> <max>] [-digrate <value>] -in <infile> -out <outfile_prefix>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-log` | Apply logarithmic conversion to 16-bit data. |
| `-leapyear` | Account for a leap year when calculating Julian Day. |
| `-usezdatime` | Use ZDA time (UTC from GPS) for the GLORIA record. |
| `-usenavtime` | Use navigation time for the GLORIA record. |
| `-usezdaDMY` | Use ZDA Day, Month, Year for date calculation. |
| `-maxpingsperfile <value>` | Specifies the maximum number of pings per output GLORIA file. If exceeded, new files are created sequentially. | `0` (no limit) |
| `-range <min> <max>` | Specifies the 16-bit range for linear scaling (min and max values). | `0` (min), `0` (max) |
| `-digrate <value>` | Specifies the digitization rate. | `2400` |
| `-in <infile>` | **Required.** The input Jacques Whitford Nortech sidescan file. |
| `-out <outfile_prefix>` | **Required.** The prefix for the output JCU GLORIA files. Two files will be created: `<outfile_prefix>.100kHz.raw` and `<outfile_prefix>.500kHz.raw`. |

## How It Works
1.  **Read JWN Record:** The tool reads Jacques Whitford Nortech records from the input file. Each record contains a header (`JWN_header`) and sidescan data (`JWN_data`).
2.  **Parse Header Information:** It extracts time, date, and position information based on the chosen options (ZDA time, navigation time, CPU time).
3.  **Coordinate Conversion:** Converts UTM coordinates (easting, northing) from the header to latitude and longitude for the GLORIA record using Mercator projection.
4.  **Populate GLORIA Header:** Populates the fields of the GLORIA record header:
    *   `time`, `centisecs`: Based on selected time source.
    *   `lat`, `lon`: Converted from UTM.
    *   `small_pixel`: Calculated from `digrate`.
    *   `pixel_size`: Set to 0 (redundant in JCU GLORIA).
    *   `azi`: Calculated from compass link.
    *   `fishdepth`: From layback.
    *   `altitude`: Set to 0.0.
5.  **Convert Sidescan Data:**
    *   For each scan line (512 samples), it converts 16-bit Nortech sidescan intensity values to 8-bit GLORIA format using `convert_16bit`. This function either applies a linear scaling within a specified range or a logarithmic conversion.
    *   It populates `out_record.stbd_data` and `out_record.port_data` for both 100kHz and 500kHz data.
6.  **Write GLORIA Record:** Two GLORIA files are created: one for 100kHz data (`.100kHz.raw`) and another for 500kHz data (`.500kHz.raw`). The populated GLORIA record (`out_record`) is written to these output files.
7.  **File Splitting (Optional):** If `maxpingsperfile` is set, the tool splits the output into multiple sequential files once the ping limit is reached.
8.  **Loop:** This process repeats until the end of the input Nortech file.
