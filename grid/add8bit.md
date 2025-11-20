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
