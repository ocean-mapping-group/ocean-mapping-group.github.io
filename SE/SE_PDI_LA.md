---
layout: default
title: SE_PDI_LA
parent: SwathEd (SE) Tools
nav_order: 12
tool_name: SE_PDI_LA
source_path: code/SE/SE_PDI_LA.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", ".watercol", ".WC_Phase1", ".WC_Phase2"]
output_formats: ["pdi_XXXXX_BBB_TTTT_slc.ppm", "pdi_XXXXX_BBB_TTTT_pie.ppm"]
related_tools: ["swathed", "SE_WaterColumn", "SE_BDI_DP", "pdi_funcs", "bdi_funcs"]
---

# `SE_PDI_LA` — Phase Detection Indicator (PDI) Track Toolkit

`SE_PDI_LA` (`code/SE/SE_PDI_LA.c`, `code/SE/SE_PDI_LA.h`) is an interactive X11 widget (`"PDI Track Toolkit"`, `PDI_LA_widget`) integrated into [`SE_WaterColumn`](SE_WaterColumn.md) and [`swathed`](swathed.md). Developed by Leonardo (Leo) and John E. Hughes Clarke (October 2019), it extends the across-beam Bottom Detection Indicator ([`SE_BDI_DP`](SE_BDI_DP.md)) by incorporating high-resolution split-beam differential phase time series (`.WC_Phase1` / `.WC_Phase2`, stored in `WHOLE_ping_WCP`) alongside water column amplitude (`.watercol`, `WHOLE_ping_WC`).

By fitting a linear phase ramp across adjacent receive beams around a candidate BDI amplitude peak at a fixed two-way travel time (TWTT) slice—a technique termed **Phase Detection Indicator (PDI)**—`SE_PDI_LA` resolves sub-beam arrival angles at zero-phase crossings across constant-range arcs.

---

## Architecture & X11 Widget Layout

`make_PDI_LA_widget()` initializes `PDI_LA_widget` (`jX_widget`) with 2 stacked 800×250 pixel graphics windows, 4 interactive sliders, and 4 toggle/action buttons:

### Graphics Windows
* **Graphic 0 (`draw_PDI_LA_AlongBeam` — Along-Beam Amplitude & Split-Beam Phase):**
  * Plots a single receive beam (`selected_beam` in `selected_swath`) over a zoomable TWTT sample window (`selected_WC_TWTT - PDI_half_twtt_win` to `selected_WC_TWTT + PDI_half_twtt_win`).
  * Left vertical axis (`-180°` to `+180°`): Plots raw split-beam differential phase (`WHOLE_ping_WCP[0][swath].watercols[beam].ts_ampl[i]` scaled to degrees) as `GREEN` polylines and `RED` sample crosses (`show_PDI_Phase`).
  * Right vertical axis (`-100` to `0` dB): Plots acoustic backscatter intensity (`0.5 * ts_ampl - 60` dB) in `BLUE` (`show_PDI_Int`), with a vertical `YELLOW` cursor at `selected_WC_TWTT` and a `MAGENTA` marker at the sonar's real-time bottom detection sample (`unknown`).
* **Graphic 1 (`draw_PDI_LA_AcrossBeam` — Across-Beam Constant-TWTT Phase & Amplitude Slice):**
  * Plots both differential phase (`-180°` to `+180°`) and intensity (`-100` to `0` dB) across receive beam pointing angles at the fixed range slice `selected_WC_TWTT` (zoomed to `selected_beam ± PDI_half_beam_win`).
  * Overlays candidate BDI amplitude peaks (`WC_BDI_pick[twtt][j].angle`, `CYAN` diamonds) and the refined PDI zero-crossing phase picks (`WC_PDI_pick[twtt][j].angle`, `RED` diamonds) along with the fitted linear phase regression slope across `[left_limit, right_limit]`.

### Interactive Sliders & Control Buttons

| Control | Label | Range / Type | Backing Variable | Description |
| :--- | :--- | :--- | :--- | :--- |
| Slider `0` | `PDI threshold dB` | `-80.0` .. `10.0` | `WC_PDI_threshold` (int) | Minimum intensity threshold (dB) required when searching for valid phase samples around a BDI peak. |
| Slider `1` | `PDI ival (1)` | `-15.0` .. `15.0` | `WC_PDI_ival` (int) | Auxiliary tuning parameter for PDI window/gate control. |
| Slider `2` | `half beam win` | `0.0` .. `50.0` | `PDI_half_beam_win` (int) | Half-width (in beam indices) of the across-beam zoom window in Graphic 1 (`0` = full swath `[-80°, +80°]`). |
| Slider `3` | `half twtt win` | `0.0` .. `300.0` | `PDI_half_twtt_win` (int) | Half-width (in TWTT samples) of the along-beam zoom window in Graphic 0 (`0` = full range trace). |
| Button `0` | `plot Phase ` | Toggle | `show_PDI_Phase` | Toggles split-beam phase curves (`GREEN`/`RED`) in both graphics canvases. |
| Button `1` | `plot Int. dB` | Toggle | `show_PDI_Int` | Toggles amplitude dB curves (`BLUE`) in both graphics canvases. |
| Button `2` | `show PDI-BDI` | Toggle | `show_PDI_BDI` | Overlays BDI peak angles and PDI linear phase regression zero-crossings in Graphic 1 and the main `SE_WaterColumn` polar fan (`plot_PDI`). |
| Button `3` | `export frames` | Action | `PDI_export_frames()` | Steps `selected_WC_TWTT` by 5 samples and exports synchronized PPM image pairs (`pdi_%05d_%3d_%04d_slc.ppm` and `_pie.ppm`) via `dump_Window()` (`SE_3D.h`). |

---

## Core Algorithms (`WC_PDI_pick_Angle_Peaks`)

1. **BDI Seed Generation:** Calls `standalone_BDI_pick_Angle_Peaks()` ([`bdi_funcs.c`](bdi_funcs.md)) to populate up to `NO_BDI` (12) amplitude peaks per time slice in `WC_BDI_pick[1500][NO_BDI]`.
2. **Across-Beam Phase Zero-Crossing Refinement:** Calls `standalone_PDI_pick_Angle_Peaks()` ([`pdi_funcs.c`](pdi_funcs.md)), which inspects the split-beam phase array (`WHOLE_ping_WCP`) in a neighborhood (`[left_limit, right_limit]`) around each BDI seed `WC_BDI_pick[twtt][j].beam`. It performs a least-squares linear regression of differential phase versus beam pointing angle ($\phi(\theta) = a + b\theta$) and solves for the zero-phase crossing angle $\theta_{\text{PDI}} = -a/b$, storing the result in `WC_PDI_pick[twtt][j].angle`.
3. **Water Column Polar Fan Overlay:** When `show_PDI` and `plot_PDI` are active in [`SE_WaterColumn`](SE_WaterColumn.md), `draw_WaterColumn()` projects every valid `WC_PDI_pick[i][j].angle` into across-track and depth coordinates and renders `RED` diamonds on the polar fan image.
