---
layout: default
title: stencil
parent: Image Tools
nav_order: 49
tool_name: stencil
source_path: code/image/stencil.c
category: Masking & Stenciling
input_formats: ["OMG1 8-bit or 32-bit float (.r4) input image", "OMG1 8-bit mask (-mask)", "Optional OMG1 underlay image (-under)"]
output_formats: ["Masked/composited OMG1 8-bit or 32-bit float (.r4) image"]
related_tools: ["stencilIPV", "mask_make", "jb_mask_make", "mask_ray"]
---

# stencil

## Description
`stencil` masks an 8-bit (`data_type = 1`) or 32-bit floating-point (`data_type = 3`, `.r4`) `OMG1` (`JHC_header`) image using an 8-bit `OMG1` mask file (`-mask`, produced by [`mask_make`](mask_make.md) or [`jb_mask_make`](jb_mask_make.md)). Masked-out pixels are filled either with a constant background value (`-undercolor`) or with corresponding pixels from a secondary underlay `OMG1` image (`-under`).

## CLI Options & Usage
```bash
stencil -mask <mask.8bit> -in <infile> -out <outfile> \
  [-inverse] [-ignore <val>] \
  [-under <underfile> | -undercolor <val>] \
  [-ashift <dn>] [-ushift <dn>]
```
* **`-mask <mask.8bit>`**: 8-bit `OMG1` mask image (need not match `<infile>` dimensions; automatically scaled across `[0..xmax, 0..ymax]`).
* **`-in <infile>`**: Primary 8-bit or 32-bit float `OMG1` image.
* **`-out <outfile>`**: Output stenciled `OMG1` image.
* **`-inverse`**: Inverts the mask logic (retains `<infile>` where `mask == ignore` instead of where `mask != ignore`).
* **`-ignore <val>`**: Mask Digital Number treated as "masked out" (default: `0`).
* **`-under <underfile>`**: Secondary `OMG1` image (same dimensions and data type as `<infile>`) revealed wherever `<infile>` is masked out.
* **`-undercolor <val>`**: Constant fill value used when `-under` is not specified (default: `255` for 8-bit, `99999.0` for `.r4`).
* **`-ashift <dn> -ushift <dn>`**: Optional greyscale offsets added to the active (`-in`) and underlay (`-under`) 8-bit images to separate their palette ranges.

## Algorithm
For every pixel `(i, j)` in `<infile>`, maps `(i, j)` proportionally into mask coordinates `(mi = i * m_xmax / xmax, mj = j * m_ymax / ymax)`. Depending on whether `mask[mi, mj] == ignore` (and `-inverse`), writes either the primary `<infile>` pixel (plus `ashift`) or the `<underfile>` / `undercolor` value (plus `ushift`) to `<outfile>`.
