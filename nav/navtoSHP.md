---
layout: default
title: navtoSHP
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 26
tool_name: navtoSHP
source_path: code/nav/navtoSHP.c
category: Navigation & Georeferencing
input_formats:
- .nav
output_formats:
- .shp
- .shx
related_tools:
- makeDBF
- iNav2SHP
- readSHP
- appendNav
---

# navtoSHP

## Description
`navtoSHP` is a lightweight, zero-dependency converter that reads a binary OMG navigation file (`.nav`, `jcu_nav_rec`) and writes a 2D ESRI Polyline Shapefile (`<basename>.shp`) and its spatial index (`<basename>.shx`) using the internal OMG Shapefile library (`code/subr/j_SHP.c`).

Unlike [`iNav2SHP`](iNav2SHP.html) (which uses external Shapelib and creates 3D `SHPT_*Z` geometries with `.dbf` and `.prj` files), `navtoSHP` writes a single 2D `JSHP_POLYLINE` (Shape Type `3`) record containing the trackline vertices and is designed to be paired with [`makeDBF`](makeDBF.html) to attach a hyperlink `.dbf` table.

---

## Usage

```bash
navtoSHP [-v] [-skip <seconds>] <filename.nav>
```

### Common Workflow Examples

**1. Convert a binary `.nav` file to `.shp` and `.shx` sampled every 5 seconds:**

```bash
navtoSHP -skip 5 merged/JD100/0001_line.nav
# Produces: merged/JD100/0001_line.shp and merged/JD100/0001_line.shx
```

**2. Complete GIS trackline workflow with `navtoSHP` + `makeDBF`:**

```bash
navtoSHP -skip 3 merged/JD100/0001_line.nav
makeDBF -dbf merged/JD100/0001_line.dbf -url images/0001_line.html
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<filename>` | **Required.** Input binary `.nav` file. `navtoSHP` strips the file extension (`mem_stripext`) and creates `<basename>.shp` and `<basename>.shx`. | None |
| `-skip <seconds>` | Time-modulo decimation interval in integer seconds. Only fixes where `((int)nav_rec.time) % skip < 1` are written to the polyline. If `0` (or omitted), every fix is included. | `0` (all fixes) |
| `-v` | Increment verbose flag. | Disabled |

> [!WARNING]
> **Static Vertex Buffer Limit & Sub-Second Sampling with `-skip`:**
> 1. `j_shape_record_contents` (`code/subr/j_SHP.h`) allocates a static array of `points[1000000]` (1,000,000 points). Ensure your input `.nav` file (after `-skip`) contains fewer than 1,000,000 vertices.
> 2. Because `-skip` checks `((int)nav_rec.time) % skip < 1`, if the input `.nav` file has multiple fixes per second (e.g., 10 Hz POS MV navigation), **all fixes within each matching whole second** will pass the modulo filter. To decimate strictly by record count instead of integer second modulo, use [`iNav2SHP -skip N`](iNav2SHP.html) or pre-decimate with [`appendNav -skip N`](appendNav.html).

---

## Binary Shapefile Structure (`j_SHP.h`)

`navtoSHP` writes standard ESRI Shapefile big-endian/little-endian mixed headers:

1. **100-Byte File Header (`j_shape_file_header`):**
   * `BE_File_Code`: `9994` (Big-Endian `int32`).
   * `BE_File_Length`: Total file length in 16-bit words (`ftell(file) / 2`, Big-Endian `int32`), updated on a second header pass after writing the geometry record.
   * `LE_Version`: `1000` (Little-Endian `int32`).
   * `LE_Shape_Type`: `3` (`JSHP_POLYLINE`, Little-Endian `int32`).
   * `LE_bounding_Xmin`, `Ymin`, `Xmax`, `Ymax`: Trackline geographic bounding box (`lon`, `lat` in decimal degrees, Little-Endian `double`).
2. **8-Byte Index Record in `.shx` (`j_shape_index_record`):**
   * `BE_Offset`: `50` (100 bytes / 2, in 16-bit words).
   * `BE_Content_Length`: `(4 + 32 + 4 + 4 + 4 * LE_noParts + LE_noPoints * 16) / 2` (in 16-bit words).
3. **Polyline Record in `.shp` (`j_shape_record_header` + `j_shape_record_contents`):**
   * Record Number `1`, `LE_Shape_Type = 3`, `LE_noParts = 1`, `parts[0] = 0`, followed by `LE_noPoints` pairs of `(LE_X = lon, LE_Y = lat)` IEEE-754 doubles.
