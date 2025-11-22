---
layout: default
title: draw_bathy
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 8
---
# draw_bathy

## Description
`draw_bathy.c` is a Motif GUI source file responsible for drawing and updating the bathymetry display within the "Submetrix 2000 unraveller" application. It visualizes the processed bathymetry data, including depths, across-track positions, and quality indicators. The drawing is performed on an `XmDrawingArea` widget and is continuously updated to reflect changes in processing parameters or data navigation. It also presents current processing parameter values on the display for user feedback.

## How It Works
1.  **`init_bathy()` function:**
    *   Initializes the `DA10` structure (a global context for the drawing area).
    *   Retrieves the geometry of the `DrawingArea` widget (`DA10.widget`).
    *   Creates an `X Pixmap` (`DA10.pixmap`) as an off-screen buffer for drawing, which prevents flickering.
    *   Fills the pixmap with a white background.
2.  **`draw_bathy()` function:** This is the main drawing routine, called to refresh the bathymetry display.
    *   **Clear Drawing Area:** Clears the pixmap with a white or black background, depending on the `current_side` (port/starboard) and `show_raw` flag.
    *   **Axis/Grid Drawing:** Draws X and Y axes (gray lines) if the `current_side` is assigned.
    *   **Port Side Display (if `current_side == SUBX_PORT`):**
        *   **Processed Bathymetry (if `!show_raw`):** Iterates through 2D bins (`dep_across_bins`) to draw a heatmap of depths. It also draws lines representing detected peaks (`peak_bin`) for bottom tracking.
        *   **Raw Data (if `show_raw == 1`):** Plots individual depth points (`depths`, `across`) based on raw processed data. Points are colored white if they meet amplitude and quality thresholds, otherwise blue.
        *   **Gate Visualization:** Draws red points representing shallow and deep gates (`gate_shal`, `gate_deep`, `track_gate_shal`, `track_gate_deep`) that define valid areas for bottom detection.
        *   **Parameter Display:** Displays current values of key processing parameters (e.g., `# sam`, `ph av`, `pr Hz`, `tx cy`, `ct rg`) as text on the drawing area.
    *   **Starboard Side Display (if `current_side == SUBX_STBD`):**
        *   The drawing logic is very similar to the port side, but adapted for the starboard data.
        *   Displays `max_variance`, `min_binned`, `qua_thresh`, `amp_perc_thresh`, `water_depth_multiplier`, and `max_across_coverage`.
    *   **Copy to Screen:** After all drawing operations are completed on the `DA10.pixmap`, the `XCopyArea` function copies the entire pixmap to the visible window (`DA10.window`), ensuring a smooth, flicker-free update.
3.  **`expose_bathy()` function:**
    *   This function is registered as an expose callback and is responsible for redrawing the contents of the window whenever an `Expose` event occurs (e.g., when the window is uncovered or resized). It simply copies the pre-rendered `DA10.pixmap` to the screen.

This file heavily relies on global variables (`DA10`, `txInfo`, `current_side`, `show_raw`, `dep_across_bins`, `peak_count`, `peak_bin`, `depths`, `across`, `anal1`, `angdiffs`, `port_thresh`, `stbd_thresh`, `qua_thresh`, `perc_watercol`, `amp_thresh`, `pr_depth`, `pr_across`, `pr_var`, `no_prs`, `min_binned`, `max_variance`, `gate_shal`, `gate_deep`, `track_gate_shal`, `track_gate_deep`, `port_pc`, `stbd_pc`, `water_depth_multiplier`, `max_across_coverage`, `phase_filter_length`, `DT`) to access and display the application's state and data.
