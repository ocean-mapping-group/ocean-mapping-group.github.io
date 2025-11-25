---
layout: default
title: SYN_ADCP
parent: GL Tools
nav_order: 1
---

# SYN_ADCP

## Description
`SYN_ADCP.c` is a source code file that provides the modeling and visualization capabilities for ADCP (Acoustic Doppler Current Profiler) methods within the interactive `glSeis` application. It is not a standalone command-line tool.

This module allows users to interactively control various ADCP parameters and visualize their effects on beam patterns, current vectors, and how the ADCP "sees" the water column in a 3D OpenGL environment. It aims to model the complex interaction between the ADCP, vessel motion, and ocean currents.

## Functionality

### `void make_ADCP_widget()`
This function constructs the GUI control panel for the ADCP model. This panel includes:
*   **Toggle Buttons:** To show/hide `beam patterns`, `beam vectors`, `current vectors`, `currents`, `layer` (current layer), `resolvable` (velocity components), `ambiguity`, `hemisphere`, `pulse`, `bins`, `foreaft`, `portstbd`, `incl. SOG`, `bottom track`, `inverted` display, `ensemble`, and `noise` components.
*   **Sliders:** Extensive sliders to adjust parameters such as:
    *   `Beam Tilt`, `Beam Width`, `Bin Size`, `Max. Depth`
    *   Simulated `Current Depth`, `Current Magnitude`, `Current Azimuth`, `Current Depression`
    *   `ADCP Vessel Speed`, `ADCP Vessel Heading`
    *   `Hemisphere Radius`, `Pulse Length`
    *   `Noise Vector (m/s)` (magnitude of random noise added to currents)
    *   `m between pings` (simulated vessel speed for ensemble visualization).

### `int manage_ADCP_widget_events(XEvent event)`
This function is the event handler for the ADCP control panel.
*   **Button Clicks:** Toggles the state of various visualization flags and calls `draw_all()` to update the 3D scene.
*   **Slider Interaction:** When sliders are adjusted, it updates the corresponding global variables, triggers a recalculation of all ADCP-related parameters (`update_all_calcs()`), and then redraws the 3D scene.
*   **Keyboard Shortcuts:** Specific keys (e.g., `KEY_LEFT`, `KEY_RIGHT` for fine-tuning sliders, `KEY_Z` to reset values, `KEY_W` for animations, `KEY_L` to focus camera on current layer, `KEY_SPACE` to toggle beam visibility) provide interactive control.

### `void draw_ADCP()`
This is the main OpenGL drawing function that renders all the ADCP-related elements in the 3D scene:
*   **Transducer Model:** Draws the ADCP transducers as cylinders.
*   **Beam Patterns:** Visualizes the acoustic beam patterns as cones emanating from the transducers.
*   **Current Vectors:** Draws simulated current vectors in UVW (global) and beam coordinates, showing their magnitude and direction.
*   **Vessel Speed Over Ground (SOG):** Displays the combined effect of current and vessel speed.
*   **Bottom Track:** Shows the intersection points of beams with the nominal seabed.
*   **Current Layers:** Visualizes the specific depth layer from which currents are being measured.

### Helper Functions

*   **`void init_ADCP_variables()`**: Initializes all global variables and default parameters for the ADCP model, including beam configurations, display flags, and initial current settings.
*   **`void calc_beam_intersect_centre()`**: Calculates the 3D intersection points of the ADCP beams with both a simulated current layer and the nominal seabed.
*   **`void calc_current_in_beam_coords()`**: Transforms the simulated current vectors from global UVW coordinates to the local coordinate system of each ADCP beam.
*   **`void calc_uvw_from_azidepmag(currvect *cv)`** and **`void calc_azidepmag_from_uvw(currvect *cv)`**: Utility functions for converting between magnitude/azimuth/depression and U/V/W (Cartesian) vector components.
*   **`void make_curr_prof()`**: Generates a synthetic current profile through the water column, extrapolating from a user-defined current vector and adding optional random noise.
*   **`void add_SOG_curr()`**: Combines the simulated ocean current with the vessel's speed over ground.
*   **`void update_all_calcs()`**: An orchestration function that re-runs all necessary calculations (beam intersects, current transformations, profile generation) when a parameter is changed in the control panel.
*   **`void draw_arrow_vector(float speed, float red, float green, float blue)`**: A utility function to draw a 3D arrow in OpenGL, representing a vector.

This module provides a comprehensive and interactive environment within `glSeis` for understanding the principles and operational characteristics of ADCPs and their interaction with the marine environment.