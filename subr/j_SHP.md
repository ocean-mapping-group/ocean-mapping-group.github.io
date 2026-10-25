---
layout: default
title: j_SHP
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_SHP.c
category: GIS Export, Contouring & Shapefile I/O
related_tools:
- navtoSHP
- readSHP
module_name: j_SHP
header_path: code/subr/j_SHP.h
---

# `j_SHP` — ESRI Shapefile (`.shp` / `.shx`) Binary Reader and Writer

## Overview & Purpose
The `j_SHP` module (`code/subr/j_SHP.c` and `code/subr/j_SHP.h`) implements a self-contained binary reader and writer for ESRI Shapefiles (`.shp` geometry files and `.shx` spatial index files). Written by John E. Hughes Clarke in October 2007 and updated in February 2023 to support high-density multi-part geometries (up to `10,000` parts and `1,000,000` vertices per record), it handles the mixed-endian ESRI Shapefile binary specification (`swap_int.h`) so OMG navigation tracklines, coastline polygons, and survey bounds can be exchanged directly with ArcGIS, QGIS, and other GIS platforms.

---

## Mixed-Endian Architecture & Data Structures (`j_SHP.h`)

### Mixed-Endian Convention
Per the ESRI Shapefile Technical Description (July 1998):
- **Big-Endian (`BE_*`) 32-bit Integers:** File codes (`9994`), file lengths, record numbers, content lengths, and `.shx` index offsets are stored in **Big-Endian** byte order and measured in **16-bit words** (`2` bytes per word). On standard little-endian (`x86_64`) Linux machines (`#ifndef MOTOROLA`), `j_SHP.c` automatically byte-swaps these fields via `swap_int()`.
- **Little-Endian (`LE_*`) Integers & IEEE Doubles:** Version numbers (`1000`), shape type codes, bounding boxes, part counts, and $(X, Y)$ vertex coordinates are stored in **Little-Endian** byte order.

### Key Structures
- **`j_shape_file_header` (100 bytes):**

  ```c
  typedef struct {
      signed int BE_File_Code;      /* Always 9994 (0x0000270A) */
      signed int BE_Unused[5];      /* Five 32-bit zeros */
      signed int BE_File_Length;    /* Total file length in 16-bit words */
      signed int LE_Version;        /* Always 1000 */
      signed int LE_Shape_Type;     /* e.g. 1 = Point, 3 = PolyLine, 5 = Polygon */
      double LE_bounding_Xmin, LE_bounding_Ymin;
      double LE_bounding_Xmax, LE_bounding_Ymax;
      double LE_bounding_Zmin, LE_bounding_Zmax;
      double LE_bounding_Mmin, LE_bounding_Mmax;
  } j_shape_file_header;
  ```
- **`j_shape_record_header` (8 bytes):** `{ signed int BE_Record_Number; signed int BE_Content_Length; }`.
- **`j_shape_index_record` (8 bytes in `.shx`):** `{ signed int BE_Offset; signed int BE_Content_Length; }`.
- **`j_shape_point` & `j_shape_bounding_box`:** 2D double-precision coordinate pair `{ double LE_X, LE_Y; }` and bounding box `{ double LE_Xmin, LE_Ymin, LE_Xmax, LE_Ymax; }`.
- **`j_shape_record_contents`:**

  ```c
  typedef struct {
      signed int LE_Shape_Type;
      j_shape_bounding_box bounds;
      signed int LE_noParts;
      signed int LE_noPoints;
      signed int parts[10000];
      j_shape_point points[1000000];
  } j_shape_record_contents;
  ```

---

## Public Functions & Signatures

### 1. Header Initialization, I/O, and Diagnostics

```c
int init_shp_header(j_shape_file_header *sh_fl_head);
int read_shp_header(FILE *file, j_shape_file_header *sh_fl_head);
int write_shp_header(FILE *file, j_shape_file_header sh_fl_head);
int print_shp_header(j_shape_file_header *sh_fl_head);
```
- **`init_shp_header()`:** Populates a default 100-byte header (`BE_File_Code = 9994`, `LE_Version = 1000`, `LE_Shape_Type = JSHP_POLYLINE (3)`, zeroed bounds).
- **`write_shp_header()`:** Determines the current end-of-file position via `ftell(file)`, computes `BE_File_Length = tot_bytes / 2` (in 16-bit words), rewinds to byte `0`, byte-swaps the big-endian header fields, and writes the 100-byte header block.

### 2. Geometry Record & Spatial Index I/O

```c
int read_shp_record(FILE *file, j_shape_record_header *sh_rec_head, j_shape_record_contents *sh_rec_cont);
int write_shp_record(FILE *file, j_shape_record_header sh_rec_head, j_shape_record_contents sh_rec_cont);
int print_shp_record(j_shape_record_header *sh_rec_head, j_shape_record_contents *sh_rec_cont);

int read_shp_index_record(FILE *file, j_shape_index_record *sh_inx_rec);
int write_shp_index_record(FILE *file, j_shape_index_record sh_inx_rec);
int print_shp_index_record(j_shape_index_record *sh_inx_rec);
```
- **`read_shp_record()`:** Reads the 8-byte `j_shape_record_header` and `LE_Shape_Type`. Supports both single-point records (`LE_Shape_Type == 1`, reading one `j_shape_point`) and multi-part polylines/polygons (`LE_Shape_Type == 3` or `5`, reading the 32-byte bounding box, `LE_noParts`, `LE_noPoints`, the `parts[]` starting-vertex index array, and the `points[]` vertex array).
- **`write_shp_record()`:** Computes `BE_Content_Length = (44 + 4 * LE_noParts + 16 * LE_noPoints) / 2` in 16-bit words, writes the byte-swapped record header, and serializes the polyline/polygon geometry payload.

---

## How It Fits Into the OMG Architecture
- **Navigation Trackline Export (`navtoSHP`):** `code/nav/navtoSHP.c` reads OMG ship navigation and swath coverage files and calls `init_shp_header()`, `write_shp_record()`, `write_shp_index_record()`, and `write_shp_header()` to produce GIS-ready `.shp` and `.shx` survey trackline layers.
- **Shapefile Inspection & Import (`readSHP`):** `code/nav/readSHP.c` uses `read_shp_header()` and `read_shp_record()` to parse external coastline, boundary, and navigation shapefiles into OMG ASCII/binary overlays.
