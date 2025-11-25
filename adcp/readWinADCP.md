---
layout: default
title: readWinADCP
parent: ADCP Tools
nav_order: 14
---

# readWinADCP

## Description
`readWinADCP` is a command-line utility specifically designed to read and process ASCII data files exported from RDI's WinADCP software. Unlike other ADCP tools that handle more standardized formats, this program is built for a specific, user-defined ASCII layout and is primarily used for data conversion and temporal averaging (stacking).

The tool reads ADCP ensembles from the text file, averages them together in groups (stacks), and outputs the resulting averaged profiles into a series of individual text files and a single binary file representing the velocity magnitude.

## Usage
```bash
readWinADCP -in <infile> -out <outfile> -nobins <num> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-in <infilename>` | **Required.** The single input ASCII file exported from WinADCP. |
| `-out <outfilenameprefix>` | **Required.** Specifies the prefix for the output files. |
| `-nobins <number>` | **Required.** The number of depth bins present in each ensemble in the input file. |
| `-stack <number>` | The number of input ensembles to average (stack) into a single output profile. Default is `1`. |
| `-start_rec <number>` | The first ensemble record number to start processing from. |
| `-end_rec <number>` | The last ensemble record number to process. |
| `-first_depth <meters>`| The depth of the center of the first bin, in meters. |
| `-depth_step <meters>`| The vertical size of each depth bin, in meters. |
| `-maxvel <m/s>` | The maximum velocity (in m/s) used for scaling the `.mag` output file. Default is `1.0`. |
| `-minvel <m/s>` | The minimum velocity (in m/s) for scaling. Default is `0.0`. |
| `-v` | Enable verbose output. |

## Input Format
This tool is sensitive to the input file's format. It expects a file with:
1.  A 16-line header which is skipped.
2.  Data lines where each line represents one ensemble.
3.  Each data line is expected to be tab-delimited and contain columns for timestamp, average backscatter for each bin, velocity magnitude for each bin, and velocity azimuth for each bin.

## How It Works

1.  **Skip Header:** The tool begins by skipping the first 16 lines of the input file, assuming it to be a header.
2.  **Read Ensembles:** It then reads the file line by line, parsing each line as a single ADCP ensemble. For each bin, it reads the backscatter, velocity, and azimuth values.
3.  **Stacking:** The North and East velocity components are calculated from the magnitude and azimuth. These components, along with the backscatter, are summed over the number of ensembles specified by the `-stack` argument.
4.  **Averaging:** Once a full stack is accumulated, the tool calculates the average N/E velocities and backscatter for each bin. From the averaged components, it re-calculates the final velocity magnitude and azimuth for the stacked profile.
5.  **Write Output:**
    *   An ASCII file is created for each stack (e.g., `<outfile>.stack0000`, `<outfile>.stack0001`, etc.). Each file contains the averaged profile, with one line per bin showing the stack count, depth, velocity magnitude, and azimuth.
    *   A single binary file (`<outfile>.mag`) is also created. For each stack, it writes a profile of 8-bit velocity magnitude values, which have been scaled according to `-minvel` and `-maxvel` and interpolated to 10x the original bin resolution. This `.mag` file can be used for imaging.

This process effectively reduces the temporal resolution of the dataset while averaging out noise, producing a series of cleaned, averaged profiles.