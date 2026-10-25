---
layout: default
title: Teledyne RDI ADCP Processing (adcp)
parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 4
has_children: true
---

# ADCP Tools (`code/adcp/`)

The `adcp/` suite provides command-line utilities for ingesting, filtering, bottom-trimming, georeferencing, and harmonically analyzing **Acoustic Doppler Current Profiler (ADCP)** datasets—including Teledyne RDI ASCII / WinADCP exports, VMDAS records, and Kongsberg EC150 / generic NetCDF-derived 3D velocity arrays (`.N.r4`, `.E.r4`, `.D.r4`).

For an end-to-end guide with architecture diagrams and command-line recipes, see the **[ADCP Processing & Tidal Current Analysis Workflow](../workflows/adcp-processing-workflow.html)**.

---

## Tool Inventory by Stage

### 1. RDI & WinADCP Ingestion and Profile Mapping
* **[`readADCP`](readADCP.html)** (`code/adcp/readADCP.c`): Primary RDI ASCII and WinADCP processor. Integrates external `.nav`, `.orientation`, `tide.nav`, and multibeam `.r4` DTMs to produce bottom-trimmed `.prof` (8-bit), `.r4` (32-bit float), `.nav` (depth-averaged current vectors), `.stack_prof`, and georeferenced `.map_prof` / `.map_r4` sections across 7 display modes (`-showMAG`, `-showBS`, `-showAZI`, `-showTAN`, `-showRAD`, `-showVERT`, `-showERR`).
* **[`readADCP_g`](readADCP_g.html)** (`code/adcp/readADCP_g.c`): Streamlined variant of `readADCP` with `-phase_zero` tidal phase referencing and `-ref_bottom` height-above-bottom binning.
* **[`readADCP_mod`](readADCP_mod.html)** (`code/adcp/readADCP_mod.c`): Modified variant of `readADCP` adding `-min_vels_to_av` filtering for depth-averaged `.nav` vector generation.
* **[`readWinADCP`](readWinADCP.html)** (`code/adcp/readWinADCP.c`): Stacks tabular WinADCP ASCII exports into ensemble-averaged ASCII profiles (`.stack####`) and 8-bit velocity magnitude rasters (`.mag`).

### 2. Generic & Kongsberg EC150 3D Velocity Processing
* **[`readGenericADCP`](readGenericADCP.html)** (`code/adcp/readGenericADCP.c`): Reads generic/EC150 `.N.r4`, `.E.r4`, and `.D.r4` velocity component rasters plus `.decXX.nav` navigation, depth-averaging currents between `-mindepth` and `-maxdepth` into a `jcu_nav` `.nav` vector file.
* **[`mapGenericADCP`](mapGenericADCP.html)** (`code/adcp/mapGenericADCP.c`): Projects generic/EC150 `.N.r4`, `.E.r4`, `.D.r4` + `.nav` onto a 2D rotated OMG mapsheet (`-map`), outputting `.N.r4`, `.E.r4`, `.D.r4`, `.Mag.r4`, `.Azi.r4`, `.Rad.r4`, `.Tan.r4`, `.history`, and `.NED_av.txt`.

### 3. Multi-Cycle M2 Tidal Phase Binning & Tidal Ellipse Fitting
* **[`combineMultiADCP`](combineMultiADCP.html)** (`code/adcp/combineMultiADCP.c`): Bins depth-averaged `.nav` current vectors from multiple M2 tidal cycles ($12.42\text{ hours} = 360^\circ$) onto a spatial grid (`-grid`) across stepping phase windows (`.phase000`, `.phase020`, ...).
* **[`combineMultiADCP_wshiftoption`](combineMultiADCP_wshiftoption.html)** (`code/adcp/combineMultiADCP_wshiftoption.c`): Extends `combineMultiADCP` with `-tshift <sec>` and `-reftime <unix_sec>` controls for multi-survey tidal epoch synchronization.
* **[`combineMultiADCP_garret`](combineMultiADCP_garret.html)** (`code/adcp/combineMultiADCP_garret.c`): Bay of Fundy / Garrett variant of `combineMultiADCP`.
* **[`calc_ellipse`](calc_ellipse.html)** (`code/adcp/calc_ellipse.c`): Computes M2 tidal current ellipse parameters (semi-major axis $a$, semi-minor axis $b$, orientation $\theta$, ellipticity $e$, and mean residual flow $N_{av}, E_{av}$) per grid cell and outputs CSV tables plus `.phase###` vector files.
* **[`calc_ellipse1`](calc_ellipse1.html)** (`code/adcp/calc_ellipse1.c`): Computes M2 tidal current ellipses and writes binary `jcu_nav` vector files (`<prefix>_ellipse.nav` and `<prefix>_residual.nav`) for direct plotting in `jview`.
* **[`calc_ellipse2`](calc_ellipse2.html)** (`code/adcp/calc_ellipse2.c`): Enhanced M2 tidal ellipse and residual current calculator supporting both binary `_ellipse.nav` / `_residual.nav` outputs and optional `-ascii` CSV export.

### 4. Section Visualization & CTD Co-Registration
* **[`makeVectorPlot`](makeVectorPlot.html)** (`code/adcp/makeVectorPlot.c`): Converts distance-averaged `.r4` velocity profiles into 8-bit JHC vertical stick-vector plots.
* **[`makeTSmap`](makeTSmap.html)** (`code/adcp/makeTSmap.c`): Interpolates ASCII CTD profiles in depth and time onto an ADCP `.stack_prof` / `.stack_ASCII` grid to produce synchronized `.Tprof` (temperature) and `.Sprof` (salinity) rasters.
