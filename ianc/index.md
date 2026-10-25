---
layout: default
title: Ian Church — Hydrodynamic & 3D Ray-Trace Suite (ianc)
parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 6
has_children: true
category: Ocean Modeling & Hydrographic Utilities (ianc)
---

# Ian Church (`ianc`) Tools

## Overview

The `code/ianc/` directory contains hydrographic, physical oceanography, and hydrodynamic ocean-model integration software developed by **Ian Church** within the Ocean Mapping Group (OMG). Built atop the core OMG `libj` libraries (`jcu_nav.h`, `j_watercolumn.h`, `j_adcp.h`, `array.h`, `soundspeed.h`, `stdtime.h`, and `wgs.h`) as well as `libnetcdf` (with OPeNDAP/DAP client support) and `PROJ`, this suite bridges operational 3D hydrodynamic ocean models (FVCOM, NEGOFS, HYCOM, NRL CONCORDE) and in-situ oceanographic sensors (MVP `.m1` profilers, CARIS `.svp` casts, vessel-mounted RDI ADCPs, ISIIS towed vehicles, and GNSS `.pos`/`.nav` streams) with multibeam echosounder ray-tracing and uncertainty analysis.

---

## Command-Line Applications (`code/ianc/`)

### Hydrodynamic Ocean Model Integration & Synthetic SVP Extraction

| Tool | Source File | Description |
| :--- | :--- | :--- |
| [`modelAnalysis`](modelAnalysis.html) | `code/ianc/modelAnalysis.c` | Comprehensive FVCOM unstructured-grid NetCDF analysis suite: computes 3D Chen-Millero sound speed, validates model T/S/SVP and ADCP velocities against field observations, performs multibeam ray-tracing depth uncertainty analysis (`modelTT`, `depthWRefSVP`) against IHO standards, calculates cross-channel volume flux (total, salt, brackish, fresh), and exports GIS/ODV datasets. |
| [`modelMerge`](modelMerge.html) | `code/ianc/modelMerge.c` | Connects via OPeNDAP to operational ocean models (`-NEGOFS`, `-GOM_HYCOM_2014`, `-GOM_HYCOM_2015`, `-GOM_NRL_CONCORDE`) along a `.nav` track or time window to extract synthetic CARIS `.svp` casts, `.tid` tide files, grid geometries, and hybrid model-observation dynamic SVPs. |
| [`HycomSSP`](HycomSSP.html) | `code/ianc/HycomSSP.c` | Queries global or regional HYCOM OPeNDAP/NetCDF servers (`-modelPath`, e.g., `GLBv0.08`) with automatic connection retry and nearest-wet-node search (`-use_nearest`) to generate CARIS `.svp` profiles, `.tid` tides, `.nav` SSH records, surface current maxima (`-outVel`), and ODV spreadsheets. |

### Physical Oceanography, MVP & ADCP Water-Column Processing

| Tool | Source File | Description |
| :--- | :--- | :--- |
| [`oceanReader`](oceanReader.html) | `code/ianc/oceanReader.c` | Reads Moving Vessel Profiler (`.m1`) casts (CSL *Heron*, *Amundsen*, *Matthew*, *TAGS*, *Barge*), CARIS `.svp` files, ISIIS towed undulations, and RDI ADCP / WinADCP current profiles; corrects ADCP compass bias; bins profiles vertically; and computes EOS-80 density, density gradient, buoyancy frequency, optical backscatter, and Richardson, Froude, and Reynolds numbers. |

### Navigation & Raster Grid Utilities

| Tool | Source File | Description |
| :--- | :--- | :--- |
| [`Check_Nav`](Check_Nav.html) | `code/ianc/Check_Nav.c` | Inspects OMG/JHC binary navigation files (`.nav`), reporting record fields, geographic bounding boxes (`-minmax`), mean and standard deviation of azimuth/elevation (`-stdev`), time-of-day filtered records (`-time`), and Grace-compatible plotting tables (`-grace`). |
| [`POStoNav`](POStoNav.html) | `code/ianc/POStoNav.c` | Converts NRCan `GPSpace` ASCII PPP position files (`.pos`) into OMG binary `.nav` files (storing ellipsoidal height `HGT` in the `azi` field), with support for record decimation (`-skip`) and chronological reversal (`-flip`). |
| [`areaNavEdit`](areaNavEdit.html) | `code/ianc/areaNavEdit.c` | Flags navigation records in an OMG binary `.nav` file that fall outside a specified latitude/longitude bounding box (`-lat1`, `-lat2`, `-lon1`, `-lon2`) by setting `flag[3] = 1`. |
| [`calcArea`](calcArea.html) | `code/ianc/calcArea.c` | Calculates the valid surveyed area (in $\text{m}^2$, $\text{km}^2$, and percentage of bounding sheet) for one or more projected OMG `.r4` floating-point or `.8bit`/`.mos` raster map sheets. |
| [`checkEmpty`](checkEmpty.html) | `code/ianc/checkEmpty.c` | Fast shell utility that scans an OMG raster grid (`.r4`, `.8bit`, `.mos`, or 16-bit short) past the 1024-byte header and exits immediately upon finding the first non-empty pixel (`NotEmpty` = exit `1`, `Empty` = exit `0`). |

