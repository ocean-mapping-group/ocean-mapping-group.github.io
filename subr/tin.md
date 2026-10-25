---
layout: default
title: tin
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/tin.c
category: Gridding, Interpolation & Contouring
related_tools:
- array
- contour
- weigh_grid
module_name: tin
header_path: code/subr/tin.h
---

# tin

## Overview
`tin` (`tin.c` / `tin.h`), written by Steve Brucker (November 2004), is an experimental helper module for **Triangulated Irregular Network (TIN)** / Delaunay triangulation point ingestion within the bounding box of an OMG `JHC_header` mapsheet.

It defines the `tin_point` vertex structure (storing geographic coordinates, depth, and up to 25 adjacent Delaunay neighbor indices) and provides `get_tin_points()` to scan ASCII degrees-minutes-seconds (`DMS`) sounding files and count points falling within a mapsheet's geographic bounds (expanded by a 10% overlap factor `olf = 1.1`).

---

## Data Structures

### `tin_point`
Defined in `tin.h` to represent a single node in a 2D Delaunay triangulation mesh:

```c
typedef struct {
    double lat;             /* Latitude in decimal degrees */
    double lon;             /* Longitude in decimal degrees */
    float  depth;           /* Sounding depth (m) */
    short  neighbours[25];  /* Indices of up to 25 adjacent TIN vertices */
} tin_point;
```

---

## Public Functions

| Function | Signature | Description |
|---|---|---|
| `get_tin_points` | `void get_tin_points(char filename[], JHC_header header)` | Opens an ASCII sounding file `filename`, reads DMS coordinates (`deglat`, `min_lat`, `dec_sec_lat`, `deglon`, `min_lon`, `dec_sec_lon`, `depth`), converts them to decimal degrees (`clat`, `clon` assuming western hemisphere negative longitude), tests whether each point lies within `[header.xmin * 1.1, header.xmax * 1.1]` and `[header.ymin * 1.1, header.ymax * 1.1]`, and prints the total `Tin count`. |

---

## Implementation Notes
- `tin.c` is a prototype/experimental module (`infile` and `extra_field` in `tin.c` reference caller-scope variables, and `tin.h` omits the semicolon on `void get_tin_points()`).
- For production bathymetric gridding and surface interpolation in the OMG suite, see [`weigh_grid`](../grid/weigh_grid.html), [`array`](array.html), [`j_farray`](j_farray.html), and [`contour`](contour.html).
