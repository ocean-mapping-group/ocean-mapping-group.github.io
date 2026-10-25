---
layout: default
title: SE_filters
parent: SwathEd (SE) Tools
nav_order: 22
tool_name: SE_filters
source_path: code/SE/SE_filters.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", ".param"]
output_formats: [".merged (beam status flags updated via dump_array)"]
related_tools: ["swathed", "SE_mainwin", "SE_AUTOFLAGwin", "SE_omgIOwin"]
---

# `SE_filters.c` — Specialized Bathymetric Outlier & Sector Artifact Filters

## Overview & Purpose
`SE_filters.c` (with header `SE_filters.h`) provides specialized automated bathymetric filtering algorithms integrated into `swathed` for cleaning 100-ping (`SE_NO_SWATHS`) blocks of multibeam data loaded in memory (`box[SE_NO_MAX][SE_NO_SWATHS]` and `offsets[SE_NO_MAX][SE_NO_SWATHS]`).

It implements four distinct filtering routines designed to address specific multibeam sonar artifacts encountered in field surveys:
1. **Sector-Boundary "Trench" Filtering (`detrench`):** Removes artificial deep "trenches" or dropouts along transmit sector boundaries on multi-sector systems (such as Kongsberg EM710, EM302, EM122, and EM2040), controllable interactively or via `-pre_detrench`.
2. **Modal Depth Estimation (`get_mode`):** Computes the dominant (modal) water depth of a 100-ping block using a 0.5 m histogram for steep-wall canyon/reservoir filtering.
3. **Steep-Wall / Lake Powell Filtering (`depowell`):** Identifies flat sedimented channel floors bounded by steep canyon walls (`port_wall`, `stbd_wall`) and flags water-column or wall-sidelobe outliers relative to the modal depth.
4. **Isolated Sounding Removal (`filter_lonely_soundings`):** Flags soundings that lack valid unflagged neighbors in a local $3 \times 3$ (beam $\times$ ping) neighborhood.

---

## Key Functions

| Function | Signature | Description |
|---|---|---|
| `get_mode` | `int get_mode()` | Bins all unflagged soundings (`box[j][i] > 0.0`) across `SE_NO_SWATHS` (100 pings) into 0.5 m depth bins up to 200.0 m (`400` bins). Adds temporal hysteresis (`25 * SE_NO_SWATHS / 2`) at `last_modal_depth` to stabilize tracking from block to block. Sets `modal_depth` if the peak bin count exceeds `25 * SE_NO_SWATHS`. |
| `detrench` | `int detrench()` | Detects and flags deep sector-boundary trench artifacts between `detrench_port_sector` (default `+20°`) and `detrench_stbd_sector` (default `-20°`) by fitting a local least-squares line to flanking beams outside the sector transition zone. |
| `depowell` | `int depowell()` | Finds the port and starboard sediment-to-wall boundaries (`port_boundary[i]`, `stbd_boundary[i]`) where at least 3 consecutive beams fall within $\pm 1\%$ of `modal_depth`, applies a 7-ping median filter along-track, computes the standard deviation over the flat floor, and flags outliers exceeding `SDmultiplier * std_dev`. |
| `filter_lonely_soundings` | `int filter_lonely_soundings()` | Scans every valid sounding `(beam_counter, ping_counter)` across all 100 swaths, counts valid neighbors in the adjacent ping/beam window, and flags soundings with fewer than `min_num_neighbours` (`1`). |

---

## Algorithms & Data Structures

### 1. Sector-Boundary Detrenching (`detrench`)
Multi-sector multibeam sonars frequently exhibit systematic deep spikes or narrow "trenches" at the angular transition between transmit sectors. For each ping `i` (`0 .. SE_NO_SWATHS - 1`), `detrench()` performs the following steps:
1. **Sonar-Relative Angle Computation:** Converts each beam's depth `box[j][i]` and across-track offset `offsets[j][i]` to transducer-relative coordinates by subtracting the vessel lever arms (`parameters[current_file].sonar[0].Zloc - WLZ` and `Yloc`):
   $$\theta = -\arctan\left(\frac{\text{offset}}{\text{depth}}\right) \cdot \frac{180}{\pi}$$
   where positive angles are to port and negative angles are to starboard.
2. **Sector Window Identification:** Locates the beam index range `[port_beam, stbd_beam]` spanning the angular sector `[detrench_port_sector, detrench_stbd_sector]` (visualized in `SE_mainwin` when `show_detrench_sector` is toggled).
3. **Flanking Least-Squares Fit:** Collects up to 10 valid beams immediately port of `port_beam` (`port_beam - 10 .. port_beam`) and 10 valid beams immediately starboard of `stbd_beam` (`stbd_beam .. stbd_beam + 10`), excluding the trench zone itself. If at least 6 valid flanking beams exist, `do_least_squares()` computes the linear seafloor trend (`intercept`, `slope`) and residual standard deviation (`fit = sqrt(variance)`).
4. **Topography Guard & Outlier Flagging:** If `fit > 1.0` m, the algorithm aborts for that ping to avoid clipping genuine rough topography (such as ice scours or bedrock ridges). Otherwise, any beam `j` inside `[port_beam, stbd_beam]` whose measured depth is deeper than the fitted line by more than `SDmultiplier * fit` (`depth_diff = fitted_depth - measured_depth > SDmultiplier * fit`) is flagged by negating `box[j][i] = -box[j][i]` and incrementing the undo bitmask `box_flags[j][i]++`.

### 2. Canyon Floor / Reservoir Filtering (`get_mode` & `depowell`)
Developed during the May 2005 Lake Powell survey, `get_mode()` and `depowell()` work together when `using_powell` is active:
- `get_mode()` establishes the flat floor reference depth `modal_depth`.
- `depowell()` marches inward from port (`j = 0`) and starboard (`j = loaded_beams[i] - 1`) until `min_count = 3` beams fall within $1\%$ of `modal_depth`, defining `port_boundary[i]` and `stbd_boundary[i]`.
- A 7-point running median (`qsort` with `int_compare`) smooths `port_boundary` and `stbd_boundary` across pings (`filt_port_boundary`, `filt_stbd_boundary`).
- Between the walls, soundings deviating from `modal_depth` by more than `SDmultiplier * std_dev` are flagged; outside the boundaries (on the steep canyon walls), soundings deeper than `modal_depth + SDmultiplier * std_dev / 2.0` (e.g., wall multipath/sidelobe echoes punching below the sediment floor) are rejected while preserving shoaler wall returns.

---

## Integration within `swathed`
- **Startup & Batch Pre-Filtering:** Invoked from [`SE_omgIOwin.c`](SE_omgIOwin.md) (`prime_array`) when `-pre_detrench` (`predetrench`) is specified on the `swathed` command line.
- **Interactive Hotkeys & Main Window Display:** Controlled via keyboard shortcuts in [`SE_event_loop.c`](SE_event_loop.md) and visualized in [`SE_mainwin.c`](SE_mainwin.md) (`graphic_window[1]`), which draws the shaded polygon sector bounds when `show_detrench_sector` is active and `[` / `]` wall indicators when `using_powell` is enabled.
- **Undo Support:** All four filter routines increment `box_flags[j][i]` and `some_flagged`, allowing interactive reversal via `undo()` in [`SE_mainwin.c`](SE_mainwin.md) and persistent write-back via `dump_array()` in [`SE_omgIOwin.c`](SE_omgIOwin.md).
