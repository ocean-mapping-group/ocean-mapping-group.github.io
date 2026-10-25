---
layout: default
title: surface
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: surface
source_path: code/grid/surface.c
category: gridding
input_formats:
- ASCII XYZ Triples (stdin or file)
output_formats:
- Binary Grid (surface.grd)
related_tools:
- weigh_grid
- r4interp
- fillGap
---

# surface

## Overview

`surface` fits a continuous, adjustable-tension bicubic / biharmonic spline surface to randomly spaced `(x, y, z)` data triples using the Smith & Wessel (1990) multigrid over-relaxation algorithm. It solves the differential equation:

$$(1 - T)\nabla^4 z - T\nabla^2 z = 0$$

where $T \in [0, 1]$ is the tension factor ($T = 0$ yields the classical minimum-curvature surface; $T = 1$ yields a harmonic membrane spline without artificial overshoots).

---

## Syntax & CLI Options

```
surface [xyz-file] -R<west>/<east>/<south>/<north> -I<xinc>[/<yinc>] \
  [-A<aspect_ratio>] [-C<convergence_limit>] [-H] [-N<n_iterations>] \
  [-O<output_grdfile_name>] [-S<search_radius>] [-T<tension>[i|b]] \
  [-V[L]] [-Z<over_relaxation_parameter>]
```

| Flag | Description |
|------|-------------|
| `[xyz-file]` | Optional input 3-column ASCII `x y z` file (defaults to `stdin`). |
| `-R<west>/<east>/<south>/<north>` | **Required.** Spatial domain bounds (`xmin/xmax/ymin/ymax`). |
| `-I<xinc>[/<yinc>]` | **Required.** Grid spacing in X and Y (append `m` or `M` to specify arc-minutes; if `<yinc>` is omitted, `yinc = xinc`). |
| `-A<aspect_ratio>` | Anisotropy aspect ratio (`yinc = xinc / aspect_ratio`, default: `1.0` for isotropic derivatives). |
| `-C<convergence_limit>` | Stop iterating when the maximum absolute node change is less than `<convergence_limit>` (default: `0.001` of the RMS $z$ range). |
| `-H` | Skip the first line of the input file (header record). |
| `-N<n_iterations>` | Maximum iterations per multigrid factor cycle (default: `250`). |
| `-O<output_grdfile_name>` | Output grid filename (default: `surface.grd`). |
| `-S<search_radius>` | Search radius for weighted-average grid initialization (default: `0.0`, skipped; append `m` or `M` for arc-minutes). |
| `-T<tension>[i\|b]` | Tension factor between `0.0` and `1.0` (default: `0.0`). Append `i` or `I` for interior equations only, `b` or `B` for boundary conditions only, or neither for both. |
| `-V` / `-VL` | Verbose (`-V`) or long-verbose (`-VL`) convergence diagnostics to `stderr`. |
| `-Z<over_relaxation_parameter>` | Successive over-relaxation (SOR) factor between `1.0` and `2.0` (default: `1.4`). |

---

## How It Works

1. **Pre-Processing & Detrending**:
   - Reads up to `500,000` `(x, y, z)` points from `[xyz-file]` or `stdin`.
   - Assigns each point to its nearest final grid node, discarding redundant points that map to the same node (`throw_away_unusables` keeps the point closest to the node center).
   - Removes the best-fitting least-squares plane (`remove_planar_trend`) and normalizes residuals by the RMS $z$ amplitude (`rescale_z_values`).
2. **Multigrid Factorization & Briggs Off-Node Constraints**:
   - Factorizes `(nx - 1)` and `(ny - 1)` into common prime factors (`factor`) so the finite-difference solver starts on a coarse sub-grid and progressively refines (`smart_divide`, `fill_in_forecast`) down to `grid = 1`.
   - Constrains grid nodes near data points using I. C. Briggs (1974) Taylor-series Laplacian coefficients (`struct BRIGGS`).
3. **Biharmonic / Harmonic Over-Relaxation**:
   - Iteratively updates the 12-point biharmonic/Laplacian finite-difference stencil (`iterate`) using the over-relaxation factor `-Z` until the maximum change falls below `-C` or `-N` iterations are reached.
   - Restores the planar trend (`replace_planar_trend`) and writes the resulting surface to `-O`.

---

## Examples

### Fit a tensioned spline surface (T = 0.35) to bathymetric XYZ soundings

```bash
surface soundings.xyz -R-67.0/-66.5/44.5/45.0 -I0.5m -T0.35 -Opassamaquoddy.grd -V
```

---

## Workflow Context

- **Related Gridding & Interpolation Tools**: [`weigh_grid`](weigh_grid.html), [`r4interp`](r4interp.html), [`fillGap`](fillGap.html).
