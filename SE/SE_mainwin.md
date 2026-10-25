---
layout: default
title: SE_mainwin
parent: SwathEd (SE) Tools
nav_order: 27
tool_name: SE_mainwin
source_path: code/SE/SE_mainwin.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", ".param"]
output_formats: ["qfactors.dat"]
related_tools: ["swathed", "SE_omgIOwin", "SE_filters", "SE_AUTOFLAGwin", "SE_event_loop"]
---

# `SE_mainwin.c` — Core Multi-Pane Swath Profile & Beam Editor Window

## Overview & Purpose
`SE_mainwin.c` (with header `SE_mainwin.h`, authored by John E. Hughes Clarke, April–July 1999) implements the core 100-ping (`SE_NO_SWATHS`) interactive graphical editor window of `swathed`. It manages the multi-pane `graphic_window[0..7]` layout where hydrographers inspect along-track beam profiles, across-track swath profiles, plan-view bottom detection maps, beam-by-ping backscatter/slope grids, and vessel motion (heave, pitch, roll, heading) time series.

Beyond rendering and cursor synchronization (`beam_update`, `highlight_beam`), `SE_mainwin.c` implements rubber-band rectangular flagging/unflagging (`flag_rectangle`), 8-level bitwise undo (`undo`, `shift_undo_flags`), across-track and along-track standard-deviation ("defluff") statistical trimming (`calc_SD_number`, `trim_by_SD`, `calc_along_SD_number`, `trim_along_by_SD`), IHO / QMS uncertainty envelope overlays, local median filtering (`compute_median`, `median_filter`), and Gasser-Sroka-Jennen-Steinmetz non-linear residual beam variance estimation (`compute_variance`).

---

## Core X11 Graphic Panes (`graphic_window[0..7]`)

`refresh_coreSE_window(Window window)` manages eight coordinated sub-windows within the main `SwathEd` canvas:

| Window | Location & Role | Interactive Features & Display Modes |
|---|---|---|
| `graphic_window[0]` | **Centre-Left: Along-Track Beam Profiles** | Plots unflagged soundings (`-box[j][i]`) along-track (`(i+2) * inter_ping_distance`). Displays `Ping Period` (s) and `Vessel Speed` (knots). Left-drag rubber-band flags soundings; middle-drag zooms (`redefine_bounds`). Supports along-track $2\sigma$ and `SDmultiplier` trimming (`calc_along_SD_number`, `trim_along_by_SD`). |
| `graphic_window[1]` | **Centre-Right: Across-Track Swath Profiles** | Plots across-track offset (`offsets[j][i]`) vs. depth (`-box[j][i]`, observed or de-trended). Optionally overlays horizontal depth lines (`Show_Depth_Lines`), common slant-range arcs (`Show_CommonRange_Lines`), sector-boundary detrench polygons (`show_detrench_sector`), Lake Powell wall brackets (`using_powell`), and IHO/QMS/SD envelopes (`plot_SD_number`, `calc_QMS`). |
| `graphic_window[2]` | **Lower-Left: Flagged ("Unlasso") Along-Track View** | Plots rejected soundings (`box[j][i] < 0`) along-track so users can inspect and rubber-band unflag (restore) valid soundings (`unlasso_flag`, toggled via Spacebar). |
| `graphic_window[3]` | **Lower-Centre: Flagged Across-Track View** | Plots rejected soundings (`box[j][i] < 0`) across-track for rubber-band unflagging and cursor inspection (`beam_update`). |
| `graphic_window[4]` | **Bottom-Centre: Plan-View Bottom Detection Map** | Plots across-track offset vs. ping index (`0..99`), coloring each sounding by bottom detection mode (`detect_mode > 127` in **RED** for amplitude, **BLUE** for phase, **CYAN** when flagged, **YELLOW** for current beam). Toggled via `plan_flag` (Spacebar). |
| `graphic_window[5]` | **Bottom-Right: Beam $\times$ Swath Backscatter / Slope Grid** | Renders a 2D pixel matrix (`paint_beam`) of beam number vs. ping index colored according to `clean_flag`: raw reflectivity (`sigs`, `0`), corrected backscatter/Q-factor (`cleansigs`, `1`), across-track slope (`across_sigs`, `2`), along-track slope (`along_sigs`, `3`), or individual status bitplanes (`4..11`). Toggled via `ampl_flag` (Spacebar). |
| `graphic_window[6]` | **Top-Left: Vessel Attitude & Motion Traces** | Plots 100-ping time series of `Heave` (green, $\pm 3\text{ m}$), `Pitch` (blue, $\pm 2^\circ$), `Roll` (red, $\pm 5^\circ$), and `Heading` (black, $0..360^\circ$). Toggled via `vrus_flag` (Spacebar). |
| `graphic_window[7]` | **Top Progress Bar: Line Position Indicator** | Shows the current 100-ping window position (`in_recnum .. in_recnum + SE_NO_SWATHS`) along the total survey line (`0 .. summary.numProfiles`). |

