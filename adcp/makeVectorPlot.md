---
layout: default
title: makeVectorPlot
parent: ADCP Tools
nav_order: 8
---

# makeVectorPlot

## Description
`makeVectorPlot` is a command-line utility that creates a graphical vector plot from distance-averaged ADCP (Acoustic Doppler Current Profiler) solutions. It reads a JHC-formatted file containing velocity data and generates a 2D image (also in JHC format) where vectors are drawn vertically to represent the magnitude and direction of the current at different locations.

The tool is designed to visualize a profile of current data, such as a cross-section of a channel, by drawing lines or bars whose lengths are proportional to the current's magnitude.

## Usage
```bash
makeVectorPlot -in <infile> -out <outfile> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-in <infile>` | **Required.** Specifies the input JHC file containing the distance-averaged ADCP vector data. | `-in adcp_vectors.jhc` |
| `-out <outfile>` | **Required.** Specifies the name for the output JHC image file. | `-out vector_plot.jhc` |
| `-max_vector <m/s>` | Sets the maximum current velocity (in m/s) for scaling. Vectors corresponding to velocities greater than this value will be capped at the maximum length. | `1.0` |
| `-pixels_per_vector <number>` | The number of vertical pixels to allocate for each horizontal data point in the input file. This effectively controls the vertical stretching of the output image to make space for the vectors. | `10` |
| `-lines` | If specified, the vectors are drawn as thin vertical lines. If omitted, they are drawn as filled grey bars. | |
| `-double_width` | A scaling option that doubles the length of the rendered vectors relative to the available space defined by `pixels_per_vector`. | |
| `-depth_average <meters>` | This argument is parsed but does not appear to be used in the code's logic. It may be a remnant from a previous version. | `2.0` |

## How It Works

1.  **Read Input Data:** The tool reads the header and data from the input JHC file. This file is expected to be a 2D array where each row is a profile and each column is a location along the profile.
2.  **Create Output Image:** It creates a new, larger output image buffer. The width is the same as the input data, but the height is increased by a factor of `pixels_per_vector` to provide vertical space for drawing the vectors.
3.  **Draw Vectors:** The tool iterates through each row (profile) of the input data:
    *   A horizontal "zero" line is drawn across the middle of the vertical space allocated for that profile.
    *   It then iterates through each data point (current velocity) in the profile.
    *   The length of the vector to be drawn is calculated by scaling the absolute current velocity against `max_vector`.
    *   If the current is positive, a vector (line or bar) is drawn downwards from the zero line.
    *   If the current is negative, the vector is drawn upwards.
    *   The color of the vector is a dark grey for positive currents and a lighter grey for negative currents (if not in `-lines` mode). The endpoints and lines are black.
4.  **Write Output File:** After processing all profiles, the tool writes the complete image buffer to the output JHC file specified by `-out`.

This process effectively transforms a numerical data file into a visual representation of current flow along a profile.