---
layout: default
title: fillGap
parent: Grid Tools
nav_order: 30
---
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

## How It Works
1.  **File Opening:** Opens the input grid file and the output grid file.
2.  **Header Reading:** Reads the `JHC_header` from the input file.
3.  **Data Loading:** Loads the entire input grid data into memory.
4.  **Gap Filling Loop:** Iterates through each pixel in the grid:
    *   If a pixel is identified as a gap (`ignore_val`):
        *   It first attempts a 4-point average interpolation using its immediate North, South, East, and West neighbors.
        *   If the 4-point average fails (e.g., not enough valid neighbors), it tries a 2-point linear interpolation using North/South neighbors.
        *   If that also fails, it tries a 2-point linear interpolation using East/West neighbors.
        *   The search for valid neighbors can extend up to 3 pixels away in cardinal directions, using a weighted average.
        *   The interpolated value replaces the `ignore_val`.
5.  **Output Header:** Creates a `JHC_header` for the output file and writes it.
6.  **Output Data:** Writes the processed (gap-filled) pixel data to the output file.

## Output Files
*   `<outfile>`: A new JHC-format grid file (`.r4` or `.8bit`) with filled gaps.

## Dependencies
*   `array.h`: For `JHC_header` structure and grid data handling.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is most effective for patching narrow, linear gaps often seen as artifacts in gridded data, especially from sonar systems. Its interpolation methods prioritize local neighbors to maintain data fidelity. More complex gap-filling (e.g., large irregular holes) might require more advanced gridding or interpolation techniques.
