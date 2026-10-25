---
layout: default
title: OMGtoPS
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 4
tool_name: OMGtoPS
source_path: code/image/OMGtoPS.c
category: Image & Raster Processing
input_formats:
- OMG1 8-bit greyscale array (JHC_header)
output_formats:
- Encapsulated PostScript (.eps / .ps)
related_tools:
- stretchacres
- 8bit2acres
- printmos
---

# OMGtoPS

## Description
`OMGtoPS` converts an 8-bit `OMG1` (`JHC_header`) greyscale raster image into a standalone Encapsulated PostScript (`EPSF-2.0`) file suitable for high-resolution laser printing or inclusion in publication figures.

## CLI Options & Usage

```bash
OMGtoPS -in <infile> -out <outfile.ps>
```
* **`-in <infile>`**: Input 8-bit `OMG1` (`JHC_header`) raster file.
* **`-out <outfile.ps>`**: Output Encapsulated PostScript file.

## Algorithm
1. Reads the `JHC_header` via `jhc_read_header()` to obtain image dimensions (`width = xmax`, `height = ymax`) and verifies that `data_type == 1` (8-bit unsigned byte).
2. Computes the aspect-ratio-preserving scaling factor (`scale = 400.0 / max(width, height)`) and centers the bounding box on the page (`xoffset`, `yoffset`).
3. Writes an `EPSF-2.0` header (`%!PS-Adobe-2.0 EPSF-2.0`, `%%BoundingBox`) and a PostScript procedure that supports both Level 2 (`currentfile /ASCIIHexDecode filter`) and Level 1 (`readhexstring` + `image`) interpreters.
4. Encodes each raster scanline in two-character hexadecimal format (`%02x`, 36 bytes / 72 hex characters per line) followed by `showpage` and `%%Trailer`.
