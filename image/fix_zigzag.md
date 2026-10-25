---
layout: default
title: fix_zigzag
parent: Image Tools
nav_order: 23
tool_name: fix_zigzag
source_path: code/image/fix_zigzag.c
category: Satellite, SAR & Format Conversion
input_formats: ["ACRES 8-bit Landsat MSS image"]
output_formats: ["Line-shift corrected ACRES 8-bit image (<infile>.fix)"]
related_tools: ["destripe", "lsfilter", "add_hilo", "landsat2acres"]
---

# fix_zigzag

## Description
`fix_zigzag` (written by A. Y. / JCU, May 1990) corrects 12-line periodic horizontal line-start synchronization ("zigzag") shifts in ACRES-format Landsat MSS imagery, writing the corrected image to `<infile>.fix`.

## CLI Options & Usage
```bash
fix_zigzag -in <acres_file>
```
* **`-in <acres_file>`**: Input ACRES-format 8-bit Landsat image (begins with a 90-byte header). Outputs `<acres_file>.fix`.

## Algorithm
1. Reads the 90-byte ACRES header (`row = header[4]`, `col = header[3]`) and copies it to `<acres_file>.fix`.
2. Processes the image in 12-scanline blocks (`i = row % 12`):
   * Scanlines `0..5` (forward mirror sweep): Shifts the scanline right by 1 pixel (`fputc(0)` at column 0, writing pixels `0 .. col-2`).
   * Scanlines `6..11` (reverse/alternate sweep): Writes the scanline unshifted (`0 .. col-1`), aligning vertical features across mirror sweeps.
