---
layout: default
title: makeDBF
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 24
tool_name: makeDBF
source_path: code/nav/makeDBF.c
category: Navigation & Georeferencing
input_formats:
- Command-line URL/path string
output_formats:
- .dbf
related_tools:
- navtoSHP
- iNav2SHP
- readSHP
---

# makeDBF

## Description
`makeDBF` generates a companion dBASE III (`.dbf`) attribute table file for single-record ESRI Polyline Shapefiles created by [`navtoSHP`](navtoSHP.html).

Because [`navtoSHP`](navtoSHP.html) writes only the geometry (`.shp`) and spatial index (`.shx`) files for a survey line track, GIS packages (such as ArcGIS and QGIS) require a matching `<line>.dbf` file with the same base name to load the Shapefile layer. `makeDBF` writes a 1-record `.dbf` file containing standard arc-node topology fields (`FNODE_`, `TNODE_`, `LPOLY_`, `RPOLY_`, `LENGTH`, `WOZZIT`, `WOZZIT_ID`, `LINE`) plus a 50-character `HYPERLINK` attribute populated with a user-specified HTML/image path (`-url`), enabling click-to-open line summary pages or sidescan/backscatter waterfall imagery directly from the GIS map canvas.

---

## Usage

```bash
makeDBF [-v] -dbf <filename.dbf> -url <hyperlink_path>
```

### Common Workflow Examples

**1. Create a `.shp`/`.shx` trackline with `navtoSHP` and generate its companion `.dbf` with `makeDBF`:**

```bash
# 1. Create 0001_line.shp and 0001_line.shx
navtoSHP -skip 5 merged/JD100/0001_line.nav

# 2. Create 0001_line.dbf with a hyperlink to the line's HTML/image preview
makeDBF -dbf merged/JD100/0001_line.dbf -url images/0001_line.html
```

**2. Batch-generate `.dbf` files for all `.shp` tracklines in a directory:**

```bash
for shp in tracks/*.shp; do
    base=$(basename "$shp" .shp)
    makeDBF -dbf "tracks/${base}.dbf" -url "images/${base}.html"
done
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-dbf <filename.dbf>` | **Required.** Output `.dbf` filename (should match the base name of the `.shp` and `.shx` files created by `navtoSHP`). | None |
| `-url <string>` | **Required.** Hyperlink string (up to 49 characters, e.g., `images/line1.html`) written into the `HYPERLINK` attribute column of record 1. | None |
| `-skip <sec>` | Parsed on the command line for CLI symmetry with `navtoSHP` (prints `"Dumping every N seconds"`), not used in `.dbf` output. | `0` |
| `-v` | Increment verbose flag. | Disabled |

---

## Binary `.dbf` File Layout

`makeDBF` writes a fixed-size **487-byte** dBASE III file consisting of a 32-byte file header, nine 32-byte field descriptors (288 bytes), a 1-byte header terminator (`0x0D`), and one 166-byte space-padded data record (167 bytes total with the terminator):

### 1. File Header (32 bytes)
* Byte `0`: `0x03` (dBASE III without memo file).
* Byte `1`: `'j'` (date stamp placeholder).
* Bytes `4..7` (`int32`): `1` (number of records in the table).
* Bytes `8..9` (`int16`): `321` (`32 + 9*32 + 1`, total byte length of the header structure).
* Bytes `10..11` (`int16`): `167` (byte length of each record).
* Byte `29`: `0x1B` (language driver ID).

### 2. Field Descriptor Array (9 × 32 bytes)

| Field # | Field Name | Type | Width (Bytes) | Record Byte Offset | Description |
|---|---|---|---|---|---|
| 1 | `FNODE_` | `'N'` (Numeric) | `11` (`0x0B`) | `1..11` | From-node topology ID |
| 2 | `TNODE_` | `'N'` (Numeric) | `11` (`0x0B`) | `12..22` | To-node topology ID |
| 3 | `LPOLY_` | `'N'` (Numeric) | `11` (`0x0B`) | `23..33` | Left polygon ID |
| 4 | `RPOLY_` | `'N'` (Numeric) | `11` (`0x0B`) | `34..44` | Right polygon ID |
| 5 | `LENGTH` | `'F'` (Float) | `20` (word `1300`) | `45..64` | Arc length field |
| 6 | `WOZZIT` | `'N'` (Numeric) | `11` (`0x0B`) | `65..75` | Feature number |
| 7 | `WOZZIT_ID` | `'N'` (Numeric) | `11` (`0x0B`) | `76..86` | Feature user ID |
| 8 | `LINE` | `'C'` (Character) | `30` (`0x1E`) | `87..116` | Survey line name |
| 9 | `HYPERLINK` | `'C'` (Character) | `50` (`0x32`) | `117..166` | URL / file path (`-url` copied at `record + 118`) |
