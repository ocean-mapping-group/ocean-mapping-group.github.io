---
layout: default
title: SE_BDI_DP
parent: SwathEd (SE) Tools
nav_order: 7
tool_name: SE_BDI_DP
source_path: code/SE/SE_BDI_DP.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", ".watercol"]
output_formats: []
related_tools: ["swathed", "SE_WaterColumn", "SE_PDI_LA", "applyBDI", "bdi_funcs"]
---

# `SE_BDI_DP` — Bottom Detection Indicator (BDI) Track Toolkit

`SE_BDI_DP` (`code/SE/SE_BDI_DP.c`, `code/SE/SE_BDI_DP.h`) is an interactive X11 diagnostic widget integrated into [`swathed`](swathed.md) and [`SE_WaterColumn`](SE_WaterColumn.md). Developed by Douglas Bergersen (M.Sc. thesis, 2014–2015) and John E. Hughes Clarke, it provides a real-time environment (`"BDI Track Toolkit"`) for testing, visualizing, and tuning Beam-to-Beam Amplitude Derivative / Parabola Peak-Picking Bottom Detection Indicator (BDI) algorithms across multibeam water column time slices (`j_EM_watercolumn`).

Unlike standard ray-along-beam amplitude/phase bottom detection, the BDI method operates orthogonally across constant two-way travel time (TWTT) arcs—locating local intensity maxima across receive beam pointing angles at each range sample.

---

## Architecture & X11 Widget Layout

`make_BDI_DP_widget()` constructs the `BDI_DP_widget` (`jX_widget` structure) with 2 stacked 800×200 pixel graphics canvases, 4 parameter sliders, and 12 algorithm-selection buttons:

### Graphics Windows
* **Graphic 0 (`draw_BDI_DP_graphic0` — `# BDI SOLUTIONS versus BEAM NUMBER`):**
  * Plots a histogram of detected BDI candidate peaks per physical beam index (`0` to `total_no_receive_beams`) for the active swath (`selected_swath`).
  * Color-codes beam bins by transmit sector (`Tx_sector_no`: Red, Green, Yellow, Blue) and overlays a vertical Magenta cursor at `selected_beam`.
  * Displays total candidate solutions (`count_Total`) and per-sector detection counts (`count_Sector0..3`), plus the active compressed/uncompressed water column byte footprint (`compressed_time_angle_image_size`).
* **Graphic 1 (`draw_BDI_DP_graphic1` — `dB versus TIME SLICE`):**
  * Plots peak acoustic intensity (dB, `-80` to `0` dB) as a function of water column time slice (`0` to `MAX_length_WC_TimeSeries`, up to 1500 samples).
  * Renders three statistical envelopes across each time slice: **Highest Peak** (`GREEN`), **Mean Peak** (`BLUE`), and **Lowest Peak** (`RED`), alongside the active **Variable Threshold** curve (`WC_BDI_variable_threshold_graphic`, `YELLOW`) and a vertical Magenta cursor at `selected_WC_TWTT`.

### Interactive Sliders
| Slider Index | Label | Range | Backing Variable | Description |
| :--- | :--- | :--- | :--- | :--- |
| `0` | `BDI Threshold (dB)` | `-40.0` .. `30.0` | `WC_BDI_threshold` (int) | Base amplitude threshold (in 0.5 dB steps) required for a time-slice peak to qualify as a BDI candidate. |
| `1` | `Threshold Slope (*10)` | `-15.0` .. `15.0` | `WC_BDI_slope` (int) | Linear range-dependent slope ($\times 10^{-2}$ dB/sample) applied after the first-arrival sample (`R0`) when using manual variable thresholding. |
| `2` | `Filter Index` | `2.0` .. `12.0` | `BDI_filter_index` (int) | Controls the half-width (`BDI_filter_index - 1`) of the moving-average boxcar filter applied across beams or time slices. |
| `3` | `# Virtual Beams` | `400.0` .. `800.0` | `No_virtual_beams` (int) | Number of interpolated virtual beam angles used when resampling non-equidistant beam pointing angles prior to parabola fitting. |

