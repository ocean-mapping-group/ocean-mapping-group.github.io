---
layout: default
title: SE_PATCHwin
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 11
tool_name: SE_PATCHwin
source_path: code/SE/SE_PATCHwin.c
category: Interactive QC & Editing (SwathEd)
input_formats:
- .merged
- .merged.100_ping_bounds
- .r4
- .lph
- .rtk
output_formats:
- PATCH.plot
- patch_XXXX.ppm
related_tools:
- swathed
- SE_GEOwindows
- SE_2Dwindow
- SE_LineListwin
- newMergeAtt
---

# `SE_PATCHwin` — Interactive Multibeam Patch Test & Lever-Arm Calibration Toolkit

`SE_PATCHwin` (`code/SE/SE_PATCHwin.c`, `code/SE/SE_PATCHwin.h`) implements the `"PATCH TEST ToolKit"` (`sub_window[43..54]`) in [`swathed`](swathed.html). Authored by John E. Hughes Clarke (April/July 1999) with automated solver and dual-head extensions by Jonathan Beaudoin (2012), it provides an interactive 3D ray/lever-arm recalculation engine for calibrating multibeam angular mounting alignments (**Roll**, **Pitch**, **Gyro/Heading**), positioning **Time Delay** (latency), and GPS/motion sensor **Transducer-to-Antenna Lever Arms** ($\Delta X, \Delta Y, \Delta Z$).

---

## Window Architecture & Controls (`sub_window[43..54]`)

Clicking the **`Patch`** icon (`icon_window[11]`) while a geographic `sub_area` (`sub_window[2]`) is active calls `view_PATCHbox()`, creating top-level form `sub_window[43]` (`650 × 450` px) and 11 child windows:

| Window | Role / Label | Description |
| :--- | :--- | :--- |
| `sub_window[44]` | **Main Profile Plot** | `640 × 320` px cross-section plotting soundings falling inside the rotatable geographic corridor (`Ecen`, `Ncen`, `rect_width`, `rect_height`, `rect_angle`), color-coded by survey line (`LINE_COLOUR(file)`). |
| `sub_window[45]` | `SOUTH` / `NORTH` / `EAST` / `WEST` | Cycles viewing projection direction (`view_dir`) relative to the corridor axis. |
| `sub_window[46]` | `NOTIDE` / `TIDE` / `dedrift` / `lpf.RTK` / `raw.RTK` / `bln.RTK` | Cycles vertical datum reduction (`apply_tide_flag` / `use_AltHeave_flag`) across unreduced, predicted tide, long-period heave (`.lph`), and RTK GPS antenna height modes. |
| `sub_window[47]` | `OBS.` / `PROC.` | Toggles between raw observed depths and processed depths (`obs_flag`). |
| `sub_window[48]` | `PRINT` | Calls `print_PATCH()` to export all projected corridor profiles to an ASCII file `PATCH.plot`. |
| `sub_window[49]` | **2D Lever-Arm Graphic** | Interactive ship plan-view diagram (`-20` to `+20` m) showing the horizontal offset (`X_tran_ant`, `Y_tran_ant`) between the transducer and GPS antenna (`Z_tran_ant` adjusted via mouse clicks). |
| `sub_window[50]` | `roll_offset` Slider | Interactive slider (`-5.0°` to `+5.0°`, step tunable) for transducer roll alignment bias. |
| `sub_window[51]` | `pitch_offset` Slider | Interactive slider (`-5.0°` to `+5.0°`) for transducer pitch alignment bias. |
| `sub_window[52]` | `gyro_offset` Slider | Interactive slider (`-5.0°` to `+5.0°`) for heading/yaw alignment bias. |
| `sub_window[53]` | `time_delay` Slider | Interactive slider (`-5.0` to `+5.0` s) for positioning latency relative to sonar ping time. |
| `sub_window[54]` | `Re-Calculate` Button | Triggers `recalculate_beam_locations()` and redraws `sub_window[44]`. |

---

## Core Algorithms & Calibration Mathematics

### 1. Spatial Corridor Extraction (`get_Swaths_inarea`)
`get_Swaths_inarea(left, right, bottom, top)` queries `.100ping_bounds` for all active survey lines (`use_status[i] == 1`) and loads up to `MAX_PATCH_SWATHS` (`3000`) full swaths (`PATCH_profile[]`, `PATCH_beams[][]`) into memory. It also loads auxiliary delayed-heave (`.lph`) and RTK (`.rtk`) time series if present (`got_lph`, `got_rtk`).

### 2. Full 3D Rigid-Body & Ray Recalculation (`recalculate_beam_locations`)
Whenever an alignment slider or lever arm is adjusted, `recalculate_beam_locations()` recomputes every sounding's 3D position from raw observations:
1. **Positioning Latency Interpolation:** Interpolates ship navigation (`PATCH_nav_east`, `PATCH_nav_north`) at `ping_time + time_delay` between adjacent swaths.
2. **Transducer-to-Antenna Lever Arm:** Applies the 3D rotation matrix (`rotate()` from `DCM_rthand.h`) using instantaneous `roll`, `pitch`, and `heading + gyro_offset` to project the lever arm (`X_tran_ant`, `Y_tran_ant`, `Z_tran_ant`) into local Easting, Northing, and vertical heave/RTK offsets.
3. **Inverse & Forward Ray Rotation:** Unrotates each beam's across-track, along-track, and depth vector (`unrotate()`) using the original recorded roll/pitch/heading, adds `roll_offset`, `pitch_offset`, and `gyro_offset` (supporting independent port/starboard head application via `side_apply_to`: `BOTH_SIDES`, `PORT_SIDES`, `STBD_SIDES` for dual-head EM3000D/EM2040D/Submetrix sonars), and forward-rotates (`rotate()`) back into earth coordinates.

### 3. Automated Minimum-Dispersion Solver (`auto_solve`)
Implemented by Jonathan Beaudoin, pressing `s` (coarse) or `S` (fine) while hovering over slider `50` (Roll), `51` (Pitch), `52` (Yaw), or `53` (Time Delay) runs `auto_solve(parameter_to_solve, solve_resolution)`:
* Sweeps the selected calibration parameter across its search window, projects all corridor soundings into `PATCH_NUM_BINS` (`50`) horizontal spatial bins across `sub_window[44]`, and minimizes the mean vertical dynamic range $\frac{1}{N}\sum (\max z_b - \min z_b)$ across bins containing at least 5 soundings.

---

## Keyboard Shortcuts in `sub_window[44]` & Sliders

* **Left-click / Right-click in `sub_window[44]`:** Sets minimum (`y_min`) / maximum (`y_max`) depth bounds of the profile plot.
* **`p` / `s` / `b` in `sub_window[44]`:** Applies calibration offsets to Port head only (`PORT_SIDES`), Starboard head only (`STBD_SIDES`), or Both heads (`BOTH_SIDES`) and recalculates.
* **`P` / `S` / `B` in `sub_window[44]`:** Displays only Port beams, only Starboard beams, or Both sides (`SE_PT_side_show`).
* **`s` / `S` in `sub_window[50..53]`:** Runs automated coarse (`PATCH_COARSE_SOLVE`) or fine (`PATCH_FINE_SOLVE`) optimization for Roll (`50`), Pitch (`51`), Yaw (`52`), or Latency (`53`).
* **`r` in `sub_window[44]`:** Toggles `PATCH_Record` to export sequential PPM screenshots (`patch_0000.ppm`...) via `SEPATCH_dump_window()` on every recalculation.
