---
layout: default
title: SE_global
parent: SwathEd (SE) Tools
nav_order: 24
tool_name: SE_global
source_path: code/SE/SE_global.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", ".param", ".watercol", ".WC_Phase1", ".waveform", ".sonar_settings", ".target"]
output_formats: []
related_tools: ["swathed", "SE_init_variables", "SE_mainwin", "SE_omgIOwin", "SE_GEOwindows"]
---

# `SE_global.c` & `SE_global.h` — Global Data Structures, Constants & Dynamic Memory Allocator

## Overview & Purpose
`SE_global.h` (originated by John E. Hughes Clarke, April 1999) and `SE_global.c` (added by Jonathan Beaudoin, May 2009) form the central state hub shared across all compilation units in `swathed` and its companion batch utilities (`newAutoRejectSoundings`).

Originally, `SE_global.h` declared large static arrays sized for `MAXFILES` (1,000 files) and `SE_NO_MAX` (1,024 beams) at compile time. In May 2009, `SE_global.c` introduced `allocate_global_memory()` to dynamically allocate these global arrays on the heap at runtime via `calloc()`, significantly reducing static BSS segment memory footprint while supporting up to 1,000 survey lines, 1,024 beams per ping, and 2,000 water-column sound velocity profiles.

---

## Core Constants & Macros (`SE_global.h`)

| Constant / Macro | Value | Description |
|---|---|---|
| `SE_NO_MAX` | `1024` | Maximum number of beams per ping (sized up to 1,024 to support high-density multibeam and GLORIA sidescan editing). |
| `SE_NO_SWATHS` | `100` | Number of consecutive swaths (pings) loaded into the main SwathEd editing buffer at a time. |
| `MAXFILES` | `1000` | Maximum number of `.merged` survey lines managed simultaneously in a SwathEd session. |
| `MAX_NUM_WATERCOLUMNS` | `2000` | Maximum number of Sound Velocity Profiles (`watercolumn` structs) loaded for raytracing in the Time Series tool. |
| `LINE_COLOUR(i)` | `(8 + i % 6)` | Maps survey line index `i` to a consistent X11 palette index across geographic, 2D, patch test, and line list windows. |
| `OMG_PORT` / `OMG_STBD` | `0` / `1` | Port and starboard transducer head identifiers. |
| `DEPTH`, `SUN`, `SUNDEPTH`, `SS_IMAGE` | `0..3` | Display colormap mode constants for DTM and sidescan background rendering. |
| `SD_DEFAULT`, `SD_MEAN` | `0`, `1` | Standard-deviation calculation mode constants (`SD_calc_method`). |

---

## Key Global Buffers & State Variables

### 1. The 100-Swath Working Matrices (`[SE_NO_MAX][SE_NO_SWATHS]`)
When [`SE_omgIOwin.c`](SE_omgIOwin.md) (`prime_array`) loads a 100-ping block starting at `in_recnum`, it populates the following core 2D arrays:
- `float box[SE_NO_MAX][SE_NO_SWATHS]`: Working beam depths (meters). **Sign convention:** positive values (`> 0.0`) represent valid unflagged soundings; negative values (`< 0.0`) represent flagged/rejected soundings; `0.0` indicates an empty/invalid beam slot.
- `float offsets[SE_NO_MAX][SE_NO_SWATHS]`: Across-track horizontal distances (meters, relative to the sonar transducer).
- `float rot_box[][]`, `rot_offsets[][]`: Slope-detrended depths and across-track offsets when `detrend_flag` is active.
- `float unrot_box[][]`, `unrot_offsets[][]`: Original un-detrended depths and offsets preserved during detrended viewing.
- `float median_box[][]`, `std_dev_box[][]`: Local median-filtered depths and standard deviations used by the median filter in [`SE_mainwin.c`](SE_mainwin.md).
- `unsigned char box_flags[SE_NO_MAX][SE_NO_SWATHS]`: 8-bit shift-register undo history per sounding (tracks the last 8 flagging/unflagging operations for `undo()`).
- `unsigned char box_status[SE_NO_MAX][SE_NO_SWATHS]`: Raw HDCS `beam.status` bitmask preserved from disk.
- `float qfactors[SE_NO_MAX][SE_NO_SWATHS]`: Ifremer quality factor (`beams[j].Ifremer_qfactor`) per sounding.

### 2. File Descriptors & Multi-Format Sonar Headers
- **Primary & Auxiliary Streams:** `infile` (`.merged`), `pingfile` (`.ss_data`), `pi16file` (`.16_data`), `pi32file` (`.32_data`), `piflfile` (`.fl_data`), `phasfile` (`.ph_data`), `ph16file` (`.ph16_data`), `glfile` (GLORIA), `WATERCOLUMNFILE` (`.watercol`), `WATERCOLUMNPHASEFILE` (`.WC_Phase1`), `WAVEFORMFILE` (`.waveform`), and `sonar_settings_file` (`.sonar_settings`).
- **HDCS & Vendor Structures:** `summary` (`OMG_HDCS_summary_header`), `profile` (`OMG_HDCS_profile_header`), `beams` (`OMG_HDCS_beam *`), `extra_summary`/`extra_profile`/`extra_beams` (for EM2040 `.extra` multi-detect files), `usl_summary`/`usl_profile`/`usl_beams` (legacy USL HDCS format), and vendor settings structures (`sonar_settings_7K`, `sonar_bathy_settings_R2Sonic`, `sonar_settings_MB1`, `sonar_settings_WASSP`).
- **Survey Line Management (`MAXFILES`):** `inname`, `supplyname`, `parameters` (`OMG_HDCS_sonar_params *`), `use`, `use_status`, `done_status`, `in_area`, `refrfile`, `target_list` (`OMG_Target_List *`), and random point bounds (`rbounds`, `rdm_count`, `rdmname`).

---

## Dynamic Memory Allocation (`allocate_global_memory`)

Defined in `SE_global.c` and called at the very start of `main()` in [`swathed.c`](swathed.md), `allocate_global_memory()` allocates:
1. **Per-Ping Beam Arrays (`SE_NO_MAX = 1024`):** `beams`, `extra_beams`, `usl_beams`, `prebeams`, `beam_variance`, `beam_qfactors`, `beam_depth`, `beam_offset`.
2. **Per-Swath Count Array (`SE_NO_SWATHS = 100`):** `loaded_beams`.
3. **Per-File Arrays (`MAXFILES = 1000`):** `parameters`, `use`, `use_status`, `done_status`, `in_area`, `rdm_count`, `rbounds`, `inname`, `supplyname`, `rdmname`, `supply_rdmname`, `refrfile`, `target_list`.
4. **Geographic Cleaned Sub-Image Tracking (`100`):** `subimage_bounds` (`window_param *`).
5. **Water Column Raytracing Profiles (`MAX_NUM_WATERCOLUMNS = 2000`):** `water_columns` and `svp_filenames`.

---

## Integration within `swathed`
- **Startup Initialization:** Immediately after `allocate_global_memory()` runs in `swathed.c`, [`SE_init_variables.c`](SE_init_variables.md) is `#include`d inline to assign default values to all variables declared in `SE_global.h`.
- **Cross-Module Coordination:** Every window module in `code/SE/` reads and updates `selected_swath`, `selected_beam`, `in_recnum`, `current_file`, and `box[][]` declared in `SE_global.h` to keep cursor highlighting and flagging synchronized across all open X11 windows.
