---
layout: default
title: project
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: project
source_path: code/grid/project.c
category: gridding
input_formats:
- .r4 (JHC 32-bit float bathymetry grid)
- .8bit (JHC 8-bit color/drape image)
- .maskmap (JHC 8-bit stencil mask)
output_formats:
- .8bit (saved 3D perspective rendered JHC_header image)
related_tools:
- r4to8bit
- addSUN
- mix_ci
- maskarray
---

# project

## Overview

`project` (`code/grid/project.c`) is an interactive X11 3D perspective viewing and rendering application for OMG `JHC_header` grids. It loads a 32-bit floating-point topographic/bathymetric surface (`<bathfile>.r4`), one or more 8-bit color/sunshade drape images (`-c <colormap>`), and an 8-bit validity mask (`-m <maskmap>`).

Users can interactively manipulate the camera azimuth, elevation, range, focal point, picture-plane distance, and vertical exaggeration using a fast wireframe skeleton preview (`SKEL`), and then render a full-resolution hidden-surface 3D perspective scene (`FULL`) with optional 3D contour lines (`-contour`) and a reference baseplane (`-baseplane`), saving the resulting 8-bit `JHC_header` image to disk.

---

## Syntax & CLI Options

```bash
project <bathfile.r4> -c <colormap.8bit> [-c <cmap2.8bit> ...] -m <maskmap> [OPTIONS]
```

| Option | Description | Default |
|---|---|---|
| `<bathfile.r4>` | **Required.** Input 32-bit floating-point `JHC_header` bathymetry/topography grid. | None |
| `-c <colormap>` | **Required** (repeatable up to 20 files). Input 8-bit `JHC_header` color/intensity image(s) (e.g., from [`mix_ci`](mix_ci.html) or [`addSUN`](addSUN.html)) to drape onto the 3D surface. | None |
| `-m <maskmap>` | **Required.** Input 8-bit `JHC_header` mask file (e.g., from [`maskarray`](maskarray.html)) indicating valid grid nodes. | None |
| `-elev_azi_range <elev> <azi> <range>` | Set initial camera viewing geometry using polar coordinates (elevation angle in degrees, azimuth in degrees, and radial distance in pixels). Mutually exclusive with `-eye`. | Computed from `-eye` and `-focus` |
| `-eye <x> <y> <z>` | Set initial camera eye position in grid pixel/depth coordinates. Mutually exclusive with `-elev_azi_range`. | `(dx + 100, dy + 100, 1000)` |
| `-focus <x> <y> <z>` | Set initial 3D focal point in grid coordinates. | `(dx / 2, dy / 2, 0.0)` |
| `-pp <dist>` | Set perspective picture-plane distance (`pp`). | `1000.0` |
| `-vs <scale>` | Set vertical exaggeration scale (`vscale`, divided internally by `header.xstep`). | `1.0` |
| `-page <nx> <ny>` | Set main 3D rendering viewport dimensions (`page_x_size`, `page_y_size`) in pixels. | `1024 900` |
| `-gres <step>` | Grid decimation step (in pixels) for the interactive wireframe skeleton (`SKEL`) preview. | `10` |
| `-limits <low> <high>` | Depth clipping limits (`low_limit`, `high_limit`). | `0.0 0.0` |
| `-contour <dz> <col>` | Draw 3D elevation contours on the rendered surface at interval `<dz>` (meters) using palette color index `<col>`. | Disabled |
| `-baseplane <z> (<col> \| <image>)` | Draw a horizontal reference baseplane at depth `<z>` colored either with palette index `<col>` or draped with an 8-bit image `<image>`. | Disabled |
| `-background <col>` | Set background palette color index. | `0` |
| `-autoj` | Enable automatic batch rendering / frame stepping mode. | Disabled |
| `-SUN` | Install X11 colormap directly (`XInstallColormap`) for legacy Sun workstations. | Disabled |
| `-nopixmap` | Render directly to the X11 window without allocating an offscreen `Pixmap`. | Disabled |

---

## How It Works

1. **Data Loading & Coordinate Scaling:**
   - Reads the `.r4` bathymetry grid (`bathbuf`), up to 20 8-bit drape images (`colrbuf[0..cm_set-1]`), and the 8-bit validity mask (`maskbuf`).
   - Normalizes vertical scale by `vscale /= header.xstep` so vertical exaggeration is true metric exaggeration.
2. **3D Perspective Transformation (`project` & `persp`):**
   - Constructs an orthonormal viewing basis (`basis.a`, `basis.b`, `basis.c`) from the `eye` and `focus` vectors.
   - Transforms each 3D surface vertex $(x, y, z \cdot \text{vscale})$ into eye-centered coordinates and projects onto the 2D picture plane:
     $$X_{\text{screen}} = \frac{v_x}{\text{foclen} - v_y} \cdot \text{pp} + \text{midx}, \quad Y_{\text{screen}} = \frac{v_z}{\text{foclen} - v_y} \cdot \text{pp} + \text{midy}$$
3. **Interactive Controls & Full Rendering:**
   - Displays 5 sub-windows (Main 3D Viewport, Azimuth dial, Elevation dial, Eye/Focus/PP status bar, and Vertical Exaggeration dial) plus 7 top toolbar icons (`EXIT`, `save`, `panic`, `coarse`, `fine`, `grey`, `pseudo`) and a `Focus Location` map window.
   - Clicking `fine` or `coarse` renders filled quadrilateral surface facets from back to front, optionally intersecting each triangle with contour planes (`contour()`) at interval `-contour <dz> <col>`.
   - Clicking `save` captures the rendered X11 viewport via `XGetImage` and writes an 8-bit `JHC_header` file recording `view_elev`, `view_azi`, and `view_exag` in the header.

---

## Examples

**Launch an interactive 3D perspective session with color-shaded bathymetry and 10 m contours:**

```bash
maskarray canyon.r4
r4to8bit -low -500 -high -50 canyon.r4 canyon.8bit
addSUN -elev 35 -azi 315 -exag 4 canyon.r4 canyon.sun
mix_ci -c canyon.8bit -i canyon.sun -m canyon_ci.8bit

project canyon.r4 -c canyon_ci.8bit -m canyon.r4.maskmap -vs 4.0 -contour 25 0 -page 1200 900
```

---

## Workflow Context

- **Upstream:** [`weigh_grid`](weigh_grid.html) $\rightarrow$ [`maskarray`](maskarray.html), [`r4to8bit`](r4to8bit.html), [`addSUN`](addSUN.html), [`mix_ci`](mix_ci.html).
- **Output:** Saved 8-bit perspective renders include `view_elev`, `view_azi`, and `view_exag` in their `JHC_header` and can be annotated with [`addstamp`](addstamp.html).
