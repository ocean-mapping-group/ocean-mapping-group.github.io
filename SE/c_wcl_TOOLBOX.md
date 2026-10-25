---
layout: default
title: c_wcl_TOOLBOX
parent: SwathEd (SE) Tools
nav_order: 32
tool_name: c_wcl_TOOLBOX
source_path: code/SE/c_wcl_TOOLBOX.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", ".watercol", ".tgtShape", ".target"]
output_formats: [".target"]
related_tools: ["swathed", "SE_WaterColumn", "SE_3D", "SE_GEOwindows"]
---

# `c_wcl_TOOLBOX.c` — Interactive Water Column 3D Target Detection & Hunting Toolbox

## Overview & Purpose
`c_wcl_TOOLBOX.c` and `c_wcl_TOOLBOX.h` (authored by Carlos Marques, February 2012) implement the interactive **"Target Detection Tools"** X11 widget (`target_widget`) integrated into the 2D Water Column viewer ([`SE_WaterColumn.c`](SE_WaterColumn.md)) of `swathed`.

Designed for automated and semi-automated detection of mid-water acoustic targets (such as gas seeps, fish shoals, wrecks, mast/buoy moorings, and hydrographic Least Depth targets) across 3D water-column volumes (`samples` $\times$ `beams` $\times$ `pings`), `c_wcl_TOOLBOX.c` provides an interactive GUI wrapping the underlying `c_wcpick.h` target-hunting and beam-pattern modeling routines (`c_hunt_for_detections`, `c_hunt_for_targets`, `c_mark_targets`, `c_loadWclSpecs`). Detected targets are stored in the global `OMG_Target_List` (`target_list`) so they can be simultaneously visualized in 2D water-column fans, the geographic map window ([`SE_GEOwindows.c`](SE_GEOwindows.md)), and the 3D OpenGL viewer ([`SE_3D.c`](SE_3D.md)), and saved to `<prefix>.target` files.

---

## X11 Widget Architecture (`make_c_WCLtoolbox_widget`)

`make_c_WCLtoolbox_widget()` configures `target_widget` (`jX_widget_params`) with **14 interactive sliders**, **11 action buttons**, and **2 graphic display panels** stacked vertically (`JX_STACK_VERT`):

### 1. Interactive Sliders (`target_widget.slider[0..13]`)

| Slider # | Label | Bound Variable | Purpose |
|---|---|---|---|
| `0` | `Static Threshold` | `tgtTBox_Threshold` (`float`) | Minimum amplitude threshold (dB) for water-column target detection (`C_RESET_THRESHOLD` to `C_MAXAMPLITUDE`). |
| `1` | `Samples Cube size` | `tgtTBox_samplesSize` (`int`) | 3D detection kernel size along the range/sample time series axis (`0 .. C_MAXTARGETSIZE`). |
| `2` | `Beams Cube size` | `tgtTBox_beamsSize` (`int`) | 3D detection kernel size across adjacent receive beams (`0 .. C_MAXTARGETSIZE`). |
| `3` | `Pings Cube size` | `tgtTBox_swathsSize` (`int`) | 3D detection kernel size along-track across consecutive swaths/pings (`0 .. C_MAXTARGETSIZE`). |
| `4` | `Block Time Series Pattern` | `tgtTBox_samplesLeak` (`int`) | Number of range samples blanked around a detection to suppress transmit pulse-length leakage (`0 .. C_MAXLEAK`). |
| `5` | `Block Angle Series Pattern` | `tgtTBox_beamsLeak` (`int`) | Number of adjacent beams blanked around a detection to suppress receive beamwidth / sidelobe leakage (`0 .. C_MAXLEAK`). |
| `6` | `Block Swath Series Pattern` | `tgtTBox_swathsLeak` (`int`) | Number of consecutive pings blanked around a detection to suppress along-track transmit beamwidth leakage (`0 .. C_MAXLEAK`). |
| `7` | `Use Sector (need button)` | `tgtTBox_maxSwaths` (`int`) | Selects a transmit sector index (`0 .. c_wcs_nSectors`) to insert into the sector search queue via Button `6`. |
| `8` & `9` | `Start Sample` / `Stop Sample` | `tgtTBox_minSamples` / `maxSamples` | Constrains the water-column range sample search window (`[tgtTBox_minSample, tgtTBox_maxSample]`). |
| `10` & `11` | `Start Beam` / `Stop Beam` | `tgtTBox_minBeams` / `maxBeams` | Constrains the receive beam search window (`[tgtTBox_minBeam, tgtTBox_maxBeam]`). |
| `12` & `13` | `Start Swath` / `Stop Swath` | `tgtTBox_minSwaths` / `maxSwaths` | Constrains the along-track swath search window (`[tgtTBox_minSwath, tgtTBox_maxSwath]`). |