---

## Key Functions

| Function | Signature | Description |
|---|---|---|
| `allocate_mainwin_memory` | `void allocate_mainwin_memory()` | Dynamically allocates per-swath motion arrays (`roll`, `pitch`, `heave`, `heading`, `pingtime`, `prof_mode`), per-beam geometry arrays (`top_x/y`, `bot_x/y`, `beamflag`), 40-bin across-track and along-track statistical arrays (`bin_averages`, `bin_SDs`, `along_bin_averages`, `along_bin_SDs`), and `lock_view[NUM_VIEWS]`. |
| `setup_for_next80` | `void setup_for_next80()` | Computes `min_depth`, `max_depth`, `min_good_depth`, and `max_good_depth` over the 100 loaded swaths, selects adaptive depth grid interval `line_interval` ($1\text{ m}$ to $100\text{ m}$), refreshes `graphic_window[0..7]`, and synchronizes child windows (`SE_REFTOOLwin`, `SE_sswindow`, `SE_listwin`, `SE_Weekley_Goodrich_Cornman`). |
| `flag_rectangle` | `void flag_rectangle(int first_window, int x0, int y0, int x1, int y1)` | Converts rubber-band pixel coordinates `(x0,y0)-(x1,y1)` to data coordinates via `jhc_scaled_values()` and flags or unflags all soundings inside (or outside, if `invert_selection_flag` is set) the box in windows `0`, `1`, `2`, `3`, `4`/`-4`, or `5`/`-5`. Operates on all swaths/beams (`ALL`) or only the active swath/beam (`SEL`). |
| `undo` / `shift_undo_flags` | `void undo()` / `int shift_undo_flags()` | Maintains an 8-step undo history using the 8 bits of `box_flags[i][j]`. Before any edit, `shift_undo_flags()` left-shifts `box_flags[i][j] <<= 1`. Modified beams increment bit 0 (`box_flags[i][j]++`). Calling `undo()` tests `box_flags[i][j] & 0x01`, inverts `box[i][j]`, and right-shifts `box_flags[i][j] >>= 1`. |
| `calc_SD_number` / `trim_by_SD` | `void calc_SD_number(int)` / `void trim_by_SD()` | Partitions the across-track swath width into `NO_STAT_BINS` (`40`) spatial bins, computes the mean depth (`bin_averages`) and standard deviation (`bin_SDs`) per bin, and ("defluffs") flags soundings deviating by more than `SDmultiplier * bin_SDs[bin_no]` or falling in sparse bins (`< 10%` of average bin density). |
| `calc_along_SD_number` / `trim_along_by_SD` | `void calc_along_SD_number(int)` / `void trim_along_by_SD()` | Computes 40-bin along-track depth averages (`along_bin_averages`) and standard deviations (`along_bin_SDs`) in `graphic_window[0]` and flags outliers exceeding `SDmultiplier * along_bin_SDs[bin_no]`. |
| `compute_median` / `median_filter` | `void compute_median()` / `void median_filter()` | Evaluates a sliding `median_filter_size` $\times$ `median_filter_size` neighborhood around each sounding, populates `median_box[j][i]` and `std_dev_box[j][i]`, and flags soundings whose deviation from the local median exceeds `median_filter_threshold` ($\%$ of water depth). |
| `compute_variance` / `plot_variance` | `void compute_variance()` / `void plot_variance()` | Estimates beam-by-beam residual variance across `SE_NO_SWATHS` using the 3-point Gasser, Sroka & Jennen-Steinmetz (1986) nonlinear regression estimator, compares against Ifremer quality factors (`beam_qfactors`), and writes `qfactors.dat`. |

---

## Integration within `swathed`
- **Data Loading & Saving:** Relies on [`SE_omgIOwin.c`](SE_omgIOwin.md) (`prime_array` and `dump_array`) to populate `box[][]` and `offsets[][]` from `.merged` files and write modified status flags back to disk.
- **Cross-Window Cursor Sync (`highlight_beam`):** Moving the mouse cursor (`beam_update`) or pressing arrow keys updates `selected_swath` and `selected_beam`, calling `highlight_beam()` to draw synchronized crosshairs in `graphic_window[0..5]` and refresh open water-column ([`SE_WaterColumn.c`](SE_WaterColumn.md)), waveform ([`SE_Waveforms.c`](SE_Waveforms.md)), phase bathymetry ([`SE_PhaseBathy.c`](SE_PhaseBathy.md)), and Anand backscatter ([`SE_AnandBS.c`](SE_AnandBS.md)) windows.
