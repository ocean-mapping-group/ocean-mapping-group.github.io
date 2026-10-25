---
layout: default
title: dmatrix
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/dmatrix.c
category: Linear Algebra, Least Squares & Trend Surface Analysis
related_tools:
- fft2dimage
- extractVertSection
- readQUODDY
module_name: dmatrix
header_path: code/subr/dmatrix.h
---

# dmatrix: Double-Precision Linear Algebra, Least-Squares & Polynomial Surface Detrending

## Overview & Purpose
`dmatrix` (`dmatrix.c` / `dmatrix.h`, 756 lines) is a linear algebra, 3D vector calculus, ordinary least-squares (OLS), and 2D trend-surface analysis library written by Danar G. Pratomo at the UNB Ocean Mapping Group in February 2012 (with 3D vector product extensions added in April 2014). It provides dynamic double-precision matrix operations, recursive cofactor/minor determinant and matrix inversion solvers, linear and quadratic polynomial trend surface removal for Digital Terrain Models (DTMs) prior to 2D Fast Fourier Transform (FFT) spectral analysis (`dspectra`), and 3D vector dot/cross/triple products.

---

## Key Macros & Data Structures

### Element Access Macros

```c
#define _cell(Elements,Row,Col)    (((Row) * Elements->col) + (Col))
#define _get(Elements,Row,Col)     ((double *)Elements->elements)[_cell(Elements,Row,Col)]
#define _set(Elements,Row,Col,Val) ((double *)Elements->elements)[_cell(Elements,Row,Col)] = Val
#define SQUARES(M)                 (M->row == M->col)
```

### `Matrix` & `Vector` Structures

```c
typedef struct {
    int   row;       /* Number of matrix rows */
    int   col;       /* Number of matrix columns */
    void *elements;  /* Pointer to row-major double array (row * col * sizeof(double)) */
} Matrix;

typedef struct {
    float x, y, z;   /* 3D Cartesian vector components */
} Vector;
```

---

## Public Functions & Signatures

### Matrix Allocation & Basic Arithmetic
* `Matrix *InitMatrix(int row, int col)`
  Allocates a `Matrix` structure and a zero-initialized `row * col` array of `double` elements.
* `Matrix *CastMatrix(double *array, int row, int col)`
  Allocates a `row` $\times$ `col` `Matrix` and copies the contents of a flat double array `array` into `self->elements`.
* `Matrix *AddMatrix(Matrix *left, Matrix *right)`
  Computes element-wise matrix addition $C = A + B$ after verifying matching dimensions.
* `Matrix *SubstractMatrix(Matrix *left, Matrix *right)`
  Computes element-wise matrix subtraction $C = A - B$.
* `Matrix *MultiplyMatrix(Matrix *left, Matrix *right)`
  Computes standard matrix multiplication $C_{m \times k} = A_{m \times n} B_{n \times k}$ when `left->col == right->row`.

### Matrix Inversion, Determinants & Least Squares
* `Matrix *TransposeMatrix(Matrix *self)`
  Returns the transpose $A^T$ (`col` $\times$ `row`).
* `Matrix *Minor(Matrix *self, int i, int j)`
  Constructs the $(n-1) \times (n-1)$ submatrix formed by removing row `i` and column `j`.
* `double Determinant(Matrix *self)`
  Computes $\det(A)$ for a square matrix (`SQUARES(self)`): uses $ad - bc$ directly for $2 \times 2$ matrices and recursive Laplace cofactor expansion along row 0 for $n \ge 3$.
* `Matrix *InverseMatrix(Matrix *self)`
  Computes $A^{-1}$ for $1 \times 1$, $2 \times 2$, and $n \times n$ ($n \ge 3$) matrices using the adjugate (cofactor transpose) divided by `Determinant(self)`.
* `Matrix *LeastSquare(Matrix *A, Matrix *L)`
  Solves the overdetermined linear system $Ax = L$ via the normal equations:
  $$x = (A^T A)^{-1} A^T L$$

### 2D Trend Surface Analysis (Unwin, 1978)
* `int dTrend(int row, int col, double *az, double *Res, double *Zt)`
  Fits a first-order planar trend surface $Z_t(x, y) = b_0 + b_1 x + b_2 y$ to a `row` $\times$ `col` grid `az` by constructing the $3 \times 3$ normal design matrix $A$ and $3 \times 1$ observation vector $L$, solving for $(b_0, b_1, b_2)^T$ with `LeastSquare(A, L)`, and writing the planar trend to `Zt` and the zero-mean detrended residual $Z - Z_t$ to `Res`.
* `int dTrendPoly(int row, int col, double *az, double *Res, double *Zt)`
  Fits a 6-parameter quadratic polynomial trend surface (dome/trough model):
  $$Z_t(x, y) = b_0 + b_1 x + b_2 y + b_3 x^2 + b_4 x y + b_5 y^2$$
  using a $6 \times 6$ normal matrix solved via `LeastSquare(A, L)`, writing the trend surface to `Zt` and residuals to `Res`.

### Matrix Diagnostics & 3D Vector Calculus
* `double MaxMatrix(Matrix *self)` / `double MinMatrix(Matrix *self)`
* `void PrintMatrix(Matrix *self, char *type)` / `void Message(char *msg)`
* `float dotProduct(Vector a, Vector b)`: Returns $\mathbf{a} \cdot \mathbf{b}$.
* `Vector crossProduct(Vector a, Vector b)`: Returns $\mathbf{a} \times \mathbf{b}$.
* `float scalarTripleProduct(Vector a, Vector b, Vector c)`: Returns $\mathbf{a} \cdot (\mathbf{b} \times \mathbf{c})$.
* `Vector vectorTripleProduct(Vector a, Vector b, Vector c)`: Returns $\mathbf{a} \times (\mathbf{b} \times \mathbf{c})$.
* `Vector subtractVector(Vector a, Vector b)`: Returns $\mathbf{a} - \mathbf{b}$.

---

## How It Fits Into the OMG Architecture
`dmatrix` underpins the 2D spectral bedform analysis module `dspectra` (`code/subr/dspectra.c`) and `fft2dimage` (`code/image/fft2dimage.c`), which call `dTrend` and `dTrendPoly` to remove regional seafloor slope before computing 2D FFTs, as well as finite-element mesh/section extraction tools (`code/grid/extractVertSection.c` and `code/grid/readQUODDY.c`).
