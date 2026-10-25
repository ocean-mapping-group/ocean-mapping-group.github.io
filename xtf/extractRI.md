---
layout: default
title: extractRI
parent: eXtended Triton Format — XTF (xtf)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 2
tool_name: extractRI
source_path: code/xtf/extractRI.c
category: Backscatter & Image Processing
input_formats:
- .xtf
output_formats:
- .8bit
- .pgm
related_tools:
- extractSnippet
- stripSS
- xtfTool
- xtf2omg_reson
---

# extractRI

## Overview
`extractRI` extracts 8-bit beam reflectivity (intensity) values from Reson SeaBat bathymetry packets (`XTF_HEADER_BATHY`, packet ID 2) inside an XTF file and writes them as a 2D grayscale raster image (width = number of beams, height = number of bathymetry pings) in either the OMG/JHC `.8bit` format or Portable Graymap (`.pgm`) format.

## Usage

```bash
extractRI [-pgm] -in <basename_without_xtf_extension>
```

> [!IMPORTANT]
> `extractRI` automatically appends `.xtf` to the argument supplied to `-in` (`strAppend(basename, ".xtf")`). Pass the filename **without** the `.xtf` extension!

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<basename>` | **Required** | Base name of the input XTF file **without** the `.xtf` suffix (opens `<basename>.xtf`). |
| `-pgm` | None | Off (`.8bit`) | Output a standard Portable Graymap (`<basename>.pgm`) instead of an OMG/JHC headered 8-bit image (`<basename>.8bit`). |

## How It Works
1. **Indexing:** Opens `<basename>.xtf`, builds an in-memory packet index via `buildXTFIndex()`, and prints the packet summary table.
2. **Intensity Verification:** Seeks to the first `XTF_HEADER_BATHY` (ID 2) record, parses the `RESON_BATHY` payload, and checks that beam intensity values (`resonBathy.intensity`) are present.
3. **Header Initialization:** Writes either a PGM header (`writePGM`) or an OMG 8-bit raster header (`writeJHC`) with dimensions `resonBathy.beam_count` columns by `numBathyRecords` rows.
4. **Radiometric Correction & Output:** Iterates through every bathymetry record, calls `corrRESON_BATHY()` to normalize the Reson beam intensities into 8-bit values (`resonBathy.intensity8bit`), and writes one row of `beam_count` bytes per ping to `<basename>.pgm` or `<basename>.8bit`.

## Practical Examples

**1. Extract Reson beam intensities to an OMG `.8bit` raster (for `jview`):**

```bash
# Reads survey_line01.xtf and writes survey_line01.8bit
extractRI -in survey_line01
```

**2. Extract Reson beam intensities to a standard `.pgm` image:**

```bash
# Reads survey_line01.xtf and writes survey_line01.pgm
extractRI -pgm -in survey_line01
```
