---
layout: default
title: subtractSurface
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: subtractSurface
source_path: code/grid/subtractSurface.c
category: gridding
input_formats:
- JHC_header (.r4)
- OMG HDCS (.merged)
output_formats:
- OMG HDCS (.merged)
related_tools:
- weigh_grid
- differ
- showError
---

# subtractSurface

## Overview

`subtractSurface` compares every valid multibeam sounding in one or more OMG HDCS `.merged` survey lines against a bilinearly interpolated `.r4` reference surface (`<r4prefix>.r4`) and writes the vertical residual (`real_depth - measured_depth`, in millimeters) directly into each beam's `offset` (file versions 2–4) or `depthAccuracy` (version 1) field in-place.

---

## Syntax & CLI Options

```
subtractSurface [-v] [-proc] [-add_dyn_draft_shift] [-latshift <min>] [-lonshift <min>] <r4prefix> <merged_files...>
```

| Flag / Argument | Description |
|-----------------|-------------|
| `-v` | Verbose per-beam residual output. |
| `-proc` | Compare `processedDepth` (instead of `observedDepth`) against the reference surface. |
| `-add_dyn_draft_shift` | Subtract `profile.longperiod_heaveCorrection / 1000.0` (dynamic draft / squat) from the measured beam depth before computing the residual. |
| `-latshift <min>` | Latitude shift in arc-minutes applied to beam coordinates before projecting onto the reference grid (default: `0.0`). |
| `-lonshift <min>` | Longitude shift in arc-minutes applied to beam coordinates before projecting onto the reference grid (default: `0.0`). |
| `<r4prefix>` | Reference `.r4` grid prefix (reads `<r4prefix>.r4`). |
| `<merged_files...>` | One or more OMG HDCS `.merged` survey line files (modified in-place). |

---

## How It Works

1. **Reference Surface Loading**:
   - Opens `<r4prefix>.r4`, reads its `JHC_header` (`data_type == 3`), and loads the floating-point depth array (`final_data`) into memory.
2. **Beam-by-Beam Residual Computation**:
   - Opens each `<merged_file>` in read-write mode (`"r+"`) and loops over all unflagged profiles (`profile.status == 0`).
   - For each valid beam (`observedDepth > 0`, `status != 22 && status != 1`):
     - Computes the beam's geographic position (`locate_beam`), applies `-latshift` / `-lonshift`, and projects onto fractional grid coordinates `(x, y)` via `Project`.
     - Computes the tide-reduced beam depth (using `processedDepth` if `-proc` is set, else `observedDepth`, and optionally applying `longperiod_heaveCorrection` if `-add_dyn_draft_shift` is set).
     - Bilinearly interpolates the reference surface depth `real_depth` from the 4 surrounding grid nodes (`get_lookup_value`), requiring all 4 neighbors to be non-zero.
     - Stores `(real_depth - depth) * 1000.0` into `beams[n].offset` (for HDCS v2–v4) or `beams[n].depthAccuracy` (v1), or `0.0` if outside the valid reference surface.
   - Writes the updated beam records back into the `.merged` file (`OMG_HDCS_put_raw_beams`).

---

## Examples

### Compute beam-by-beam depth residuals against a reference patch-test grid

```bash
subtractSurface -proc ref_patch line01.merged line02.merged
```

### Evaluate residuals with a trial navigation offset of +0.02' latitude and -0.03' longitude

```bash
subtractSurface -latshift 0.02 -lonshift -0.03 ref_surface survey_line.merged
```

---

## Workflow Context

- **Upstream**: [`weigh_grid`](weigh_grid.html) (builds the reference `.r4` bathymetric surface).
- **Downstream**: `swathEd` (visualizes the stored `offset` / residual across beams to diagnose roll, pitch, latency, sound speed, or dynamic draft artifacts).
