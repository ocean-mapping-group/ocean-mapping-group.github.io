---
layout: default
title: contgrid
parent: Grid Tools
nav_order: 12
---
# contgrid

## Description
`contgrid` is a command-line utility for generating contour lines from a JHC-format 32-bit floating-point (`.r4`) grid file. It creates a binary vector file (presumably in a custom format) that represents these contour lines, which can then be used for plotting or further visualization. The tool supports different map projections and allows users to specify the range of depth values to contour.

## Usage
```bash
contgrid [OPTIONS] <input_float_file.r4> <output_vector_file>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `<input_float_file.r4>` | **Required.** The path to the input JHC-format 32-bit floating-point grid file (DTM). | `bathymetry.r4` |
| `<output_vector_file>` | **Required.** The path for the output binary vector file containing the contour lines. | `contours.bin` |
| `-low <value>` | Specifies the minimum depth value (inclusive) in the input grid to be considered for contouring. | (Determined automatically from data range) |
| `-high <value>` | Specifies the maximum depth value (inclusive) in the input grid to be considered for contouring. | (Determined automatically from data range) |
