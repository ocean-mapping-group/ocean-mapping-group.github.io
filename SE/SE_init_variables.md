---
layout: default
title: SE_init_variables
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 25
tool_name: SE_init_variables
source_path: code/SE/SE_init_variables.c
category: Interactive QC & Editing (SwathEd)
input_formats: []
output_formats: []
related_tools:
- swathed
- SE_global
- SE_mainwin
- SE_2Dwindow
- SE_AUTOFLAGwin
- SE_PATCHwin
---

# `SE_init_variables.c` — Startup Default Initialization for SwathEd Subsystems

## Overview & Purpose
`SE_init_variables.c` is an inline initialization script (`#include "SE_init_variables.c"` inside `main()` of [`swathed.c`](swathed.html)) that sets deterministic startup defaults for all global state variables, UI labels, filter thresholds, and viewing geometry parameters across the entire `SwathEd` (`SE`) suite before command-line arguments are parsed.

Because `swathed` encompasses over a dozen interactive X11 windows—each with its own header file (`SE_2Dwindow.h`, `SE_AUTOFLAGwin.h`, `SE_BSwindow.h`, `SE_GEOwindows.h`, `SE_PATCHwin.h`, `SE_SUBBOTwin.h`, `SE_REFTOOLwin.h`, `SE_mainwin.h`, `SE_omgIOwin.h`, `SE_sswindow.h`, `SE_listwin.h`, `SE_filters.h`)—`SE_init_variables.c` centralizes their default configurations in one place, organized section-by-section by module header.

---

## Default Configuration by Module

### 1. 2D Sounding Scatterplot Window (`SE_2Dwindow.h`)

| Variable | Default Value | Meaning |
|---|---|---|
| `colour_scheme` | `BY_SWATH` | Color soundings by survey line (`LINE_COLOUR(i)`). |
| `show_type` | `D2_ALL_DETECTS` | Show both amplitude and phase bottom detections. |
| `show_flagged` | `0` | Hide already-flagged ("dirty") soundings on initial open to speed up redraws (added by J. Beaudoin, May 2013). |
| `D2tide_flag` | `1` | Apply tidal corrections by default in the 2D window. |
| `D2_dirn` | `SOUTH` | Default 2D profile viewing direction (looking South). |
| `obs_proc` / `D2_Sense` | `OBS` / `FLAG_2D` | Display observed depths; mouse rubber-band defaults to flagging mode. |
| `auto_flag_distance` | `5.0` | Default auto-flag threshold distance (meters) from the overlaid DTM. |

### 2. Automated Flagging Window (`SE_AUTOFLAGwin.h`)

| Variable | Default Value | Meaning |
|---|---|---|
| `spike_sense` | `UP_DOWN` | Detect both shoal (upward) and deep (downward) spikes. |
| `apply_to` | `AF_ALL_DETECTS` | Apply auto-flagging to both amplitude and phase detections (`"Amp/Phase"`). |
| `ACROSS_twoslopelimit` | `25.0` | Across-track two-slope spike threshold ($25^\circ$). |
| `ALONG_twoslopelimit` | `25.0` | Along-track two-slope spike threshold ($25^\circ$). |
| `use_ACROSS_two`, `use_ALONG_two` | `1`, `1` | Enable both across-track and along-track two-slope tests. |
| `use_FOREAFT`, `use_LEFTRIGHT` | `1`, `1` | Enable fore-aft and left-right isolated sounding gap tests. |
| `label_*` arrays | `mem_strcpy(...)` | Initializes button label strings (`"Unflag OFF"`, `"1-Pass".."5-Pass"`, `"Any 2 OFF"`, etc.). |

