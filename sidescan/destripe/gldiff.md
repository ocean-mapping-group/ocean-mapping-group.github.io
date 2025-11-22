---
layout: default
title: gldiff
parent: Destripe Tools
grand_parent: sidescan
nav_order: 5
---
# gldiff

## Description
`gldiff` is a utility designed to calculate and visualize the difference between two JCU GLORIA format merged sidescan files. It typically compares a backscatter file (`.bksct`) with a synthetic file (`.synth`) to produce a difference image (`.diff`), handling specific unique identifiers provided by the `offtrack` program.

## Usage
```bash
gldiff [-weight1 <value>] [-weight2 <value>] <infile_prefix>
```

## Arguments

| Option | Description |
|---|---|
| `-weight1 <value>` | Weight for the first input file (not currently used in the logic). |
| `-weight2 <value>` | Weight for the second input file (not currently used in the logic). |
| `<infile_prefix>` | **Required.** The prefix for input files. The tool assumes `<infile_prefix>.bksct` and `<infile_prefix>.synth` as input, and will output to `<infile_prefix>.diff`. |

## How It Works
1.  **Input Files:** The tool reads two JCU GLORIA files: the first from `<infile_prefix>.bksct` and the second from `<infile_prefix>.synth`.
2.  **File Length Check:** It determines the number of records in the input files, assuming they have the same length.
3.  **Pixel-wise Difference:** For each corresponding pixel across all records:
    *   It checks if the pixel value in the first input file (`in_rec1.stbd_data[k]`) is within a valid range (between 16 and 254).
    *   If valid, it calculates the difference between the two input pixel values, centered around 128:
        `stbd_value = 128 + (int)in_rec1.stbd_data[k] - (int)in_rec2.stbd_data[k];`
    *   The resulting `stbd_value` is clamped to be between 16 and 254.
    *   If the original `in_rec1` pixel was outside the valid range (16-254) or 255, the output pixel retains the value from `in_rec1`.
4.  **Header Copy:** The header information for the output record (`out_rec`) is copied from the first input record (`in_rec1`).
5.  **Write Output:** The resulting difference record (`out_rec`) is written to the output file (`.diff`).
6.  **Loop:** This process repeats until all records from both input files have been processed.
