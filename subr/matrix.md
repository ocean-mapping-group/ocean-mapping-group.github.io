---
layout: default
title: matrix
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/matrix.c
category: 3D Vector, Matrix & Perspective Graphics Math
related_tools:
- 3D visualization utilities
- jview
- gl / 3D mesh viewers
module_name: matrix
header_path: code/subr/matrix.h
---

# `matrix` — 3D Vector, 3×3 Matrix Algebra & Perspective Projection Library

## Overview & Purpose in the OMG Architecture

`matrix` (`code/subr/matrix.c`, `code/subr/matrix.h`), written by Guy Carpenter on July 20, 1989, is a clean, pass-by-value 3D vector (`mat_vector`) and 3×3 matrix (`mat_matrix`) algebra library designed to support 3D graphics transformations and perspective viewing projections in the OMG visualization tools.

To maximize code readability and avoid pointer-aliasing bugs in 3D rendering loops, all functions in `matrix` accept and return `mat_vector` and `mat_matrix` structures by value, with all 3×3 matrix loops completely unrolled. In addition to standard vector/matrix operations (dot product, cross product, normalization, determinant, inverse, transpose, multiplication), `matrix` provides `mat_persp_proj()`, which constructs an orthonormal camera basis from a 3D `eye` and `focus` position for perspective rendering of bathymetric surfaces.

---

## Key Data Structures (`code/subr/matrix.h`)

### `mat_vector`
Represents a 3D Cartesian point or direction vector in double precision:

```c
typedef struct {
    double x;
    double y;
    double z;
} mat_vector;
```

### `mat_matrix`
Represents a 3×3 matrix composed of three 3D vector rows/columns (`a`, `b`, `c`):

```c
typedef struct {
    mat_vector a;
    mat_vector b;
    mat_vector c;
} mat_matrix;
```

---

## Public Functions & Signatures

### 3D Vector Operations
- `mat_vector mat_make_vector(double x, double y, double z)`
  Constructs and returns a `mat_vector` initialized to `(x, y, z)`.
- `double mat_vector_length(mat_vector v)`
  Computes the Euclidean norm $\sqrt{v_x^2 + v_y^2 + v_z^2}$.
- `mat_vector mat_normalize(mat_vector v)`
  Divides `v` by `mat_vector_length(v)` to return a unit vector of length `1.0`.
- `mat_vector mat_vector_add(mat_vector v1, mat_vector v2)`
  Returns the component-wise vector sum $\mathbf{v}_1 + \mathbf{v}_2$.
- `mat_vector mat_vector_sub(mat_vector v1, mat_vector v2)`
  Returns the component-wise vector difference $\mathbf{v}_1 - \mathbf{v}_2$.
- `double mat_dot_product(mat_vector v1, mat_vector v2)`
  Returns the scalar dot product $v_{1x}v_{2x} + v_{1y}v_{2y} + v_{1z}v_{2z}$.
- `mat_vector mat_cross_product(mat_vector v1, mat_vector v2)`
  Returns the 3D vector cross product $\mathbf{v}_1 \times \mathbf{v}_2$.

### 3×3 Matrix Operations
- `mat_matrix mat_make_matrix(mat_vector a, mat_vector b, mat_vector c)`
  Constructs and returns a `mat_matrix` from three `mat_vector` components.
- `double mat_determinate(mat_matrix m)`
  Computes the scalar determinant of the 3×3 matrix `m` using Sarrus' rule (unrolled cofactor expansion).
- `mat_matrix mat_transpose(mat_matrix m)`
  Returns the 3×3 transpose $M^T$ by swapping off-diagonal elements.
- `mat_matrix mat_invert(mat_matrix m)`
  Computes the 3×3 matrix inverse $M^{-1}$ by dividing the cofactor matrix by `mat_determinate(m)` and transposing via `mat_transpose()`.
- `mat_matrix mat_multiply(mat_matrix m, mat_matrix n)`
  Computes the 3×3 matrix product $P = M \cdot N$ with fully unrolled inner products.

### 3D Camera Perspective Projection
- `mat_matrix mat_persp_proj(mat_vector eye, mat_vector focus)`
  Constructs an orthonormal camera viewing transformation matrix given a 3D camera position (`eye`) and look-at target (`focus`):
  1. Forms the viewing axis `basis.b = mat_vector_sub(eye, focus)`.
  2. Constructs a horizontal right-hand vector `basis.a = (b.y, -b.x, 0)` (or `(1, 0, 0)` if viewing straight down/up) so the horizon remains level.
  3. Computes the orthogonal up vector `basis.c = mat_cross_product(basis.b, basis.a)`.
  4. Normalizes all three basis vectors and returns `mat_transpose(mat_invert(basis))`.

---

## How It Fits Into the OMG Architecture

`matrix` provides 3D viewing geometry for OMG's wireframe, shaded-relief, and 3D perspective visualization tools (`code/gl/`, `code/JV/`), complementing the general-purpose dynamic `N × M` matrix solver in `dmatrix.c`.
