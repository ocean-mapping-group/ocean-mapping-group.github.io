---
layout: default
title: add8bit
parent: Grid Tools
nav_order: 2
---
---
layout: default
title: add8bit
parent: Grid Tools
nav_order: 2
---
# add8bit

## Description
`add8bit` is a command-line utility that combines two JHC-format 8-bit grid files (`.8bit` files). It can either add the values of the second file (scaled) to the first file, or find the maximum value between corresponding pixels of the two files. The output is a new 8-bit grid file.

## Usage
```bash
add8bit [OPTIONS] -first <file1.8bit> -second <file2.8bit> -out <output.8bit>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-first <file1.8bit>` | **Required.** Specifies the path to the first input JHC-format 8-bit grid file. | `grid1.8bit` |
| `-second <file2.8bit>` | **Required.** Specifies the path to the second input JHC-format 8-bit grid file. | `grid2.8bit` |
| `-out <output.8bit>` | **Required.** Specifies the path for the output JHC-format 8-bit grid file. | `combined_grid.8bit` |
| `-max` | If specified, the output pixel value will be the maximum of the corresponding pixel values from the two input files. If not specified, the values are added (after scaling). | (Addition is default) |
| `-totalscale <value>` | A scaling factor applied to the final calculated value (after addition or max operation). | `1.0` |
| `-firstscale <value>` or `-scale <value>` | A scaling factor applied to the *second* input file's pixel values before they are added to the first file's values. | `1.0` |
| `-centre <value>` | A center value that is subtracted from the second file's pixel values before scaling and addition. This allows for shifting the "zero" point of the second grid. | `128.0` |

## How It Works
1.  **File Opening:** Opens the two input JHC 8-bit grid files (`-first`, `-second`) and the output 8-bit grid file (`-out`).
2.  **Header Reading:** Reads the `JHC_header` from both input files, ensuring their dimensions match.
3.  **Pixel-wise Operation:** Iterates through each pixel in the input grids:
    *   Reads the 8-bit pixel values from the first and second input files.
    *   Applies `firstscale` to the second pixel value and subtracts `centre`.
    *   If `-max` is specified, the output pixel value is the maximum of the (unscaled) first pixel and the (scaled) second pixel.
    *   Otherwise (default addition), the output pixel value is the sum of the (unscaled) first pixel and the (scaled) second pixel.
    *   The result is then multiplied by `totalscale` and clamped to the valid 8-bit range (0-254).
4.  **Output Header:** Creates a `JHC_header` for the output file (copied from the first input file's header, but with updated `min_value` and `max_value`) and writes it to the output file.
5.  **Output Data:** Writes the processed 8-bit pixel data to the output file.

## Output Files
*   `<output.8bit>`: A new JHC-format 8-bit grid file.

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions.
*   `support.h`: For general utility functions and error handling.

## Notes
The `scale` option is an alias for `firstscale`. `centre` can be used to effectively shift the dynamic range of the second grid before combination. `totalscale` scales the final result.
