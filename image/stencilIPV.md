---
layout: default
title: stencilIPV
parent: Image Tools
nav_order: 50
tool_name: stencilIPV
source_path: code/image/stencilIPV.c
category: Masking & Stenciling
input_formats: ["Multi-plane .ipv raster (-in)", "OMG1 8-bit mask (-mask)", "Optional .ipv underlay (-under)"]
output_formats: ["Stenciled multi-plane .ipv raster (-out)"]
related_tools: ["stencil", "mask_make", "jb_mask_make"]
---

# stencilIPV

## Description
`stencilIPV` is a specialized variant of [`stencil`](stencil.md) designed for Magdy Halim's multi-plane `.ipv` image files (which begin with a 2048-byte header followed by `-planes <n>` sequential 8-bit image planes stored in bottom-to-top row order).

## CLI Options & Usage
```bash
stencilIPV -mask <mask.8bit> -in <in.ipv> -out <out.ipv> \
  [-planes <n>] [-inverse] [-ignore <val>] \
  [-under <under.ipv> | -undercolor <val>]
```
* **`-mask <mask.8bit>`**: 8-bit `OMG1` (`JHC_header`) mask file (whose `xmax × ymax` dimensions define the plane dimensions).
* **`-in <in.ipv>`**: Input `.ipv` multi-plane file (2048-byte header + `planes × xmax × ymax` bytes).
* **`-out <out.ipv>`**: Output stenciled `.ipv` file.
* **`-planes <n>`**: Number of image planes in `<in.ipv>` (default: `1`).
* **`-inverse`**: Reverses the mask selection logic.
* **`-ignore <val>`**: Mask pixel value treated as masked out (default: `0`).
* **`-under <under.ipv>` / `-undercolor <val>`**: Underlay `.ipv` file or constant byte value (default: `255`) placed in masked regions.

## Algorithm
1. Reads the `OMG1` mask from `<mask.8bit>` and flips its rows vertically (`flipped_mask[i, ymax - 1 - j] = mask[i, j]`) to match the bottom-up coordinate orientation of `.ipv` files.
2. Copies the 2048-byte `.ipv` header from `<in.ipv>` to `<out.ipv>`, then loops through all `0 .. planes-1` planes, applying the flipped mask to select either `<in.ipv>` or `<under.ipv>` / `undercolor` for each pixel.
