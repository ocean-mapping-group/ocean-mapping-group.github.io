---
layout: default
title: replacecloud
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 44
tool_name: replacecloud
source_path: code/image/replacecloud.c
category: Satellite, SAR & Format Conversion
input_formats:
- Destriped ACRES image (-in)
- Extracted cloud file (-cloud)
output_formats:
- Cloud-restored ACRES image (in-place)
related_tools:
- removecloud
- lsfilter
- add_hilo
- limit_change
---

# replacecloud

## Description
`replacecloud` (written by A. Y. / JCU, May 1990) is the final step in the cloud-masked Landsat destriping pipeline. After [`removecloud`](removecloud.html), [`lsfilter`](lsfilter.html), [`add_hilo`](add_hilo.html), and [`limit_change`](limit_change.html) have been run, `replacecloud` restores the original unclipped cloud pixels from `<cloud_file>` back into the destriped ACRES image (`-in`).

## CLI Options & Usage

```bash
replacecloud -in <destriped_acres_file> -cloud <cloud_file>
```
* **`-in <destriped_acres_file>`**: Destriped ACRES-format 8-bit image (updated in-place).
* **`-cloud <cloud_file>`**: `.cloud` file previously extracted by [`removecloud`](removecloud.html).

## Algorithm
1. Reads the 90-byte ACRES header from `<destriped_acres_file>` to determine `row` and `col`, and skips the 90-byte header of `<cloud_file>`.
2. Scans all `row × col` pixels in lockstep: wherever `<cloud_file>` contains a non-zero byte (`c != 0`), seeks back 1 byte in `<destriped_acres_file>` and overwrites the clamped pixel with the original cloud intensity `c`.
