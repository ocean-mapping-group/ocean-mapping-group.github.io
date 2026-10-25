---
layout: default
title: comboVPs
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 12
tool_name: comboVPs
source_path: code/image/comboVPs.c
category: Multibeam Water Column & Acoustic Modeling
input_formats:
- OMG1 .vert_prof water-column vertical profiles
output_formats:
- Concatenated .vert_prof vertical profile (OMG1)
related_tools:
- comboTAs
- makeWC
- fillGap
- stretchacres
---

# comboVPs

## Description
`comboVPs` concatenates multiple along-track multibeam water-column vertical profile files (`*.vert_prof`, produced by [`makeWC`](../omg/makeWC.html) or [`comboTAs`](comboTAs.html)) side-by-side into a single long-line `.vert_prof` echogram in `OMG1` (`JHC_header`) format.

## CLI Options & Usage

```bash
comboVPs [-v] -out <comboprefix> <file1.vert_prof> [<file2.vert_prof> ...]
```
* **`-out <comboprefix>`**: Output combined `.vert_prof` filename.
* **`-v`**: Verbose mode reporting the `xmax × ymax` dimensions of each input `.vert_prof` file as it is appended.
* **`<file1.vert_prof> ...`**: Ordered list of `.vert_prof` files to concatenate horizontally along the X (ping/time) axis.

## Algorithm
1. Reads the `JHC_header` of every input `.vert_prof` file, summing the total along-track ping count (`tot_x += head.xmax`) and finding the deepest vertical sample dimension (`max_y = max(max_y, head.ymax)`).
2. Allocates a `tot_x × max_y` 8-bit canvas initialized to `255` (background).
3. Sequentially copies each input `.vert_prof` array into its horizontal column offset `[start_x .. start_x + head.xmax - 1]` and writes the combined `OMG1` header and raster payload to `<comboprefix>`.
