---
layout: default
title: editazi
parent: Sidescan Tools
grand_parent: azibat
nav_order: 1
---
# editazi

## Description
`editazi` is a utility used to edit the azimuth of a JCU format sidescan image to create a more coherent image. It looks for singular bad azimuths (over a threshold different from both the azimuth behind and that in front). It also has an option to handle repeated azimuth values.

## Usage
```bash
editazi [-v] [-r] [-t <threshold>] <infile> <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-r` | If specified, the tool will handle repeated azimuth values by replacing them with interpolated values. |
| `-t <threshold>` | The threshold for detecting a bad azimuth. Default is `6.0`. |
| `<infile>` | **Required.** The input JCU format sidescan file. |
| `<outfile>` | **Required.** The output JCU format sidescan file with the corrected azimuths. |

## How It Works
1.  **Read Azimuths:** The tool first reads all the azimuths from the input file into an array.
2.  **Edit Azimuths:**
    *   **Default Method:** It iterates through the azimuths and checks if a single azimuth is significantly different from both its preceding and succeeding values. If the difference is greater than the specified threshold, the bad azimuth is replaced with the preceding one.
    *   **Repeat Replace Method (`-r`):** If the `-r` option is specified, the tool looks for repeated azimuths. It replaces the repeated values with linearly interpolated values between the last unique azimuth and the next unique azimuth.
3.  **Write Output:** The tool then writes the original data with the corrected azimuths to the output file.
