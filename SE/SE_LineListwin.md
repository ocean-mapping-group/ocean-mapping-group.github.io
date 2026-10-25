---
layout: default
title: SE_LineListwin
parent: SwathEd (SE) Tools
nav_order: 10
tool_name: SE_LineListwin
source_path: code/SE/SE_LineListwin.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged"]
output_formats: [".done", "selected_files.list"]
related_tools: ["swathed", "SE_GEOwindows", "SE_2Dwindow", "SE_PATCHwin"]
---

# `SE_LineListwin` — Survey Line Selection & Activation Window

`SE_LineListwin` (`code/SE/SE_LineListwin.c`, `code/SE/SE_LineListwin.h`) implements the `"Survey Line Selection/Activation Window"` (`sub_window[57]` and `sub_window[58]`) in [`swathed`](swathed.md). Originally written by John E. Hughes Clarke (July 1999) and updated with multi-page pagination by Jonathan Beaudoin (February 2011), it provides a visual dashboard for managing up to hundreds of loaded `.merged` survey lines—allowing the operator to switch the active editing line, toggle which lines participate in 2D/Patch/Backscatter sub-area plots, and mark lines as completed.

---

## Window Layout & Visual Status Indicators

Clicking the **`Lines`** icon (`icon_window[12]`) on the main `swathed` toolbar calls `view_useprof_box()`, which creates top-level container `sub_window[57]` (`400 × 610` px) and drawing canvas `sub_window[58]`.

`refresh_useprof_window()` paginates the loaded survey lines (`no_in`) into pages of `MAX_NUM_LINES_IN_LIST` (`30`) lines per page (`line_list_page_number` of `num_line_list_pages`). Each row $i$ displays four visual fields across the horizontal coordinate range $x \in [0, 100]$:

| Horizontal Column | Visual Element | Meaning & Backing State |
| :--- | :--- | :--- |
| $x \in [0, 20]$ | **Line Color Swatch** | Filled rectangle drawn in `LINE_COLOUR(i)`—the unique color assigned to line $i$ when plotting soundings by survey line in [`SE_2Dwindow`](SE_2Dwindow.md) (`D2_BY_FILE`) or [`SE_PATCHwin`](SE_PATCHwin.md). |
| $x = 20$ | **Completion Marker (`"X"`)** | Drawn in `BLACK` if `done_status[i]` is non-zero (indicating `<line>.done` exists or the line was marked finished with the `d` key). |
| $x \in [25, 85]$ | **Active / Area Background Bar & Filename** | Background bar colored **`MAGENTA`** if $i == \text{current\_file}$ (the line currently loaded in the 80-ping editor), **`BLUE`** if `in_area[i]` is set (the line intersects the active 2D/Patch/BS geographic sub-area), or **`CYAN`** otherwise. Prints either the basename (`mem_basename(inname[i])`) or full path (`inname[i]` when `plot_line_list_paths` is enabled). |
| $x \in [85, 100]$ | **Enable/Disable Toggle Box** | Filled **`GREEN`** if `use_status[i] == 1` (line is enabled for sub-area 2D, Patch Test, and Geographic trackline display) or **`RED`** if `use_status[i] == 0` (line is excluded). |

At the bottom of `sub_window[58]`, a status footer displays `"Page %d of %d (use left/right arrows to change page)"`.

---

## Core Functions (`SE_LineListwin.c`)

* **`view_useprof_box()`:**
  * Computes `num_line_list_pages = ceil((float)no_in / MAX_NUM_LINES_IN_LIST)` (`30` lines per page) and initializes `line_list_page_number = 1`.
  * Creates `sub_window[57]` (`400 × 610` px) and `sub_window[58]` (`394 × 604` px) with `y_min = MAX_NUM_LINES_IN_LIST + 1` at the bottom and `y_max = 0` at the top so row index `(int)ry` increases downward.
* **`refresh_useprof_window(Window the_window)`:**
  * Determines `start_line = (line_list_page_number - 1) * MAX_NUM_LINES_IN_LIST` and `end_line`, then renders each line's color swatch (`LINE_COLOUR(i)`), `"X"` completion status (`done_status[i]`), active/in-area bar (`current_file` vs. `in_area[i]`), filename (`plot_line_list_paths`), and enable/disable indicator (`use_status[i]`).

---

## Interactive Controls & Workflows

All mouse and keyboard interactions inside `sub_window[58]` are dispatched by `process_x_events()` in [`SE_event_loop.c`](SE_event_loop.md):

| Input in `sub_window[58]` | Action |
| :--- | :--- |
| **Left-click (`Button1`)** | Saves any pending flag edits in the current line (`dump_array()`), sets `current_file` to the clicked row, opens the selected `.merged` file (`start_file()`), and loads its swaths into the main `swathed` editing windows (`prime_array()`). |
| **Right-click (`Button3`)** | Toggles `use_status[i]` between `1` (Green/enabled) and `0` (Red/disabled) for the clicked survey line, then automatically refreshes `sub_window[1]`, `sub_window[2]`, [`SE_2Dwindow`](SE_2Dwindow.md) (`sub_window[23]`), and [`SE_PATCHwin`](SE_PATCHwin.md) (`sub_window[44]`) so excluded lines immediately disappear from multi-line overlays. |
| **`i` key** | Calls `invert_use_status()` (`SE_generic.c`) to invert the enabled/disabled state (`use_status[i] = !use_status[i]`) of every loaded survey line simultaneously and refreshes all active geographic/2D/Patch views. |
| **`p` key** | Toggles `plot_line_list_paths` between displaying compact basenames and full filesystem paths. |
| **`d` key** | Marks the line under the cursor as completed (`done_status[file_number] = 1`), creates an empty `<line_prefix>.done` sentinel file on disk, and draws an `"X"` next to its color swatch. |
| **`l` key** | Calls `write_file_list()` to export a text list of all currently enabled (`use_status[i] == 1`) survey line filenames. |
| **`Left` / `Right` Arrow keys** | Decrements or increments `line_list_page_number` to browse through survey projects with more than 30 lines. |
