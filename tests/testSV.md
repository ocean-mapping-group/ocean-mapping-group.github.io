---
layout: default
title: testSV
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 23
tool_name: testSV
source_path: code/tests/testSV.c
category: Seawater Sound Speed & Oceanographic Functions (tests)
input_formats:
- Interactive stdin (Salinity, Temperature, Depth) or -stz CLI args
- 3-column ASCII profile: depth (m), temperature (°C), salinity (ppt) (-dofile)
- OMG j_watercolumn SVP file (-dotrace)
output_formats:
- Sound speed (m/s) or UNESCO seawater density (kg/m³) on stdout
- 400x300 OMG .r4 floating-point T-S sound speed surface (<outfile>)
related_tools:
- speed2salinity
- speedtosalinity
- testAtten
- one
- two
- RTlite
---

# testSV

## Overview
`testSV` (`code/tests/testSV.c`, authored by John Hughes Clarke in July 1994 and updated by Jason Bartlett in 2004–2007 and JHC in 2015–2019) is the primary OMG testbed for empirical seawater sound speed equations, UNESCO seawater density equations, and `j_watercolumn` sound velocity profile (SVP) sorting and interpolation.

It supports five distinct modes of operation:
1. **Single-Point / Interactive Sound Speed & Density Calculator (Default or `-stz`):** Computes seawater sound speed using either **Chen & Millero (1977)** (`-chenmill`, default, requiring `-lat <deg>` for latitude-dependent depth-to-pressure conversion via `depth2press()`) or **Wilson (1962)** (`-wilson`), or computes **UNESCO Seawater Density** (`-unesco_density`, via `density()` from `water.h`).
2. **Batch ASCII CTD Profile Processing (`-dofile <file>`):** Reads 3-column `(depth, temp, sal)` records from `<file>` and prints `(depth, sound_speed)` or `(depth, density)` to `stdout`.
3. **SVP Cast Sorting & Ray-Trace Layer Interpolation (`-dotrace <svpfile>`):** Loads an OMG `j_watercolumn` SVP file via `jWC_read()`, sorts asynchronous down/up casts via `jWC_sort_async(&wc, JWC_BOTHCAST)`, and interpolates depth/velocity layers down to `-maxdepth` (`jWC_interp_zv()`).
4. **2D Temperature–Salinity Sound Speed Grid Generation (when `<inname> <outname>` are supplied):** Computes a $400 \times 300$ floating-point matrix of sound speeds at $z = 2.0\text{ m}$ across Salinity $S \in [0, 40]\text{ ppt}$ ($\Delta S = 0.1\text{ ppt}$) and Temperature $T \in [0, 30]^\circ\text{C}$ ($\Delta T = 0.1^\circ\text{C}$) and writes an `OMG1` `.r4` grid to `<outname>`.

---

## Syntax & CLI Options

```bash
# 1. Single-point evaluation on command line (Chen-Millero requires -lat)
testSV [-chenmill -lat <deg> | -wilson | -unesco_density] [-atmos <kg/cm2>] -stz <sal_ppt> <temp_C> <depth_m>

# 2. Interactive loop on stdin
testSV [-chenmill -lat <deg> | -wilson | -unesco_density]

# 3. Process a 3-column (depth, temp, sal) ASCII profile
testSV [-chenmill -lat <deg> | -wilson | -unesco_density] -dofile <ctd_profile.txt>

# 4. Test j_watercolumn SVP reading, sorting, and interpolation
testSV [-v] -dotrace [-maxdepth <m>] [-maxSV <m/s>] <svpfile>

# 5. Export a 400x300 (Salinity x Temperature) OMG .r4 sound speed surface
testSV [-wilson | -chenmill -lat <deg>] <dummy_in> <grid_out.r4>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-chenmill` | Use Chen & Millero's (1977) equation (`do_cml = 1`). **Requires `-lat <deg>`** so `depth2press(depth, latitude)` can account for gravitational variation with latitude. | Enabled by default (`1`) |
| `-lat <deg>` | Geographic latitude in decimal degrees (required when `-chenmill` is active). | `0.0` (must be non-zero for `-chenmill`) |
| `-wilson` | Use W. D. Wilson's (1962) equation (`vsw`, `do_wilson = 1`, `do_cml = 0`). | `0` |
| `-unesco_density` | Compute UNESCO (1981) seawater density (`density(sal, temp, pressure)` from `water.h`) instead of sound speed. | `0` |
| `-stz <S> <T> <Z>` | Evaluate a single point with Salinity `<S>` (ppt), Temperature `<T>` ($^\circ\text{C}$), and Depth `<Z>` (m), print the result, and exit (`do_just_once = 1`). | Interactive loop |
| `-dofile <file>` | Read 3-column `(depth, temp, sal)` lines from `<file>` and print `depth value` pairs to `stdout`. | Disabled |
| `-dotrace` | Test `jWC_init`, `jWC_read`, `jWC_sort_async`, and `jWC_interp_zv` on `<inname>`. | Disabled |
| `-maxdepth <m>` | Maximum interpolation depth (meters) passed to `jWC_interp_zv()` in `-dotrace` mode. | `100.0` |
| `-maxSV <m/s>` | Maximum sound velocity parameter for `-dotrace` *(note: line 158 assigns to `max_interp_depth` in source).* | `1490.0` |
| `-atmos <val>` | Atmospheric pressure in $\text{kg/cm}^2$ added to hydrostatic gauge pressure in Wilson / UNESCO / `-dofile` modes. | `1.0332` |
| `-v` | Enable verbose output (calls `jWC_print(&wc)` in `-dotrace` mode). | `0` |

---

## Oceanographic Equations & Historical Verification Notes

1. **Latitude-Dependent Pressure & Chen-Millero (`soundspeed.c`):**
   As documented by Jason Bartlett (`JDB`, February 2007, lines 303–317), in interactive/`-stz` Chen-Millero mode, `testSV` converts depth $z$ (m) and latitude $\phi$ (deg) to pressure in MPa via `depth2press(depth, latitude)`, scales to bars (`MPA_TO_BARS * pressure`), and calls the NPL-validated `ChenMillero(sal, temp, press_bars)` from `subr/soundspeed.c`—achieving agreement with Sea-Bird SBE CTD software on CCGS *Amundsen*.
2. **Correction of `this_vchemilli` (`a3` term, line 479) and `this_vsw` (`vstp` term, line 430):**
   `testSV.c` contains both the corrected `a3` term (`1.0405e-12 * pow(t, 4)`) and the corrected additive `+ p *` cross-terms in `this_vsw()` that were buggy in earlier standalone files ([`one.c`](one.html), [`speed2salinity.c`](speed2salinity.html), and [`speedtosalinity.c`](speedtosalinity.html)).

---

## Example Usage

```bash
# 1. Compute Chen-Millero sound speed at S=34.5 PSU, T=4.2°C, Z=500 m at 70.5°N latitude
testSV -chenmill -lat 70.5 -stz 34.5 4.2 500.0

# 2. Compute UNESCO seawater density at S=35.0 PSU, T=10.0°C, Z=100 m
testSV -unesco_density -stz 35.0 10.0 100.0

# 3. Generate a 400x300 Salinity-Temperature sound speed .r4 raster using Wilson's equation
testSV -wilson dummy_in ts_wilson_grid.r4
```
