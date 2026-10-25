---
layout: default
title: fillquad2
parent: Mosaicking Tools
nav_order: 3
module_name: fillquad2
source_path: code/newmos/fillquad2.c
category: Backscatter & Sidescan Mosaicking
related_tools: ["mos2", "cache", "support"]
---

# fillquad2

## Overview
`fillquad2` (`code/newmos/fillquad2.c`, originally written as `quadfill.c` by Guy Carpenter, February 26, 1990) is the high-speed **integer Bresenham quadrilateral scan-conversion and linear intensity interpolation engine** linked directly into [`mos2`](mos2.md) (`mos2: mos2.o fillquad2.o` in `code/newmos/makefile`).

When `mos2` projects two consecutive sidescan or multibeam backscatter pings onto the output mapsheet (unless `-just_drop` is specified), each adjacent pair of across-track samples between Ping $k-1$ and Ping $k$ forms a 4-vertex quadrilateral in pixel coordinates:
- Vertex 0: `(x0, y0)` with backscatter intensity `c0`
- Vertex 1: `(x1, y1)` with backscatter intensity `c1`
- Vertex 2: `(x2, y2)` with backscatter intensity `c2`
- Vertex 3: `(x3, y3)` with backscatter intensity `c3`

Because a single survey line can require filling millions of sub-swath quadrilaterals, `fill_quad2()` avoids all floating-point arithmetic (`float`/`double`), performing perimeter rasterization and horizontal scanline intensity (`z` / `c`) interpolation purely with integer addition, subtraction, and bit-shifts (`<< 1`).

---

## Algorithm & Internal State

`fillquad2.c` maintains a dynamically grown scanline edge table across calls:
- `int qf_base, qf_top` — Minimum `y` coordinate (`qf_base`) and number of horizontal scanlines (`qf_top = y_max - y_min + 1`) spanned by the current quadrilateral.
- `char *qf_count` — Array of `qf_size` bytes tracking how many perimeter points (`0`, `1`, or `>= 2`) have been recorded on each horizontal scanline `y - qf_base`.
- `int *qf_xzxz` — Array of `4 * qf_size` integers storing the left and right span endpoints `[x_left, z_left, x_right, z_right]` for each scanline `y`.

### Step-by-Step Execution
1. **Scanline Table Initialization (`qf_init(y_min, y_max)`)**:
   Computes the vertical bounding span `[y_min, y_max]`, grows `qf_count` and `qf_xzxz` via `malloc`/`realloc` (with `QF_GROW = 10` padding) if `qf_top > qf_size`, and zeroes `qf_count` via `memset`.
2. **Perimeter Bresenham Rasterization (`qf_perimeter` & `qf_point`)**:
   Traces the four edges of the quadrilateral in order `0 -> 1 -> 3 -> 2 -> 0`. Along each edge from `(x0, y0, z0)` to `(x1, y1, z1)`, `qf_perimeter()` steps `y` by `sy = ±1` and simultaneously interpolates both horizontal pixel coordinate `x` and backscatter DN value `z` over `dy = abs(y1 - y0)` using dual integer Bresenham error accumulators (`ddx`, `ddz`). Each perimeter point `(x, y, z)` is inserted into `qf_xzxz[4 * (y - qf_base)]` via `qf_point()`, which maintains `rec[0] <= rec[2]` (`x_left <= x_right`) and discards interior points if more than two perimeter hits occur on the same scanline.
3. **Horizontal Scanline Fill & Weight Autoseaming (`qf_unload(weight)`)**:
   Iterates over each scanline `y` from `qf_base` to `qf_base + qf_top - 1`. For every scanline with two span endpoints (`rec[0] != rec[2]`), `qf_unload()` runs a 1D integer Bresenham interpolation of the backscatter intensity `z` from `z0 = rec[1]` to `z1 = rec[3]` across `x = rec[0] .. rec[2]`, invoking `fill_point(x, y, z, weight)` (defined in `mos2.c`) at every pixel to perform the `.ran` autoseam comparison and write to the `.mos` and `.ran` caches.

---

## Public & Internal Functions

| Function | Signature | Description |
|---|---|---|
| `fill_quad2` | `void fill_quad2(int x0, int y0, int c0, int x1, int y1, int c1, int x2, int y2, int c2, int x3, int y3, int c3, unsigned char weight)` | **Main Entry Point (called by `mos2`)**: Rasterizes and Gouraud-interpolates the quadrilateral `0 -> 1 -> 3 -> 2 -> 0` with priority `weight`, calling `fill_point(x, y, c, weight)` for every interior and boundary pixel. |
| `qf_init` | `void qf_init(int y0, int y1)` | Resizes and clears the scanline edge buffers (`qf_count`, `qf_xzxz`) for vertical range `[y0, y1]`. |
| `qf_perimeter` | `void qf_perimeter(int x0, int y0, int z0, int x1, int y1, int z1)` | Rasterizes one directed edge from `(x0, y0, z0)` to `(x1, y1, z1)` along `y` using integer Bresenham arithmetic. |
| `qf_point` | `void qf_point(int x, int y, int z)` | Inserts a perimeter sample `(x, z)` into scanline `y`'s `[x_left, z_left, x_right, z_right]` slot, keeping `x` sorted ascending. |
| `qf_unload` | `void qf_unload(unsigned char weight)` | Scans across `x` from `x_left` to `x_right` on each scanline `y`, interpolating color `z` and invoking `fill_point(x, y, z, weight)`. |

---

## Architectural Role
`fillquad2.c` is the inner-loop rasterization workhorse of [`mos2`](mos2.md). By interpolating across-track and along-track pixels as continuous quadrilaterals between pings (whenever ping spacing is within `-maxdist`, `-maxtime`, and `-maxazi`), it eliminates inter-ping gaps on the outer swath while maintaining high throughput.
