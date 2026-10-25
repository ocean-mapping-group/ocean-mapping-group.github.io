---
layout: default
title: tidecor2.42
parent: Finite-Element Tidal Prediction (Tidecor)
tool_name: tidecor2.42
source_path: code/Tidecor/tidecor2.42.c
category: Tidal Prediction & Datum Reduction
input_formats: [".nod", ".ele", ".bat", ".v2c / constituent files", ".merged", ".nav", ".r4", ".8bit (model_map)"]
output_formats: [".merged (updated in-place)", ".nav", ".r4", ".csv", "ASCII stdout"]
related_tools: ["plotTides", "weigh_grid", "jview"]
---

# tidecor2.42

## Overview
`tidecor2.42` (`code/Tidecor/tidecor2.42.c`) is the Ocean Mapping Group's 2D finite-element astronomical tidal prediction and hydrographic water-level reduction program. Originally derived from Mike Foreman's (IOS) tidal harmonic prediction routines and Patrick Roussel / Jason Chaffey's (BIO/DFO) triangular finite-element mesh interpolator (`interp2d.c`), it was extended by Jonathan Beaudoin, John E. Hughes Clarke, and Ian Church to operate directly on OMG-HDCS `.merged` swath files, `.nav` files, `.r4` grids, and fixed geographic stations.

`tidecor2.42` loads a regional triangular finite-element tidal mesh (`.nod` node coordinates, `.ele` triangle connectivity, `.bat` bathymetry, and harmonic constituent amplitude/phase files configured via `tidecor2.1.cfg` inside `$TIDECOR_PATH/<model>/`), locates the mesh triangle enclosing each ship fix or grid node via barycentric interpolation (`basis2d` / `phi2d`, or nearest-node fallback `-use_nearest`), and evaluates nodal astronomical arguments (`astro_angles`, `setvuf`, `TideP`) across the major harmonic and shallow-water constituents.

---

## Environment Requirement
Requires the `TIDECOR_PATH` environment variable pointing to the root directory containing regional tidal model subdirectories (e.g., `arctic`, `halifax_harbour`, `HRglobal`, `hudson_bay`, `northeast_pacific`, `northwest_atlantic`, `scotian_shelf`, `upper_fundy`).

---

## Usage & Five Operating Modes

### Mode 1: Apply Tidal Reduction Directly to an OMG `.merged` Swath File
```bash
tidecor2.42 -model upper_fundy -onto_merged -in line01.merged [-use_nearest] [-datum_shift 4.5] [-time_shift 15]
```

### Mode 2: Predict Tides Along a Binary or ASCII `.nav` Track
```bash
tidecor2.42 -model scotian_shelf -onto_nav -in ship.nav -out ship_tide.nav -into_azi [-use_nearest] [-datum_shift 1.2]
```

### Mode 3: Generate a Synthetic Tide Time Series at a Fixed Station (`-onto_position`)
```bash
tidecor2.42 -model northwest_atlantic -onto_position 45.250 -66.050 \
  -start 2024 06 01 -end 2024 06 05 -interval 6 \
  -to_csv saint_john_tide.csv
```

### Mode 4: Sample Tidal Constituent Amplitude, Phase, or Mesh Depth onto an `.r4` Grid
```bash
# Sample M2 amplitude or ISLW (M2+S2+K1+O1) onto a blank .r4 grid
tidecor2.42 -model upper_fundy -onto_grid -in bay.r4 -amp -M2 -out bay_M2_amp.r4
tidecor2.42 -model upper_fundy -onto_grid -in bay.r4 -amp -ISLW -out bay_ISLW.r4
tidecor2.42 -model upper_fundy -onto_grid -in bay.r4 -depths -out bay_mesh_depth.r4
```

### Mode 5: Query Harmonic Constituents at a Single Point
```bash
tidecor2.42 -model halifax_harbour -get_coeffs_at 44.650 -63.570
```

---

## Command-Line Options

### Model Selection & Corrections

| Option | Description |
|---|---|
| `-model <name>` | Regional tidal model subdirectory inside `$TIDECOR_PATH/` (e.g., `arctic`, `halifax_harbour`, `HRglobal`, `hudson_bay`, `northeast_pacific`, `northwest_atlantic`, `scotian_shelf`, `upper_fundy`). Mutually exclusive with `-model_map`. |
| `-model_map <map.8bit>` | Use an 8-bit OMG raster polygon map (`Map` struct) whose pixel values encode which regional tidal model ID to load dynamically as the vessel transits across model boundaries (e.g., ArcticNet transits spanning Northwest Atlantic, Hudson Bay, and Arctic meshes). |
| `-use_nearest` | When a vessel position falls slightly outside the coastal finite-element mesh boundary, extrapolate from the closest mesh node (`closestnode` using Manhattan distance optimization) instead of returning `0.0`. |
| `-datum_shift <meters>` | Additive vertical datum offset (chart datum minus Mean Sea Level, in meters) added to predicted tidal elevations. |
| `-time_shift <minutes>` | Additive time shift in minutes applied to query timestamps before harmonic evaluation. |
| `-addGPSrolloverwraps <n>` | Add `<n>` 1024-week GPS epoch rollover wraps to input timestamps (added in 2025 for legacy POS MV week-rollover logs). |
| `-v` | Enable verbose diagnostic output. |

### Input/Output Mode Flags

| Option | Description |
|---|---|
| `-onto_merged -in <file.merged>` | Updates `profile.tide` (in millimeters) in-place for every ping in an OMG-HDCS `.merged` file. |
| `-onto_nav` / `-onto_ascii_nav` | Reads `-in <in.nav>` and writes predicted tides into `-out <out.nav>` inside the selected `jcu_nav_rec` field: `-into_azi` (default, stores tide in `rec.azi`), `-into_vel` (`rec.velocity`), or `-into_depth`. |
| `-onto_position <lat> <lon>` | Generates a time series at fixed coordinates over `-start <YYYY MM DD> -end <YYYY MM DD>` (or `-start1970 <sec> -end1970 <sec>`) at `-interval <minutes>` steps. Outputs either a `.nav` file (`-out`) or a CSV file (`-to_csv <file.csv>`). |
| `-onto_grid -in <in.r4> -out <out.r4>` | Interpolates tidal mesh properties across every cell of a `JHC_header` float grid: `-depths` (mesh bathymetry), `-amp` (constituent amplitude), or `-phase` (constituent phase) for `-M2`, `-S2`, `-N2`, `-K1`, `-O1`, or `-ISLW` ($\text{M}_2 + \text{S}_2 + \text{K}_1 + \text{O}_1$ Indian Spring Low Water approximation). |
| `-get_coeffs_at <lat> <lon>` | Prints interpolated constituent amplitudes and phases at `<lat> <lon>` to `stdout`. |
