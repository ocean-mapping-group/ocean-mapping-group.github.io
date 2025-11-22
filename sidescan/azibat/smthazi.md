---
layout: default
title: smthazi
parent: Sidescan Tools
grand_parent: azibat
nav_order: 8
---
# smthazi

## Description
`smthazi` is a utility used to smooth the azimuth of a JCU format sidescan image to create a more coherent image. It applies a low-pass filter to the azimuth data, taking care not to smooth over large azimuth changes or time steps, which might indicate a corner or a period of non-transmission.

## Usage
```bash
smthazi [-v] [-l] [-f <filter_size>] [-t <threshold>] <infile> <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-l` | If specified, the tool will list the timestamps and azimuths to standard output. |
| `-f <filter_size>` | The size of the low-pass filter to apply. The filter window will be `2 * filter_size + 1`. Default is `10`. |
| `-t <threshold>` | The threshold for detecting a discontinuity in the azimuth data. If the change in azimuth between two consecutive records is greater than this threshold, the filter will not be applied across the discontinuity. Default is `6.0`. |
| `<infile>` | **Required.** The input JCU format sidescan file. |
| `<outfile>` | **Required.** The output JCU format sidescan file with the smoothed azimuths. |

## How It Works
1.  **Read Azimuths:** The tool first reads all the azimuth values from the input file into an array.
2.  **Low-Pass Filter:** It then applies a low-pass filter to the azimuth data. For each azimuth value, it calculates a weighted average of the surrounding azimuths within the specified filter window. The tool is designed to not smooth over large changes in azimuth (corners) or time gaps. It does this by converting the azimuths to vectors, summing the vectors, and then converting the resultant vector back to an azimuth.
3.  **Write Output:** Finally, the tool writes the original data with the new smoothed azimuths to the output file.
