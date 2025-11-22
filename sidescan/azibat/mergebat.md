---
layout: default
title: mergebat
parent: Sidescan Tools
grand_parent: azibat
nav_order: 7
---
# mergebat

## Description
`mergebat` is a utility used to merge altitude data into a JCU format sidescan image. The tool takes a "pick file" (which is actually a mask file from `jview`) containing a series of picks (x, y coordinates) and interpolates these picks to generate a new altitude profile. This new profile is then written into the header of the JCU sidescan file.

## Usage
```bash
mergebat [-v] [-s] [-c <count>] [-t <threshold>] <infile> <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-s` | If specified, the tool will write a blue line into the sidescan image at the location of the new altitude profile. |
| `-c <count>` | This option is present in the `USAGE` string but is not implemented in the `main` function. |
| `-t <threshold>` | This option is present in the `USAGE` string but is not implemented in the `main` function. |
| `<infile>` | **Required.** The input pick file (mask file from `jview`). |
| `<outfile>` | **Required.** The JCU format sidescan file to be modified. This file is modified in place. |

## How It Works
1.  **Read Picks:** The tool reads the pick data from the input file. The pick file is expected to contain the dimensions of the image, the number of picks, and the x, y coordinates of each pick.
2.  **Read Altitudes:** It then reads the original altitude values from the output JCU sidescan file.
3.  **Interpolate Altitudes:** The tool iterates through each record of the sidescan file and, for each record, it finds the two nearest picks in the pick file. It then performs a linear interpolation between these two picks to calculate a new altitude value for the current record.
4.  **Write Output:** Finally, the tool writes the new interpolated altitude values back into the `altitude` field of the header of each record in the JCU sidescan file. If the `-s` option is specified, it also modifies the image data to draw a blue line at the location of the new altitude profile.
