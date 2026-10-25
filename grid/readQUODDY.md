---
layout: default
title: readQUODDY
parent: Grid Tools
tool_name: readQUODDY
source_path: code/grid/readQUODDY.c
category: gridding
input_formats: ["QUODDY Finite-Element Mesh (.nod, .ele, .bat)", "QUODDY Harmonic Tide/Current Files", "JHC_header (.r4)"]
output_formats: ["ASCII XYZ (.xyz)", "ASCII Mesh Elements (.ele_out)", "Harmonic Current/Tide Grids (.ampl, .phase, .umag, .vmag, .currvec, .mocktide)", "Binary Residual Current (.justresid)", "JHC_header (.r4)"]
related_tools: ["showModelMesh", "makemesh", "plotADCPgridcurrents", "weigh_grid"]
---

# readQUODDY

## Overview

`readQUODDY` reads 3D finite-element hydrodynamic model meshes and harmonic output products from the Dartmouth **QUODDY** circulation model (`.nod` nodes, `.ele` triangular elements, `.bat` node depths, tidal amplitude/phase files, and M2 harmonic or residual current files). It exports node/element ASCII tables, harmonic tidal current vectors at 10° phase increments, synthetic OMG tide station files, and planar-interpolated `.r4` bathymetric or tidal grids.

---

## Syntax & CLI Options

```
readQUODDY [OPTIONS] -model <quoddy_prefix> -out <deriv_prefix> \
  [-tide <amp_phase_file>] [-curr <curr_file>] [-residcurr <resid_file>] \
  [-into <map.r4> -interp <interp_prefix> [-dontflip] [-vshift <val>] [-mapelem] [-no_bat]]
```

| Flag | Description |
|------|-------------|
| `-model <prefix>` | Input QUODDY model prefix (reads `<prefix>.nod`, `<prefix>.ele`, and `<prefix>.bat`). |
| `-out <prefix>` | Output prefix for derived ASCII and vector products. |
| `-no_bat` | Skip reading `<prefix>.bat` (sets all node depths to `0.0`). |
| `-tide <file>` | Read a QUODDY harmonic tidal elevation file (amplitude and phase per node) and write `<out>.ampl` and `<out>.phase`. |
| `-curr <file>` | Read a QUODDY M2 harmonic current file (`umag, uphase, vmag, vphase` per node) and write `<out>.umag`, `<out>.vmag`, 36 phase snapshots (`<out>_000.currvec` .. `<out>_350.currvec`), and synthetic tide files (`<out>.mocktide`, `<out>.mocktide_rev`). |
| `-residcurr <file>` | Read a QUODDY residual current file and export binary `jcu_nav_rec` records to `<out>.justresid`. |
| `-into <map.r4>` | Reference `.r4` mapsheet used as the target grid geometry for triangular mesh interpolation. |
| `-interp <prefix>` | Output `.r4` prefix for the interpolated surface (`<prefix>.r4`). Requires `-into`. |
| `-dontflip` | Do not negate depths when interpolating onto `-into` (used when interpolating elevations or amplitudes rather than positive-down depths). |
| `-vshift <val>` | Apply a constant vertical datum offset (`val`) to interpolated node values. |
| `-mapelem` | Also write `MapElement.r4` recording the 1-based triangular element index covering each grid pixel. |
| `-utm` | Project node coordinates into WGS84 North UTM (requires `-merid`). |
| `-merid <deg>` | Central meridian for `-utm` or custom rotated projections. |
| `-xorigin <lon>` | Origin longitude for custom rotated local coordinates (`PROJ_CLUMSY`). |
| `-yorigin <lat>` | Origin latitude for custom rotated local coordinates (`PROJ_CLUMSY`). |
| `-rotangle <deg>` | Rotation angle (degrees) for custom rotated local coordinates (`PROJ_CLUMSY`). |
| `-proj_custom_kenneb` | Use the hardcoded Kennebec River local rotated UTM projection (`merid = -69°`, `origin = -69.750116°, 43.702612°`, `rot = -9°`). |

---

## How It Works

1. **Mesh Ingestion**:
   - Reads node coordinates `(index, lon, lat)` from `<model>.nod` (up to `MAX_NODES = 20000`), triangle connectivity `(index, n1, n2, n3)` from `<model>.ele` (up to `MAX_ELEMENTS = 30000`), and node depths `(index, depth)` from `<model>.bat`.
   - Exports `<out>.xyz` (`lat lon depth`) and `<out>.ele_out` (`3-line vertex blocks per triangle`).
2. **Harmonic Tide & Current Processing**:
   - With `-tide`, reads node tidal amplitude and phase (skipping the 3-line header) and writes `<out>.ampl` (`lon lat ampl`) and `<out>.phase` (`lon lat phase`). If `-into` is also given, replaces node depths with tidal amplitudes so the interpolated `.r4` surface maps tidal amplitude.
   - With `-curr`, reads surface M2 velocity components (`umag, uphase, vmag, vphase`), writes `<out>.umag` and `<out>.vmag`, and steps through `phase = 0°..350°` in `10°` increments (corresponding to 20.69-minute intervals of a 12.42-hour M2 cycle), writing `<out>_<phase>.currvec` (`lat lon speed_cm_s dir_deg`) and synthetic 12.42-hour tide curves (`<out>.mocktide` and `<out>.mocktide_rev`).
3. **Barycentric Triangle Interpolation (`-into` & `-interp`)**:
   - Projects mesh vertices into the target `.r4` mapsheet coordinates (`utm`, `mercator`, `geographic`, or `clumsy`).
   - For each triangular element, computes its bounding box in grid rows/columns, tests candidate pixel centers against the three directed triangle edges (`d Side1, Side2, Side3`), and evaluates the planar facet equation (`A*x + B*y + C*z + D = 0` via `dSurf`) to populate `<interp>.r4`.

---

## Examples

### Interpolate a QUODDY bathymetric mesh onto a target `.r4` mapsheet
```bash
readQUODDY -model bay_quoddy -out bay_mesh -into bay_template.r4 -interp bay_quoddy_bathy -mapelem
```

### Extract M2 tidal current vectors and synthetic phase tide files
```bash
readQUODDY -model bay_quoddy -out bay_m2 -curr bay_quoddy.s2c
```

---

## Workflow Context

- **Related Mesh & Current Tools**: [`showModelMesh`](showModelMesh.html), [`makemesh`](makemesh.html), [`plotADCPgridcurrents`](plotADCPgridcurrents.html).
