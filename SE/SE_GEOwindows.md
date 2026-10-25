---
layout: default
title: SE_GEOwindows
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 9
tool_name: SE_GEOwindows
source_path: code/SE/SE_GEOwindows.c
category: Interactive QC & Editing (SwathEd)
input_formats:
- .r4
- .8bit
- .mos
- .merged
- .merged.100_ping_bounds
- .merged.global_bounds
- .lookup
- .cleaned_areas
- .tgt
output_formats:
- .lookup
- .cleaned_areas
- .tgt
related_tools:
- swathed
- SE_TOOLBOXwin
- SE_2Dwindow
- SE_PATCHwin
- SE_BSwindow
- getBounds
- jview
---

# `SE_GEOwindows` — Geographic Coverage & Sub-Area Map Windows

`SE_GEOwindows` (`code/SE/SE_GEOwindows.c`, `code/SE/SE_GEOwindows.h`) manages the geographic map windows in [`swathed`](swathed.html): the full-area overview window (`sub_window[1]`, titled `"Terrain Coverage : <grid>"` or `"Geographic Coverage"`) and the zoomable sub-area window (`sub_window[2]`, titled `"sub_area"`). Authored by John E. Hughes Clarke (July 1999), it links georeferenced gridded bathymetry (`.r4`) and sidescan/backscatter mosaics (`.8bit`/`.mos`) directly to multibeam survey lines (`.merged`), supporting spatial ping lookup, sun-illuminated relief generation, corridor selection for [`SE_2Dwindow`](SE_2Dwindow.html) and [`SE_PATCHwin`](SE_PATCHwin.html), and target/cleaned-box tracking.

---

## Window Architecture & Initialization

* **`sub_window[1]` (Main Geographic Overview):**
  * Initialized by `setup_main_area()` when `-locate <grid.r4>` is passed on the command line, or by `setup_blank_area()` when clicking the `geo` icon (`icon_window[14]`) without a background grid (sizing the map bounds automatically from `.global_bounds` files via `check_global_bounds()`).
  * Supports standard buffered file I/O (`read_farray`) or memory-mapped I/O (`mmap_farray` when `-nmap` / `use_nmap` is enabled) for large `.r4` grids, plus up to 50 co-registered `.8bit` sidescan mosaics (`ss_image[]`) loaded via `load_images()`.
* **`sub_window[2]` (Zoomed Sub-Area Window):**
  * Created dynamically by `view_subimage(left, right, bottom, top)` when the user drags a left-mouse rubber-band box in `sub_window[1]`.
  * Scaled up to 400×400 pixels with optional bilinear interpolation (`smooth_sub_area()` when `smooth_flag` is active) and panned in half-window increments via `shift_subimage(dir)` using arrow keys.

---

## Core Subsystems & Algorithms

### 1. Synthetic Sun-Illuminated Relief (`setup_sunmap`)
When displaying a `.r4` bathymetric grid, `setup_sunmap()` computes a shaded-relief byte array (`sun_array`) controlled interactively by [`SE_TOOLBOXwin`](SE_TOOLBOXwin.html):
* Evaluates local east-west and north-south depth gradients (`dz/dx`, `dz/dy`), scales them by vertical exaggeration (`exag`), and computes the surface normal dot product against the illumination vector defined by `azi` ($0^\circ, 90^\circ, 180^\circ, 270^\circ$) and `elev` ($0^\circ\text{–}90^\circ$).
* Depending on `colormap_flag` (`SUN`, `DEPTH`, or `SS_IMAGE`), `prime_main_area()` and `prime_sub_area()` blend depth hue and sun-illumination intensity into 8-bit/24-bit XImage buffers (`main_image`, `sub_image`).

### 2. Spatial Ping Lookup Table (`set_up_LUT` & `<prefix>.lookup`)
To allow instant middle-click jumping from any pixel on the map to the corresponding survey file and ping number:
* `set_up_LUT()` allocates a 32-bit integer array `ref_table` matching the pixel dimensions of `sub_window[1]`.
* If `<grid_prefix>.lookup` exists on disk (`-lookup`), it reads the precomputed table; otherwise, it iterates through all loaded `.merged` files (`no_in`), projects each ping's nadir coordinate (`profile.latitude`, `profile.longitude`) via `proj()`, and packs `(file_no << 16) + ping_no` into `ref_table`, saving `<grid_prefix>.lookup` for subsequent sessions.
* Middle-clicking (`Button2`) in `sub_window[1]` or `sub_window[2]` searches a 7×7 pixel spiral (`search[49][2]`) around the cursor in `ref_table`, unpacks `file` and `recno`, and loads the 80-swath block centered on that ping.

### 3. Spatial Indexing & Corridor Overlays
* **Fast Bounding-Box Culling (`check_swath_in_area`, `check_random_in_area`):** Reads `<line>.merged.100_ping_bounds` (`swath_bounds`) to test whether 100-ping segments intersect a geographic sub-box before reading full `.merged` records.
* **Rotatable Corridor Box (`plot_rot_box`):** Renders the oriented rectangular corridor (`Ecen`, `Ncen`, `rect_width`, `rect_height`, `rect_angle`) used by [`SE_2Dwindow`](SE_2Dwindow.html), [`SE_BSwindow`](SE_BSwindow.html), and [`SE_PATCHwin`](SE_PATCHwin.html), drawing the viewing-direction arrow (`NORTH`, `SOUTH`, `EAST`, `WEST`) and slice bounds.
* **Cleaned Area & Target Overlays:**
  * `load_cleaned()` and `dump_cleaned()` read/write `<prefix>.cleaned_areas`, rendering completed editing sub-boxes in red on `sub_window[1]` (marked via `c` in `sub_window[2]`, cleared via `n`).
  * `load_targets()`, `add_target()`, `write_targets()`, and `load_vectbin()` overlay point targets (`.tgt` / target files) and binary coastline/contour vectors on both map windows.

---

## Interactive Mouse & Keyboard Controls

| Window | Input | Action |
| :--- | :--- | :--- |
| `sub_window[1]` | **Left-drag** | Rubber-band a geographic sub-area and open/update `sub_window[2]` (`view_subimage()`). |
| `sub_window[1]` / `[2]` | **Middle-click** | Query `ref_table` (5-pixel radius) and load the nearest survey line and ping into `swathed`; print cursor Lat/Lon to terminal. |
| `sub_window[2]` | **Left-click** / **Right-click** | When `2D`, `Class`, or `Patch` is active, repositions the corridor center (`Ecen`, `Ncen`) or rotates `rect_angle` toward the cursor. |
| `sub_window[2]` | **Arrow keys** | Pan `sub_window[2]` North, South, East, or West by half the sub-window span (`shift_subimage()`). |
| `sub_window[2]` | `[` / `]` | Narrow or widen the corridor width (`rect_width`) for 2D/Patch/BS analysis. |
| `sub_window[2]` | `c` / `n` | Mark the current sub-area as cleaned (`dump_cleaned()`) / clear all cleaned sub-area boxes. |
| `sub_window[1]` / `[2]` | `t` / `w` | Jump to the closest acoustic target (`.tgt`) near the cursor (`t`) or write updated targets to disk (`w`). |
