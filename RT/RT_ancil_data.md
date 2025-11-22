---
layout: default
title: RT_ancil_data
parent: RT Tools
nav_order: 186
---
# RT_ancil_data

## Description
`RT_ancil_data.c` is a module within the `RT` (Real-Time) toolkit responsible for handling and plotting ancillary data such as navigation lines, waypoints (targets), and grid lines within the interactive X-windows display. It provides functions to draw these elements on the main graphical window, supporting both the detailed image view and the overview mode.

This module helps to contextualize the processed sonar data by overlaying critical survey information, aiding in real-time monitoring and quality control during multibeam surveys.

## Functions

### `draw_nav()`
Draws navigation lines on the display.
*   **Purpose:** To visualize navigation tracks from loaded `.nav` files.
*   **Details:** Iterates through loaded navigation arrays (`navi_array`) and plots individual points as crosses within the current viewable area.

### `draw_targets()`
Draws target points (waypoints) on the display.
*   **Purpose:** To display user-defined waypoints or targets from loaded files.
*   **Details:** Iterates through loaded target arrays (`targ_array`) and plots diamonds with crosses, along with associated text labels, within the current viewable area.

### `draw_runline()`
Draws the current runline on the display.
*   **Purpose:** To visualize the planned survey line, typically defined by start (SOL) and end (EOL) points.
*   **Details:** Uses `SOL_lon`, `SOL_lat`, `EOL_lon`, `EOL_lat` to draw a line on the display.

### `draw_vectors()`
Draws vector data on the display.
*   **Purpose:** To display vector lines (e.g., from external ASCII files) on the map.
*   **Details:** Iterates through loaded vector arrays (`vect_array`) and plots segments as lines, handling potential gaps (indicated by `-999.0`).

### `draw_scale()`
Draws a graphical scale bar on the display.
*   **Purpose:** To provide a visual reference for distances on the map.
*   **Details:** Calculates an appropriate step size based on the current map extent and draws alternating black and yellow rectangles to form a scale bar, with a text label for the step distance.

### `load_up_nav()`
Loads navigation data from files.
*   **Purpose:** Reads `jcu_nav_rec` formatted navigation data from specified files into `navi_array`.
*   **Details:** Opens navigation files (`naviname`), reads records, and populates `navi_array` (latitude, longitude) and `navi_count`.

### `load_up_vectors()`
Loads vector data from files.
*   **Purpose:** Reads ASCII vector data (latitude, longitude, dummy value) from specified files.
*   **Details:** Opens vector files (`vectname`), reads records, calculates segment lengths, and populates `vect_array` and `vect_count`. It can handle gaps in vectors.

### `load_up_targets()`
Loads target (waypoint) data from files.
*   **Purpose:** Reads ASCII target data (latitude, longitude, label) from specified files.
*   **Details:** Opens target files (`targname`), reads records, and populates `targ_array` (longitude, latitude) and `tlabel`.

### `draw_grid()`
Draws a latitude/longitude grid on the display.
*   **Purpose:** To provide geographic context on the map.
*   **Details:** Calculates an appropriate grid interval based on the current view extent. Plots crosses and diamonds at grid intersections and labels them with approximate latitude/longitude values.

## Output Files
This module primarily focuses on display and does not directly produce output files.

## Dependencies
*   `RT_global.h`: Global variables for the `RT` toolkit.
*   `RT_ancil_data.h`: Declarations for ancillary data functions.
*   `jcu_nav.h`: Navigation data structures and functions.
*   `X_extra.h`: X-windows graphics utilities.
*   `array.h`: Array manipulation utilities.
*   `j_area.h`: Area and projection handling.
```
```