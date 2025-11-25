---
layout: default
title: SYN_MRU
parent: GL Tools
nav_order: 15
---

# SYN_MRU

## Description
The MRU (Motion Reference Unit) module, conceptually defined within `SYN_global.h` and implemented primarily within the large `synSwath.c_prerationalisation` file (or its active equivalent in the `SYN` project), is responsible for simulating, visualizing, and interacting with Motion Reference Unit data within the `glSeis` application. It allows users to demonstrate and analyze the behavior of MRUs, including their measured attitudes, accelerations, angular rates, and magnetic fields, in a 3D OpenGL environment. It is not a standalone command-line tool.

This module provides tools for understanding how MRU data is collected, processed, and how sensor offsets and derived quantities (like gravity) are handled.

## Functionality

### `void make_MRU_widget()`
*   **Purpose:** Configures and creates the "Seatex MRU Demonstrations" control panel, which serves as the user interface for the MRU module.
*   **Action:** Sets up a panel with:
    *   **Sliders:** For adjusting parameters related to ship dynamics or MRU processing, such as "Ship Velocity (knots)", "Radius of Turn (m)", and "VGA period (seconds)".
    *   **Buttons:** To toggle the display of various MRU outputs: "Accelerations", "Angular Rates", "MRU Orientation" (raw MRU data), "Pendulum Orientation" (orientation derived from accelerations), "Ang. Rate Orient." (orientation derived from angular rates), "Calc Grav." (to calculate gravity), "MRU Z Position", "MRU XY Position", "Magnetic Field", "Residual NED accels", "Offset Sensor" (to simulate lever arm effects), and "Beach Ball" (a spherical representation of motion).

### `int manage_MRU_widget_events (XEvent event)` (part of `SYN_event_loop.c` / `synSwath.c`)
*   **Purpose:** Handles user interactions within the MRU control widget.
*   **Action:**
    *   **Button Clicks:** Toggles display flags (e.g., `MRU_display_accels`, `MRU_display_angrates`, `MRU_display_magfield`, `MRU_offset_sensor`, `MRU_beach_ball`, `MRU_orientation`, `MRU_Zposition`, `MRU_XYposition`, `MRU_display_residaccels`) and triggers functions like `calc_grav_vect()`.
    *   **Slider Interaction:** Updates global variables linked to the sliders and triggers `draw_all()` to refresh the scene.
    *   **Keyboard Shortcuts:** (Not explicitly in a separate MRU event handler, but part of the main `process_x_events` which dispatches to MRU widget for some keys like `KEY_SPACE` for toggling `MRU_at_RP`).

### `void show_MRU()`
*   **Purpose:** Reads and processes MRU data from an external file (`mrufile`).
*   **Action:**
    *   Reads binary MRU telegrams (specifically a 40-byte telegram starting with 'q' or 'Q').
    *   Extracts raw MRU measurements: roll, pitch, heading (as `MRU_roll`, `MRU_pitch`, `MRU_heading`), angular rates (`MRU_angR`, `MRU_angP`, `MRU_angY`), accelerations (`MRU_accelX`, `MRU_accelY`, `MRU_accelZ`), heave, surge, sway (`MRU_heave`, `MRU_surge`, `MRU_sway`), and magnetic field components (`MRU_magR`, `MRU_magP`, `MRU_magY`).
    *   Performs byte swapping if necessary (for `INTEL` endianness).
    *   Applies selected display modes for orientation and position (`MRU_orientation`, `MRU_Zposition`, `MRU_XYposition`).
    *   Calls `calc_MRU_derivs()` to compute derived quantities.
    *   Triggers `draw_all()` periodically to update the visualization.

### `void draw_MRU()`
*   **Purpose:** Renders a visual representation of the MRU and its various data outputs in the 3D OpenGL scene.
*   **Action:**
    *   Draws the MRU body as a grey cylinder. Its position can be at the reference point (`MRU_at_RP`) or offset.
    *   **Beach Ball:** If `MRU_beach_ball` is enabled, a transparent sphere visualizes the total specific force vector.
    *   **Offset Sensor:** If `MRU_offset_sensor` is enabled, it draws cylinders representing X and Y lever arm displacements, and a simplified sonar model (e.g., a Seabat).
    *   **Angular Rates:** If `MRU_display_angrates` is enabled, arcs are drawn to indicate angular rates around the X, Y, and Z axes.
    *   **Accelerations:** If `MRU_display_accels` is enabled, cylinders are drawn representing X, Y, and Z accelerations, and a magenta cylinder for the total specific force vector, oriented by its azimuth and depression.
    *   **Magnetic Field:** If `MRU_display_magfield` is enabled, cylinders are drawn for magnetic field components (Roll, Pitch, Yaw) and a grey cylinder for the total magnetic field vector, oriented by its azimuth and depression.
    *   Calls `write_MRU_values()` to update the numerical display.

### `void write_MRU_values()`
*   **Purpose:** Updates a 2D graphic window within the MRU widget with numerical values of various MRU parameters.
*   **Action:** Displays formatted text for:
    *   MRU-reported Roll, Pitch, Heading.
    *   Accelerations (X, Y, Z).
    *   Angular Rates (Roll, Pitch, Yaw).
    *   Heave, Surge, Sway.
    *   Total Specific Force Vector (magnitude, azimuth, depression).
    *   Magnetic Field components (Roll, Pitch, Yaw, magnitude, azimuth, depression).
    *   Residual NED (North-East-Down) accelerations (X, Y, Z).
    *   Estimated gravity.

### `void calc_grav_vect()`
*   **Purpose:** Calculates an estimate of gravity from the MRU's specific force measurements.
*   **Action:** Averages a history of `tot_Accel` (total specific force vector magnitude) measurements to derive `MRU_grav`. The sign is then inverted to represent gravity.

### `void calc_MRU_derivs()`
*   **Purpose:** Calculates derived quantities from the raw MRU measurements.
*   **Action:**
    *   Computes the magnitude of the total specific force vector (`tot_Accel`) and its azimuth (`SFV_azi`) and depression (`SFV_depression`).
    *   Maintains a history of `tot_Accel` in `grav_hist` for gravity estimation.
    *   Calculates geographically referenced residual accelerations (`MRU_residaccelX`, `MRU_residaccelY`, `MRU_residaccelZ`).
    *   Computes the magnitude of the total magnetic field vector (`tot_Magfield`) and its azimuth (`TMF_azi`) and depression (`TMF_depression`).

This MRU module provides a powerful interactive environment for demonstrating, analyzing, and understanding the complex dynamics and data outputs of Motion Reference Units in a simulated 3D context.
