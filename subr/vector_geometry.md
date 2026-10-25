---
layout: default
title: vector_geometry
parent: Shared Core Libraries (subr)
module_name: vector_geometry
source_path: code/subr/vector_geometry.c
header_path: code/subr/vector_geometry.h
category: Matrix, Vector & Orientation Math
related_tools: ["DCM_rthand", "orientation", "grazing_angle", "sonar_geometry", "jGL_draw"]
---

# vector_geometry

## Overview
`vector_geometry` (`vector_geometry.c` / `vector_geometry.h`) provides fundamental 3D Cartesian vector algebra operations—addition, subtraction, Euclidean norm, unit normalization, dot product, and right-handed cross product—operating on the single-precision `fvect` (`struct { float x, y, z; }`) type defined in [`DCM_rthand.h`](DCM_rthand.md).

It is used throughout the Ocean Mapping Group's 3D acoustic geometry, seafloor normal estimation, grazing-angle calculation, and OpenGL visualization modules.

---

## Data Type Dependency

From [`DCM_rthand.h`](DCM_rthand.md):
```c
typedef struct {
    float x;
    float y;
    float z;
} fvect;
```

---

## Public Functions

All functions return `0` on completion and write their output through a pointer argument:

| Function | Signature | Mathematical Operation | Description |
|---|---|---|---|
| `add_vector` | `int add_vector(fvect vector_a, fvect vector_b, fvect *result)` | $\mathbf{r} = \mathbf{a} + \mathbf{b}$ | Computes component-wise sum: `result->x = a.x + b.x`, `result->y = a.y + b.y`, `result->z = a.z + b.z`. |
| `subtract_vector` | `int subtract_vector(fvect vector_a, fvect vector_b, fvect *result)` | $\mathbf{r} = \mathbf{a} - \mathbf{b}$ | Computes component-wise difference: `result->x = a.x - b.x`, `result->y = a.y - b.y`, `result->z = a.z - b.z`. |
| `length_vector` | `int length_vector(fvect vector, float *length)` | $\|\mathbf{v}\| = \sqrt{v_x^2 + v_y^2 + v_z^2}$ | Computes the Euclidean magnitude of `vector` and stores it in `*length`. |
| `normalize_vector` | `int normalize_vector(fvect *vector)` | $\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\|}$ | Normalizes `vector` in-place to unit length if $\|\mathbf{v}\| > 0$; safely leaves the zero vector `(0, 0, 0)` unchanged. |
| `cross_product` | `int cross_product(fvect vector_a, fvect vector_b, fvect *result)` | $\mathbf{r} = \mathbf{a} \times \mathbf{b}$ | Computes the 3D cross product:<br>$r_x = a_y b_z - a_z b_y$<br>$r_y = -(a_x b_z - a_z b_x) = a_z b_x - a_x b_z$<br>$r_z = a_x b_y - a_y b_x$. |
| `dot_product` | `int dot_product(fvect vector_a, fvect vector_b, float *result)` | $r = \mathbf{a} \cdot \mathbf{b}$ | Computes the scalar dot product $a_x b_x + a_y b_y + a_z b_z$ and stores it in `*result`. |

---

## Architectural Role
While [`orientation`](orientation.md) provides 3D Euler rotations (`rotate` / `unrotate`) on `vector_3D` and [`DCM_rthand`](DCM_rthand.md) defines direction cosine matrices (`fmatx`) and `fvect`, `vector_geometry` supplies the vector arithmetic used by [`grazing_angle`](grazing_angle.md) (computing 3D ray vectors and local DEM surface normal vectors to determine true seabed incidence angles) and 3D swath rendering routines.
