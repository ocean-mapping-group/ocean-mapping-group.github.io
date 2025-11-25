---
layout: default
title: SYN_M3
parent: GL Tools
nav_order: 14
---

# SYN_M3

## Description
`SYN_M3.c` is a module within the `glSeis` application, specifically designed to simulate and visualize the imaging geometries of the M3 multibeam sonar system. It is not a standalone command-line tool.

The M3 sonar is a multi-mode multibeam sonar often used for high-resolution imaging in shallow water environments. This module allows users to configure and display various M3 sonar setups (e.g., different deployment anchor configurations) and visualize their beam patterns, associated sensors, and deployment infrastructure in a 3D OpenGL environment.

## Functionality

### Widget Management
*   **`void make_M3_widget()`**: Configures and creates the graphical user interface for the "M3 Sonar Array Control" panel. This panel includes:
    *   **Buttons**: To toggle the display of the `fan` (representing the swath beam pattern), `pulse` (a simulated acoustic pulse visualization), and switch between `anchors` configurations (e.g., dual anchor or quad anchor deployments).
    *   **Sliders**: For adjusting parameters of the currently selected M3 sonar or associated device, such as `Range`, `X Location`, `Y Location`, `Z Location`, `Receiver Width`, `Transmitter Width`, `Azimuth`, `Depression`, and `Roll`.
    *   **Graphic Area**: A list-like display that allows the user to select which M3 sonar or associated device's properties are currently being modified by the sliders.
*   **`int manage_M3_widget_events(XEvent event)`**: Handles all user interaction events (button clicks, slider movements, keyboard input) within the M3 control widget.
    *   **Button Clicks:** Toggles various display flags (`M3_show_fan`, `M3_show_pulse`) and dynamically switches between `M3_dual_anchor` and `M3_quad_anchor` configurations by calling `init_dual_anchor_M3_variables()` or `init_quad_anchor_M3_variables()` respectively.
    *   **Graphic Area Clicks:** Updates `current_M3` to select an M3 device from the list, and then refreshes the sliders to reflect the properties of the newly selected device.
    *   **Slider Interaction:** Modifies the values of linked global variables (e.g., `M3props[current_M3].range`, `M3props[current_M3].x`, etc.) and triggers `draw_all()` to refresh the scene.
    *   **Keyboard Shortcuts:** `KEY_Z` resets the currently focused slider's value to a default. Arrow keys (`KEY_LEFT`, `KEY_RIGHT`) allow incremental adjustments to slider values.
*   **`void refresh_M3_widget_window(Window window)`**: A standard refresh function for the M3 widget's display elements. It redraws buttons, sliders, and the list of M3 devices as needed.

### Drawing Functions
*   **`void draw_all_M3s()`**: The primary OpenGL drawing function for rendering all M3 sonars and associated sensors.
    *   Iterates through an array of `M3props` (properties for each M3 device or associated sensor).
    *   For each visible M3 device, it draws its physical model (a small M3 unit) at its specified location and orientation.
    *   Can optionally display the M3's `fan` (representing the swath beam pattern) or a simulated `pulse` visualization.
    *   Calls `M3_draw_other_bits()` to render additional components.
*   **`void M3_draw_other_bits()`**: Renders auxiliary components related to the M3 system's deployment:
    *   **Suspension Lines**: Draws lines representing the suspension for both dual and quad anchor configurations.
    *   **Other Sonars/Sensors**: Draws models for other commonly integrated sensors, such as an ADCP, 28 kHz and 200 kHz single-beam echosounders, and an EM710 multibeam sonar, based on their visibility flags.
    *   **MVP Profiler**: Renders a winch line and a small MVP (Moving Vessel Profiler) profiler.
    *   **Mooring Anchors**: Draws buoys and mooring lines for both dual and quad anchor configurations.

### Initialization Functions
*   **`void init_quad_anchor_M3_variables()`**: Initializes global variables and parameters for the M3 system when configured in a quad anchor deployment. This includes setting default positions, ranges, beam widths, azimuths, depressions, and visibility flags for various M3 devices and associated sensors (e.g., ADCP, 28kHz, 200kHz, EM710, Mooring Anchors, MVP Profiler). It also defines the names for each M3 device displayed in the widget list.
*   **`void init_dual_anchor_M3_variables()`**: Similar to the above, but initializes parameters specific to a dual anchor deployment configuration for the M3 system.

This module provides a rich, interactive, and visually detailed environment within `glSeis` for visualizing and understanding the deployment scenarios and operational characteristics of the M3 multibeam sonar and its integrated sensor suite.