---
layout: default
title: SE_event_loop
parent: SwathEd (SE) Tools
nav_order: 21
tool_name: SE_event_loop
source_path: code/SE/SE_event_loop.c
category: Interactive QC & Editing (SwathEd)
input_formats: []
output_formats: ["dump.data", "distort.grid", "across_XXXXX.ppm", "along_XXXXX.ppm", "both_XXXXX.gif", ".done"]
related_tools: ["swathed", "SE_mainwin", "SE_GEOwindows", "SE_2Dwindow", "SE_PATCHwin", "SE_WaterColumn", "SE_W_TimeSeries"]
---

# `SE_event_loop` — Central X11 Event Dispatcher & Interactive Command Router

`SE_event_loop` (`code/SE/SE_event_loop.c`, 6,498 lines) is the central nervous system of [`swathed`](swathed.md). Authored by John E. Hughes Clarke with extensive additions by Jonathan Beaudoin, Carlos Rubio, Anand, Douglas Bergersen, and Leonardo, it implements `process_x_events()`—the single top-level X11 event loop that receives every `KeyPress`, `ButtonPress`, `ButtonRelease`, `MotionNotify`, `Expose`, `EnterNotify`, `LeaveNotify`, `ConfigureNotify`, and `UnmapNotify` event across all `swathed` windows and dispatches them either to modular `jX_widget` handlers or to built-in editing, filtering, and navigation routines.

---

## Two-Tier Event Dispatch Architecture

When `swathed` finishes initializing its X11 windows, `main()` enters `process_x_events()`, which runs until `done` is set (or `parse_which_widget()` returns `999` on clicking the `exit` icon):

1. **Event Queue Coalescing:**
   * Drains intermediate `MotionNotify` events (`XEventsQueued(display, QueuedAlready)`) during rubber-band dragging so cursor tracking never lags behind X11 server traffic.
   * Deduplicates redundant `Expose` events (`XCheckTypedWindowEvent(..., Expose, &event)`) before calling `refresh_window()` (added by JDB, March 2003).
2. **Tier 1 — Widget Router (`parse_which_widget`):**
   * Checks whether `event.xany.window` belongs to the main toolbar (`manage_ICON_events`), main window frame (`manage_MAIN_events`), Sub-Bottom viewer (`manage_SUBBOTTOM_events`), or any of the 11 `jX_widget` toolkits via `jX_is_any_win()`:
     * [`SE_W_TimeSeries`](SE_W_TimeSeries.md) (`TimeSeries_widget`, `TSplot_widget`, `TSpram_widget`)
     * [`SE_AnandBS`](SE_AnandBS.md) (`AnandBS_widget`, `ARC_widget`)
     * [`SE_BDI_DP`](SE_BDI_DP.md) (`BDI_DP_widget`) and [`SE_PDI_LA`](SE_PDI_LA.md) (`PDI_LA_widget`)
     * [`SE_WaterColumn`](SE_WaterColumn.md) (`WaterColumn_widget`) and [`c_wcl_TOOLBOX`](c_wcl_TOOLBOX.md) (`target_widget`)
     * [`SE_PhaseBathy`](SE_PhaseBathy.md) (`PhaseBathy_widget`), [`SE_Waveforms`](SE_Waveforms.md) (`Waveform_widget`), and [`SE_3D`](SE_3D.md) (`SE3D_widget`)
3. **Tier 2 — Classic Sub-Window & Main Editor Event Loop (`managed == 0`):**
   * Handles all keyboard shortcuts, mouse clicks, and rubber-band selections for the 8 core `swathed` panels (`graphic_window[0..7]`) and classic sub-windows (`sub_window[1..61]` and `REF_OFFSET` `61..73`).

---

## Toolbar Icon Launcher (`manage_ICON_events`, `icon_window[0..17]`)

Clicking any of the 18 toolbar icons (`icon_window[0..17]`) executes `manage_ICON_events()`:

