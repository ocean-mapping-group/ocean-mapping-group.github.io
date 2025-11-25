---
layout: default
title: SYN_currents
parent: GL Tools
nav_order: 3
---

# SYN_currents

## Description
`SYN_currents.c` is a source code file from the `glSeis` application, specifically designed for modeling and visualizing ocean currents, particularly those from ADCP (Acoustic Doppler Current Profiler) data. It is not a standalone command-line tool.

This module provides a GUI control panel for current visualization, functions to draw current vectors and profiles in the 3D OpenGL scene, and logic to handle user interactions within this specialized widget.

## Functionality

### `void make_currents_widget()`
This function constructs the GUI for the "Currents" control panel. This panel includes:
*   **Buttons:** Labeled "Temp", "Salinity", "Backscatter", "Velocities" (likely to switch between displaying these different water column parameters in the 3D scene).
*   **Sliders:**
    *   `Depth Scale`: Controls the scaling of current depth values.
    *   `Velocity Scale`: Controls the scaling of current velocity magnitudes.
*   **Graphics Area:** A 2D sub-window dedicated to visualizing current profiles (e.g., a "hovmoller" plot of current magnitude/depth).

### `int manage_currents_widget_events(XEvent event)`
This function is the event handler for the "Currents" control panel.
*   **Button Clicks:** When a button is pressed, it triggers a corresponding display change or action in the 3D scene or 2D graphic.
*   **Slider Interaction:** Adjusts global `curr_depth_scale` and `curr_veloc_scale` variables, which then affect how currents are rendered.
*   **Mouse Clicks (on 2D graphic):** Allows the user to select specific current profiles for detailed display (`current_to_plot`), and to define X-axis display ranges (`x_min`, `x_max`).
*   **Keyboard Shortcuts:**
    *   `KEY_LEFT` / `KEY_RIGHT`: Navigates through the loaded current profiles.
    *   `KEY_R`: Resets the X-axis range of the 2D current graphic.
    *   `KEY_D`: Triggers an animation where each current profile is sequentially displayed, saving frames to a file (for creating animation videos).

### `void draw_currents(int curr_to_plot)`
This function renders a specific current profile (identified by `curr_to_plot`) in the 3D OpenGL scene:
*   It iterates through the depth bins of the selected current profile.
*   For each bin, it calculates the 3D coordinates (`dx`, `dy`, `depth`) of the current vector's endpoint based on its magnitude and azimuth.
*   It draws a blue 3D line from the origin to this endpoint, representing the current vector.
*   It then draws translucent yellow panels between adjacent current vectors to visualize the continuous current profile in 3D.

### `void draw_currents_graphic()`
This function draws a 2D visualization of the loaded current profiles in the control widget's dedicated graphics area. It displays multiple profiles over time (or some other index), with color representing current magnitude (or another parameter). It also draws a red vertical line indicating the `current_to_plot` profile currently selected for 3D display.

### `int load_currents()`
This function is responsible for loading current profile data from external ASCII files. It reads values for valid beams, current depth, magnitude, and azimuth, and identifies the maximum depth and velocity for internal scaling.

### `void init_currents_variables()`
This function initializes all global variables and flags related to current visualization to their default states when the application starts.

This module is a powerful tool within `glSeis` for the interactive exploration and analysis of 3D ocean current data.