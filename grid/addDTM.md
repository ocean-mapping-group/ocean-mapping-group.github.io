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