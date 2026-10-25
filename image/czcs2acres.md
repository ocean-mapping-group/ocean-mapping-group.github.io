---
layout: default
title: czcs2acres
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 14
tool_name: czcs2acres
source_path: code/image/czcs2acres.c
category: Satellite, SAR & Format Conversion
input_formats:
- 4-band BIL Coastal Zone Color Scanner (CZCS) raw tape file
output_formats:
- Four ACRES 8-bit band files (.band1 .. .band4)
related_tools:
- landsat2acres
- 8bit2acres
- PCItoJHC
- stretchacres
---

# czcs2acres

## Description
`czcs2acres` de-interleaves a 4-band Band-Interleaved-by-Line (BIL) Nimbus-7 Coastal Zone Color Scanner (CZCS) raw image into four separate ACRES-format 8-bit raster files (`<out>.band1` through `<out>.band4`).

## CLI Options & Usage

```bash
czcs2acres -in <raw_czcs> -out <acres_prefix> [-rows <n>] [-cols <n>]
```
* **`-in <raw_czcs>`**: Input 4-band BIL CZCS image file (begins with a 90-byte header followed by interleaved scanlines).
* **`-out <acres_prefix>`**: Output filename prefix generating `<acres_prefix>.band1`, `.band2`, `.band3`, and `.band4`.
* **`-rows <n>`**: Number of scanlines per band (default: `970`).
* **`-cols <n>`**: Number of pixels per scanline (default: `1968`).

## Algorithm
1. Reads the initial 90-byte header from `<raw_czcs>`, writes `rows` and `cols` into `header[4]` and `header[3]` (16-bit integer fields), and writes this 90-byte ACRES header to each of the four output files (`.band1`..`.band4`).
2. Loops through `0 .. rows-1`; on each iteration, reads four consecutive `cols`-byte scanlines (one for each spectral band `k = 0..3`) and writes each to its respective `.band<k+1>` output file.
