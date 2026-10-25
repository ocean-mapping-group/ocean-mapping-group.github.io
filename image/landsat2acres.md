---
layout: default
title: landsat2acres
parent: Image Tools
nav_order: 28
tool_name: landsat2acres
source_path: code/image/landsat2acres.c
category: Satellite, SAR & Format Conversion
input_formats: ["4-band BIL Landsat MSS raw image"]
output_formats: ["Four ACRES 8-bit band files (.band1 .. .band4)"]
related_tools: ["czcs2acres", "addheader", "destripe", "fix_zigzag", "lsfilter"]
---

# landsat2acres

## Description
`landsat2acres` de-interleaves a 4-band Band-Interleaved-by-Line (BIL) Landsat MSS raw tape file into four single-band ACRES-format 8-bit image files (`<out>.band1` through `<out>.band4`).

## CLI Options & Usage
```bash
landsat2acres -in <raw_landsat> -out <acres_prefix> [-rows <n>] [-cols <n>]
```
* **`-in <raw_landsat>`**: Input 4-band BIL Landsat image (with 90-byte header).
* **`-out <acres_prefix>`**: Output prefix producing `<acres_prefix>.band1`, `.band2`, `.band3`, and `.band4`.
* **`-rows <n>`**: Number of scanlines per band (default: `2400`).
* **`-cols <n>`**: Number of pixels per scanline (default: `3240`).

## Algorithm
1. Reads the 90-byte header from `<raw_landsat>`, updates the 16-bit `rows` (`header[4]`) and `cols` (`header[3]`) fields, and writes the 90-byte ACRES header to all four output `.band1..4` files.
2. Iterates over `0 .. rows-1`, reading four consecutive `cols`-byte lines (`band 1..4`) per scanline row and writing each to its corresponding band file.
