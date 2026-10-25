---
layout: default
title: calcArea
parent: Ian Church (ianc) Tools
nav_order: 5
tool_name: calcArea
source_path: code/ianc/calcArea.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats: ["OMG R4 Floating-Point Grid (.r4)", "OMG 8-Bit Raster Grid (.8bit / .mos)"]
output_formats: ["ASCII Area Summary (stdout)"]
related_tools: ["checkEmpty", "modelAnalysis"]
---

# calcArea

## Description

`calcArea` calculates the valid data coverage area (in square meters and square kilometers) of one or more OMG/JHC raster grid files (`.r4` 32-bit floating-point grids or `.8bit`/`.mos` 8-bit unsigned integer grids). Written by Ian Church in December 2012, the tool reads the 1024-byte `JHC_header` of each input map sheet, verifies that the grid uses a projected coordinate system, computes the area of each pixel (`xstep * ystep`), and sums the area of all non-empty grid cells across each file and across the entire batch of input files.

## Usage

```bash
calcArea [-v] -in <mapSheet1> [mapSheet2 ...]
```

### Example Commands

Calculate the surveyed area of a single `.r4` bathymetric grid:

```bash
calcArea -in bay_of_fundy_2m.r4
```

Calculate individual sheet areas and total combined coverage across multiple `.r4` or `.8bit` map sheets:

```bash
calcArea -v -in sheet01.r4 sheet02.r4 sheet03.r4
```

## CLI Arguments and Options

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-v` | None | Increments the verbosity flag (`verbose_flag`). |
| `-in` | `<file1> [file2 ...]` | **Required.** One or more OMG raster grid files (`.r4`, `.8bit`, `.mos`), up to 10,000 files. Consumes all subsequent arguments until the next `-` flag or end of command line. |

## File Formats

### Input Formats: OMG Raster Grids (`.r4`, `.8bit`, `.mos`)
* **Header**: 1024-byte `JHC_header` read via `read_JHC_header(FILE *, JHC_header *)` (from `array.h`). Key header fields used by `calcArea`:
  * `projection`: Must not be `0` (unprojected) or `3` (geographic lat/lon); otherwise `calcArea` prints `Map is not projected, so can't calculate area....skipping` and skips the file.
  * `data_type`: `3` indicates 32-bit floating-point (`float`, `.r4`); other values are treated as 8-bit unsigned char (`unsigned char`, `.8bit`/`.mos`).
  * `dx`, `dy`: Grid dimensions in pixels (columns and rows).
  * `xstep`, `ystep`: Cell resolution in meters along X and Y.
* **Grid Data Payload**:
  * For `.r4` files (`data_type == 3`): A pixel is counted as valid data if `varF != 0.0f`.
  * For 8-bit files (`data_type != 3`): A pixel is counted as valid data if `var != 0 && var != 255` (since both `0` and `255` represent background/no-data in OMG 8-bit images).

### Output Format
For each valid projected map sheet, `calcArea` prints a single summary line to `stdout`:
```text
Map <filename> area: <sumArea> m^2 of <mapArea> m^2 total area ( <percent> percent )
```
When more than one input file is provided (`nFiles > 1`), a grand total line is printed at the end:
```text
Total Area of all input maps: <totalArea> m^2 or <totalArea_km2> km^2
```

## How It Works

1. **Header Inspection & Projection Check**: For each file passed after `-in`, `calcArea` opens the file in binary read mode (`"rb"`) and calls `read_JHC_header()`. If `JHChead.projection == 0 || JHChead.projection == 3`, the grid steps are not in linear meters, so the file is skipped.
2. **Pixel & Bounding Box Area Calculation**:
   * Total number of grid cells: `pixels = JHChead.dx * JHChead.dy`
   * Single-cell area: `pixArea = JHChead.xstep * JHChead.ystep`
   * Total bounding-box area: `mapArea = pixArea * pixels`
3. **Cell-by-Cell Accumulation**:
   * If `JHChead.data_type == 3` (`r4Flag == 1`), the program reads 4-byte `float` values until `feof()`, adding `pixArea` to `sumArea` whenever `varF != 0`.
   * Otherwise, it reads 1-byte `unsigned char` values until `feof()`, adding `pixArea` to `sumArea` whenever `var != 0 && var != 255`.
4. **Multi-Sheet Aggregation**: Each sheet's `sumArea` is added to `totalArea`, and if `nFiles > 1`, the total area is reported in both square meters (`m^2`) and square kilometers (`totalArea / 1000000`).
