---
layout: default
title: makecolcomp
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 31
tool_name: makecolcomp
source_path: code/image/makecolcomp.c
category: Image & Raster Processing
input_formats:
- Three OMG1 8-bit band files (-red, -green, -blue)
output_formats:
- 8-bit 3-3-2 RGB composite OMG1 image (-out)
- 256-entry ASCII RGB colormap (-print_colormap)
related_tools:
- PCItoJHC
- landsat2acres
- czcs2acres
- pastemos
- stretchacres
---

# makecolcomp

## Description
`makecolcomp` combines three co-registered 8-bit `OMG1` (`JHC_header`) single-band images (`-red`, `-green`, `-blue`) into a single 8-bit 3-3-2 bit-packed RGB color composite (`-out`), or prints the corresponding 256-entry RGB lookup table (`-print_colormap`) for 8-bit pseudocolor displays (`jview`).

## CLI Options & Usage

```bash
makecolcomp -red <band_r> -green <band_g> -blue <band_b> -out <comp.8bit> [-hack]
makecolcomp -print_colormap > rgb332.cmap
```
* **`-red <file> -green <file> -blue <file>`**: Input 8-bit `OMG1` band images (must share identical `xmax × ymax` dimensions).
* **`-out <comp.8bit>`**: Output 8-bit `OMG1` color composite.
* **`-hack`**: Leaves pixels where all three bands are `255` as `255` (background) and clamps `255` composite values to `254`.
* **`-print_colormap`**: Prints the 256-line `index R G B` lookup table (`0..255` scaled to `0..255` per channel) to stdout and exits.

## Algorithm
For each pixel across the three input bands, extracts the top 3 bits of Red (`(R >> 5) << 5`), the top 3 bits of Green (`(G >> 5) << 2`), and the top 2 bits of Blue (`B >> 6`), bitwise-ORing them into a single 8-bit `[RRRGGGBB]` pixel:

```c
out = ((red >> 5) << 5) | ((green >> 5) << 2) | (blue >> 6);
```