---

## Subroutine Library Modules (`code/ianc/subr/`)

The `code/ianc/subr/` directory builds `libiwc.a`, providing shared data structures, equations of state, binary format parsers, and spatial/statistical algorithms across the `ianc` applications:

| Module | Source & Header | Description |
| :--- | :--- | :--- |
| [`iwc_adcp`](iwc_adcp.html) | `code/ianc/subr/iwc_adcp.c`<br>`code/ianc/subr/iwc_adcp.h` | Provides `fixADCPBinVel()` to adjust ADCP bin velocity directions by an external compass heading bias (`azi_bias`) and recompute eastward and northward velocity components. |
| [`iwc_gwc`](iwc_gwc.html) | `code/ianc/subr/iwc_gwc.c`<br>`code/ianc/subr/iwc_gwc.h` | Complete binary reader and packet structure definitions (`GWC_FileHeader`, `GWC_WaterColumnPacket`, `GWC_Installation`, `GWC_SoundSpeed`, `GWC_Tide`, `GWC_NavInfo`) for Generic Water Column (`.gwc`) multibeam water-column files. |
| [`iwc_model`](iwc_model.html) | `code/ianc/subr/iwc_model.c`<br>`code/ianc/subr/iwc_model.h` | Defines OPeNDAP/THREDDS catalog and DODS endpoint macros (`NEGOFS`, `GOM2015`, `GOM2014`, `NRL_CONCORDE`) for operational hydrodynamic models. |
| [`iwc_support`](iwc_support.html) | `code/ianc/subr/iwc_support.c`<br>`code/ianc/subr/iwc_support.h` | General utility library providing 2D array allocation (`make2D*`, `convert2D`, `free2D*`), 1967 International Gravity Formula (`gravity`), descriptive and outlier statistics (`mean1`, `median1`, `standarddeviation1`, `rmse1`, `centralFreq`), and 1st/2nd/3rd/*N*-th nearest-neighbor spatial, temporal, and depth search routines (`closeDist*`, `closeTime`, `closeValue`, `closeXFloat`). |
| [`iwc_water`](iwc_water.html) | `code/ianc/subr/iwc_water.c`<br>`code/ianc/subr/iwc_water.h` | Defines `oceanObs` and `iwc_watercol` structures; implements UNESCO 1983 (EOS-80) seawater density (`density0`, `calcDensity`), buoyancy frequency (`calcBuoy`), Richardson number (`calcRichard`), Froude number (`calcFroude`), Reynolds number (`calcReynolds`), uniform depth binning (`binOceanObs`), and `jwc2iwc` / `iwc2jwc` conversions. |
| [`visit_writer`](visit_writer.html) | `code/ianc/subr/visit_writer.c`<br>`code/ianc/subr/visit_writer.h` | LLNL VisIt VTK Legacy (`# vtk DataFile Version 2.0`) mesh writer supporting point, unstructured, regular, rectilinear, and curvilinear 3D meshes in ASCII or big-endian binary format. |

---

## Typical End-to-End Workflows

1. **GNSS & Navigation Preparation**: Convert PPP `.pos` solutions to OMG binary `.nav` using [`POStoNav`](POStoNav.html), clip out-of-bounds turns or transits with [`areaNavEdit`](areaNavEdit.html), and verify timestamps, bounding coordinates, and vertical height statistics with [`Check_Nav`](Check_Nav.html).
2. **In-Situ MVP & ADCP Water-Column Analysis**: Process raw `.m1` MVP casts and `.adcp` ensembles with [`oceanReader`](oceanReader.html) (using [`iwc_water`](iwc_water.html) and [`iwc_adcp`](iwc_adcp.html)) to generate `.svp` casts, correct ADCP gyro bias from `.orientation` files, and compute stratification and turbulence metrics (`Ri`, `Fr`, `Re`, $N$) for Ocean Data View.
3. **Operational Model Assimilation & Uncertainty Evaluation**: Extract synthetic or model-dynamics-adjusted `.svp` and `.tid` files along the survey track from HYCOM, NEGOFS, or NRL CONCORDE using [`HycomSSP`](HycomSSP.html) or [`modelMerge`](modelMerge.html), or evaluate 3D FVCOM model skill and multibeam ray-tracing depth uncertainty against IHO standards using [`modelAnalysis`](modelAnalysis.html).
4. **Bathymetric Sheet Coverage Auditing**: Filter empty gridded tiles in batch scripts with [`checkEmpty`](checkEmpty.html) and compute total surveyed area in $\text{m}^2$ and $\text{km}^2$ with [`calcArea`](calcArea.html).