### Control Buttons
| Button | Label | Action / Algorithm Mode |
| :--- | :--- | :--- |
| `0`–`3` | `MT 3Pt PBL 1pk` / `2pk`, `MT 5Pt PBL 1pk` / `2pk` | Selects **Manual Threshold (MT)** mode (`threshold_method = 1`) with 3-point or 5-point parabolic peak interpolation (`parabola_pts = 3` or `5`), retaining either the single highest peak (`1pk`) or top two peaks (`2pk`) per transmit sector at each time slice (`choose_BDI_method = 1..4`). |
| `4`–`7` | `AT 3Pt PBL 1pk` / `2pk`, `AT 5Pt PBL 1pk` / `2pk` | Selects **Automatic Threshold (AT)** mode (`threshold_method = 2`), deriving an adaptive per-slice noise floor from the mean and standard deviation of across-beam intensities (`choose_BDI_method = 5..8`). |
| `8` | `Manual Filter` | Enables boxcar smoothing using the manual `BDI_filter_index` slider (`filter_method = 1`) and triggers `WC_BDI_pick_Angle_Peaks()`. |
| `9` | `Aut Filter` | Enables automatic filter window sizing (`filter_method = 2`) and re-runs peak picking. |
| `10` | `Compress Data` | Toggles in-memory wavelet/DCT water column compression (`compress_flag`, calling `compress_watercolumn()`) to evaluate BDI sensitivity to lossy water column compression. |
| `11` | `MT Closest Beam` | Selects Manual Threshold mode (`choose_BDI_method = 9`) snapping candidate peaks to the nearest physical beam center without parabolic sub-beam interpolation. |

---

## Core Algorithms & Data Structures

* **`BDI` Candidate Structure (`SE_BDI_DP.h`):**
  * Each time slice $i \in [0, 1499]$ stores up to `NO_BDI` (12) detections in `WC_BDI_pick[1500][NO_BDI]`, recording `intensity` (0.5 dB units), `angle` (interpolated pointing angle in degrees), `beam` (nearest physical beam index), and `sector` (transmit sector ID).
* **Across-Beam Peak Picking (`WC_BDI_pick_Angle_Peaks`):**
  * Delegates core mathematical processing to `standalone_BDI_pick_Angle_Peaks()` (defined in [`bdi_funcs.c`](bdi_funcs.md)), passing the active `WHOLE_ping_WC[SIDE_TO_VIEW][swath]` structure, threshold/slope parameters, parabola stencil size, and virtual beam count.
  * When displayed inside [`SE_WaterColumn`](SE_WaterColumn.md) (`show_BDI` and `plot_BDI`), each valid `WC_BDI_pick[i][j].angle` is projected into across-track/depth space $(x = -R\sin\theta, z = R\cos\theta)$ and rendered as a blue cross over the polar water column fan.

---

## Keyboard Shortcuts & Interactive Workflow

1. **Launch:** Click the **`BDI Track`** button (`button[11]`) inside the [`SE_WaterColumn`](SE_WaterColumn.md) toolkit to map `BDI_DP_widget`.
2. **Navigate Swaths, Beams & Time Slices:**
   * `Left` / `Right` arrows: Step `selected_beam` port or starboard and refresh both BDI plots and the main water column display.
   * `Up` / `Down` arrows: Step `selected_swath` forward or backward within the 80-ping block.
   * Left-click in Graphic 0 selects `selected_beam`; left-click in Graphic 1 selects `selected_WC_TWTT` and updates the across-beam angle series in `SE_WaterColumn`.
   * `b`: Toggles `plot_BDI` overlay in the main water column polar fan and across-beam slice plots.
   * `q`: Unmaps and closes the `BDI Track Toolkit` window.
