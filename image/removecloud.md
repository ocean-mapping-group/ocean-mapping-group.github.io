---
layout: default
title: removecloud
parent: Image Tools
nav_order: 43
tool_name: removecloud
source_path: code/image/removecloud.c
category: Satellite, SAR & Format Conversion
input_formats: ["ACRES 8-bit Landsat image"]
output_formats: ["Cloud-clamped ACRES image (in-place)", "Extracted cloud layer (<infile>.cloud)"]
related_tools: ["replacecloud", "lsfilter", "add_hilo", "limit_change"]
---

# removecloud

## Description
`removecloud` (written by A. Y. / JCU, May 1990) is the first step in the cloud-masked Chavez (1986) Landsat destriping workflow. Bright clouds saturate spatial boxcar filters ([`lsfilter`](lsfilter.md)) and create dark halo artifacts in water areas. `removecloud` thresholds pixels brighter than `-thresh`, clamping them to `thresh` in-place in `<infile>` while saving the original bright cloud pixels into `<infile>.cloud` for later restoration via [`replacecloud`](replacecloud.md).

## CLI Options & Usage
```bash
removecloud -in <acres_file> -thresh <0..255>
```
* **`-in <acres_file>`**: Input ACRES-format 8-bit image (modified in-place after its 90-byte header), also producing `<acres_file>.cloud`.
* **`-thresh <0..255>`**: Intensity threshold above which pixels are classified as cloud.

## Algorithm
1. Reads the 90-byte ACRES header (`row = header[4]`, `col = header[3]`) from `<infile>` and writes a matching 90-byte header to `<infile>.cloud`.
2. Scans every pixel in `<infile>`:
   * If `pixel <= thresh`: Leaves `<infile>` unchanged and writes `0` to `<infile>.cloud`.
   * If `pixel > thresh`: Writes the original `pixel` value to `<infile>.cloud` and overwrites that byte in `<infile>` with `thresh`.
