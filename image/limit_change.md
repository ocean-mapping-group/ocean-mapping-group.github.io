---
layout: default
title: limit_change
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 29
tool_name: limit_change
source_path: code/image/limit_change.c
category: Satellite, SAR & Format Conversion
input_formats:
- Original ACRES image (<in>) and destriped ACRES image (<in>.des)
output_formats:
- Artifact-limited ACRES image (<in>.des_limit)
related_tools:
- lsfilter
- add_hilo
- removecloud
- replacecloud
---

# limit_change

## Description
`limit_change` (written by A. Y. / JCU, May 1990) is a post-processing filter in the Chavez (1986) Landsat destriping pipeline. It compares an original ACRES image (`<in>`) with its high/low-pass reconstructed destriped version (`<in>.des` from [`add_hilo`](add_hilo.html)) and reverts pixels whose radiometric change exceeds a user-specified threshold (`-limit`), writing the result to `<in>.des_limit`. This prevents filter ringing near sharp coastlines, reefs, or cloud edges.

## CLI Options & Usage

```bash
limit_change -in <acres_prefix> -limit <thresh>
```
* **`-in <acres_prefix>`**: Base filename; opens `<acres_prefix>` and `<acres_prefix>.des` and creates `<acres_prefix>.des_limit`.
* **`-limit <thresh>`**: Threshold against which `abs(orig_pixel + des_pixel)` is compared.

## Algorithm
1. Reads the 90-byte ACRES header from `<acres_prefix>`, copies it to `<acres_prefix>.des_limit`, and advances `<acres_prefix>.des` past its 90-byte header.
2. For every pixel across `row × col`, if `abs(orig + des) < limit`, writes the destriped pixel `des`; otherwise restores the original pixel `orig`.
