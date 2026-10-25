---
layout: default
title: getTVG
parent: eXtended Triton Format — XTF (xtf)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 4
tool_name: getTVG
source_path: code/xtf/getTVG.c
category: Backscatter & Image Processing
input_formats:
- .xtf
output_formats:
- .txt (ASCII range-amplitude table)
related_tools:
- stripSS
- deTVG
- 7kTVG
- xtfTool
---

# getTVG

## Overview
`getTVG` analyzes 16-bit sidescan sonar traces (`XTF_HEADER_SONAR`, packet ID 0) and Reson bathymetry headers (`XTF_HEADER_BATHY`, packet ID 2) inside an XTF file to compute empirical mean amplitude vs. slant range curves. It bins sidescan trace samples by slant range (in meters) across a specified range of pings and outputs a two-column ASCII table (`<range_m> <mean_amplitude_or_dB>`) useful for diagnosing Time Varying Gain (TVG) curves.

## Usage

```bash
getTVG [-v] [-log] [-range_resolution <m>] [-from <ping_idx>] [-to <ping_idx>] [-port_only | -stbd_only] -in <input.xtf> -out <output.txt>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<input.xtf>` | **Required** | Path to the input `.xtf` file. |
| `-out` | `<output.txt>` | **Required** | Path to the output ASCII file (`range_m mean_value`). |
| `-range_resolution` | `<meters>` | `1.0` | Slant-range bin width in meters. |
| `-from` | `<index>` | `0` | Starting sidescan record index (0-based) for averaging. |
| `-to` | `<index>` | Total pings | Ending sidescan record index for averaging. |
| `-port_only` | None | Both channels | Accumulate only port sidescan channel samples (`do_stbd = 0`). |
| `-stbd_only` | None | Both channels | Accumulate only starboard sidescan channel samples (`do_port = 0`). |
| `-log` | None | Linear | Output bin averages in decibels (`20 * log10(mean)`) instead of raw 16-bit linear digital numbers. |
| `-v` | None | Off | Print the XTF file header and verbose diagnostics. |

## How It Works
1. **Header & Sound Speed Lookup:** Builds an XTF index via `buildXTFIndex()`, reads the first sidescan packet (`XTF_HEADER_SONAR`) to determine `SlantRange` and `NumSamples`, and reads the first Reson bathymetry packet (`XTF_HEADER_BATHY`) to obtain the sound speed (`resonBathy.velocity`).
2. **Range Binning:** Allocates `SlantRange / range_resolution` bins. For each ping between `-from` and `-to`, reads the port (`inputBuffer`) and starboard (`inputBuffer2`) 16-bit little-endian trace arrays, converts each sample index `k` into slant range in meters (accounting for the reversed port sample ordering `NumSamples - k - 1`), and accumulates the sample amplitudes and sample counts per range bin.
3. **ASCII Output:** Writes `<range_in_metres> <mean_value>` (or `20 * log10(mean_value)` with `-log`) for each bin to `-out`.

## Practical Examples

**1. Compute 0.5 m range-binned sidescan backscatter in dB for pings 100 to 500:**

```bash
getTVG -log -range_resolution 0.5 -from 100 -to 500 -in line01.xtf -out line01_tvg.txt
```

**2. Extract port-only linear amplitude profile across the entire XTF file:**

```bash
getTVG -port_only -in line01.xtf -out line01_port_tvg.txt
```
