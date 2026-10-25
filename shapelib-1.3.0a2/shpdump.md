---
layout: default
title: shpdump
parent: Shapelib GIS Library & Tools (shapelib-1.3.0a2)
nav_order: 8
tool_name: shpdump
source_path: code/shapelib-1.3.0a2/shpdump.c
category: GIS & ESRI Shapefile Library / Tools
input_formats: [".shp", ".shx (ESRI Shapefile)"]
output_formats: ["STDOUT human-readable geometry & bounds dump"]
related_tools: ["shpcreate", "shpadd", "shprewind", "shpopen", "dbfdump"]
---

# shpdump

## Overview

`shpdump` (`code/shapelib-1.3.0a2/shpdump.c`) is a command-line diagnostic utility authored by Frank Warmerdam that reads an **ESRI Shapefile** (`.shp` and `.shx`) and dumps its global bounding box, shape type, entity count, and per-shape vertex coordinates, part boundaries (`+`), part types (`Ring`, `OuterRing`, `InnerRing`, `TriangleStrip`, `TriangleFan`), and polygon ring orientation validity to `stdout`.

---

## Usage

```bash
shpdump [-validate] [-ho] <shp_file>
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-validate` | *(none)* | Calls `SHPRewindObject(hSHP, psShape)` on each shape as it is read and reports how many polygon rings were wound in the wrong direction (`<n> rings wound in the wrong direction.` and `<total> object has invalid ring orderings.`). Must be passed **first** if combined with `-ho`. |
| `-ho` | *(none)* | **Header Only**: Prints only the global shapefile type, total shape count, and 4D file bounds (`adfMinBound[0..3]` to `adfMaxBound[0..3]`), skipping individual shape records. |
| `<shp_file>` | *(positional)* | **Required.** Path or basename of the input `.shp` file (opened read-only via `SHPOpen(argv[1], "rb")`). |

---

## Internal Execution Flow & Output Details

1. **Global Header Summary (`SHPGetInfo`)**:
   - Calls `SHPGetInfo(hSHP, &nEntities, &nShapeType, adfMinBound, adfMaxBound)`.
   - Prints `Shapefile Type: <SHPTypeName>   # of Shapes: <nEntities>` and the 4D `(X, Y, Z, M)` global `File Bounds`.
2. **Per-Shape Inspection Loop (`!bHeaderOnly`)**:
   - Iterates `for (i = 0; i < nEntities && !bHeaderOnly; i++)`:
     - Reads shape `i` via `psShape = SHPReadObject(hSHP, i)`.
     - Checks `psShape->bMeasureIsUsed`: if true, prints 4D `(X, Y, Z, M)` shape bounds and vertices; if false, prints 3D `(X, Y, Z)` shape bounds and vertices (avoiding bogus `no-data` measure values $< -10^{38}$).
     - Validates `psShape->panPartStart[0] == 0` when `nParts > 0`, emitting a warning to `stderr` if non-zero.
     - Prints each vertex `j` (`0 .. nVertices - 1`), prefixing the first vertex of each secondary part (`j == panPartStart[iPart]`) with a `+` marker and appending the part type name (`SHPPartTypeName(panPartType[iPart])`).
     - If `-validate` is set, invokes `SHPRewindObject(hSHP, psShape)` and increments `nInvalidCount` whenever one or more rings had to be reversed.
     - Frees the object with `SHPDestroyObject(psShape)`.

---

## Example Output

```text
$ shpdump -validate survey_bounds.shp
Shapefile Type: Polygon   # of Shapes: 1

File Bounds: (     -63.600,      44.600,0,0)
         to  (     -63.500,      44.700,0,0)

Shape:0 (Polygon)  nVertices=5, nParts=1
  Bounds:(     -63.600,      44.600, 0)
      to (     -63.500,      44.700, 0)
     (     -63.600,      44.600, 0) Ring 
     (     -63.600,      44.700, 0)  
     (     -63.500,      44.700, 0)  
     (     -63.500,      44.600, 0)  
     (     -63.600,      44.600, 0)  
0 object has invalid ring orderings.
```
