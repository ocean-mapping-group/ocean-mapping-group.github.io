---
layout: default
title: shpadd
parent: Shapelib GIS Library & Tools (shapelib-1.3.0a2)
nav_order: 6
tool_name: shpadd
source_path: code/shapelib-1.3.0a2/shpadd.c
category: GIS & ESRI Shapefile Library / Tools
input_formats: [".shp", ".shx", "CLI vertex coordinate stream"]
output_formats: [".shp", ".shx (with appended shape entity)"]
related_tools: ["shpcreate", "shpdump", "shpopen", "dbfadd", "dbfcreate"]
---

# shpadd

## Overview

`shpadd` (`code/shapelib-1.3.0a2/shpadd.c`) is a command-line utility authored by Frank Warmerdam for appending a new geometric shape (2D, 3D `Z`, Measured `M`, or 4D `ZM`, with single or multiple rings/parts)—or a `SHPT_NULL` shape—to an existing ESRI Shapefile (`.shp` and `.shx`).

Together with [`shpcreate`](shpcreate.md), [`dbfcreate`](dbfcreate.md), and [`dbfadd`](dbfadd.md), `shpadd` allows shell scripts and batch hydrographic pipelines to construct complete point, polyline (`ARC`), polygon, or multipoint shapefiles directly from command-line coordinate lists without writing custom C programs.

---

## Usage

```bash
# 1. Append a 2D shape (X Y vertex pairs, with optional '+' separating multiple parts/rings):
shpadd <shp_file> [[<x> <y>] [+]]*

# 2. Append a 2D+Measure (-m) shape (X Y M vertex triplets):
shpadd <shp_file> -m [[<x> <y> <m>] [+]]*

# 3. Append a 3D (-z) shape (X Y Z vertex triplets):
shpadd <shp_file> -z [[<x> <y> <z>] [+]]*

# 4. Append a 3D+Measure (-zm) shape (X Y Z M vertex quadruplets):
shpadd <shp_file> -zm [[<x> <y> <z> <m>] [+]]*

# 5. Append a NULL shape (SHPT_NULL) by supplying no vertex coordinates:
shpadd <shp_file>
```

### Command-Line Options & Syntax

| Argument / Token | Description |
| :--- | :--- |
| `<shp_file>` | **Required.** Path or basename of an existing ESRI Shapefile (opened in `"r+b"` mode via `SHPOpen()`). |
| `-z` | Indicates that each vertex on the command line consists of 3 floating-point values: `<x> <y> <z>`. |
| `-m` | Indicates that each vertex on the command line consists of 3 floating-point values: `<x> <y> <m>`. |
| `-zm` | Indicates that each vertex on the command line consists of 4 floating-point values: `<x> <y> <z> <m>`. |
| `+` | Starts a new part (polyline segment or polygon inner/outer ring) at the current vertex index (`panParts[nParts++] = nVertices`). Up to 1,000 parts are supported per shape. |

---

## Internal Execution Flow & Dynamic Vertex Allocation

1. **Shapefile Open & Shape Type Detection**:
   - Opens `<shp_file>` via `hSHP = SHPOpen(filename, "r+b")` and queries the layer's default `nShapeType` via `SHPGetInfo(hSHP, NULL, &nShapeType, NULL, NULL)`.
   - If no vertex arguments follow `<shp_file>` (and any `-z`/`-m`/`-zm` flag), overrides `nShapeType = SHPT_NULL` (`0`) so a null geometry record can be appended.
2. **Dynamic Vertex & Part List Construction**:
   - Initializes `nVMax = 1000` and allocates heap arrays `padfX`, `padfY` (plus `padfZ` if `tuple` contains `'z'` and `padfM` if `tuple` contains `'m'`), along with `panParts` (capacity `1000`, `panParts[0] = 0`, `nParts = 1`).
   - Loops through all remaining CLI arguments:
     - If `argv[i][0] == '+'`, records the start of a new part at `panParts[nParts++] = nVertices`.
     - Otherwise, if `nVertices == nVMax`, doubles `nVMax = nVMax * 2` and `realloc()`s `padfX`, `padfY`, `padfZ`, and `padfM`.
     - Parses `<x>`, `<y>`, and optional `<z>` and `<m>` using `sscanf(argv[i++], "%lg", ...)` and increments `nVertices`.
3. **Object Creation & Append**:
   - Calls `psObject = SHPCreateObject(nShapeType, -1, nParts, panParts, NULL, nVertices, padfX, padfY, padfZ, padfM)`.
   - Appends the shape at the end of `.shp`/`.shx` (`iShape = -1`) via `SHPWriteObject(hSHP, -1, psObject)`.
   - Frees memory (`SHPDestroyObject(psObject)`, `SHPClose(hSHP)`, `free()`).

---

## Example Workflow

```bash
# Create a 3D trackline shapefile and append a two-part 3D survey line (X Y Z)
shpcreate track_3d arcz
shpadd track_3d -z \
    -63.5710 44.6250 -15.2 \
    -63.5720 44.6260 -18.5 \
    + \
    -63.5800 44.6300 -22.1 \
    -63.5810 44.6310 -24.0
```
