---
layout: default
title: gldropStripes
parent: Destripe Tools
grand_parent: sidescan
nav_order: 6
---
# gldropStripes

## Description
`gldropStripes` is a utility designed to detect and remove "black stripes" (anomalously low-intensity pings) from JCU GLORIA format sidescan files. It achieves this by calculating an average intensity within a specified inboard and outboard range for each ping, then comparing this average to a running median. Pings that deviate significantly from the median are considered striped and are rejected from the output.

## Usage
```bash
gldropStripes [-inboard <value>] [-outboard <value>] [-median <value>] [-reject <value>] [-verbose] -in <infile> -out <outfile>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-inboard <value>` | Specifies the inner boundary (sample number) of the zone used for calculating average intensity. | `50` |
| `-outboard <value>` | Specifies the outer boundary (sample number) of the zone used for calculating average intensity. | `200` |
| `-median <value>` | Specifies the number of pings to use for estimating the running median intensity. | `9` |
| `-reject <value>` | Specifies the threshold (in Digital Number - DN values) for rejecting a ping. Pings whose average intensity deviates from the median by more than this value are rejected. | `5` |
| `-verbose` | Enable verbose output, showing ping-by-ping averages, medians, and differences. | (None) |
| `-in <infile>` | **Required.** The input JCU GLORIA format sidescan file. |
| `-out <outfile>` | **Required.** The output JCU GLORIA format sidescan file with rejected pings removed. |

## How It Works
1.  **Calculate Ping Averages (`Taverage`):**
    *   The tool reads through the input GLORIA file ping by ping.
    *   For each ping, it calculates the average pixel intensity within the specified `inboard` and `outboard` range (considering both port and starboard data). Pixels with a value of 255 are ignored.
    *   These average intensities are stored in the `Taverage` array.
2.  **Calculate Running Median (`Tmedian`):**
    *   It then calculates a running median of the `Taverage` values. The `-median` parameter determines the window size for this median calculation.
    *   Edge cases for the median calculation (beginning and end of the file) are handled by extending the median value.
3.  **Detect and Reject Stripes (`Tdiff`):**
    *   For each ping, it calculates the difference (`Tdiff`) between its average intensity (`Taverage`) and the running median (`Tmedian`).
    *   If the absolute value of `Tdiff` is greater than the `-reject` threshold, the ping is considered to contain a "black stripe" and is *not* written to the output file.
    *   If the deviation is within the threshold, the original ping is written to the output file.
4.  **Output:** Only the pings that pass the rejection criteria are written to the output GLORIA file. A summary of the percentage of rejected pings is printed.
