---
layout: default
title: makemesh
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: makemesh
source_path: code/grid/makemesh.c
category: gridding
input_formats:
- JHC_header (optional reference image via -getsizeimage)
output_formats:
- .8bit (JHC 8-bit mesh, colorbar, or phase-difference pattern)
related_tools:
- make_blank
- selectcb
- mix_ci
- maskarray
---

# makemesh

## Overview

`makemesh` creates a synthetic 8-bit `JHC_header` raster (`data_type = 1`) containing one of three patterns:
1. **Regular Grid / Mesh (default):** Horizontal and vertical grid lines spaced every `-spacing` pixels (with configurable line and background digital numbers).
2. **Colorbar / Greyscale Wedge (`-colorbar`):** A 2D 8-color $\times$ 30-shade color-intensity palette wedge (or 0–255 vertical greyscale ramp with `-grey`).
3. **Interferometric Phase-Difference Circular Pattern (`-wavelengths` / `-mount_angle`):** A circular polar plot illustrating two-element interferometric sonar phase wraps (`dlambda = wavelengths * sin(angle - mount_angle)`) across a transducer stave pair.

---

## Syntax & CLI Options

```bash
makemesh (-xlen <nx> -ylen <ny> | -getsizeimage <ref_file>) [OPTIONS] -out <filename>
```

| Option | Description | Default |
|---|---|---|
| `-out <filename>` | **Required.** Output 8-bit `JHC_header` filename. | None |
| `-xlen <pixels>` | Horizontal width (`dx`) of the output array in pixels. | Required unless `-getsizeimage` is used |
| `-ylen <pixels>` | Vertical height (`dy`) of the output array in pixels. | Required unless `-getsizeimage` is used |
| `-getsizeimage <file>` | Copy `dx`, `dy`, and georeferencing metadata from an existing `JHC_header` file. | Disabled |
| `-spacing <pixels>` | Grid line interval in pixels for mesh mode. | `10` |
| `-xoffset <pixels>` | Horizontal phase offset (`j % spacing == xoffset`) for vertical mesh lines. | `0` |
| `-yoffset <pixels>` | Vertical phase offset (`i % spacing == yoffset`) for horizontal mesh lines. | `0` |
| `-line <DN>` | Digital number (`0..255`) for mesh grid lines. | `0` (`255` if `-invert`) |
| `-back <DN>` | Digital number (`0..255`) for mesh background pixels. | `255` (`0` if `-invert`) |
| `-invert` | Swap default mesh colors so grid lines are `255` and background is `0`. | Disabled |
| `-colorbar` | Generate a 2D color-intensity palette bar (`16 + 30*(j/xlen) + 30*int(8*i/ylen)`) instead of a mesh. | Disabled |
| `-grey` | Used with `-colorbar`: generate a smooth vertical `0..255` greyscale ramp instead of the 8-color $\times$ 30-shade palette. | Disabled |
| `-wavelengths <N>` | Enable interferometric phase-difference pattern mode with transducer baseline separation `<N>` wavelengths ($d/\lambda$). | `0.5` |
| `-mount_angle <deg>` | Enable interferometric phase-difference pattern mode with stave tilt angle `<deg>` degrees. | `0.0` |
| `-360` | Used in phase-difference mode: plot across the full $360^\circ$ circle instead of restricting to the forward hemisphere ($-90^\circ$ to $+90^\circ$). | Disabled |

---

## How It Works

1. **Header Initialization:** Either reads an existing `JHC_header` via `-getsizeimage` or constructs a new `OMG1` header with `dx = xlen`, `dy = ylen`, and `data_type = 1` (8-bit unsigned char).
2. **Pattern Generation:**
   - **Mesh Mode (default):** Sets pixel `(j, i)` to `MESH_LINE` whenever `i % spacing == yoffset` or `j % spacing == xoffset`, and `MESH_BACK` otherwise.
   - **Colorbar Mode (`-colorbar`):** Maps horizontal position `j` across 30 intensity shades and vertical position `i` across 8 color bands (`DN = 16 .. 255`), matching the default [`mix_ci`](mix_ci.html) color-intensity table.
   - **Phase-Difference Mode (`-wavelengths` or `-mount_angle`):** Within a circle of radius $\min(\text{xlen}, \text{ylen})/2$, computes polar angle $\theta$ relative to `mount_angle`, evaluates wrapped phase path difference $\Delta\lambda = \text{frac}(d/\lambda \cdot \sin\theta) \in [-0.5, 0.5)$, and maps it to palette indices `16..254`.

---

## Examples

**1. Create a 20-pixel mesh matching the dimensions and projection of an existing `.r4` grid:**

```bash
makemesh -getsizeimage survey.r4 -spacing 20 -line 0 -back 255 -out survey_mesh.8bit
```

**2. Create a 2D color-intensity legend bar for `mix_ci` maps:**

```bash
makemesh -xlen 100 -ylen 400 -colorbar -out ci_legend.8bit
```

**3. Generate a 2-wavelength interferometric sonar phase-wrap diagram tilted at 30°:**

```bash
makemesh -xlen 500 -ylen 500 -wavelengths 2.0 -mount_angle 30.0 -out interf_phase.8bit
```

---

## Workflow Context

- Mesh grids generated with `-getsizeimage` can be reprojected with [`project`](project.html) to visualize map distortion or overlaid onto imagery via [`add8bit`](add8bit.html) / [`mix_ci`](mix_ci.html).
