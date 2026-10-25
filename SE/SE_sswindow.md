---
layout: default
title: SE_sswindow
parent: SwathEd (SE) Tools
nav_order: 29
tool_name: SE_sswindow
source_path: code/SE/SE_sswindow.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", ".ss_data", ".16_data", ".ph_data", ".ph16_data"]
output_formats: []
related_tools: ["swathed", "SE_mainwin", "SE_omgIOwin", "SE_BSwindow", "SE_AnandBS"]
---

# `SE_sswindow.c` — Interactive Raw Sidescan, Snippet Trace & Phase Viewer Window

## Overview & Purpose
`SE_sswindow.c` (with header `SE_sswindow.h`, authored by John E. Hughes Clarke, April 1999) provides the interactive sidescan and snippet time-series diagnostic window (`sub_window[16]`, containing upper plot canvas `sub_window[13]` and lower waterfall strip `sub_window[15]`) in `swathed`.

When a `.merged` line has an accompanying `<line>.merged.ss_data` (8-bit or 16-bit sidescan/snippet trace file) and optionally `<line>.merged.ph_data` (differential phase file), `SE_sswindow.c` allows the user to inspect the acoustic backscatter and interferometric phase returns for the currently highlighted ping (`in_recnum + selected_swath`) alongside a scrolling 80-ping sidescan waterfall strip.

---

## X11 Window Architecture (`view_sidescan`)

Calling `view_sidescan()` creates a top-level parent window `sub_window[16]` ($906 \times 392$ px) titled according to the active `summary.toolType` (e.g., `"EM12D/12S/121A/1002/1000/950/300/3000S/3002/3000D Raw Sidescan Data"`, `"Seabeam 2000 Strip Sidescan Data"`, `"ISIS Submetrix 2000 Sidescan Data"`, `"ATLAS Hydrosweep MD2/30 Sidescan Data"`), divided into two child windows:
1. **`sub_window[13]` ($900 \times 300$ px, upper canvas):** Renders the single-ping detailed plot for `rec_no = in_recnum + selected_swath` in one of four user-selectable coordinate modes (`ssplot_type`).
2. **`sub_window[15]` ($900 \times 80$ px, lower canvas):** Renders the 80-ping 8-bit/24-bit sidescan waterfall image (`strip_image` / `strip_data`, populated by `load_up_strip()` in [`SE_omgIOwin.c`](SE_omgIOwin.md)) with a horizontal indicator line marking the currently selected swath.

---

## Display Modes (`ssplot_type`) in `plot_sidescan`

Users can cycle `ssplot_type` between four analytical views in `sub_window[13]`:

| Mode Constant | Value | Description & Visual Overlays |
|---|---|---|
| `HORIZ_RANGE` | `0` | **Across-Track Horizontal Range vs. Depth Profile:** Plots radial ray vectors from the transducer `(0,0)` to each beam's `(offset, depth)` (**RED** for port beams, **GREEN** for starboard beams), marks bottom detections with diamonds/crosses (**BLUE** for amplitude `Q_factor <= 127`, **CYAN** for phase `Q_factor > 127`), and draws the radial snippet trace window extent (`before` and `after` `beams[i].centre_no` scaled by `sample_length`) along each beam ray. |
| `SLANT_RANGE` | `1` | **Two-Way Travel Time (Slant Range) vs. Beam Number Strip:** Plots two-way travel time (seconds/ms) on the X-axis against beam index (`0 .. numDepths`) on the Y-axis. Highlights the minimum slant range ($R_0$ to $1.1 R_0$ first-arrival zone) in **YELLOW**, overlays greyscale snippet intensity bars (`SS_data[j]`) around each beam's `centre_no` sample, and marks the picked bottom detection sample with a black diamond. |
| `TIME_SERIES` | `2` | **Across-Track Backscatter Snippet & Phase Trace Plot:** Projects each beam's snippet sample series (`SS_data[0 .. no_samples-1]`) onto horizontal across-track range (`begin` to `the_end` via flat-seafloor slant-range geometry $\sqrt{R^2 - Z^2}$) and plots amplitude (dB reference lines from $-50\text{ dB}$ to $-10\text{ dB}$) and optional 16-bit differential phase (`PH_data` from `.ph_data`) along with per-beam reflectivity crosses. |
| `PLAN_VIEW` | `3` | **Plan-View Yaw-Steered Swath Footprint:** Plots across-track vs. along-track beam locations (`yoffset`, `yalong`) rotated by vessel yaw steering (`show_yaw`), fitting a least-squares line (`Xacross`, `Xalong`) to inspect yaw stabilization and snippet footprint alignment. |

### Specialized Interferometric Mode (`ISIS_Submetrix` / `SEA_SwathPlus`)
When editing dual-head interferometric sonar data (`summary.toolType == ISIS_Submetrix`), `plot_sidescan()` processes port/starboard ping pairs (`SUBX_PORT` / `SUBX_STBD`) and provides:
- **`ssplot_type == 0`:** Raw 16-bit sidescan amplitude trace (`ss16trc[the_swath][i]`).
- **`ssplot_type == 1`:** Three-vernier differential phase traces (`ABphase` in **RED**, `ACphase + 256` in **GREEN**, `ADphase + 512` in **BLUE**).
- **`ssplot_type == 2`:** Live interferometric bottom-detection re-computation (`init_jSUBX_vals`, `handle_raw_sonar_data`), plotting raw phase-derived `(across[i], -depths[i])` scatterers, water-depth multiplier and max coverage gates in **YELLOW**, tracking gates (`gate_shal`, `gate_deep`, `track_gate_shal`, `track_gate_deep`) in **RED**, and binned bathymetric solutions (`pr_across`, `pr_depth`).

---

## Key Functions & Globals

| Symbol | Type | Description |
|---|---|---|
| `view_sidescan()` | Function | Initializes and maps `sub_window[16]`, `sub_window[13]`, and `sub_window[15]`, sets `got_a_sswindow = 1`, and calls `load_up_strip()`. |
| `plot_sidescan(int rec_no, int resetss)` | Function | Reads profile and snippet/phase records for `rec_no` and renders the active `ssplot_type` view in `sub_window[13]` (resetting zoom bounds if `resetss == 1`). |
| `refresh_sidescan()` | Function | Redraws the 80-ping `strip_image` in `sub_window[15]` via `XPutImage()` and overlays the current ping marker. |
| `ss_pixel` | `float` | Across-track pixel size (meters, default `1.0`, configurable via `swathed -pixel <m>`) used when gridding the sidescan strip in `make_ss()`. |

---

## Integration within `swathed`
- **Invocation:** Activated from the `swathed` toolbox or keyboard shortcut when `got_ss == 1` (`.ss_data` present).
- **Synchronization:** Automatically updated by `setup_for_next80()` and `beam_update()` in [`SE_mainwin.c`](SE_mainwin.md) whenever the user changes the selected ping (`selected_swath`) or beam (`selected_beam`), or advances to a new 100-ping block (`prime_array` in [`SE_omgIOwin.c`](SE_omgIOwin.md)).
