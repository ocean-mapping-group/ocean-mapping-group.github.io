---
layout: default
title: 8bit2acres
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 2
tool_name: 8bit2acres
source_path: code/image/8bit2acres.c
category: Image & Raster Processing
input_formats:
- Raw 8-bit raster
- Raw 32-bit float raster (-float)
- Netpbm PGM (-pgm)
- 1160-col GLORIA (-isgloria)
output_formats:
- OMG1 8-bit or 32-bit float array (JHC_header)
related_tools:
- stretchacres
- PCItoJHC
- subimage
- jview
---

# 8bit2acres

## Description
`8bit2acres` converts raw headerless 8-bit greyscale rasters, raw 32-bit floating-point arrays (`-float`), Netpbm `.pgm` images (`-pgm`), or 1160-column raw GLORIA scanline files (`-isgloria`) into the Ocean Mapping Group's `OMG1` (`JHC_header`, historically ACRES) georeferenced array format. It supports byte-offset skipping (`-offset`), row/column inversion (`-flip`, `-invert`), and optional geographic or projected bounding-box metadata.

## CLI Options & Usage

```bash
8bit2acres -in <rawimage> -out <acresimage> [-pgm] [-rows <n> -cols <n>] \
  [-offset <bytes>] [-float] [-isgloria] [-invert] [-flip] \
  [-tlon <deg> -tlat <deg> -blon <deg> -blat <deg> -dx <m> -dy <m>]
```
* **`-in <filename>`**: Input raw raster or `.pgm` file.
* **`-out <filename>`**: Output `OMG1` (`JHC_header`) file.
* **`-pgm`**: Parses image dimensions (`cols`, `rows`) and max grey value directly from a `P5` binary PGM header.
* **`-rows <n> -cols <n>`**: Explicit dimensions for headerless raw files (required unless `-pgm` is set).
* **`-offset <bytes>`**: Skips `<bytes>` at the start of the input file before reading raster lines.
* **`-float`**: Treats input pixels as 4-byte floats (`data_type = 3`) instead of 1-byte unsigned chars (`data_type = 1`).
* **`-isgloria`**: Extracts a 992-column swath from 1160-byte raw GLORIA records (skipping the 64-byte header on each row).
* **`-invert`**: Inverts 8-bit pixel intensities (`val = 255 - val`, mapping `0` to `254`).
* **`-flip`**: Reverses the vertical row order (bottom-to-top to top-to-bottom).
* **`-tlon`, `-tlat`, `-blon`, `-blat`, `-dx`, `-dy`**: Populates geographic bounds and pixel spacing in the output `JHC_header` (`projection = GEOGRAPHIC` if bounds are given without `dx/dy`, or `MERCATOR` when `dx/dy` are also supplied).

## Algorithm
1. Initializes a 1024-byte `OMG1` `JHC_header` structure via `jhc_init_header()` with `xmin = 0`, `xmax = cols`, `ymin = 0`, `ymax = rows`.
2. If `-pgm` is specified, reads the `P5` header (skipping `#` comment lines) to determine `cols`, `rows`, and the byte offset to the binary payload.
3. Reads the input raster (applying `-offset` or `-isgloria` row slicing), optionally reverses row order (`-flip`) or inverts greyscale values (`-invert`), and writes the `JHC_header` followed by the raster payload via `jhc_write_header()`.
