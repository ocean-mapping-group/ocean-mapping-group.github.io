---
layout: default
title: makeazi
parent: Sidescan Tools
grand_parent: azibat
nav_order: 6
---
# makeazi

## Description
`makeazi` is a utility used to make the azimuth of a JCU format sidescan image for the USGS case where none is provided. It calculates the azimuth based on the course made good between consecutive records.

## Usage
```bash
makeazi [-v] [-t <threshold>] <infile> <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-t <threshold>` | This option is present in the `USAGE` string but is not implemented in the `main` function. |
| `<infile>` | **Required.** The input JCU format sidescan file. |
| `<outfile>` | **Required.** The output JCU format sidescan file with the calculated azimuths. |

## How It Works
1.  **Read Coordinates:** The tool first reads all the latitude and longitude values from the input file into arrays.
2.  **Calculate Azimuth:** It then iterates through the records and calculates the change in latitude and longitude between consecutive records. It uses these differences to calculate the azimuth (course made good) for each record.
3.  **Write Output:** Finally, the tool writes the original data with the new calculated azimuths to the output file.
