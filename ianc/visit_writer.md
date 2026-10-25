---
layout: default
title: visit_writer
parent: Ian Church (ianc) Tools
nav_order: 15
tool_name: visit_writer
source_path: code/ianc/subr/visit_writer.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats: ["In-memory 3D point, unstructured, regular, rectilinear, or curvilinear mesh arrays"]
output_formats: ["VTK Legacy DataFile Version 2.0 (.vtk, ASCII or Big-Endian Binary)"]
related_tools: ["modelAnalysis", "iwc_gwc", "iwc_support"]
---

# visit_writer

## Description

`visit_writer` (`code/ianc/subr/visit_writer.c` and `code/ianc/subr/visit_writer.h`) is the Lawrence Livermore National Laboratory (LLNL) VisIt VTK mesh export library (originally authored by Hank Childs, LLNL, 2004–2010) included in `code/ianc/subr/` for exporting 3D oceanographic model meshes, acoustic water-column point clouds, and rectilinear/curvilinear bathymetric grids into **VTK Legacy Format (`# vtk DataFile Version 2.0`, `.vtk`)** for 3D visualization in VisIt or ParaView.

The library supports five mesh topologies—**Point Meshes**, **Unstructured Meshes** (triangles, quads, tetrahedra, hexahedra, wedges, pyramids, pixels, voxels, lines, vertices), **Regular Meshes**, **Rectilinear Meshes**, and **Curvilinear/Structured Meshes**—and can write output in either human-readable **ASCII** or portable **Big-Endian Binary** format with arbitrary numbers of nodal (point-centered) and zonal (cell-centered) scalar and 3-component vector variables.

## Public API & Usage

### Header Include

```c
#include "visit_writer.h"
```

### Example C Usage: Unstructured Triangular Mesh

```c
#include "visit_writer.h"

/* Four unique 3D vertices (x, y, z) forming two triangles */
float pts[12] = { 0.0f, 0.0f, -10.0f,
                  0.0f, 1.0f, -12.0f,
                  1.0f, 1.0f, -15.0f,
                  1.0f, 0.0f, -11.0f };
int npts = 4;
int ncells = 2;
int celltypes[2] = { VISIT_TRIANGLE, VISIT_TRIANGLE };
int conn[6] = { 0, 1, 2,  0, 2, 3 };

/* One point-centered scalar variable ("sound_speed") */
float ssp[4] = { 1490.2f, 1491.0f, 1492.5f, 1490.8f };
int vardim[1] = { 1 };
int centering[1] = { 1 }; /* 1 = point-based, 0 = cell-based */
const char *varnames[1] = { "sound_speed" };
float *vars[1] = { ssp };

write_unstructured_mesh("fvcom_slice.vtk", 0, npts, pts,
                        ncells, celltypes, conn,
                        1, vardim, centering, varnames, vars);
```

## Cell Type Constants (`visit_writer.h`)

Used in the `celltypes` array passed to `write_unstructured_mesh()`:

| Macro Constant | VTK Cell ID | Number of Vertices | Geometry Description |
| :--- | :--- | :--- | :--- |
| `VISIT_VERTEX` | `1` | `1` | Single 3D point vertex. |
| `VISIT_LINE` | `3` | `2` | 2-node line segment. |
| `VISIT_TRIANGLE` | `5` | `3` | 3-node triangle (e.g., FVCOM surface/sigma element). |
| `VISIT_PIXEL` | `8` | `4` | Axis-aligned 2D quadrilateral pixel. |
| `VISIT_QUAD` | `9` | `4` | General 4-node 2D/3D quadrilateral. |
| `VISIT_TETRA` | `10` | `4` | 4-node 3D tetrahedron. |
| `VISIT_VOXEL` | `11` | `8` | Axis-aligned 3D 8-node brick/voxel. |
| `VISIT_HEXAHEDRON` | `12` | `8` | General 8-node 3D hexahedron. |
| `VISIT_WEDGE` | `13` | `6` | 6-node 3D triangular prism / wedge (e.g., 3D FVCOM sigma prism). |
| `VISIT_PYRAMID` | `14` | `5` | 5-node 3D quad-base pyramid. |

