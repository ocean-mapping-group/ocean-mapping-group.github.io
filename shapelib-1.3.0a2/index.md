---
layout: default
title: Shapelib GIS Library & Tools (shapelib-1.3.0a2)
has_children: true
nav_order: 29
category: GIS & ESRI Shapefile Library / Tools
source_path: code/shapelib-1.3.0a2/
related_tools: ["shpopen", "dbfopen", "shptree", "safileio", "shpcreate", "shpadd", "shpdump", "shprewind", "shptest", "shptreedump", "shputils", "dbfcreate", "dbfadd", "dbfdump", "iNav2SHP"]
---

# Shapelib 1.3.0a2 GIS Library & Utilities (`shapelib-1.3.0a2/`)

## Overview

The `shapelib-1.3.0a2/` (`code/shapelib-1.3.0a2/`) directory houses **Shapelib 1.3.0a2** (authored by Frank Warmerdam, with `shputils` by Bill Miller and UTF-8/codepage hooks by Bram de Greve), the standard C library and command-line toolset for reading, writing, indexing, and manipulating **ESRI Shapefiles** (`.shp` geometry, `.shx` spatial offset index, `.dbf` xBase attribute table, and `.qix` quadtree spatial index).

In the **UNB Ocean Mapping Group (OMG)** build architecture (`compile_every_gd_thing`), `shapelib-1.3.0a2/shapefil.h` is installed into `$DEVELOPMENT_HOME/local/include/shapefil.h` and its core object modules (`shpopen.o`, `dbfopen.o`, `shptree.o`, `safileio.o`) are linked into GIS export utilities such as [`iNav2SHP`](../nav/iNav2SHP.md) (`code/nav/iNav2SHP.c`), enabling survey navigation tracklines, swath coverage polygons, and acoustic feature picks to be exported directly into ESRI ArcView / ArcGIS / QGIS shapefiles.

---

## Core C Library Modules (`shapefil.h`)

| Module | Source File | Primary Role & Public API |
| :--- | :--- | :--- |
| **[`shpopen`](shpopen.md)** | `code/shapelib-1.3.0a2/shpopen.c` | Core `.shp` and `.shx` geometry I/O library (`SHPOpen`, `SHPCreate`, `SHPGetInfo`, `SHPReadObject`, `SHPWriteObject`, `SHPCreateObject`, `SHPRewindObject`, `SHPClose`). |
| **[`dbfopen`](dbfopen.md)** | `code/shapelib-1.3.0a2/dbfopen.c` | Core `.dbf` (xBase) tabular attribute I/O library (`DBFOpen`, `DBFCreate`, `DBFAddField`, `DBFRead*Attribute`, `DBFWrite*Attribute`, `DBFCloneEmpty`, `DBFClose`). |
| **[`shptree`](shptree.md)** | `code/shapelib-1.3.0a2/shptree.c` | In-memory and on-disk (`.qix`) spatial quadtree indexing and bounding-box search API (`SHPCreateTree`, `SHPTreeFindLikelyShapes`, `SHPWriteTree`, `SHPSearchDiskTree`). |
| **[`safileio`](safileio.md)** | `code/shapelib-1.3.0a2/safileio.c` | Abstracted file I/O and error/locale hook layer (`SAHooks`, `SASetupDefaultHooks`, `SASetupUtf8Hooks`, `SADFOpen`, `SADFRead`, `SADFWrite`, `SADFSeek`). |

---

## Command-Line Utilities

| Tool | Source File | Primary Role |
| :--- | :--- | :--- |
| **[`shpcreate`](shpcreate.md)** | `code/shapelib-1.3.0a2/shpcreate.c` | Creates a new empty `.shp` / `.shx` shapefile pair of a specified 2D, 3D (`Z`), or Measured (`M`) geometry type (`point`, `arc`, `polygon`, `multipoint`, `pointz`, `arcz`, `polygonz`, etc.). |
| **[`shpadd`](shpadd.md)** | `code/shapelib-1.3.0a2/shpadd.c` | Appends a new multi-part or single-part geometric shape (`X Y [Z] [M]` vertex tuples separated by `+` for ring/part boundaries) to an existing `.shp` / `.shx` file. |
| **[`shpdump`](shpdump.md)** | `code/shapelib-1.3.0a2/shpdump.c` | Dumps shapefile header bounds, entity counts, part types, and per-vertex coordinates (`-ho` for header-only, `-validate` to verify polygon ring winding order). |
| **[`shprewind`](shprewind.md)** | `code/shapelib-1.3.0a2/shprewind.c` | Validates and corrects polygon ring vertex winding orientation (clockwise outer rings, counter-clockwise inner holes) per the ESRI Shapefile specification. |
| **[`shptest`](shptest.md)** | `code/shapelib-1.3.0a2/shptest.c` | Regression test generator (`test0.shp` through `test13.shp`) exercising all 14 ESRI shape types (`Null`, `Point`, `PointZ`, `PointM`, `MultiPoint*`, `Arc*`, `Polygon*`, `MultiPatch`). |
| **[`shptreedump`](shptreedump.md)** | `code/shapelib-1.3.0a2/shptreedump.c` | Builds, dumps, queries (`-search xmin ymin xmax ymax`), and exports (`-o <index.qix>`) spatial quadtrees for shapefiles. |
| **[`shputils`](shputils.md)** | `code/shapelib-1.3.0a2/shputils.c` | Comprehensive GIS processing Swiss-Army knife: describes schemas, appends shapefiles with automatic DBF field merging, filters by attribute (`SELECT`/`UNSEL`), clips/erases by bounding box (`CLIP`/`ERASE`), rescales units (`FACTOR`), and shifts coordinates (`SHIFT`). |
| **[`dbfcreate`](dbfcreate.md)** | `code/shapelib-1.3.0a2/dbfcreate.c` | Creates a new empty `.dbf` xBase attribute table with user-defined string (`-s name width`) and numeric (`-n name width decimals`) columns. |
| **[`dbfadd`](dbfadd.md)** | `code/shapelib-1.3.0a2/dbfadd.c` | Appends a new attribute record (row) of string, numeric, or `NULL` (`""`) field values to an existing `.dbf` table. |
| **[`dbfdump`](dbfdump.md)** | `code/shapelib-1.3.0a2/dbfdump.c` | Dumps `.dbf` xBase records to `stdout` in formatted columns, raw unformatted strings (`-r`), multi-line record blocks (`-m`), and with schema field headers (`-h`). |
