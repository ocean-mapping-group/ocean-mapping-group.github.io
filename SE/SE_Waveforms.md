---
layout: default
title: SE_Waveforms
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 19
tool_name: SE_Waveforms
source_path: code/SE/SE_Waveforms.c
category: Interactive QC & Editing (SwathEd)
input_formats:
- .merged
- .waveform
output_formats: []
related_tools:
- swathed
- SE_WaterColumn
---

# `SE_Waveforms` — Airborne Bathymetric LiDAR Multi-Channel Waveform Analysis Toolkit

`SE_Waveforms` (`code/SE/SE_Waveforms.c`, `code/SE/SE_Waveforms.h`) implements the `"Waveform Analysis Toolkit"` (`Waveform_widget`) in [`swathed`](swathed.html). Authored by John E. Hughes Clarke (June 2005) incorporating Pim Kuus's (`pm_Process_Wave`, `pm_waveform.h`) derivative-based optical pulse analysis algorithms, it provides an interactive X11 viewer for inspecting 4-channel Airborne Laser Bathymetry (ALB / SHOALS LiDAR) time-series waveforms stored in `.waveform` files alongside `.merged` sounding records.

---

## Multi-Channel LiDAR Waveform Architecture

Each laser sounding (`WF_beams[swath][beam]`) in a SHOALS/ALB `.merged` file contains a byte offset (`offset`) into the companion `.waveform` binary file (`Waveformfile`) along with sample counts for four optical receiver channels:
1. **`PMT` (Photomultiplier Tube — Deep Green 532 nm Channel):** Up to `MAX_NO_PMT` (`500`) samples (`WF_trace_PMT`), capturing both the surface return and deep benthic bottom reflection.
2. **`GAPD` (Geiger-mode Avalanche Photodiode — Shallow Green 532 nm Channel):** Up to `MAX_NO_GAPD` (`500`) samples (`WF_trace_GAPD`) for shallow-water and surface interface detection.
3. **`IR` (Infrared 1064 nm Surface Channel):** Up to `MAX_NO_IR` (`500`) samples (`WF_trace_IR`) for sea-surface / land-water interface timing.
4. **`RAMAN` (Red 647 nm Water Raman Backscatter Channel):** Up to `MAX_NO_RAMAN` (`500`) samples (`WF_trace_RAMAN`) for water surface and volumetric clarity discrimination.

---

## X11 Widget Layout (`Waveform_widget`)

Clicked via the **`WC`/`WF`** icon (`icon_window[16]`) when a `.waveform` file is active (`got_wf`), `make_Waveform_widget()` creates `"Waveform Analysis Toolkit"` with **2 stacked 800×400 px graphics windows**, **2 sliders**, and **4 channel-toggle buttons**:

### Graphics Windows
* **Graphic 0 (Across-Swath Stacked Waveform Waterfall, 800×400 px):**
  * Plots all laser shots (`0` to `WF_profile[swath].numDepths`) across the active scan line (`selected_swath`), positioning each vertical trace at its across-track offset (`offsets[j][swath]`) and deflecting sample amplitudes horizontally (`Max_Xoffset / MaxExpectedIntensity[0..3]`).
  * Color-codes the four optical channels: **`PMT` (`YELLOW`)**, **`GAPD` (`CYAN`)**, **`IR` (`RED`)**, and **`RAMAN` (`GREEN`)**, while highlighting `selected_beam` in **`WHITE`**.
  * Overlays the automated surface-return (`s_start_sur`) and bottom-return (`s_start_bot`, `s_top_bot`, `s_end_bot`) picks computed by `pm_Process_Wave()` as `CYAN`, `RED`, and `BLUE` crosses/diamonds.
* **Graphic 1 (Single-Shot Trace & Derivative Inspector / Depth-vs-Intensity Scatterplot, 800×400 px):**
  * **`WF_PLOT_TRACE` Mode (Default):** Plots the full-resolution amplitude waveforms (`PMT`, `GAPD`, `IR`, `RAMAN`) for `(selected_swath, selected_beam)` over the sample window `[WF_lef_solo, WF_rig_solo]`.
    * Overlays Pim Kuus's smoothed first derivative (`PMT_wave_pt->d_trace_smooth[]`, `CYAN`, scaled to `[-4, +4]`) and smoothed second derivative (`PMT_wave_pt->dd_trace_smooth[]`, `BLUE`, scaled to `[-3, +1]`), plus vertical cursor lines marking the detected bottom pulse onset (`s_start_bot`, `RED`), peak (`s_top_bot`, `CYAN`), and trailing edge (`s_end_bot`, `BLUE`).
  * **`WF_PLOT_SCATT` Mode (Toggled via `t` key):** Plots a scatterplot of observed water depth (`the_depth`) versus peak bottom return intensity (`PMT_wave[i][j].i_top_bot`) across all 80 swaths to evaluate depth-dependent optical attenuation.

### Control Buttons & Sliders
* **Buttons `0..3` (`PMT`, `GAPD`, `IR`, `RAMAN`):** Independently toggle `show_PMT`, `show_GAPD`, `show_IR`, and `show_RAMAN` in both Graphic 0 and Graphic 1.
* **Sliders `0..1` (`WF 1 slider`, `WF 2 slider`):** Bound to `WF_slide1` and `WF_slide2` (`-1.0` to `+1.0`) for interactive threshold tuning.

---

## Interactive Controls (`manage_Waveform_widget_events`)

* **Left-drag in Graphic 0 or Graphic 1:** Rubber-bands a sample/amplitude zoom window (`WF_bot_main`..`WF_top_main` in Graphic 0; `WF_lef_solo`..`WF_rig_solo` and `WF_bot_solo`..`WF_top_solo` in Graphic 1).
* **`r` key:** Resets zoom bounds to full 500-sample / 500-intensity extents in the active graphic window.
* **`t` key:** Toggles `type_wf_plot` between single-shot trace/derivative inspection (`WF_PLOT_TRACE`) and 80-swath depth-vs-intensity scatterplot (`WF_PLOT_SCATT`).
* **Arrow keys (`Left`/`Right`, `Up`/`Down`):** Steps `selected_beam` or `selected_swath` and synchronously updates the main `swathed` cross-section and plan-view cursors.
