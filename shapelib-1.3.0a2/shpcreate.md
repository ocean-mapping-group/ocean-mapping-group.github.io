---
layout: default
title: shpcreate
parent: Shapelib GIS Library & Tools (shapelib-1.3.0a2)
nav_order: 7
tool_name: shpcreate
source_path: code/shapelib-1.3.0a2/shpcreate.c
category: GIS & ESRI Shapefile Library / Tools
input_formats: ["CLI shape type specification"]
output_formats: [".shp", ".shx (empty ESRI Shapefile pair)"]
related_tools: ["shpadd", "shpdump", "shpopen", "dbfcreate"]
---

# shpcreate

## Overview

`shpcreate` (`code/shapelib-1.3.0a2/shpcreate.c`) is a command-line utility authored by Frank Warmerdam for creating a new, empty **ESRI Shapefile** pair (`.shp` main geometry file and `.shx` spatial index file) initialized with a 100-byte header for a specified 2D, 3D (`Z`), or Measured (`M`) geometry type.

In command-line GIS workflows, `shpcreate` is the first step when generating a new shapefile layer, typically followed by [`dbfcreate`](dbfcreate.md) (to create the companion `.dbf` attribute table) and repeated invocations of [`shpadd`](shpadd.md) and [`dbfadd`](dbfadd.md) to populate features.

---

## Usage

```bash
shpcreate <shp_file> <shape_type>
```

### Supported `<shape_type>` Values (Case-Insensitive)

`shpcreate` maps the second command-line argument (`argv[2]`, upper- or lower-case) to the corresponding Shapelib `SHPT_*` constant defined in `shapefil.h`:

| `<shape_type>` Argument | `shapefil.h` Constant | Integer Code | Geometry Description |
| :--- | :--- | :--- | :--- |
| `POINT` / `point` | `SHPT_POINT` | `1` | 2D Point $(X, Y)$ |
| `ARC` / `arc` | `SHPT_ARC` | `3` | 2D Polyline / Arc $(X, Y)$ |
| `POLYGON` / `polygon` | `SHPT_POLYGON` | `5` | 2D Polygon ring(s) $(X, Y)$ |
| `MULTIPOINT` / `multipoint` | `SHPT_MULTIPOINT` | `8` | 2D MultiPoint cluster $(X, Y)$ |
| `POINTZ` / `pointz` | `SHPT_POINTZ` | `11` | 3D Point $(X, Y, Z, M)$ |
| `ARCZ` / `arcz` | `SHPT_ARCZ` | `13` | 3D Polyline / Arc $(X, Y, Z, M)$ |
| `POLYGONZ` / `polygonz` | `SHPT_POLYGONZ` | `15` | 3D Polygon ring(s) $(X, Y, Z, M)$ |
| `MULTIPOINTZ` / `multipointz` | `SHPT_MULTIPOINTZ` | `18` | 3D MultiPoint cluster $(X, Y, Z, M)$ |
| `POINTM` / `pointm` | `SHPT_POINTM` | `21` | 2D Measured Point $(X, Y, M)$ |
| `ARCM` / `arcm` | `SHPT_ARCM` | `23` | 2D Measured Polyline / Arc $(X, Y, M)$ |
| `POLYGONM` / `polygonm` | `SHPT_POLYGONM` | `25` | 2D Measured Polygon ring(s) $(X, Y, M)$ |
| `MULTIPOINTM` / `multipointm` | `SHPT_MULTIPOINTM` | `28` | 2D Measured MultiPoint cluster $(X, Y, M)$ |

### Exit Codes

| Exit Code | Condition |
| :--- | :--- |
| `0` | `.shp` and `.shx` files successfully created and closed. |
| `1` | Incorrect argument count (`argc != 3`); prints `shpcreate shp_file [point/arc/polygon/multipoint][/m/z]`. |
| `2` | Unrecognized `<shape_type>` string (`Shape Type '<arg>' not recognised.`). |
| `3` | `SHPCreate(argv[1], nShapeType)` returned `NULL` (`Unable to create:<file>`). |

---

## Internal Execution Flow

1. Validates `argc == 3` and resolves `argv[2]` to `nShapeType`.
2. Calls `hSHP = SHPCreate(argv[1], nShapeType)`, which strips any existing extension from `argv[1]`, creates `<basename>.shp` and `<basename>.shx` in `"wb"` mode, writes the initial 100-byte big/little-endian ESRI header (magic cookie `9994` = `0x0000270a`, version `1000`, shape type `nShapeType`, and zeroed bounds), and returns an open `SHPHandle`.
3. Calls `SHPClose(hSHP)` to flush headers and close both files.

---

## Example Usage

```bash
# Create a 2D polyline shapefile for ship navigation tracklines
shpcreate nav_tracks arc

# Create a 3D point shapefile for multibeam sounding picks
shpcreate soundings pointz
```
