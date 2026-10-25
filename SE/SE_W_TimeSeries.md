---
layout: default
title: SE_W_TimeSeries
parent: SwathEd (SE) Tools
nav_order: 17
tool_name: SE_W_TimeSeries
source_path: code/SE/SE_W_TimeSeries.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", ".lph", ".rtk", ".2ndAtt"]
output_formats: [".fixed.merged", "Xplot.out"]
related_tools: ["swathed", "fix_TimeSeries", "newMergeAtt", "SE_REFTOOLwin"]
---

# `SE_W_TimeSeries` — Full-Line Motion, Attitude & Seafloor Slope Time-Series Analysis Toolkit

`SE_W_TimeSeries` (`code/SE/SE_W_TimeSeries.c`, `code/SE/SE_W_TimeSeries.h`) implements a three-widget X11 diagnostic and motion-compensation suite in [`swathed`](swathed.md). Authored by John E. Hughes Clarke (January 2003, ported and expanded from `DelayEditor`), it loads up to 79 simultaneous ping-by-ping time series (`TS_NO_VARIABLES = 79`) across an entire `.merged` survey line to diagnose roll, pitch, yaw, heave, delayed heave (`.lph`), RTK antenna height (`.rtk`), secondary attitude sensors (`.2ndAtt`), transmit sector steering, and seafloor slope residuals ("wobbles").

---

## Three-Widget Architecture

Enabled via the `-ts` command-line flag and mapped by clicking the **`TS`** icon (`icon_window[15]`), `SE_W_TimeSeries` coordinates three `jX_widget` windows:

1. **`TimeSeries_widget` (`"TimeSeries Analysis Toolkit"`):**
   * **3 Stacked Time-Series Canvases:** Graphic `0` (`TS_draw_Full` — full survey line overview), Graphic `1` (`TS_draw_Mid` — intermediate zoom window with yellow bounding box), and Graphic `2` (`TS_draw_Zoom` — high-resolution ping-by-ping zoom window marking the active 80-swath `swathed` window).
   * **9 Interactive Sliders:** Dynamically rebound by `TS_apply_fix` to control either:
     * **Roll Correction (`TS_FIX_ROLL`):** `Roll Offset (deg)`, `Roll Scale (%)`, `Roll Phase (s)`, `Pitch Scale (%)`, `Pitch Phase (s)`.
     * **Heave / Lever-Arm Correction (`TS_FIX_HEAVE`):** `Heave Offset (m)`, `Heave Scale (%)`, `Heave Phase (s)`, `Lever X (m)`, `Lever Y (m)`, `Lever Z (m)`, `Roll Scale`, `Pitch Scale`, `Yaw Scale`.
     * **Outer-Beam / Pitch Wobble (`TS_FIX_OUTER`):** `Port Slope (%)`, `Stbd Slope (%)`, `Slope Phase (s)`, `Pitch Scale (%)`, `Pitch Phase (s)`, `Pitch Lever X/Y/Z`.
     * **FFT / Boxcar Filtering:** Low-pass / band-pass frequency cutoffs (`TS_freq1..4`) and moving-average window lengths (`av_step_size`, `diff_step_size`).
   * **9 Action Buttons:** `Set Scale`, `Load Beams`, `Show CrossPlot`, `Correct Data`, `ProperCorrect`, `WriteOutFixed`, `FFT 1/2/3`, `Apply Fix`, and `Filter`.

2. **`TSpram_widget` (`"TS Parameter"` Selection Matrix):**
   * Displays a color-coded button matrix for toggling any of the 79 tracked variables (`TS_var_state[k]`: Off, Plot in Group 1, Plot in Group 2, or Cross-Plot X/Y axis), plus 4 quick-preset buttons (`Roll Slopes`, `Pitch Slopes`, `2nd Att.`, `Clear All`).

3. **`TSplot_widget` (`"TS Xplot Tool"` — Cross-Plot, FFT & Histogram Analyzer):**
   * **Cross-Correlation & Linear Regression (`TS_draw_Xplot`):** Plots `Xplot_var1` vs. `Xplot_var2` over the zoomed ping range, fits a least-squares linear regression ($y = a + bx$, correlation $r$), and exports ASCII pairs to `Xplot.out`.
   * **Power Spectrum (`TS_calc_FFT`, `TS_draw_FFT`):** Computes a 2048-point FFT power spectrum (`0` to `0.5` Hz) for up to 4 selected variables simultaneously to isolate vessel roll/pitch resonant periods.
   * **Histogram (`TS_calc_HISTO`, `TS_draw_HISTO`):** Computes 100-bin probability distributions (`mean`, `stddev`) for active parameters.

---

## Tracked Parameter Groups (`TS_NO_VARIABLES = 79`)

`load_TimeSeries_variables()` extracts and derives:
* **Primary Attitude & Rates (`0..11`):** `Roll`, `Pitch`, `Gyro`, `Heave`, first derivatives (`dRoll/dt`, `dPitch/dt`, `dGyro/dt`, `dHeave/dt`), and second derivatives (`ddRoll/dt` ... `ddHeave/dt`).
* **Bathymetric Least-Squares Seafloor Slopes (`12..19`):** Port, Starboard, Full-Swath, and Inner-Swath across-track regression slopes (`atan(b)`) and correlation coefficients ($R^2$), plus `Nadir Depth` (`20`), `Smoothed Nadir` (`21`), and `Residual Nadir` (`22`).
* **Course Made Good & Speed (`23..30`):** Raw and smoothed `CMG`, `Crab Angle` ($\text{CMG} - \text{Gyro}$), and vessel speed (`knots`).
* **Multi-Sector Transmit Geometry (`31..39`, `55..62`):** Per-sector tilt angles (`Sector 1..3 Tilt`), frequencies, time offsets, and depth differences between adjacent transmit sectors (`Sect 0-1 Diff`, `Sect 1-2 Diff`).
* **External Vertical & Attitude References (`40..54`, `63..78`):** Tide, Sound Speed (`Surf SS`), Delayed Heave (`.lph`), RTK GPS elevation/geoid/COG/SOG (`.rtk`), and Secondary Motion Sensor roll/pitch/heading/heave differences (`.2ndAtt`).

---

## Motion Residual Simulation & Correction

* **Fast Empirical Correction (`correct_dataset` — `Correct Data` button):** Applies slider gains, phase lags, and lever arms directly to the in-memory `box[j][i]` and `offsets[j][i]` arrays for immediate visual feedback.
* **Rigorous 3D Ray Re-Merging (`correct_dataset_properly` — `ProperCorrect` button):** Re-runs the full [`newMergeAtt`](../merge/newMergeAtt.md) 3D coordinate transformation (`remerge_swath()`) across every beam in the survey line.
* **Export (`write_out_modified` — `WriteOutFixed` button):** Writes the motion-corrected survey line to `<line_prefix>.fixed.merged` (paralleling standalone tool [`fix_TimeSeries`](fix_TimeSeries.md)).
