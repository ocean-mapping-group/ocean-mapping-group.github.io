---
layout: default
title: 8bittor4
parent: Grid Tools
nav_order: 1
---
# 8bittor4

## Description
`8bittor4` is a command-line utility that converts a JHC-format 8-bit or 16-bit (short integer) array grid file into a 32-bit floating-point (r4) grid file. It allows for scaling digital numbers (DN) to a specified range of floating-point values, and can handle ignored values and apply a dB scaling if needed.

## Usage
```bash
8bittor4 [OPTIONS] <8bit_input_file> <float_output_file>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-dB` | Apply a dB scaling to the output. If this flag is used, `-low` and `-high` are ignored and effectively set to 0. | |
| `-min <value>` | Specifies the minimum digital number (DN) value in the input file that corresponds to the `low_limit` float value. Used in conjunction with `-max`. | `0` (for 8-bit) |
| `-max <value>` | Specifies the maximum digital number (DN) value in the input file that corresponds to the `high_limit` float value. Used in conjunction with `-min`. | `255` (for 8-bit) |
| `-low <value>` | Specifies the floating-point value that corresponds to the `min` digital number. | `0` (if `-dB` not used) |
| `-high <value>` | Specifies the floating-point value that corresponds to the `max` digital number. | `0` (if `-dB` not used) |
| `-ignore <value>` | Specifies a digital number value in the input file to be treated as an "ignore" or null value. These values will be set to `0.0` in the output float file. | `256` (effectively no ignore for 8-bit) |
| `-xystep <value>` | Overrides the X and Y step values in the output JHC header with the specified float value. | |
| `-odd` | (Used with `-short`) If set, and a short integer value is even, it will be treated as an ignore value. | |
| `-short` | Indicates that the input file contains 16-bit short integers instead of 8-bit unsigned characters. When used, `-min` and `-max` default to `-32768` and `32767` respectively. | |
| `<8bit_input_file>` | **Required.** The input JHC-format 8-bit or 16-bit grid file. | `input_grid.8bit` |
| `<float_output_file>` | **Required.** The output JHC-format 32-bit floating-point grid file. | `output_grid.r4` |
