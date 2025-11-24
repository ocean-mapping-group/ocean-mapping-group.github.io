---
layout: default
title: contgrid
parent: Grid Tools
nav_order: 12
---
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

## How It Works
1.  **File Opening:** Opens the input `.r4` grid file for reading and the output vector file for writing.
2.  **Header Reading:** Reads the `JHC_header` from the input file to get grid dimensions and geographic information.
3.  **Contour Generation:**
    *   Iterates through each grid cell.
    *   For each cell, it compares its value with its neighbors to identify where contour lines cross cell boundaries.
    *   For each contour level within the specified `low` and `high` range, it traces the contour line by connecting these crossing points.
4.  **Vector Output:** Writes the generated contour lines (as a series of connected points or line segments) to the output binary vector file. The exact format of this binary file is defined internally by the tool.

## Output Files
*   `<output_vector_file>`: A binary file containing contour lines.

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions.
*   `support.h`: For general utility functions and error handling.

## Notes
The binary vector output is designed to be consumed by other internal plotting or visualization tools within the OMG ecosystem. This tool is a fundamental step in producing cartographic products from gridded bathymetry.
