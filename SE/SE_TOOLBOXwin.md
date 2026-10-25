---
layout: default
title: SE_TOOLBOXwin
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 16
tool_name: SE_TOOLBOXwin
source_path: code/SE/SE_TOOLBOXwin.c
category: Interactive QC & Editing (SwathEd)
input_formats: []
output_formats: []
related_tools:
- swathed
- SE_GEOwindows
- SE_WaterColumn
- SE_AnandBS
- jview
---

# `SE_TOOLBOXwin` — Color Palette Stretch & Synthetic Sun-Illumination Control Box

`SE_TOOLBOXwin` (`code/SE/SE_TOOLBOXwin.c`, `code/SE/SE_TOOLBOXwin.h`) implements the compact `"tool_box"` window (`sub_window[3..11]`) in [`swathed`](swathed.html). Authored by John E. Hughes Clarke (April/July 1999), it provides real-time interactive control over X11 color/greyscale look-up tables (`col_min`, `col_max`, `grey_flag`, `col_1_flag`) and synthetic sun-illumination geometry (`azi`, `elev`, `exag`, `colormap_flag`) shared across [`SE_GEOwindows`](SE_GEOwindows.html), [`SE_WaterColumn`](SE_WaterColumn.html), [`SE_AnandBS`](SE_AnandBS.html), and the main `swathed` amplitude map (`graphic_window[5]`).

---

## Window Hierarchy & Controls (`sub_window[3..11]`)

`view_toolbox()` creates top-level container `sub_window[3]` (`174 × 114` px) positioned in the upper-right corner of the screen, containing a 256-level color bar (`sub_window[4]`), three interactive vector dials (`sub_window[5..7]`), and four mode-selection buttons (`sub_window[8..11]`):

| Sub-Window | Dimensions | Widget Role | Backing Variables & Visual Representation |
| :--- | :--- | :--- | :--- |
| `sub_window[4]` | `162 × 20` | **256-Level Palette Bar** | Renders the active 256-entry colormap (`lut[0..255]`) across $x \in [0, 255]$. Left-click sets `col_min`; right-click sets `col_max`, dynamically stretching contrast via `do_colormap(EIGHT_PLUS)`. |
| `sub_window[5]` | `50 × 50` | **Sun Azimuth Dial (`azi`)** | Draws a circular compass rose (`jhc_circle`) and a yellow ray vector from the origin to $(\sin(\text{azi}), \cos(\text{azi}))$. Clicking snaps `azi` to cardinal directions ($0^\circ, 90^\circ, 180^\circ, 270^\circ$) and triggers `setup_sunmap()`. |
| `sub_window[6]` | `50 × 50` | **Vertical Exaggeration Dial (`exag`)** | Draws an ellipse (`jhc_ellipse`) whose horizontal/vertical aspect ratio (`rx = 0.05 + 0.90/exag`, `ry = 0.90`) reflects the current terrain vertical exaggeration factor (`exag`). |
| `sub_window[7]` | `50 × 50` | **Sun Elevation Quadrant (`elev`)** | Draws a $0^\circ\text{–}90^\circ$ quarter-circle arc and a yellow ray at angle `elev` ($\arctan(y/x)$). Clicking updates `elev` and recalculates `setup_sunmap()`. |
| `sub_window[8]` | `36 × 20` | **`SUN` Button** | Sets `colormap_flag = SUN` (`grey_flag = 1`, `col_1_flag = 0`), rendering synthetic sun-illuminated relief in [`SE_GEOwindows`](SE_GEOwindows.html) (`sub_window[1]` and `[2]`). |
| `sub_window[9]` | `42 × 20` | **`DEPTH` Button** | Sets `colormap_flag = DEPTH` (`grey_flag = 0`, `col_1_flag = 1`), rendering color-coded bathymetry in `sub_window[1]` and `[2]`. |
| `sub_window[10]` | `42 × 20` | **`IMAGE` Button** | Sets `colormap_flag = SS_IMAGE` and cycles `current_ss` through loaded `.8bit`/`.mos` sidescan mosaics (`ssname[current_ss]`) in `sub_window[1]` and `[2]`. |
| `sub_window[11]` | `30 × 20` | **`COL` / `GREY` Toggle** | Toggles between rainbow color (`col_1_flag = 1`, `"COL"`) and linear greyscale (`grey_flag = 1`, `"GREY"`), resetting `col_min = 0` and `col_max = 255`. |

---

## Core Functions (`SE_TOOLBOXwin.c`)

* **`view_toolbox()`:**
  * Queries screen dimensions (`DisplayWidth`, `DisplayHeight`), creates `sub_window[3..11]` via `jMOD_XCreateSimpleWindow()`, assigns `NorthWestGravity` (`CWWinGravity`), registers `KeyPressMask`, `ButtonPressMask`, `EnterWindowMask`, `LeaveWindowMask`, and `ExposureMask` events, and applies `new_cmap`.
* **`refresh_toolbox_windows(Window the_window)`:**
  * Redraws the requested sub-window (`sub_window[4..11]`).
  * In `sub_window[4]`, iterates $i \in [0, 255]$ and draws vertical color bars using `jhc_fill_rect(-4, i, 0, i+1, 1, lut[i])`.
  * In `sub_window[5..7]`, draws geometric dial indicators for `azi`, `exag`, and `elev` using `jhc_circle()`, `jhc_ellipse()`, and `jhc_line()`.
  * In `sub_window[8..11]`, renders centered button labels (`"SUN"`, `"DEPTH"`, `"IMAGE"`, `"COL"`/`"GREY"`), highlighting buttons in `YELLOW` on cursor `EnterNotify`.

---

## Integration Across `swathed` Modules

Whenever the operator adjusts `col_min` (Left-click in `sub_window[4]`), `col_max` (Right-click in `sub_window[4]`), or `COL`/`GREY` (`sub_window[11]`), `process_x_events()` in [`SE_event_loop.c`](SE_event_loop.html) calls `do_colormap(EIGHT_PLUS)` (`SE_generic.c`) and immediately propagates the updated palette across all active TrueColor / PseudoColor image views:
1. **Main Swath Editor:** Refreshes `graphic_window[5]` (the 80-swath plan-view backscatter amplitude panel).
2. **Geographic Maps ([`SE_GEOwindows`](SE_GEOwindows.html)):** Calls `refresh_maingeo_window()` (`sub_window[1]`) and `refresh_sub_geo_window()` (`sub_window[2]`), or recalculates the shaded-relief array via `setup_sunmap()` when `azi` (`sub_window[5]`) or `elev` (`sub_window[7]`) is clicked.
3. **Water Column Toolkit ([`SE_WaterColumn`](SE_WaterColumn.html)):** Redraws the active polar water column fan (`draw_WaterColumn()`) or 2D along-track curtain (`draw_WC2D()`) using the stretched lookup table.
4. **Backscatter Snippet Toolkit ([`SE_AnandBS`](SE_AnandBS.html)):** Redraws the greyscale beam time-series waterfall (`draw_beam_trace()`).
