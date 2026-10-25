---
layout: default
title: orientation
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/orientation.c
category: Navigation, Attitude & Geodesy
related_tools:
- newMergeAtt
- swathed (SE)
- applyBDI
- jview (JV)
- xse2omg
- targethunt
module_name: orientation
header_path: code/subr/orientation.h
---

# orientation

## Overview & Purpose

`orientation` provides the fundamental 3D Euler angle, vector rotation, $3 \times 3$ rotation matrix, and $4 \times 4$ matrix inversion mathematics used throughout the Ocean Mapping Group (OMG) codebase for vessel attitude compensation, lever-arm transformation, multibeam cone-cone intersection, and patch test calibration.

## Key Data Structures, Constants & Macros

### Core Structs
- `orientation`: Represents 3D Euler attitude angles and optional 3D translational offsets:
  - `float roll`: Roll angle in degrees.
  - `float pitch`: Pitch angle in degrees.
  - `float heave`: Heave in meters.
  - `float heading`: Heading/yaw angle in degrees.
  - `double x`, `double y`, `double z`: 3D Cartesian coordinates or lever-arm translations (meters).
- `vector_3D`: 3D double-precision Cartesian vector (`double x`, `double y`, `double z`).
- `rotation_matrix`: $3 \times 3$ row-major rotation matrix with elements:
  $$\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}$$
- `matrix_4x4`: $4 \times 4$ double-precision matrix with elements `a1..a4`, `b1..b4`, `c1..c4`, `d1..d4` arranged as:
  $$\begin{bmatrix} a_1 & b_1 & c_1 & d_1 \\ a_2 & b_2 & c_2 & d_2 \\ a_3 & b_3 & c_3 & d_3 \\ a_4 & b_4 & c_4 & d_4 \end{bmatrix}$$
  Added (Jan 2013) to support 3D cone-cone intersection and quadric matrix inversion in `sonar_geometry.c` (`intersect_cones_travis`).

## Public Functions & Signatures

### Direct Vector Rotations
- `void unrotate(vector_3D orig, orientation rotate, vector_3D *final)`
  - Transforms a 3D vector `orig` from the rotated body/sensor frame into the local level/geographic reference frame using the compound Euler rotation matrix $R = R_z(\text{heading}) R_y(\text{pitch}) R_x(\text{roll})$:
    - `final->x = cosp*cosy*x + (sinr*sinp*cosy - cosr*siny)*y + (cosr*sinp*cosy + sinr*siny)*z`
    - `final->y = cosp*siny*x + (sinr*sinp*siny + cosr*cosy)*y + (cosr*sinp*siny - sinr*cosy)*z`
    - `final->z = -sinp*x + sinr*cosp*y + cosr*cosp*z`
- `void rotate(vector_3D orig, orientation rotate, vector_3D *final)`
  - Applies the inverse (transpose) rotation $R^T$ to transform a vector `orig` from the local level/geographic frame back into the rotated body/sensor frame.

### $3 \times 3$ Rotation Matrix Operations
- `void matrix_identity(rotation_matrix *matrix)`
  - Sets `matrix` to the $3 \times 3$ identity matrix ($a = e = i = 1.0$, all other elements $0.0$).
- `void matrix_build(rotation_matrix *matrix, orientation *rotate)`
  - Populates `matrix` with the $3 \times 3$ direction cosine matrix corresponding to `rotate->roll`, `rotate->pitch`, and `rotate->heading`.
- `vector_3D matrix_rotate(rotation_matrix *matrix, vector_3D *vector)`
  - Multiplies the $3 \times 3$ `matrix` by `vector` and returns the rotated `vector_3D`.
- `rotation_matrix matrix_multiply(rotation_matrix *lmatrix, rotation_matrix *rmatrix)`
  - Computes the $3 \times 3$ matrix product $K = L \cdot R$.
- `rotation_matrix matrix_transpose(rotation_matrix *m)`
  - Returns the transpose $M^T$ of the $3 \times 3$ matrix `m` (equivalent to the inverse for orthogonal rotation matrices).
- `orientation matrix_solve_angles(rotation_matrix *m)`
  - Extracts Euler angles (`roll`, `pitch`, `heading` in degrees) from a $3 \times 3$ rotation matrix using `roll = atan(h/i)`, `pitch = acos(i / cos(roll))`, and `heading = acos(a / cos(pitch))`.

### $4 \times 4$ Matrix Inversion & Determinants
- `int invert_4x4(matrix_4x4 in, matrix_4x4 *out)`
  - Computes the inverse of `in` via the classical adjoint method: $\text{out} = \frac{1}{\det(\text{in})} \text{adj}(\text{in})$.
- `int adjoint(matrix_4x4 in, matrix_4x4 *out)`
  - Computes the transposed $4 \times 4$ cofactor matrix of `in` using 16 calls to `det3x3`.
- `double det4x4(matrix_4x4 m)` / `double det3x3(...)` / `double det2x2(double a, double b, double c, double d)`
  - Recursive Laplace cofactor expansion determinants for $4 \times 4$, $3 \times 3$, and $2 \times 2$ matrices.

## How It Fits Into the OMG Architecture

`orientation` is a core dependency of **`sonar_geometry`** (`code/subr/sonar_geometry.c`), **`grazing_angle`**, **`omg_target`**, **`newMergeAtt`**, **`swathed` (`SE`)** (`SE_PATCHwin.c`, `SE_BDI_DP.c`, `applyBDI.c`), **`jview` (`JV`)**, **`xse2omg`**, and **`recalc_simrad`**, performing all lever-arm and beam vector coordinate transformations.
