---
layout: default
title: SEIS_watercolumn
parent: GLSEIS Tools
nav_order: 6
---

# SEIS_watercolumn

## Description
`SEIS_watercolumn.c` is a source code file from the `glSeis` application that creates and manages the "Watercolumn" widget. This widget serves as a detailed control panel for visualizing EM (multibeam) watercolumn data within the main 3D OpenGL window. It is not a standalone command-line tool.

This module allows the user to load, process, and render watercolumn data, control visualization parameters like color and intensity thresholds, and interact with representations of the sonar's field of view.

## Functionality

### `void make_watercolumn_widget()`
This function constructs the GUI for the watercolumn control panel. The panel includes:
*   **Buttons:** To toggle various display options, such as showing the scan boundaries (`Show Scan Bounds`), rendering the 3D volume data (`Show Volume`), switching between full-resolution and stacked data, and differencing between scans (`Show Difference`).
*   **Sliders:** To interactively adjust key parameters:
    *   `dB Threshold` / `dB Maximum`: Controls the lower and upper bounds for backscatter intensity mapping.
    *   `Mount Pitch` / `Mount Heading`: Adjusts the orientation of the sonar head.
    *   `Range Averaging`: Controls the amount of averaging applied along the range axis.
    *   `Diff Min` / `Diff Max`: Sets thresholds for viewing the difference between scans.
*   **Control Graphics:** Four small 2D graphical displays that visualize the sonar's transmit/receive geometry and allow for interactive manipulation of the field of view.

### `int manage_watercolumn_widget_events(XEvent event)`
This is the event handler for the watercolumn widget. It processes user input from the control panel:
*   **Button Clicks:** Activates or deactivates display flags (e.g., `show_volume`, `do_lighting`) and triggers data processing actions like advancing to the `next scan`.
*   **Slider Adjustments:** Updates the global variables tied to the sliders (e.g., `dB_thresh`, `mount_pitch`) and immediately redraws the main 3D scene to reflect the changes.
*   **Keyboard Shortcuts:** Provides extensive and context-sensitive controls.
    *   **`Z`:** Resets the slider that has focus to its default value.
    *   **`A`:** Triggers an animation sequence that steps through a parameter's range (e.g., rotating the view, changing a threshold) and saves each frame as an image file.
    *   **`W`:** Dumps the currently loaded watercolumn data for each ping as a series of individual PGM image files.
    *   **Arrow keys:** Adjust the selected cone angles or scan number depending on which sub-window has focus.

### `void draw_WC_scan()`
This is the main OpenGL rendering function for the watercolumn data.
*   It iterates through the loaded pings and beams for the current scan.
*   For each sample in the watercolumn that exceeds the `dB_thresh`, it draws a point in 3D space.
*   The point can be rendered as a simple cross (`TARGET_CROSS`) or a sphere (`TARGET_SPHERE`).
*   The color of each point can be mapped to its intensity (`BY_INTENSITY`) or its depth (`BY_DEPTH`).
*   The size of the point can be scaled by its intensity (`scale_by_I`).
*   It can also render the geometric boundaries of the sonar scan (`show_bounds`) as a wireframe.

### Data Handling Functions
*   **`extract_steering_angle()`**: Parses a merged file to automatically detect the start and end pings of each sonar scan cycle.
*   **`load_watercolumn_data()`**: Reads the binary watercolumn data from a `.watercol` file for the currently selected scan.
*   **`proc_watercolumn_data()`**: Performs processing on the loaded data, such as stacking (averaging) multiple pings together.
*   **`diff_watercolumn_data()`**: Computes the difference in backscatter between the current scan and the previous one.
*   **`initialise_watercolumn_variables()`**: Sets all watercolumn-related parameters to their default values when the application starts.