---
layout: default
title: j_farray
parent: Core Shared Libraries (subr)
module_name: j_farray
source_path: code/subr/j_farray.c
header_path: code/subr/j_farray.h
category: Data Structures & Numerical Containers
related_tools:
  - jb_watercolumn
  - soundscape
  - weigh_grid
---

# `j_farray` — 2D Floating-Point Grid Container & Bilinear Interpolation Library

## Overview & Purpose in the OMG Architecture

`j_farray` (`code/subr/j_farray.c`, `code/subr/j_farray.h`), written by John E. Hughes Clarke in August 1998, provides a lightweight, self-contained C data structure (`farray`) and accessor API for allocating, indexing, and bilinearly interpolating 2D floating-point grids in memory.

Throughout the OMG water-column raytracing (`j_watercolumn`, `jb_watercolumn`), acoustic modeling, and gridding subsystems, algorithms frequently need temporary 2D lookup tables parameterized by real-world physical coordinates (such as depth vs. depression angle, or range vs. two-way travel time) without the full disk-header overhead of a 1024-byte `JHC_header`. `j_farray` encapsulates the grid dimensions, physical origin (`xmin`, `ymin`), step sizes (`xstep`, `ystep`), and heap buffer pointer into a single struct with bounds-checked integer and continuous real-coordinate accessors.

---

## Key Data Structures (`code/subr/j_farray.h`)

### `farray`
```c
typedef struct {
    int x, y;           /* Number of columns (x) and rows (y) */
    int alloced;        /* 1 if data buffer is allocated, 0 otherwise */
    float xmin, ymin;   /* Physical coordinate origin at index (0, 0) */
    float xstep, ystep; /* Physical step size per grid cell in X and Y */
    float *data;        /* Pointer to row-major float array (x * y elements) */
} farray;
```

---

## Public Functions & Signatures

### Lifecycle Management
- `int jFA_init(farray *fa, int x, int y, float xmin, float ymin, float xstep, float ystep)`
  Initializes the `farray` metadata fields (`x`, `y`, `xmin`, `ymin`, `xstep`, `ystep`) and allocates `x * y * sizeof(float)` bytes on the heap. Sets `fa->alloced = 1` and returns `1` on success, or sets `fa->alloced = 0` and returns `0` if `malloc` fails.
- `void jFA_free(farray *fa)`
  Frees `fa->data` and resets `fa->alloced = 0`.

### Coordinate Conversion
- `int jFA_ixy_to_rxy(farray *fa, int ix, int iy, float *rx, float *ry)`
  Converts discrete integer grid indices `(ix, iy)` into continuous physical coordinates:
  $$\text{rx} = \text{xmin} + \text{ix} \cdot \text{xstep}, \quad \text{ry} = \text{ymin} + \text{iy} \cdot \text{ystep}$$
  Returns `1` if `(ix, iy)` lies within `[0..x-1, 0..y-1]`, or `0` if out of bounds.
- `int jFA_rxy_to_ixy(farray *fa, int *ix, int *iy, float rx, float ry)`
  Converts continuous physical coordinates `(rx, ry)` into truncated integer cell indices `(*ix, *iy)` and returns `1` if within the array bounds, or `0` if outside.

### Cell Access & Interpolation
- `float jFA_get_ivalue(farray *fa, int x, int y)`
  Returns the floating-point value stored at integer grid cell `(x, y)` (`*(fa->data + y * fa->x + x)`). Returns `-1.0` if `fa` is unallocated, or `0.0` if `(x, y)` is outside the valid grid dimensions.
- `int jFA_set_ivalue(farray *fa, int x, int y, float value)`
  Writes `value` into grid cell `(x, y)`. Returns `1` on success, `-1` if unallocated, or `0` if out of bounds.
- `float jFA_get_rvalue(farray *fa, float rx, float ry)`
  Retrieves an interpolated value at continuous physical coordinates `(rx, ry)`:
  1. Locates the top-left cell index `(xoffset, yoffset)` via `jFA_rxy_to_ixy()`.
  2. Fetches the four surrounding cell values (`tl`, `tr`, `bl`, `br`) via `jFA_get_ivalue()`.
  3. If all four corner values are non-zero, performs 2D bilinear interpolation; otherwise returns `0.0`.

---

## How It Fits Into the OMG Architecture

`j_farray` is included directly by `j_watercolumn.h` and `jb_watercolumn.c`, making it available to every tool in the OMG suite that performs sound velocity profile (SVP) processing, raytracing, or water-column uncertainty analysis.
