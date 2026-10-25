---
layout: default
title: readixBlueXTF
parent: Knudsen Chirp Sub-Bottom (knudsen)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 14
tool_name: readixBlueXTF
source_path: knudsen/readixBlueXTF.c
category: format_conversion
input_formats:
- XTF
output_formats:
- OMG_HDCS
- OMG_SS_DATA
- OMG_FL_DATA
- JCU_NAV
- OMG_ORIENTATION
- BINARY_RASTER
related_tools:
- kflto8
- makeSeisPlot
- xtfTool
---

# readixBlueXTF

## Overview

`readixBlueXTF` unpacks sub-bottom profiler traces recorded in eXtended Triton Format (`.xtf`) by an **iXblue Echoes 3000 / 3500** chirp sub-bottom profiler (which stores acoustic traces in XTF `HeaderType = 202` packets as well as standard `0`/`8` ping packets and `HeaderType = 3` attitude packets). It rectifies the bipolar floating-point waveform (`fabs`), applies a smoothing envelope filter, scales traces to 8-bit (`.chan1`), extracts binary navigation (`.nav`) and attitude (`.orientation`), and optionally writes OMG HDCS `.merged`, `.merged.ss_data`, and `.merged.fl_data` files (`-out_as_OMG`).

## Usage

```
readixBlueXTF (-v) (-log | -lin | -sqrt) (-min -3 -max 10) (-autoscale | -autoplus) \
              (-out_as_OMG) -in infile(s) -out outfile_prefix
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<file1.xtf> [...]` | *required* | One or more input iXblue Echoes `.xtf` files. |
| `-out` | `<outfile_prefix>` | *required* | Output file prefix for `.chan1`, `.nav`, `.orientation`, and (with `-out_as_OMG`) `.merged`, `.merged.ss_data`, and `.merged.fl_data`. |
| `-out_as_OMG` | none | `0` | Write OMG HDCS v1 `.merged` (`toolType = Knudsen_320`, 2 beams), 8-bit `.merged.ss_data`, and 32-bit float `.merged.fl_data`. |
| `-lin` / `-log` / `-sqrt` | none | `-lin` | Use linear, logarithmic (`-log`), or square-root (`-sqrt`) scaling when quantizing rectified float traces to 8-bit. |
| `-min` / `-max` | `<float_val>` | `0` / `2e8` | Minimum and maximum trace amplitude bounds for 8-bit scaling. |
| `-autoscale` / `-autoplus` | none | `0` | Automatically scale each trace using its per-ping min/max (`1` or `2`). |
| `-v` | none | `0` | Enable verbose output (prints XTF file headers, packet offsets, and ping channel headers). |

## How It Works

1. **XTF Packet Scanning**: Reads `XTFFILEHEADER` and scans each input `.xtf` file for `0xFACE` magic numbers via `peekPACKETPEEKER()`.
2. **Trace Rectification & Filtering (`HeaderType` 0, 8, 202)**:
   - Reads `XTFPINGHEADER` and `XTFPINGCHANHEADER`, then reads `pingchan.NumSamples` 32-bit float samples into `ftrace_data`.
   - Rectifies the bipolar waveform (`rect_ftrace_data[j] = fabs(ftrace_data[j])`), applies a boxcar/envelope smoothing filter (`rect_filt_ftrace_data`), and scales the envelope to 8-bit (`uctrace_data`) via `scale_to_8bit()`.
   - Writes 8-bit traces to `<out>.chan1`, navigation fixes (`SensorYcoordinate`, `SensorXcoordinate`) to `<out>.nav`, and when `-out_as_OMG` is set, writes `.merged`, `.merged.ss_data`, and `.merged.fl_data`.
3. **Attitude Extraction (`HeaderType` 3)**: Reads `XTFATTITUDEDATA` packets and writes roll, pitch, heave, and heading records to `<out>.orientation`.

## Practical Examples

### Convert iXblue Echoes 3500 `.xtf` files into OMG HDCS sub-bottom format

```bash
readixBlueXTF -log -min -4.0 -max 2.0 -out_as_OMG \
              -in echoes_line01.xtf -out echoes_line01
```
