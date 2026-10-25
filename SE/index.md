---
layout: default
title: SwathEd (SE) Tools
nav_order: 20
has_children: true
---

# SwathEd (`SE`) Suite — Interactive Multibeam QC, Water Column & Calibration Tools

The `code/SE/` directory contains **`swathed`** (the Ocean Mapping Group's flagship interactive X-Windows / OpenGL multibeam sonar editor, continuously developed by John E. Hughes Clarke and collaborators since 1990), three standalone batch command-line utilities (`applyBDI`, `fix_TimeSeries`, `newAutoRejectSoundings`), and 31 modular GUI window, I/O, and acoustic signal-processing components.

---

## 1. Main Interactive Application & Standalone CLI Utilities

| Tool | Source File | Description |
|---|---|---|
| [`swathed`](swathed.md) | `code/SE/swathed.c` | Flagship interactive X11/OpenGL multibeam sounding editor, live DTM cleaner (`-locate`), 2D/3D water column viewer (`-show_WC2D`, `-show_WC3D`), patch test calibrator, refraction editor, and motion time-series analyzer (`-ts`). |
| [`applyBDI`](applyBDI.md) | `code/SE/applyBDI.c` | Standalone batch CLI tool that runs the Beam-Direction Indicator (BDI) constant-TWTT parabolic peak-picking algorithm across `.watercol` files, outputs `.merged_BDI` or full raytraced `newMergeAtt` swaths. |
| [`fix_TimeSeries`](fix_TimeSeries.md) | `code/SE/fix_TimeSeries.c` | Standalone batch CLI processor that applies motion sensor latency, RC filter lag, amplitude scale, lever-arm, yaw misalignment, surface sound speed, and cosine-tapered long-period heave drift (`-heave_drift`) corrections diagnosed in `SE_W_TimeSeries`. |
| [`newAutoRejectSoundings`](newAutoRejectSoundings.md) | `code/SE/newAutoRejectSoundings.c` | Standalone batch CLI outlier rejector that applies a saved `swathed` Auto-Flag criteria file (`-criteria`) across multiple `.merged` survey lines in 100-ping overlapping blocks. |

---

## 2. Core SwathEd Architecture, I/O & Event Loop Modules

| Module | Source File | Description |
|---|---|---|
| [`SE_global`](SE_global.md) | `code/SE/SE_global.c`, `.h` | Central state definitions (`box[1024][100]`, `offsets[1024][100]`, file handles, HDCS headers) and runtime heap allocator (`allocate_global_memory`). |
| [`SE_init_variables`](SE_init_variables.md) | `code/SE/SE_init_variables.c` | Startup initialization script setting deterministic defaults for all SwathEd windows, filters, and viewing parameters prior to CLI parsing. |
| [`SE_mainwin`](SE_mainwin.md) | `code/SE/SE_mainwin.c`, `.h` | Core 8-pane 100-ping swath profile and along-track beam editor (`graphic_window[0..7]`), rubber-band flagging, 8-level bitwise undo, IHO/QMS/SD statistical trimming, median filtering, and Gasser-Sroka beam variance estimation. |
| [`SE_omgIOwin`](SE_omgIOwin.md) | `code/SE/SE_omgIOwin.c`, `.h` | Multibeam file I/O engine (`start_file`, `prime_array`, `dump_array`), companion file loader (`.orientation`, `.sectors`, `.watercol`, `.WC_Phase1`, `.ss_data`, `.flag_bk`), and least-squares planar slope detrending (`calc_Detrend_Slopes`). |
| [`SE_event_loop`](SE_event_loop.md) | `code/SE/SE_event_loop.c`, `.h` | Master X11 event dispatcher routing mouse, rubber-band, slider, button, and keyboard shortcut events across all active SwathEd windows. |
| [`SE_TOOLBOXwin`](SE_TOOLBOXwin.md) | `code/SE/SE_TOOLBOXwin.c`, `.h` | Master SwathEd control toolbox window managing sub-window launch buttons, colormap selectors, and display toggles. |
| [`SE_listwin`](SE_listwin.md) | `code/SE/SE_listwin.c`, `.h` | Interactive `"Beam Listing"` window (`sub_window[14]`) decoding ping navigation/attitude, vendor-specific sonar settings, Kongsberg filter bits, and a 3-page tabular beam inspector (`ping_list.data` export). |
| [`SE_generic`](SE_generic.md) | `code/SE/SE_generic.c`, `.h` | Boilerplate C/H template stub used for creating new modular SwathEd extensions. |

---

## 3. Geographic Area Cleaning, Patch Testing & Filtering Modules

| Module | Source File | Description |
|---|---|---|
| [`SE_GEOwindows`](SE_GEOwindows.md) | `code/SE/SE_GEOwindows.c`, `.h` | Geographic locator map window (`-locate`), live `.r4` / `.r4_weights` DTM dynamic re-gridding as outliers are flagged, and rubber-band sub-area selection. |
| [`SE_LineListwin`](SE_LineListwin.md) | `code/SE/SE_LineListwin.c`, `.h` | Survey line list manager window (`sub_window[58]`) for toggling active lines, highlighting tracks, and tracking cleaned status across multi-line projects. |
| [`SE_2Dwindow`](SE_2Dwindow.md) | `code/SE/SE_2Dwindow.c`, `.h` | Rotatable 2D geographic sub-area sounding scatterplot (`sub_window[23]`), DTM profile overlay, IHO bars, and multi-line outlier editing (`dump_back_out_2D`). |
| [`SE_PATCHwin`](SE_PATCHwin.md) | `code/SE/SE_PATCHwin.c`, `.h` | Interactive multibeam patch test calibration toolkit for roll, pitch, heading (gyro), latency, and lever-arm offset determination. |
| [`SE_AUTOFLAGwin`](SE_AUTOFLAGwin.md) | `code/SE/SE_AUTOFLAGwin.c`, `.h` | Interactive Auto-Flag configuration GUI (`sub_window[18..21, 55..56]`) and two-slope / isolated-neighbor outlier detection engine (`check_data`). |
| [`SE_filters`](SE_filters.md) | `code/SE/SE_filters.c`, `.h` | Specialized bathymetric artifact filters: Kongsberg sector-boundary trench removal (`detrench`), modal depth estimation (`get_mode`), steep canyon-wall filtering (`depowell`), and isolated sounding removal (`filter_lonely_soundings`). |
| [`SE_Weekley_Goodrich_Cornman`](SE_Weekley_Goodrich_Cornman.md) | `code/SE/SE_Weekley_Goodrich_Cornman.c`, `.h` | Weekley-Goodrich-Cornman fuzzy-logic / statistical swath outlier filter and diagnostic window (`sub_window[60]`). |

---

## 4. Water Column (2D/3D), BDI/PDI Bottom Detection & Target Hunting

| Module | Source File | Description |
|---|---|---|
| [`SE_WaterColumn`](SE_WaterColumn.md) | `code/SE/SE_WaterColumn.c`, `.h` | Interactive 2D water-column polar wedge ("pie"), beam-trace, and constant-time-slice viewer (`-show_WC2D`) for `.watercol` and `.WC_Phase1` data. |
| [`SE_3D`](SE_3D.md) | `code/SE/SE_3D.c`, `.h` | Interactive 3D OpenGL viewer (`-show_WC3D`) rendering 3D acoustic beam cones, water-column scatterers, seafloor mesh, DTM surfaces, targets, and 3D vessel attitude model. |
| [`SE_BDI_DP`](SE_BDI_DP.md) | `code/SE/SE_BDI_DP.c`, `.h` | Interactive Beam-Direction Indicator (BDI) analysis widget for tuning constant-TWTT across-beam amplitude peak picking on steep and complex seafloors. |
| [`bdi_funcs`](bdi_funcs.md) | `code/SE/bdi_funcs.c`, `.h` | Standalone 5-stage BDI peak-picking, $R_0$ detection, 3/5-point parabolic interpolation, footprint filtering, and virtual-beam compression library. |
| [`SE_PDI_LA`](SE_PDI_LA.md) | `code/SE/SE_PDI_LA.c`, `.h` | Interactive Phase-Direction Indicator (PDI) analysis widget for constant-TWTT across-beam split-beam phase zero-crossing bottom detection. |
| [`pdi_funcs`](pdi_funcs.md) | `code/SE/pdi_funcs.c`, `.h` | Standalone PDI zero-crossing phase interpolation algorithm (`after_BDI_PDI_pick_Angle_Peaks`) operating on `.WC_Phase1` split-beam phase fans. |
| [`c_wcl_TOOLBOX`](c_wcl_TOOLBOX.md) | `code/SE/c_wcl_TOOLBOX.c`, `.h` | Interactive 3D water-column Target Detection & Hunting toolbox widget (`target_widget`) with 14 sliders for cube size, sidelobe leakage blanking, sector queuing, and beam-pattern overlay. |
| [`SE_PhaseBathy`](SE_PhaseBathy.md) | `code/SE/SE_PhaseBathy.c`, `.h` | Interactive interferometric / split-beam phase bathymetry ramp and bottom-detection analyzer. |
| [`SE_Waveforms`](SE_Waveforms.md) | `code/SE/SE_Waveforms.c`, `.h` | Interactive bathymetric LiDAR (Optech SHOALS) and acoustic full-waveform (`<prefix>.waveform`) viewer. |

---

## 5. Refraction, Motion Time Series, Backscatter & Sub-Bottom Modules

| Module | Source File | Description |
|---|---|---|
| [`SE_REFTOOLwin`](SE_REFTOOLwin.md) | `code/SE/SE_REFTOOLwin.c`, `.h` | Interactive sound speed profile (SVP) and surface sound speed refraction correction toolkit (`sub_window[REF_OFFSET + 1..12]`, `.ref_coeffs`). |
| [`SE_W_TimeSeries`](SE_W_TimeSeries.md) | `code/SE/SE_W_TimeSeries.c`, `.h` | Interactive attitude and motion-residual time-series analyzer (`-ts`) for diagnosing roll/pitch/heave latency, filter phase lag, scaling, lever-arm, yaw, and long-period heave drift. |
| [`SE_sswindow`](SE_sswindow.md) | `code/SE/SE_sswindow.c`, `.h` | Interactive raw sidescan, snippet trace, slant-range, and interferometric phase viewer (`sub_window[13, 15, 16]`) with an 80-ping waterfall strip. |
| [`SE_BSwindow`](SE_BSwindow.md) | `code/SE/SE_BSwindow.c`, `.h` | Interactive multibeam backscatter angular response, grazing angle, and TVG / ensonified area analyzer (`sub_window[36]`). |
| [`SE_AnandBS`](SE_AnandBS.md) | `code/SE/SE_AnandBS.c`, `.h` | Anand's multi-sector Backscatter & Angular Response Curve (ARC) calibration toolkit (`-ABS`), computing de-TVG backscatter, Bottom Target Strength (BTS), and sector-by-sector VRA/GRA/SRA response curves. |
| [`SE_SUBBOTwin`](SE_SUBBOTwin.md) | `code/SE/SE_SUBBOTwin.c`, `.h` | Interactive sub-bottom profiler and low-frequency nadir trace viewer (`sub_window[SUBBOT_OFFSET + ...]`). |
