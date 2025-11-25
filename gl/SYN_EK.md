---
layout: default
title: SYN_EK
parent: GL Tools
nav_order: 5
---

# SYN_EK

## Description
`SYN_EK.c` is a source code file within the `glSeis` application, specifically designed for modeling and visualizing multi-EK (Echosounder) imaging geometries. It is not a standalone command-line tool.

This module allows users to interactively configure and display the physical setup, beam patterns, and simulated responses of multiple echosounder transducers within a 3D OpenGL environment. It's used to explore how different EK configurations and parameters affect acoustic imaging.

## Functionality

### `void make_EK_widget()`
This function constructs the GUI control panel for the EK model. This panel includes:
*   **Toggle Buttons:** To show/hide the mounting `frame`, select `which EK` transducer to currently focus on (0-3 for individual, 4 for all), toggle the display of the `BP` (beam pattern) cone, toggle `show CTD` (a simulated CTD frame), trigger `cycle Azi/Graz` and `cycle Along/Graz` animations, and toggle `BullsEye` plot visibility.
*   **Sliders:** To adjust parameters such as:
    *   `Total Depth` (`EK_seafloor_depth_m`): Simulates the seafloor depth.
    *   `Frame Depth` (`EK_frame_depth_m`): Depth of the EK mounting frame below the surface.
    *   `Frame Tilt` (`EK_frame_tilt_deg`): Pitch angle of the mounting frame.
    *   `Frame Azimuth` (`EK_frame_azi_deg`): Heading of the mounting frame.

### `int manage_EK_widget_events(XEvent event)`
This is the event handler for the EK control widget.
*   **Button Clicks:** Toggles display flags (`EK_show_frame`, `EK_show_bp`, etc.), cycles through transducer selections (`EK_current_transducer`), and initiates animations (`EK_animate_AziGraz()`, `EK_animate_AlongGraz()`).
*   **Slider Interaction:** Updates global variables linked to the sliders (e.g., `EK_seafloor_depth_m`, `EK_frame_tilt_deg`). Changes trigger `calc_EK_variables()` (to re-run calculations) and then `draw_all()` (to refresh the 3D scene).
*   **Keyboard Shortcuts:**
    *   `KEY_Z`: Resets the slider that has focus to a default value (e.g., seafloor depth to 20m, frame tilt to 0). It also clears detected targets in the bullseye plot.
    *   `KEY_UP`/`KEY_DOWN`/`KEY_LEFT`/`KEY_RIGHT`: Adjusts the `EK_target_pos_x` and `EK_target_pos_y` for a simulated target in the bullseye graphic, and updates its intensity.

### `void draw_all_EK()`
This is the main OpenGL drawing function that renders all the EK-related elements in the 3D scene:
*   **Mounting Frame:** Draws the `EK_frame` (mounting plate) and the individual transducer units.
*   **Transducer Units:** Renders each EK transducer (e.g., cylindrical shapes).
*   **Beam Patterns:** Visualizes the `beam patterns` of selected transducers as cones (if `EK_show_bp` is enabled).
*   **Simulated CTD Frame:** Can display a simulated CTD rosette (if `EK_show_ctd` is enabled).
*   **Simulated Target:** When `EK_show_bullseye` is active, it draws a simulated target (sphere) and a blue line representing the acoustic path from the transducer to the target.

### Helper Functions

*   **`void init_EK_variables()`**: Initializes all global variables and default parameters for the EK model, including the properties of multiple EK transducers (e.g., ES-333, ES-200, ES-120, ES-70) such as their center frequency, bandwidth, beamwidth, and physical dimensions.
*   **`void calc_EK_variables()`**: Recalculates parameters related to the EK system's geometry and beam patterns when control panel settings are changed.
*   **`int EK_animate_AziGraz()`** and **`int EK_animate_AlongGraz()`**: These functions generate animated sequences to demonstrate scanning patterns (e.g., varying azimuth and grazing angle, or along-track position and grazing angle). They update the scene for each frame and can dump frames for video creation.
*   **`float calc_EK_target_intensity(float pos_x, float pos_y)`**: Calculates the simulated intensity of a target at a given (x,y) position within the beam, based on a simple cosine model.
*   **`void draw_2D_EK_bullseye()`**: Draws a 2D "bullseye" plot in an OpenGL overlay, visualizing detected targets and their intensities in a top-down view relative to the beam center.

This module provides a rich interactive environment within `glSeis` for visualizing and understanding multi-EK echosounder array geometries and their imaging capabilities in a dynamic 3D space.