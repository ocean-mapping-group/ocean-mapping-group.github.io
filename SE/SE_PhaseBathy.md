---
layout: default
title: SE_PhaseBathy
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 13
tool_name: SE_PhaseBathy
source_path: code/SE/SE_PhaseBathy.c
category: Interactive QC & Editing (SwathEd)
input_formats:
- .merged
- .raw_ping
- .raw_phas
output_formats:
- .merged (updated in-memory soundings)
related_tools:
- swathed
- SE_sswindow
- SE_WaterColumn
---

# `SE_PhaseBathy` — Interferometric / Phase-Differencing Bathymetry Analysis Toolkit

`SE_PhaseBathy` (`code/SE/SE_PhaseBathy.c`, `code/SE/SE_PhaseBathy.h`) implements the `"PhaseBathy Analysis Toolkit"` (`PhaseBathy_widget`) in [`swathed`](swathed.html). Authored by John E. Hughes Clarke (December 2007), it provides an interactive X11 workbench for inspecting and re-solving raw multi-baseline interferometric / phase-differencing sidescan sonar data—specifically SEA SWATHplus / Submetrix 2000 systems (`SEA_SwathPlus`, defined in `j_SUB2K.h`).

When clicking the **`ss`** icon (`icon_window[7]`) on a `SEA_SwathPlus` dataset, `swathed` opens `PhaseBathy_widget` to display raw 16-bit port/starboard amplitude traces (`pingfile`) and 8-bit 3-baseline differential phase traces (`AB`, `AC`, `AD` in `phasfile`), allowing interactive Vernier phase unwrapping, amplitude/quality gating, and sounding regeneration.

---

## Architecture & X11 Widget Layout

`make_PhaseBathy_widget()` configures `PhaseBathy_widget` (`jX_widget`) with **5 stacked 800-pixel-wide graphics canvases**, **7 parameter sliders**, and **8 control buttons**:

### 5 Stacked Graphics Canvases
1. **Graphic 0 (`draw_PhaseBathy`, 800×250 px — Across-Track Polar Cross-Section):**
   * Plots across-track distance (`-PB_max_across_m` to `+PB_max_across_m`) vs. depth (`0` to `-WaterDepth * PB_WD_multiple`).
   * Renders constant-range arcs (`CYAN`), gated raw Vernier phase angle trajectories (`GREEN` when `show_RAW_PHASE` is active), accepted interferometric sounding solutions (`YELLOW` crosses when `show_SOLUTIONS` is active), or a 2D spatial density grid (`show_DENSITY`), plus min/max range gates (`show_GATES`).
2. **Graphic 1 (`draw_PB_Intensity`, 800×125 px — Port/Starboard Amplitude Trace):**
   * Plots raw 16-bit linear or log-scaled (`PB_linear`) port (left of center) and starboard (right of center) amplitude time series (`PB_trace_16[][2][]`), overlaid with the 8-bit compressed trace (`BLUE`) and the dynamic percentage amplitude threshold curve (`GREEN`).
3. **Graphic 2 (`draw_PB_Phases`, 800×125 px — Multi-Baseline Differential Phases):**
   * Plots the three raw receiver-pair differential phases (`AB` in `RED`, `AC` in `GREEN`, `AD` in `BLUE`) and the unwrapped Vernier synthetic phase (`YELLOW`) across port and starboard range samples.
4. **Graphic 3 (`draw_PB_Angles`, 800×125 px — Unwrapped Ray Angle & Phase Quality):**
   * Plots the resolved depression/elevation angle (`0°` to `90°`, `YELLOW`) and the multi-baseline phase coherence / quality metric (`0` to `256`, `GREEN`) against the active `PB_qual_thresh` cutoff line (`RED`).
5. **Graphic 4 (`draw_PB_Sidescan`, 800×80 px — 80-Swath Sidescan Waterfall Strip):**
   * Displays an 80-ping port/starboard sidescan waterfall (`PBss_c`) compressed from the 16-bit amplitude traces via `make_8bit_sidescan()`, with a horizontal red cursor indicating `selected_swath`.

### Sliders & Control Buttons

| Control | Label | Range / Function | Backing Variable |
| :--- | :--- | :--- | :--- |
| Slider `0` / `1` | `Min 16` / `Max 16` | `0` .. `65536` | `PB_min_16`, `PB_max_16` — 16-bit amplitude display bounds for Graphic 1 and 8-bit sidescan compression (`make_8bit_sidescan`). |
| Slider `2` | `Phase Quality Threshold` | `0` .. `255` | `PB_qual_thresh` — Minimum Vernier phase quality required to accept a phase sample. |
| Slider `3` / `4` | `Port` / `Stbd % Amplitude Threshold` | `0` .. `100` | `PB_port_amp_thresh`, `PB_stbd_amp_thresh` — Percentage of running mean envelope required to pass amplitude gating. |
| Slider `5` | `Water Depth Multiplier` | `1.0` .. `8.0` | `PB_WD_multiple` — Vertical depth scale multiplier relative to nadir water depth. |
| Slider `6` | `Max Across Coverage (m)` | `5.0` .. `250.0` | `PB_max_across_m` — Horizontal half-swath range (m) across all 5 graphics windows. |
| Buttons `0`–`3` | `show GATES`, `show_RAW_PHASE`, `show_SOLUTIONS`, `show_DENSITY` | Visual Toggles | Toggles range gates, raw phase cloud, accepted soundings, or 2D sounding density grid in Graphic 0. |
| Button `4` | `load used params` | `load_orig_PB_params()` | Restores filtering/gating thresholds from the `OMG_HDCS_Submetrix_params` header stored in the `.merged` file. |
| Button `5` | `nadir filter` | `PB_filter_nadir` | Toggles nadir specular artifact filtering during solution generation. |
| Button `6` | `linear/log` | `PB_linear` | Toggles Graphic 1 between linear 16-bit amplitude and logarithmic dB scaling. |
| Button `7` | `method 1/2/3` | `PB_method` (`1..3`) | Cycles the phase-to-angle binning and despiking algorithm in `recalc_PB_solutions()`. |

---

## Core Processing Pipeline (`recalc_PB_solutions`)

When sliders or method buttons are adjusted, `recalc_PB_solutions(swath)` invokes the Submetrix Vernier phase unwrapper and angle solver (`j_SUB2K.h`):
1. Evaluates 3-baseline differential phases (`AB`, `AC`, `AD`) at each range sample to resolve the $2\pi$ ambiguity (Vernier phase `vern_phase` and coherence quality `vern_qual`) and maps phase into physical depression angle (`vern_angle`) using transducer tilt and baseline spacing (`spacing_AB`, `spacing_AC`, `spacing_AD`, `lambda`).
2. Applies range gates (`min_gate`, `max_gate`), `PB_qual_thresh`, and port/starboard amplitude envelope thresholds (`PB_port_amp_thresh`, `PB_stbd_amp_thresh`), then bins/averages valid angle-range pairs into bathymetric soundings (`PB_beams[swath][]`).