### 3. Backscatter & Geographic Windows (`SE_BSwindow.h`, `SE_GEOwindows.h`)
- **Backscatter (`SE_BSwindow.h`):** Sets `detect_choice = BS_ALL_DETECTS`, `draft = 2.5` m, `flat_seafloor = 1`, `Atten_Gain = 0.0`, and disables `BS_flag`, `use_bs_flag`, `fullss_flag`, `use_asph`, `corr_inson`, and `use_refract`.
- **Geographic Locator (`SE_GEOwindows.h`):** Initializes `dot_size = 1`, `skip_pingnav = 10` (plots navigation fix every 10 pings), and zeroes all overlay flags (`locate_flag`, `locr4_flag`, `ss_flag`, `target_flag`, `tgt_flag`, `vectbin_flag`, `boxes_flag`, `use_nmap`).

### 4. Patch Test, Sub-Bottom & Refraction Tools (`SE_PATCHwin.h`, `SE_SUBBOTwin.h`, `SE_REFTOOLwin.h`)
- **Patch Test (`SE_PATCHwin.h`):** Zeroes calibration offsets (`roll_offset = 0.0`, `pitch_offset = 0.0`, `gyro_offset = 0.0`, `time_delay = 0.0`, lever arms `X/Y/Z_tran_ant = 0.0`), sets `PATCH_draft = 2.5` m, `PATCH_dirn = P_SOUTH`, `PATCHobs_proc = P_OBS`, and `show_patch_bin = 0`.
- **Sub-Bottom (`SE_SUBBOTwin.h`):** Sets window index offset `SUBBOT_OFFSET = 100` and `SUBBOT_flag = 0`.
- **Refraction Tool (`SE_REFTOOLwin.h`):** Sets `array_type = HORIZ_LINE`, `REF_OFFSET = 62`, 3D perspective parameters (`azi = 270.0°`, `elev = 35.0°`, vertical exaggeration `exag = 3.0`), and palette range (`colormap_flag = SUN`, `mincol = 0`, `maxcol = 255`).

### 5. Main Editor, I/O, Filters & Water Column (`SE_mainwin.h`, `SE_omgIOwin.h`, `SE_filters.h`)

| Variable | Default Value | Meaning |
|---|---|---|
| `speed_knts` / `ping_int` / `coverage` | `8.0` / `4.0` / `URI_COV (1.5)` | Default vessel speed, ping interval, and swath width-to-depth coverage ratio. |
| `ampl_flag`, `plan_flag`, `vrus_flag`, `unlasso_flag` | `1` | Enable all four toggleable sub-panes in the main SwathEd window on startup. |
| `detrench_port_sector` / `detrench_stbd_sector` | `20` / `-20` | Default angular sector bounds ($\pm 20^\circ$) for `detrench()` in [`SE_filters.c`](SE_filters.html). |
| `Shoallest_Allowed` / `Deepest_Allowed` | `0.0` / `12000000.0` | Default depth gate bounds in millimeters ($0\text{ m}$ to $12,000\text{ m}$). |
| `SDmultiplier` | `3.0` | Default $3\sigma$ standard-deviation multiplier for `trim_by_SD()`, `detrench()`, and `depowell()`. |
| `median_filter_threshold` / `median_filter_size` | `200` / `3` | Default median filter threshold ($2.00\%$ of water depth) and $3 \times 3$ window size. |
| `raytrace_method` / `wc_binsize` | `CONST_LAYERS` / `0.5` | Default water-column raytracing method and depth bin size ($0.5\text{ m}$), plus calls `jWC_init(&this_watercolumn)` and `init_sounding_geometry(&sounding)`. |
| `Ship_3D_LOA` | `100.0` | Default 3D vessel model Length Overall ($100\text{ m}$) for [`SE_3D.c`](SE_3D.html). |

---

## Integration within `swathed`
In [`swathed.c`](swathed.html), `SE_init_variables.c` is included immediately after `allocate_global_memory()` and `allocate_mainwin_memory()`, and right before the `while (*(++argv))` command-line parser. Any command-line flags (such as `-Allowed`, `-detrend_2D`, `-pre_defluff`, `-pre_detrench`, `-ship_LOA`, or `-ABS`) then override these baseline values prior to X11 window creation.
