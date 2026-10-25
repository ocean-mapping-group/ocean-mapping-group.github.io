---
layout: default
title: showModelMesh
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: showModelMesh
source_path: code/grid/showModelMesh.c
category: gridding
input_formats:
- JHC_header (.lat.r4, .lon.r4, .mask.r4)
output_formats:
- ASCII Mesh Line Segments (.mesh.llz)
related_tools:
- makemesh
- readQUODDY
- extractNodeProf
---

# showModelMesh

## Overview

`showModelMesh` reads three co-registered floating-point `.r4` model grids (`<prefix>.lat.r4`, `<prefix>.lon.r4`, and `<prefix>.mask.r4`) representing a curvilinear hydrodynamic or oceanographic model grid, and exports an ASCII wireframe line file (`<prefix>.mesh.llz`) connecting adjacent active (non-zero mask) nodes along grid rows and columns.

---

## Syntax & CLI Options

```
showModelMesh [-v] -prefix <modelprefix>
```

| Flag | Description |
|------|-------------|
| `-v` | Verbose output. |
| `-prefix <modelprefix>` | Prefix of the three input `.r4` files (`<modelprefix>.lat.r4`, `<modelprefix>.lon.r4`, and `<modelprefix>.mask.r4`). Writes `<modelprefix>.mesh.llz`. |

---

## How It Works

1. **Grid Ingestion & Validation**:
   - Opens `<prefix>.lat.r4`, `<prefix>.lon.r4`, and `<prefix>.mask.r4`, verifies that all three are 32-bit floating-point grids (`data_type == 3`) with identical `dx` and `dy` dimensions, and reads their float arrays (`jswapfloat_fread`).
2. **Wireframe Segment Generation**:
   - Iterates through every cell `(i, j)` for `i = 0..yno-2` and `j = 0..xno-2`.
   - Retrieves `(lat, lon, mask)` at `(i, j)`, its eastern neighbor `(lat1, lon1, mask1)` at `(i, j+1)`, and its southern neighbor `(lat2, lon2, mask2)` at `(i+1, j)`.
   - If both `mask` and `mask1` are non-zero, writes a 2-point horizontal segment followed by a `0.0 0.0 0.0` pen-up terminator:

     ```
      <lat> <lon> <mask>
      <lat1> <lon1> <mask1>
      0.0 0.0 0.0
     ```
   - If both `mask` and `mask2` are non-zero, writes the vertical segment connecting `(i, j)` to `(i+1, j)` followed by `0.0 0.0 0.0`.

---

## Examples

### Export a wireframe mesh from curvilinear model coordinate grids

```bash
showModelMesh -prefix gom_pom
```

---

## Workflow Context

- **Related Model Tools**: [`extractNodeProf`](extractNodeProf.html), [`convert3D_TSZ_to_SV`](convert3D_TSZ_to_SV.html), [`readQUODDY`](readQUODDY.html), [`makemesh`](makemesh.html).