| Icon Index | Label | Action |
| :--- | :--- | :--- |
| `0` | `exit` | Calls `dump_array(&in_recnum)` to save pending flag edits to `.merged` and returns `999` to exit `swathed`. |
| `1` / `2` | `fwd` / `bck` | Saves edits (`dump_array()`) and steps `in_recnum` forward or backward by `SE_NO_SWATHS - 4` (`76` pings), calling `prime_array()`. |
| `3` | `ALL/sel` | Toggles `all_sel_flag` between flagging all 80 swaths in a rubber-band box (`ALL`) vs. only `selected_swath`/`selected_beam` (`SEL`). |
| `4` | `p-B-s` | Cycles `psb_flag` between viewing Port (`P-b-s`), Starboard (`p-b-S`), or Both (`p-B-s`) half-swaths. |
| `5` | `next` | Saves edits and advances `current_file` to the next loaded `.merged` survey line (`start_file()`, `prime_array()`). |
| `6` | `list` | Opens the ASCII ping/beam header inspector (`view_list()`, `plot_list()` in [`SE_listwin`](SE_listwin.md)). |
| `7` | `ss` | Launches [`SE_sswindow`](SE_sswindow.md) (multibeam sidescan), [`SE_PhaseBathy`](SE_PhaseBathy.md) (`SEA_SwathPlus`), or [`SE_SUBBOTwin`](SE_SUBBOTwin.md) (`Knudsen_320`). |
| `8` | `auto` | Opens the automated slope/spike flagging window ([`SE_AUTOFLAGwin`](SE_AUTOFLAGwin.md)) and runs `check_data(1)`. |
| `9` | `2D` | Opens the 2D sub-area sounding scatterplot editor ([`SE_2Dwindow`](SE_2Dwindow.md)) and loads profiles via `get_D2_profiles_inarea()`. |
| `10` | `Class` | Launches [`SE_AnandBS`](SE_AnandBS.md) (`make_AnandBS_widget()`) or [`SE_BSwindow`](SE_BSwindow.md) (`view_BSbox()`). |
| `11` | `Patch` | Opens the interactive Patch Test toolkit ([`SE_PATCHwin`](SE_PATCHwin.md)) and loads corridor swaths via `get_Swaths_inarea()`. |
| `12` | `Lines` | Opens the paginated survey line manager ([`SE_LineListwin`](SE_LineListwin.md)). |
| `13` | `Refr.` | Opens the empirical refraction and induced-heave modeling tool ([`SE_REFTOOLwin`](SE_REFTOOLwin.md)). |
| `14` | `geo` | Initializes a blank geographic trackline locator window (`setup_blank_area()` in [`SE_GEOwindows`](SE_GEOwindows.md)) when no `.r4` grid was provided. |
| `15` | `TS` | Maps `TimeSeries_widget` and `TSpram_widget` ([`SE_W_TimeSeries`](SE_W_TimeSeries.md)). |
| `16` | `WC` / `WF` | Maps `WaterColumn_widget` ([`SE_WaterColumn`](SE_WaterColumn.md)) or `Waveform_widget` ([`SE_Waveforms`](SE_Waveforms.md)). |
| `17` | `WGC` | Opens the Weekley–Goodrich–Cornman neighbor-depth filter window ([`SE_Weekley_Goodrich_Cornman`](SE_Weekley_Goodrich_Cornman.md)). |

---

## Key Interactive Hotkeys in the Main Editing Windows (`graphic_window[0..7]`)

* **Rubber-Band Flagging / Unflagging / Zooming:**
  * **Left-drag (`Button1`):** Flags soundings inside the rubber-band box in `graphic_window[0]` (along-track), `[1]` (across-track), `[4]`, or `[5]`; unflags soundings in `graphic_window[2]` or `[3]`.
  * **Middle-drag (`Button2`):** Zooms the view (`lock_view`) to the dragged rectangle in `graphic_window[0]`, `[1]`, or `[5]`; pressing `r` unlocks and resets the zoom.
  * **Right-click (`Button3`):** Selects `selected_beam` and `selected_swath` (`highlight_beam()`) across all linked views.
* **Automated Filters & Editing Hotkeys ([`SE_filters`](SE_filters.md)):**
  * `u`: Undo last flagging operation (`undo()`, up to 10 levels via `shift_undo_flags()`).
  * `d` / `D`: Toggle linear seafloor detrending (`detrend_flag`, `update_for_detrend()`) and phase-only detrend criteria (`Detrend_Criteria`).
  * `f`: Run statistical standard-deviation "defluffing" (`defluff()`) on detrended soundings (`F1`–`F6` set `SDmultiplier = 1.0..6.0`; `F` cycles `SD_calc_method`).
  * `m` / `M` / `<` / `>` / `%`: Run 2D median filter (`compute_median()`, `median_filter()`), toggle auto-premedian (`premedian_flag`), adjust kernel size (`median_filter_size`, `2..10`), and increment depth threshold (`median_filter_threshold`).
  * `e` / `E` / `(` / `)`: Run nadir/tunnel "detrenching" (`detrench()`), toggle `predetrench`, and adjust `detrench_port_sector` / `detrench_stbd_sector`.
  * `l`: Reject isolated "lonely" soundings (`filter_lonely_soundings()`).
  * `p`: Run modal-depth Powell filter (`depowell()`).
  * `w`: Run Weekley–Goodrich–Cornman filter (`do_weekley_filter()`).
  * `s` / `t`: Flag entire `selected_swath` (`s`) or all 80 swaths in the current block (`t`).
  * `F7`–`F12`: Control CARIS HIPS flag preloading (`preload_flags`, `load_flags()`) and ping-offset synchronization (`HIPS_ping_offset`, `guess_flag_offset()`).
  * `W`: Export 80 sequential PPM/GIF animation frames (`across_%05d.ppm`, `along_%05d.ppm`, `both_%05d.gif`) across the current 80-ping block.
