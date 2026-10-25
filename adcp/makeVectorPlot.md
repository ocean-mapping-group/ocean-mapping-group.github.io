---
layout: default
title: makeVectorPlot
parent: ADCP Tools
nav_order: 8
tool_name: makeVectorPlot
source_path: code/adcp/makeVectorPlot.c
category: adcp
input_formats:
  - JHC Float Velocity Array (.r4)
output_formats:
  - JHC 8-bit Vector Plot Image
related_tools:
  - readADCP
  - mapGenericADCP
---

# makeVectorPlot

## Description
`makeVectorPlot` is a command-line utility that creates an 8-bit graphical stick/bar vector plot from distance-averaged ADCP (Acoustic Doppler Current Profiler) `.r4` velocity sections. It reads a JHC-formatted floating-point velocity array and generates a vertically stretched 8-bit JHC image where vertical bars or lines represent current speed and sign at each depth layer and horizontal bin.

## Usage
```bash
makeVectorPlot -in <infile> -out <outfile> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-in <infile>` | **Required.** Input JHC `.r4` file containing the ADCP velocity section. | `-in adcp_vectors.r4` |
| `-out <outfile>` | **Required.** Output 8-bit JHC image file. | `-out vector_plot.8bit` |
| `-max_vector <m/s>` | Maximum current velocity (in m/s) for full-scale vector length. | `1.0` |
| `-pixels_per_vector <number>` | Number of vertical pixels allocated per input depth row in the stretched output image. | `10` |
| `-lines` | Draw vectors as thin vertical lines rather than filled grey bars. | |
| `-double_width` | Doubles the rendered vector length relative to `pixels_per_vector`. | |
| `-depth_average <meters>` | Vertical depth averaging parameter (in meters). | `2.0` |

## How It Works

1.  **Read Input Data:** Reads the JHC header and floating-point velocity grid from `-in`.
2.  **Allocate Stretched Canvas:** Allocates an 8-bit output buffer whose height is `dy * pixels_per_vector`.
3.  **Render Vectors:** For each depth row, draws a horizontal zero-velocity baseline and renders vertical bars/lines proportional to `velocity / max_vector` (downward for positive flow, upward for negative flow).
4.  **Write Output:** Writes the rendered 8-bit JHC raster to `-out`.
