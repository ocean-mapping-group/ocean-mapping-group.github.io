---
layout: default
title: readWinADCP
parent: ADCP Tools
nav_order: 14
tool_name: readWinADCP
source_path: code/adcp/readWinADCP.c
category: adcp
input_formats:
  - WinADCP Tabular ASCII Export
output_formats:
  - JHC 8-bit Velocity Magnitude Image (.mag)
  - Per-Stack ASCII Profiles (.stack####)
related_tools:
  - readADCP
---

# readWinADCP

## Description
`readWinADCP` is a command-line utility designed to read and stack tabular ASCII data files exported from Teledyne RDI's WinADCP software. It reads ADCP ensembles from the text file, vector-averages the North and East velocity components and backscatter over groups of `-stack <N>` ensembles, and outputs both per-stack ASCII profile tables (`<outfile>.stack####`) and an 8-bit JHC velocity magnitude image (`<outfile>.mag`).

## Usage
```bash
readWinADCP -in <infile> -out <outfile> -nobins <num> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-in <infilename>` | **Required.** Input tabular ASCII file exported from WinADCP. |
| `-out <outfilenameprefix>` | **Required.** Prefix for the output `.mag` and `.stack####` files. |
| `-nobins <number>` | **Required.** Number of vertical depth bins per ensemble in the input file. |
| `-stack <number>` | Number of consecutive input ensembles to average into a single output profile (default `1`). |
| `-start_rec <number>` | First ensemble record number to process. |
| `-end_rec <number>` | Last ensemble record number to process. |
| `-first_depth <meters>`| Depth of the center of the first vertical bin, in meters. |
| `-depth_step <meters>`| Vertical spacing of each depth bin, in meters. |
| `-maxvel <m/s>` | Maximum velocity (in m/s) used for scaling the 8-bit `.mag` output file (default `1.0`). |
| `-minvel <m/s>` | Minimum velocity (in m/s) for scaling (default `0.0`). |
| `-v` | Enable verbose output. |