## Public Functions (`visit_writer.c`)

| Function | Signature | Description |
| :--- | :--- | :--- |
| `write_point_mesh` | `void write_point_mesh(const char *filename, int useBinary, int npts, float *pts, int nvars, int *vardim, const char * const *varnames, float **vars)` | Writes `npts` 3D points (`pts` of length `3 * npts`) as a `DATASET UNSTRUCTURED_GRID` composed of `VISIT_VERTEX` cells, with all `nvars` treated as point-centered (`centering[i] = 1`). |
| `write_unstructured_mesh` | `void write_unstructured_mesh(const char *filename, int useBinary, int npts, float *pts, int ncells, int *celltypes, int *conn, int nvars, int *vardim, int *centering, const char * const *varnames, float **vars)` | Writes an arbitrary unstructured 3D mesh (`DATASET UNSTRUCTURED_GRID`) with `npts` vertices, `ncells` cells of types `celltypes[i]`, vertex connectivity `conn`, and cell/point variables. |
| `write_regular_mesh` | `void write_regular_mesh(const char *filename, int useBinary, int *dims, int nvars, int *vardim, int *centering, const char * const *varnames, float **vars)` | Writes a uniform regular grid of dimensions `dims[3] = {nX, nY, nZ}` by synthesizing integer coordinate arrays `x = 0..nX-1`, `y = 0..nY-1`, `z = 0..nZ-1` and delegating to `write_rectilinear_mesh()`. |
| `write_rectilinear_mesh` | `void write_rectilinear_mesh(const char *filename, int useBinary, int *dims, float *x, float *y, float *z, int nvars, int *vardim, int *centering, const char * const *varnames, float **vars)` | Writes a `DATASET RECTILINEAR_GRID` with dimensions `dims[3]` and 1D coordinate vectors `x[dims[0]]`, `y[dims[1]]`, and `z[dims[2]]`. |
| `write_curvilinear_mesh` | `void write_curvilinear_mesh(const char *filename, int useBinary, int *dims, float *pts, int nvars, int *vardim, int *centering, const char * const *varnames, float **vars)` | Writes a `DATASET STRUCTURED_GRID` with logical dimensions `dims[3] = {nI, nJ, nK}` and explicit 3D coordinates `pts` of length `3 * nI * nJ * nK`. |
| `write_variables` | `void write_variables(int nvars, int *vardim, int *centering, const char * const *varname, float **vars, int npts, int ncells)` | Internal/shared helper that writes `CELL_DATA <ncells>` followed by `POINT_DATA <npts>`, grouping primary `SCALARS` (`vardim == 1`), primary `VECTORS` (`vardim == 3`), and secondary `FIELD FieldData` blocks. |

## File Formats

* **VTK Legacy File (`.vtk`)**: If `filename` does not already contain the `.vtk` suffix, `open_file()` automatically appends `.vtk`. Each file begins with the 3-line VTK header:
  ```text
  # vtk DataFile Version 2.0
  Written using VisIt writer
  ASCII (or BINARY)
  ```
  followed by the `DATASET` geometry block (`UNSTRUCTURED_GRID`, `RECTILINEAR_GRID`, or `STRUCTURED_GRID`), `CELL_DATA`, and `POINT_DATA`.

## How It Works

1. **Automatic Big-Endian Conversion**: The VTK Legacy binary specification requires all binary `int` and `float` values to be stored in big-endian byte order. When `useBinary != 0`, `force_big_endian()` tests host endianness once at runtime and swaps the 4 bytes of every `int` and `float` on little-endian architectures (such as x86_64 Linux) before calling `fwrite()`.
2. **VTK Field Data Grouping**: Because VTK's legacy reader fails when scalar and vector arrays are mixed inside a single `FIELD FieldData` block, `write_variables()` makes multiple passes over `vars`: for both `CELL_DATA` (`centering[i] == 0`) and `POINT_DATA` (`centering[i] != 0`), it emits the first scalar as `SCALARS <name> float`, the first 3-component vector as `VECTORS <name> float`, all remaining scalars in a dedicated `FIELD FieldData <num_scalars>` block, and all remaining vectors in a second `FIELD FieldData <num_vectors>` block.
