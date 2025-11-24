---
layout: default
title: addDTM
parent: Grid Tools
nav_order: 3
---
---
layout: default
title: addDTM
parent: Grid Tools
nav_order: 3
---
# addDTM

## Description
`addDTM` is a command-line utility for combining two JHC-format 32-bit floating-point grid files (`.r4` files) or adding a constant value to a base grid. It takes a "base" grid and an "on-top" grid (or a constant), applies a multiplier and offset to the "on-top" data, and then adds (or subtracts) it to the base grid. The result is a new 32-bit floating-point grid file. This tool is useful for creating synthetic bathymetry, applying corrections, or combining different terrain models.

## Usage
```bash
addDTM [OPTIONS] -base <base_r4_file> [-ontop <second_r4_file> | -addConstant <value>] -out <output_r4_file>
```
Note: You must either provide `-ontop` or `-addConstant`, but not necessarily both.

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-base <base_r4_file>` | **Required.** Specifies the path to the base input JHC-format 32-bit floating-point grid file. | `base_bath.r4` |
| `-ontop <second_r4_file>` | Specifies the path to the second input JHC-format 32-bit floating-point grid file whose values will be added/subtracted from the base. | `correction.r4` |
| `-addConstant <value>` | Instead of an "on-top" file, a constant float value can be added to every non-zero point in the base grid. | `10.5` |
| `-out <output_r4_file>` | **Required.** Specifies the path for the output JHC-format 32-bit floating-point grid file. | `combined_bath.r4` |
| `-subtract` | If specified, the (scaled and offset) "on-top" values (or constant) will be subtracted from the base grid instead of added. | (Adds by default) |
| `-offset <value>` | A floating-point offset value applied to the "on-top" grid's values before multiplication and addition/subtraction. This offset is subtracted from the "on-top" values. | `0.0` |
| `-multiplier <value>` | A scaling factor applied to the "on-top" grid's values (after offset) before addition/subtraction. | `1.0` |
| `-addtoZero` | Modifies the behavior for handling zero values. If this flag is present, a `ZERO` value becomes `9999999.99` internally, affecting how operations are performed on grid cells that might otherwise be considered "no data" or ignored. Used in conjunction with `useZeroAdd`. | |
| `-useZeroAdd` | If set, it forces operations even on "on-top" grid cells that are zero, if the base grid cell is non-zero. Otherwise, a zero in the "on-top" grid is treated as "no data" and the base value is retained. | |
| `-v` | Enable verbose output during processing. | |

## How It Works
1.  **File Opening:** Opens the base input `.r4` file, the optional "on-top" input `.r4` file, and the output `.r4` file.
2.  **Header Reading:** Reads the `JHC_header` from the base file and the "on-top" file (if provided), ensuring their dimensions match.
3.  **Data Processing:** Iterates through each pixel in the grids:
    *   Reads the float value from the base grid.
    *   If `-ontop` is used: Reads the float value from the "on-top" grid. If this value is `0.0` and `-useZeroAdd` is not set, the base value is retained. Otherwise, the "on-top" value is adjusted by `offset` and `multiplier`.
    *   If `-addConstant` is used: The `addConstant` value is used as the "on-top" value.
    *   If `-subtract` is used, the adjusted "on-top" value is subtracted from the base value. Otherwise, it is added.
    *   The result is written to the output `.r4` file.
4.  **Output Header:** Creates a `JHC_header` for the output file (copied from the base file's header, with updated `min_value` and `max_value`) and writes it to the output file.

## Output Files
*   `<output_r4_file>`: A new JHC-format 32-bit floating-point grid file (`.r4`).

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is flexible for combining or modifying elevation models by applying either another grid or a constant value. The `addtoZero` and `useZeroAdd` options provide control over how zero values (often representing "no data") are handled during calculations.