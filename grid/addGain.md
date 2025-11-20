---
layout: default
title: addGain
parent: Grid Tools
nav_order: 4
---
# addGain

## Description
`addGain` is a command-line utility that applies a gain correction to an 8-bit image (likely a sidescan mosaic or intensity map) based on depth information from a corresponding floating-point (`.r4`) depth grid. This effectively normalizes the image intensity with respect to the water depth, compensating for signal loss over longer ranges. The output is a new 8-bit image file.

## Usage
```bash
addGain [OPTIONS] <base_filename> <output_8bit_file>
```
The `<base_filename>` is expected to be a prefix that will be appended with `.r4` for the float depth file and `.mos` for the 8-bit mosaic file. The `<output_8bit_file>` will be the resulting gained 8-bit image.

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-normal <value>` | Specifies a "normal" depth value (in meters) around which the gain normalization is centered. Depths shallower than this value will receive less gain, and deeper values more gain. | `100.0` |
| `<base_filename>` | **Required.** The base name for the input files. The tool will look for `<base_filename>.r4` (for depth) and `<base_filename>.mos` (for the 8-bit mosaic to be gained). | `survey_area` (looks for `survey_area.r4` and `survey_area.mos`) |
| `<output_8bit_file>` | **Required.** The name of the output 8-bit grid file, which will contain the depth-gained image. | `gained_image.8bit` |
