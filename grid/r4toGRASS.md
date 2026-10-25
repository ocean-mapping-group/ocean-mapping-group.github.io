---
layout: default
title: r4toGRASS
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: r4toGRASS
source_path: code/grid/r4toGRASS.c
category: gridding
input_formats:
- JHC_header (.r4)
output_formats:
- GRASS GIS Header (.grass_head)
- GRASS GIS Raster Data (.grass_data)
related_tools:
- r4toESRI
- r4toASCII
- r4to16bit
---

# r4toGRASS

## Overview

`r4toGRASS` exports an OMG 32-bit floating-point grid (`<r4prefix>.r4`) into a GRASS GIS raster header (`<r4prefix>.grass_head`) and uncompressed binary cell array (`<r4prefix>.grass_data`) in UTM coordinates.

---

## Syntax & CLI Options

```
r4toGRASS [-v] -merid <central_merid> <r4prefix>
```

| Flag / Argument | Description |
|-----------------|-------------|
| `-v` | Verbose output. |
| `-merid <central_merid>` | Central meridian (in decimal degrees) defining the target UTM zone. |
| `<r4prefix>` | Input `.r4` filename prefix (reads `<r4prefix>.r4`). |

---

## How It Works

1. **Header & UTM Coordinate Calculation**:
   - Opens `<r4prefix>.r4` and reads its 1024-byte `JHC_header` along with the floating-point data array (`fbuf`).
   - Computes the UTM zone number from `central_merid` via `zone = 30 - (int)((-central_merid) / 6.0)`.
   - If the grid is already in UTM (`head.projection == 2`), converts the kilometer header bounds (`xmin`, `xmax`, `ymin`, `ymax`, `xstep`, `ystep`) directly to meters (`* 1000.0`).
   - Otherwise, projects the geographic bounds (`xmin`, `ymin`) and (`xmax`, `ymax`) to UTM meters using `geoutm` with the specified `central_merid`.
2. **GRASS Header & Data Export**:
   - Writes `<r4prefix>.grass_head` containing:

     ```
     proj:       1
     zone:       <zone>
     north:      <ymax_m>
     south:      <ymin_m>
     east:       <xmax_m>
     west:       <xmin_m>
     cols:       <dx>
     rows:       <dy>
     e-w resol:  <xstep_m>
     n-s resol:  <ystep_m>
     format:     3
     compressed: 0
     ```
   - Writes the raw array buffer (`dx * dy * 4` bytes) to `<r4prefix>.grass_data`.

---

## Examples

### Convert a UTM `.r4` grid (Zone 19, central meridian -69°) to GRASS GIS format

```bash
r4toGRASS -v -merid -69.0 bay_bathy
```

---

## Workflow Context

- **Upstream**: [`weigh_grid`](weigh_grid.html), [`combine`](weigh_grid.html).
- **Related Export Tools**: [`r4toESRI`](r4toESRI.html), [`r4toASCII`](r4toASCII.html).
