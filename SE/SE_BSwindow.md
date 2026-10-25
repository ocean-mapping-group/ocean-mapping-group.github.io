---
layout: default
title: SE_BSwindow
parent: SwathEd (SE) Tools
nav_order: 8
tool_name: SE_BSwindow
source_path: code/SE/SE_BSwindow.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", ".merged.100_ping_bounds", ".r4", ".8bit", ".ss"]
output_formats: ["BS_plot"]
related_tools: ["swathed", "SE_AnandBS", "SE_GEOwindows", "SE_2Dwindow", "make_mos"]
---

# `SE_BSwindow` — Backscatter Angular Response & Classification Tool

`SE_BSwindow` (`code/SE/SE_BSwindow.c`, `code/SE/SE_BSwindow.h`) is the classic X11 `"Backscatter Classification Tool "` in [`swathed`](swathed.md), authored by John E. Hughes Clarke (April 1999). It extracts per-beam seabed backscatter amplitudes (`beams[j].reflectivity`) and plots grazing angle ($0^\circ\text{–}90^\circ$) versus backscatter strength ($\text{dB}$, `0` to `-70` dB), enabling interactive evaluation of radiometric and geometric corrections (seafloor slope, inverse Lambert's law, spherical vs. aspherical spreading, insonified area, and ray refraction).

> **Note:** In recent `swathed` builds (`SE_event_loop.c`, March 2024), clicking the `Class` icon (`icon_window[10]`) defaults to launching the expanded [`SE_AnandBS`](SE_AnandBS.md) toolkit (`show_ABS`), while `SE_BSwindow` remains compiled and accessible for sub-area and subset angular response inspection.

---

## Window Hierarchy & Controls (`sub_window[35..42]`)

`view_BSbox()` creates top-level window `sub_window[35]` (`"Backscatter Classification Tool "`), containing main plotting canvas `sub_window[36]` (`BS_WIDTH` $\times$ `BS_HEIGHT` = 300×300 px) and 6 interactive control buttons (`sub_window[37..42]`):

| Sub-Window | Button States | Backing Flag / Function | Description |
| :--- | :--- | :--- | :--- |
| `sub_window[36]` | *(Main Plot Canvas)* | `refresh_BS_windows()` | Plots grazing angle ($0^\circ$ at right to $90^\circ$ normal incidence at left) vs. dB (`0` at top to `-70` dB at bottom), individual beam scatter points, 1° binned mean curve `Av_bs[90]`, and Simrad empirical model curves (`BSn`, `BSo`, `Xover`). |
| `sub_window[37]` | `flat` / `slopecorr` | `flat_seafloor` | Toggles between assuming a flat horizontal seafloor (`flat_seafloor = 1`) and computing true 3D local seafloor slope (`flat_seafloor = 0`) from across-track (`atan2(dz, dy)`) and along-track (`atan2(dz, dx)`) depth gradients. |
| `sub_window[38]` | `Lambert` / `No Lambert` | `apply_inverse_Lambert_flag` | Toggles removal of the Simrad real-time Lambertian/normal-incidence TVG model (`BSn`, `BSo`, `Xover`) via `remove_Simrad_Lambert()` to recover true un-normalized backscatter strength. |
| `sub_window[39]` | `Aspher.` / `Spher.` | `use_asph` | Toggles spherical vs. aspherical spreading loss compensation (`asph_range`) using the user-adjustable refraction/spreading scale factor (`asph`, tuned with `+`/`-` keys). |
| `sub_window[40]` | `Real Inson.` / `Flat Inson` | `corr_inson` | Toggles correction for true pulse-limited and beam-limited insonified area on a sloping seabed vs. flat-bottom nominal insonified area. |
| `sub_window[41]` | `Print` | `print_BS()` | Exports the 1°-binned mean angular response curve (`Av_bs[k]`) to an ASCII file named `BS_plot` in the current working directory. |
| `sub_window[42]` | `Refract` / `No Refract` | `use_refract` | Toggles ray-bending grazing angle adjustment (`ref_flat_GA` vs. `noref_flat_GA`). |

---

## Data Extraction Modes & Algorithms

### 1. Geographic Sub-Area Mode (`get_BS_profiles_inarea`)
When a `.r4` locator grid (`locr4_flag`) and geographic `sub_area` window (`sub_window[2]`) are active:
* `get_BS_profiles_inarea(left, right, bottom, top)` scans `.100ping_bounds` files via `check_swath_in_area()` to identify survey lines and 100-ping blocks intersecting the rotatable geographic corridor (`Ecen`, `Ncen`, `rect_width`, `rect_height`, `rect_angle`).
* Up to `MAX_BS_PROFILES` (1000) swaths (`BS_profile[]`, `BS_beams[][]`) are loaded into memory.
* For every beam falling inside the rotated bounding box, it computes:
  * **Flat-bottom refracted grazing angle (`ref_flat_GA`):** Derived from observed depth and across-track distance, corrected for vessel roll and sound speed profile ray bending.
  * **Flat-bottom unrefracted grazing angle (`noref_flat_GA`):** Derived directly from the beam depression angle (`beam_depress_angle`).
  * **True 3D slope-corrected grazing angle (`true_GA` / `noref_slope_GA`):** Computes unit vectors along the incoming acoustic ray ($\mathbf{a}$) and the local seafloor surface normal ($\mathbf{b}$, formed from adjacent beam and ping depth differences) and evaluates $\theta_g = 90^\circ - \arccos(\mathbf{a}\cdot\mathbf{b})$.

### 2. Swath Subset Mode (`get_beam_in_subset`)
When launched without a `.r4` grid (or via rubber-band selection in `graphic_window[5]`), `get_beam_in_subset(start_beam, end_beam, start_swath, end_swath)` extracts beam backscatter directly from the active 80-swath editing buffer.

### 3. Simrad Model Inversion (`remove_Simrad_Lambert`)
Simrad multibeam echosounders normalize raw echo levels using a piecewise model parameterized by normal-incidence backscatter ($BS_n$), oblique backscatter ($BS_o$), and crossover angle ($\theta_x = \text{Xover}$):
* Above $\theta_g > 90^\circ - \theta_x$, the sonar assumes a linear roll-off between $BS_n$ and $BS_o$.
* Below $\theta_g \le 90^\circ - \theta_x$, the sonar assumes a $\sin^2(\theta_g)$ Lambertian dependence.
* When `apply_inverse_Lambert_flag` is enabled (or when interactive sliders/keys adjust `BSn`, `BSo`, `Xover`, and `Atten_Gain`), `refresh_BS_windows()` adds the forward model back to the recorded residual (`reflectivity * 0.5` dB) and recomputes the 1° average curve `Av_bs[0..89]`.