### 2. Action Buttons (`target_widget.button_labels[0..10]`)

| Button # | Label | Underlying Action |
|---|---|---|
| `0` | `Get Detections` | Calls `c_hunt_for_detections()` over the configured 3D search volume and plots the applied per-swath dB threshold curve in Graphic `0`. |
| `1` | `Get Targets` | Calls `c_hunt_for_targets()` (using a `.tgtShape` target definition file) to classify and extract multi-detection targets. |
| `2` | `Mark All Targets` | Calls `c_mark_targets()` to group existing point detections in `c_SE_targetList` into targets using a `.tgtShape` file. |
| `3` | `Del Detections` | Calls `c_excludeDetections(c_SE_targetList, 0)` to clear all auto-detected points from the target list. |
| `4` | `Del Targets` | Calls `c_excludeTargets(c_SE_targetList, 0)` to clear all auto-marked targets from the target list. |
| `5` | `Use Single Swath` / `Use Multi Swath` | Toggles `c_user_multipleswath` between 3D multi-swath hunting and 2D single-swath hunting. |
| `6` | `Insert Sector` | Adds the transmit sector selected on Slider `7` to `c_user_sectors[]` queue for sector-specific target hunting. |
| `7` | `Reset Sectors` | Clears `c_user_sectors[]` (`c_user_nsectors = 0`) and restores automatic all-sector search. |
| `8` | `Show Search Area` / `Hide Search Area` | Toggles `tgtTBox_DrawBoundaries` to overlay the `[minSample..maxSample, minBeam..maxBeam]` bounding box on the 2D Water Column fan in [`SE_WaterColumn.c`](SE_WaterColumn.md). |
| `9` | `Store Tgt List` | Calls `write_OMG_Target_List(&c_SE_targetList[current_file])` to save detected targets to disk. |
| `10` | `Show wcl BP` / `Hide wcl BP` | Toggles `tgtTBox_ShowBP` and runs `c_loadWclSpecs()` to compute and overlay theoretical 2D transmit/receive beam-pattern sidelobe arcs at the selected beam and range sample. |

---

## Key Functions

| Function | Signature | Description |
|---|---|---|
| `set_target_widget_variables` | `int set_target_widget_variables(...)` | Binds pointers to the loaded 100-ping `j_EM_watercolumn` array (`c_wcs`), `OMG_Target_List` (`c_SE_targetList`), `WC_profileHead`, `geo_cen`, `heading`, and `pingtime`, scans the maximum sectors/beams/samples, updates slider upper bounds, and calls `c_resetUserVars()`. |
| `make_c_WCLtoolbox_widget` | `void make_c_WCLtoolbox_widget()` | Initializes all 14 sliders, 11 buttons, and 2 graphic windows and calls `jX_setup_widget(&target_widget)`. |
| `manage_target_widget_events` | `int manage_target_widget_events(XEvent event)` | Handles X11 `Expose`, `EnterNotify`/`LeaveNotify` (displaying context-sensitive hover help `c_buttonHelp[i]` in Graphic `1`), `ButtonPress`, and `KeyPress` (Left/Right/Up arrow keys for fine slider adjustment). |
| `refresh_target_widget_window` | `void refresh_target_widget_window(Window window)` | Redraws buttons, dynamically constrained sliders, the applied dB threshold plot (`draw_Threshold` in Graphic `0`), and the status/help banner (`draw_Info` / `draw_Help` in Graphic `1`). |
| `set_drawVars` | `int set_drawVars()` | Synchronizes `tgtTBox_min/maxSample`, `Beam`, and `Swath` from the sliders and calls `draw_WaterColumn(selected_swath, selected_beam)` to live-update the search boundary overlay. |
