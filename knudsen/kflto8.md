---
layout: default
title: kflto8
parent: Knudsen Chirp Sub-Bottom (knudsen)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 5
tool_name: kflto8
source_path: knudsen/kflto8.c
category: radiometric_processing
input_formats:
- OMG_FL_DATA
- OMG_HDCS
output_formats:
- OMG_SS_DATA
related_tools:
- k16to8
- readSB_SEGY
- readixBlueXTF
- readEA600
- makeSeisPlot
---

# kflto8

## Overview

`kflto8` converts 32-bit IEEE floating-point sub-bottom trace files (`<prefix>.merged.fl_data`, such as those produced by [`readSB_SEGY`](../segy/readSB_SEGY), [`readixBlueXTF`](readixBlueXTF), or [`readEA600`](readEA600)) into 8-bit unsigned byte trace files (`<prefix>.merged.ss_data`) so they can be plotted with [`makeSeisPlot`](makeSeisPlot) or inspected in `SwathEd`.

## Usage

```
kflto8 (-v) (-log | -lin) (-max16 8000) (-min16 10) (-nosams 16000) \
       -in infile.merged.fl_data -out outfile.merged.ss_data
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<infile>` | *required* | Input 32-bit float trace file (`<prefix>.merged.fl_data`); also opens `<prefix>.merged` via `mem_stripext(inname)`. |
| `-out` | `<outfile>` | *required* | Output 8-bit trace file (`<prefix>.merged.ss_data`). |
| `-min16` | `<float_val>` | `1.0` | Minimum floating-point sample value mapped to `0` (clamped below `min16`). |
| `-max16` | `<float_val>` | `65535.0` | Maximum floating-point sample value mapped to `255` (clamped above `max16`). |
| `-nosams` | `<samples>` | `0` (from `.merged`) | Override the number of samples per trace when determining record count (`file_size / (nosams * 4)`). |
| `-lin` / `-log` | none | `-lin` | Set linear or logarithmic mode flag (note: current loop performs linear clamping and scaling `255.0 * (val - min16) / (max16 - min16)`). |
| `-custom_dump` | `<prefix>` | none | Set custom dump prefix flag. |
| `-v` | none | `0` | Enable verbose output (prints per-trace and overall file min/max float values). |

## How It Works

1. **Companion `.merged` Lookup**: Opens `-in` (`.merged.fl_data`) and strips the last extension (`mem_stripext(inname)`) to open the `.merged` file and read `OMG_HDCS_summary_header`.
2. **Trace Seeking & Float Byte-Swapping**: For each ping `i`, reads `OMG_HDCS_profile_header` and `OMG_HDCS_beam` from `.merged`, gets `tracelength = beams[0].no_samples`, seeks to `beams[0].offset * sizeof(float)` in `.merged.fl_data`, and reads `tracelength` byte-swapped floats via `jswapfloat_fread()`.
3. **8-Bit Scaling**: Maps each float sample linearly from `[min16, max16]` into `[0, 255]` (clamping values `<= min16` to `0` and `>= max16` to `255`) and writes `tracelength` bytes to `-out`.

## Practical Examples

### Inspect float dynamic range and re-scale `.merged.fl_data` to `.merged.ss_data`

```bash
kflto8 -v -min16 -60.0 -max16 0.0 \
       -in ek80_line01.merged.fl_data -out ek80_line01.merged.ss_data
```
