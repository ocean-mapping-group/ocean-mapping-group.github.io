---
layout: default
title: SE_SUBBOTwin
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 15
tool_name: SE_SUBBOTwin
source_path: code/SE/SE_SUBBOTwin.c
category: Interactive QC & Editing (SwathEd)
input_formats:
- .merged
- .sub
- .raw_ping
output_formats:
- .merged (updated observedDepth and race_track bottom picks)
related_tools:
- swathed
- j_sub
---

# `SE_SUBBOTwin` — Vertical Incidence & Sub-Bottom Profiler Time-Series Viewer

`SE_SUBBOTwin` (`code/SE/SE_SUBBOTwin.c`, `code/SE/SE_SUBBOTwin.h`) implements the `"Vertical Incidence Time Series Viewer"` (`sub_window[SUBBOT_OFFSET .. SUBBOT_OFFSET + 15]`, where `SUBBOT_OFFSET = 76`) in [`swathed`](swathed.html). Authored by John E. Hughes Clarke (January 2000) with manual bottom-repicking additions by Jonathan Beaudoin (November 2007), it provides a dedicated seismic/echogram waterfall, full-waveform trace inspector, 1D FFT spectral filter, and bottom-tracker editor for single-beam / dual-frequency normal-incidence and chirp sub-bottom profilers (e.g., Knudsen 320B/320M, Simrad EA500, and Kongsberg SBP120).

---

## Window Architecture & Controls (`sub_window[76..91]`)

Launched automatically when clicking the **`ss`** icon (`icon_window[7]`) on a `Knudsen_320` dataset (or via `-sub`), `view_subbottom_box()` creates top-level form `sub_window[76]` (`1025 × 820` px) containing:

### Waterfall, Trace, and Spectral Windows

| Window | Dimensions | Function | Description |
| :--- | :--- | :--- | :--- |
| `sub_window[77]` (`+1`) | `600 × 200` | `load_deci()` | **Decimated 600-Ping Echogram Overview:** Displays 600 consecutive pings (`NO_SUB_SWATHS = 600`) across the full recorded depth window (`top_depth` to `bot_depth`), marking heave (`RED`), tide (`BLUE`), and active bottom picks (`GREEN`). |
| `sub_window[78]` (`+2`) | `600 × 450` | `load_orig()` | **Full-Resolution Zoomed Echogram:** Displays a vertically zoomed window (`zoom_height` samples) across the 600 pings, either in true depth (`SHOW_BY_DEPTH`) or aligned relative to the bottom pick (`SHOW_BY_TRACE`). |
| `sub_window[79]` (`+3`) | `400 × 70` | `plot_info()` | **Ping Metadata Header:** Displays ping number, date/time (`j_time`), pulse length (`pulse_length`), frequency, gain (`Rx_gain`), and sample interval (`sample_interval`) for `selected_sub_ping`. |
| `sub_window[80]` (`+4`) | `400 × 125` | `plot_profile()` | **Full-Range Single-Ping Trace:** Plots the complete amplitude/waveform trace (`data[]` or `data_16[]`/`data_32[]`/`data_float[]`) for `selected_sub_ping`, marking the current bottom pick in `RED`. |
| `sub_window[81]` (`+5`) | `400 × 125` | `plot_profile()` | **Zoomed 8-bit Single-Ping Trace:** Plots the trace within the zoom window alongside the smoothed first-difference derivative used for bottom picking. |
| `sub_window[87]` (`+11`) | `400 × 125` | `plot_fft()` | **FFT Power Spectrum & Bandpass Filter:** Plots the 4096-point real/imaginary FFT amplitude spectrum (`0` to Nyquist kHz) of `selected_sub_ping`, with interactive frequency cutoff markers (`filter_freq[0..3]`). |
| `sub_window[88]` (`+12`) | `400 × 125` | `plot_profile()` | **16-bit / Full-Waveform Zoom Trace:** Plots signed bipolar or envelope 16-bit/32-bit/float traces (`data_16`, `data_32`, `data_float`) and filtered time-domain waveforms (`filt_trace`). |

### Interactive Sliders (`sub_window[82..85]`) & Buttons (`button_window[9..14]`)
* **Bottom-Picking Sliders (`sub_window[82..85]`):**
  * `sub_window[82]` (`Pick Thresh %`): Amplitude threshold percentage (`pick_thresh`, `0`–`100%` of trace max).
  * `sub_window[83]` (`Pick Window`): Derivative smoothing window length (`pick_win`, `1`–`50` samples).
  * `sub_window[84]` (`Pick Thresh % [deriv]`): Derivative threshold percentage (`ofwhich`, `0`–`100%`).
  * `sub_window[85]` (`Min. Pick Depth`): Minimum blanking depth (`min_pick_depth`) above which echoes are ignored.
* **Control Buttons (`button_window[SUBBOT_BUTT_OFFSET + 0..5]`):**
  * **`0` (`ByDepth` / `ByTrace`):** Toggles `sub_plot_type` between true depth and bottom-flattened display.
  * **`1` (`Marks` / `NoMarks`):** Toggles heave, tide, and bottom-pick tracking overlays (`mark_heave`).
  * **`2` (`HF` / `LF`):** Switches between High-Frequency (`CHANNEL_1`, `.sub` Channel 0) and Low-Frequency (`CHANNEL_2`, `.sub` Channel 1) transducer channels (`which_channel`).
  * **`3` (`orig.` / `repick`):** Toggles between original recorded bottom depths (`orig_depth[]`) and newly repicked depths (`new_depth[]`).
  * **`4` (`RePickAll`):** Calls `repickall()` to run automated threshold/derivative bottom picking (`pick_trace()`) across all 600 loaded pings.
  * **`5` (`Write`):** Calls `write_out_new_picks()` to write updated `observedDepth` and `race_track` two-way travel times directly back into the `.merged` file.

---

## Interactive Workflow (`manage_SUBBOTTOM_events`)

* **Left-click in `sub_window[77]` or `[78]`:** Selects `selected_sub_ping` and updates the single-ping trace and FFT spectrum plots (`calc_sub_fft()`).
* **Middle-click in `sub_window[77]`:** Centers the vertical zoom window (`sub_window[78]`) at the clicked depth.
* **Right-click in `sub_window[78]`:** Manually sets `new_depth[selected_sub_ping]` to the clicked sample depth (`JDB`, Nov 2007) for surgical correction of bottom-tracking dropouts.
* **`w` key in `sub_window[78]`:** Immediately writes modified bottom picks to the `.merged` file (`write_out_new_picks()`) and reloads the 600-ping buffer.
