---
layout: default
title: editbat
parent: Sidescan Tools
grand_parent: azibat
nav_order: 2
---
# editbat

## Description
`editbat` is a utility used to edit the altitude of a JCU format sidescan image to create a more coherent image. It identifies and corrects bad depths (altitudes) by applying a median filter and replacing values that are significantly different from the median.

## Usage
```bash
editbat [-v] [-c <count>] [-t <threshold>] <infile> <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-c <count>` | The number of surrounding records to look for a good depth value when an invalid one is found. Default is `10`. |
| `-t <threshold>` | The depth threshold below which a depth value is considered bad. Default is `5.0`. |
| `<infile>` | **Required.** The input JCU format sidescan file. |
| `<outfile>` | **Required.** The output JCU format sidescan file with the corrected altitudes. |

## How It Works
1.  **Read Depths:** The tool first reads all the altitude (depth) values from the input file into an array.
2.  **Median Filtering:** It applies a median filter to the depth array. For each depth value, it calculates the median of the surrounding `median_length` (hardcoded to 10) values.
3.  **Outlier Detection:** It then compares the original depth with the median-filtered depth. If the difference is greater than 10% of the median depth, the original depth value is considered an outlier and is set to 0.
4.  **Interpolation:** The tool then iterates through the depth array again. If it finds a bad depth value (below the threshold), it searches for the nearest valid preceding and succeeding depth values within the range specified by `count`. It then performs a weighted linear interpolation between these two valid depths to calculate a new depth for the bad record.
5.  **Write Output:** Finally, the tool writes the original data with the corrected altitudes to the output file.
