---
layout: default
title: draw_view
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 9
---
# draw_view

## Description
`draw_view.c` is a Motif GUI source file that encapsulates the drawing logic for multiple general-purpose drawing areas (`DA1`, `DA2`, `DA3`, `DA4`) within the "Submetrix 2000 unraveller" application. It is responsible for rendering various types of processed data from the Submetrix 2000 system onto these graphical canvases. Depending on the `type` of data specified (e.g., different phase differences, amplitude logs, or raw sidescan), it scales the data and draws appropriate representations, providing visual feedback to the user on different aspects of the sonar data.

## How It Works
1.  **`draw_view(jX_win_param *DA, int type)` function:** This is the main drawing routine, called to refresh a specific drawing area (`DA`) with data of a particular `type`.
    *   **Clear Drawing Area:** If `current_side` is unassigned, the drawing area is cleared with a white background. Otherwise, it prepares for drawing based on the `current_side` (port or starboard).
    *   **Data Type Dispatch:** A series of `if-else if` statements checks the `type` argument to determine which kind of data to draw:
        *   **`RTS_NOTHING`:** Clears the drawing area.
        *   **`RTS_AB_PHASE`, `RTS_AC_PHASE`, `RTS_AD_PHASE`, `RTS_BC_PHASE`, `RTS_AB_BC_PHASE`, `RTS_CD_PHASE` (Phase Difference Plots):**
            *   Sets the plot's X and Y ranges (`DA->x_min/max`, `DA->y_min/max`) for phase values (typically 0-255 DN).
            *   Draws background gray lines.
            *   Selects the appropriate `phase` array (e.g., `ab_filt`, `ac_filt`).
            *   Iterates through samples, plotting points (`jX_point`) in red/green (for valid data above a threshold) or blue (for invalid data). Port and starboard sides are drawn in different colors and in mirrored fashion along the X-axis.
        *   **`RTS_LOG_AMPL` (Log Amplitude Plot):**
            *   Sets X and Y ranges for amplitude data.
            *   Draws the amplitude curve (`anal1` array) as a line (`jX_line`) in red/green for port/starboard.
            *   Draws blue lines for `port_thresh`/`stbd_thresh` and `amp_thresh` as thresholds.
        *   **`RTS_ORIENT` (Orientation/Attitude Plot):**
            *   This section seems to draw a rolling display of attitude data. It `memmove`s the existing image data down one line, blanks the top line, and then draws new attitude values (`mru.roll`, `mru.pitch`, `mru.heading`, `mru.height`) as colored pixels on the top line.
        *   **`RTS_SIDESCAN`, `RTS_SLR_SIDES`, `RTS_SLR_BATHY` (Sidescan/Slant Range/Bathymetry Imagery):**
            *   **`RTS_SIDESCAN`:** Shoves the current sidescan image down one line, blanks the top line, and draws a new line of sidescan data (`anal1`) onto the top. A red/green point (`btrack`) is drawn for the amplitude threshold.
            *   **`RTS_SLR_BATHY`:** For the port and starboard halves, it maps `ll_depth` (likely slant-range corrected depths) into colors based on `cont_int` and draws them. It considers `min_binned` and `max_variance` for quality.
        *   **`RTS_ANGLE` (Angle Plot):**
            *   Sets X and Y ranges for angle data (-90 to 90 degrees).
            *   Draws background gray lines.
            *   Plots `prangs` (phase-derived angles) as points, color-coded by `qua_thresh`.
        *   **`RTS_ANGDIFFS` (Angle Difference Plot):**
            *   Sets X and Y ranges for angle differences.
            *   Draws background gray lines.
            *   Plots `angdiffs` (angle differences) as points, color-coded by `qua_thresh`.
    *   **Copy to Screen:** After all drawing operations are completed on the `DA->pixmap`, the `XCopyArea` function copies the entire pixmap to the visible window (`DA->window`).
2.  **`expose_view(jX_win_param *DA)` function:**
    *   This function is registered as an expose callback and simply copies the pre-rendered `DA->pixmap` to the visible window when an `Expose` event occurs.

This file heavily relies on global variables (`DA10`, `txInfo`, `current_side`, `phase_filter_length`, `anal1`, `port_thresh`, `stbd_thresh`, `amp_thresh`, `mru`, `ll_depth`, `no_prs`, `min_binned`, `pr_var`, `max_variance`, `prangs`, `angdiffs`, `qua_thresh`, `jX_grey`, `red`, `green`, `blue`, `yellow`, `orange`, `gray`, `white`, `black`) to access application state and raw/processed data.
