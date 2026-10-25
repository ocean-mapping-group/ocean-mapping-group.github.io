---
layout: default
title: tifftor4
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: tifftor4
source_path: code/grid/tifftor4.c
category: gridding
input_formats:
- TIFF / GeoTIFF (.tif)
output_formats:
- JHC_header (.r4)
related_tools:
- 8bittor4
- r4to8bit
- r4toESRI
---

# tifftor4

## Overview

`tifftor4` inspects a TIFF image (`libtiff`)—extracting its width, height, bits per sample, samples per pixel, compression, and X/Y resolution tags—and initializes a 32-bit floating-point OMG `.r4` header (`JHC_header`) with matching dimensions (`dx`, `dy`, and `-xystep`).

---

## Syntax & CLI Options

```
tifftor4 [-dB] [-min <DN>] [-max <DN>] [-low <val>] [-high <val>] [-ignore <val>] [-short] [-odd] [-xystep <step>] <tifffile> <r4file>
```

| Flag | Description |
|------|-------------|
| `-xystep <step>` | Pixel grid spacing assigned to `JHChead.xstep` and `JHChead.ystep`. |
| `-dB` | Enable decibel conversion flag. |
| `-min <DN>` | Minimum digital number (default: `0`, or `-32768` with `-short`). |
| `-max <DN>` | Maximum digital number (default: `255`, or `32767` with `-short`). |
| `-low <val>` | Output value corresponding to `-min`. |
| `-high <val>` | Output value corresponding to `-max`. |
| `-ignore <val>` | Input digital number to ignore / map to `0.0` (default: `256`). |
| `-short` | Treat input samples as 16-bit signed integers. |
| `-odd` | When used with `-short`, ignore even sample values. |
| `<tifffile>` | Input TIFF filename. |
| `<r4file>` | Output `.r4` filename. |

---

## How It Works

1. Opens `<tifffile>` via `TIFFOpen(bytename, "r")` from `libtiff`.
2. Queries and prints standard TIFF tags:
   - `TIFFTAG_IMAGEWIDTH` (`dx`) and `TIFFTAG_IMAGELENGTH` (`dy`)
   - `TIFFTAG_SAMPLESPERPIXEL`, `TIFFTAG_BITSPERSAMPLE`, `TIFFTAG_IMAGEDEPTH`, and `TIFFTAG_COMPRESSION`
   - `TIFFTAG_XPOSITION`, `TIFFTAG_XRESOLUTION`, `TIFFTAG_YPOSITION`, and `TIFFTAG_YRESOLUTION`
3. Initializes an `OMG1` `JHC_header` with `dx`, `dy`, `xstep = ystep = step`, and `data_type = 3`, and writes the header to `<r4file>`.

---

## Examples

### Inspect a TIFF file and write an `.r4` header with 5 m grid spacing

```bash
tifftor4 -xystep 5.0 survey_bathy.tif survey_bathy.r4
```

---

## Workflow Context

- **Related Conversion Tools**: [`8bittor4`](8bittor4.html), [`r4to8bit`](r4to8bit.html), [`r4toESRI`](r4toESRI.html).
