---
layout: default
title: jhc2SUN
parent: HAWAII MR1 Towed Sidescan (mr1)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 4
tool_name: jhc2SUN
source_path: mr1/jhc2SUN.c
category: format_conversion
input_formats:
- JHC_ARRAY
output_formats:
- SUN_RASTER
related_tools:
- plotmr1
- edbathy
---

# jhc2SUN

## Overview

`jhc2SUN` converts an 8-bit OMG/JHC raster array file (`JHC_header` with `data_type == 1`) into a standard 8-bit Sun Rasterfile (`struct rasterfile`, `RAS_MAGIC = 0x59a66a95`), optionally inverting pixel greyscale values (`255 - val`) and padding odd row widths to 16-bit word boundaries as required by the Sun Rasterfile specification.

## Usage

```
jhc2SUN (-invert) jhc8bitfilename SUNrasterfilename
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<jhc8bitfilename>` | `<path>` | *required* | First positional argument: input 8-bit JHC array file. |
| `<SUNrasterfilename>` | `<path>` | *required* | Second positional argument: output Sun Rasterfile (`.ras`). |
| `-invert` | none | `0` | Invert 8-bit pixel intensities (`*(bbuf + x) = 255 - *(bbuf + x)`). |

## How It Works

1. **Header Validation**: Reads the input `JHC_header` via `get_print_JHC_header(floatfile, 1)`, extracts `dx` (width) and `dy` (height), and verifies `JHChead.data_type == 1` (8-bit unsigned byte).
2. **Sun Raster Header Construction**: Populates `struct rasterfile` (`ras_magic = RAS_MAGIC`, `ras_width = dx`, `ras_height = dy`, `ras_depth = 8`, `ras_length = dx * dy`, `ras_type = RT_STANDARD`, `ras_maptype = RMT_NONE`, `ras_maplength = 0`) and writes it to the output file.
3. **Row Conversion & Word Padding**: Reads `dy` scanlines of `dx` bytes, optionally inverts each pixel when `-invert` is set, and writes `dx + 1` bytes per row if `dx` is odd (`dx % 2`) or `dx` bytes if `dx` is even.

## Practical Examples

### Convert an 8-bit JHC mosaic into an inverted Sun Rasterfile

```bash
jhc2SUN -invert mr1_mosaic.i1 mr1_mosaic.ras
```
