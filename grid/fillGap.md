---
layout: default
title: fillGap
parent: Grid Tools
nav_order: 30
---
# fillGap

## Description
`fillGap` is a utility designed to fill small gaps or holes in JHC-format grid files (`.r4` or `.8bit`). It iterates through the grid and, for each pixel identified as a gap (based on an ignore value), it attempts to interpolate a new value from its valid neighbors.

The interpolation logic is primarily designed to fill single-pixel-wide gaps, particularly those oriented along the grid's cardinal axes (North-South or East-West).

## Usage
```bash
fillGap [OPTIONS] <infile> <outfile>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `<infile>` | **Required.** The input JHC grid file (`.r4` or `.8bit`) containing gaps to be filled. | |
| `<outfile>` | **Required.** The name for the new output grid file with the gaps filled. | |
| `-ignore <value>` | Specifies the numerical value that represents a gap or "no data" pixel in the input grid. | For 8-bit grids: `255` <br> For float grids: `0.0` |
| `-v` | Enable verbose output. | |

## Interpolation Method
The tool uses a hierarchical search pattern to find valid data for interpolation:
1.  It first attempts a 4-point average using the immediate North, South, East, and West neighbors.
2.  If that is not possible, it attempts a 2-point linear interpolation using the North and South neighbors.
3.  If that fails, it tries a 2-point linear interpolation using the East and West neighbors.
4.  The tool will expand its search up to 3 pixels away in the cardinal directions to find data to interpolate from, using a weighted average.

This method is most effective at patching narrow, linear gaps (e.g., single lines of missing data) that are common artifacts in sonar data processing.
