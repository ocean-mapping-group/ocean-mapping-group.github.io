---
layout: default
title: shprewind
parent: ESRI Shapefile C Library (shapelib-1.3.0a2)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 10
tool_name: shprewind
source_path: code/shapelib-1.3.0a2/shprewind.c
category: GIS & ESRI Shapefile Library / Tools
input_formats:
- .shp
- .shx (Polygon / PolygonZ / PolygonM ESRI Shapefile)
output_formats:
- .shp
- .shx (rewound ESRI Shapefile)
related_tools:
- shpdump
- shpopen
- shputils
---

# shprewind

## Overview

`shprewind` (`code/shapelib-1.3.0a2/shprewind.c`) is a command-line geometry repair utility authored by Frank Warmerdam that validates and resets the vertex winding order of rings in polygon shapefiles (`SHPT_POLYGON`, `SHPT_POLYGONZ`, `SHPT_POLYGONM`) to conform strictly to the **ESRI Shapefile Technical Description**.

According to the ESRI Shapefile specification, multi-ring polygons distinguish exterior boundaries from interior holes ("islands" vs. "lakes") solely by vertex winding orientation:
- **Outer (Exterior) Rings** must be wound **clockwise** (when viewed in a standard Cartesian coordinate system where $+X$ is East and $+Y$ is North).
- **Inner (Hole) Rings** must be wound **counter-clockwise**.

When third-party converters or hand-digitized scripts produce polygons with reversed ring orientations, GIS engines (such as ArcGIS, QGIS, or CARIS) may misinterpret outer boundaries as negative-area holes or fail during spatial intersection operations. `shprewind` reads every shape from `<in_shp_file>`, invokes `SHPRewindObject()` to test and reverse any improperly wound rings, and writes the corrected geometries to `<out_shp_file>`.

---

## Usage

```bash
shprewind <in_shp_file> <out_shp_file>
```

> [!NOTE]
> `shprewind` only copies and rewinds the `.shp` and `.shx` geometry files. If `<in_shp_file>` has an associated `.dbf` attribute table (and `.prj` projection file), copy `<in_basename>.dbf` to `<out_basename>.dbf` alongside running `shprewind` so the output shapefile retains its attributes.

### Positional Arguments & Exit Codes

| Argument / Exit Code | Description |
| :--- | :--- |
| `<in_shp_file>` | **Required.** Source shapefile path/basename (opened read-only via `SHPOpen(argv[1], "rb")`). |
| `<out_shp_file>` | **Required.** Destination shapefile path/basename (created via `SHPCreate(argv[2], nShapeType)`). |
| Exit `0` | Completed successfully and printed `<nInvalidCount> objects rewound.`. |
| Exit `1` | Missing arguments (`argc != 3`), or `SHPOpen` / `SHPCreate` failed. |

---

## Internal Ring-Winding Algorithm (`SHPRewindObject` in `shpopen.c`)

For each entity `i` in `0 .. nEntities - 1`:
1. `shprewind` reads the feature via `psShape = SHPReadObject(hSHP, i)`.
2. Calls `SHPRewindObject(hSHP, psShape)` (`code/shapelib-1.3.0a2/shpopen.c`, lines 2036–2205):
   - If `psShape->nSHPType` is not `SHPT_POLYGON`, `SHPT_POLYGONZ`, or `SHPT_POLYGONM` (or has `nVertices == 0` or `nParts == 0`), returns `0` immediately.
   - **Step A (Inner vs. Outer Ring Classification)**: For each ring `iOpRing` (`0 .. nParts - 1`), picks a test point strictly on an edge segment of `iOpRing` and runs a ray-casting point-in-ring test against all other rings `iCheckRing` in the same `SHPObject`. If the point is enclosed by an odd number of other rings, `iOpRing` is classified as an **Inner Ring** (`bInner = TRUE`); otherwise it is an **Outer Ring** (`bInner = FALSE`).
   - **Step B (Signed Area & Winding Check)**: Computes the shoelace signed sum $\sum (X_i Y_{i+1} - X_{i+1} Y_i)$ around `iOpRing`.
   - **Step C (In-Place Reversal)**: If an Outer Ring is counter-clockwise (`dfSum > 0`) or an Inner Ring is clockwise (`dfSum < 0`), reverses the ring's `padfX`, `padfY`, `padfZ`, and `padfM` arrays in-place and increments `nAltered`.
3. Writes the corrected object to `hSHPOut` via `SHPWriteObject(hSHPOut, -1, psShape)` and frees `psShape`.
4. Closes both handles and prints `<nInvalidCount> objects rewound.`.
