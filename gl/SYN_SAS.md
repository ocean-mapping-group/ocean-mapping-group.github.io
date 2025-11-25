---
layout: default
title: SYN_SAS
parent: GL Tools
nav_order: 23
---

# SYN_SAS

## Description
`SYN_SAS.c` is a module within the `SYN` project (likely `synSwath`), located in the `gl/` directory. Its purpose is to simulate and visualize the complex imaging geometries of a Synthetic Aperture Sonar (SAS) system. It allows users to define parameters related to the platform's motion, the SAS array's acoustic characteristics, and the target's position, then visualize the formation of the synthetic array, the acoustic paths, and associated uncertainties in a dynamic 3D OpenGL environment. It is not a standalone command-line tool.

This module is a valuable tool for understanding the principles of SAS, the impact of platform motion on synthetic aperture formation, and the resulting imaging capabilities and limitations.

## Functionality

### `void make_SAS_widget()`
*   **Purpose:** Configures and creates the "SAS Sonar Array Control" panel, which serves as the user interface for this module.
*   **Action:** Sets up a panel containing:
    *   **Sliders**: For defining numerous simulation and array parameters:
        *   **Platform Motion**: `Velocity`, `Sway Magnitude`, `Sway Period`, `Heave Magnitude`, `Heave Period`, `Platform Crab`, `Platform Trim`.
        *   **SAS Array Characteristics**: `Tx Azi Width` (Transmit Azimuthal Width), `Tx Elev. Width` (Transmit Elevation Width), `Total Array (m)`, `Array Mount Roll (deg)`.
        *   **Target Parameters**: `Target Horiz Range (m)`, `Target Elevation (deg)`.
        *   **Simulation Controls**: `SAS Max Range (m)`, `# Shot Points` (number of physical sub-array positions contributing to the synthetic aperture), `Current Shot Point` (to highlight a specific sub-array).
    *   **Buttons**: To toggle various display options: `show Syn Aperture` (the full synthetic array), `show Sub Aperture` (individual physical sub-arrays), `show Target` (the acoustic path to the target), `show Interf.` (for interferometric SAS display), `show Uncertainty` (positional uncertainty), `show Phase Centres`, `show Tx Bp` (Transmit Beam Pattern), `Target on Seafloor` (button to automatically adjust target elevation to match a nominal seafloor depth), and `animate Syn Array` (to trigger a synthetic array formation animation).

### `int manage_SAS_widget_events(XEvent event)`
*   **Purpose:** Handles all user interaction events (button clicks, slider movements, keyboard input) within the SAS widget.
*   **Action:**
    *   **Quit Button:** Unmaps the widget's window.
    *   **Button Clicks:** Toggles display flags (e.g., `SAS_show_syn_array`, `SAS_show_sub_array`, `SAS_show_path_to_target`, `SAS_show_pos_uncert`, `SAS_show_phase_centres`, `SAS_show_txBP`, `SAS_show_interf`). The "Target on Seafloor" button calls `calc_SAS_slr_elev()` to adjust the target's elevation. The "animate Syn Array" button triggers `SAS_animate_SynArray()`.
    *   **Slider Interaction**: Updates global variables linked to the sliders (e.g., `SAS_velocity`, `SAS_sway_mag`, `SAS_target_horiz_range_m`, `SAS_mount_roll`, `no_SAS_sub_arrays`, `current_SAS_sub_array`). After updates, it calls `calc_SAS_subarray()` to recalculate the array geometry and `draw_all()` to refresh the scene.
    *   **Keyboard Shortcuts**: `KEY_Z` resets the selected slider to its default or a common zero value. Arrow keys (`KEY_LEFT`, `KEY_RIGHT`) incrementally adjust slider values. `KEY_PLUS`/`KEY_MINUS` adjusts `SAS_max_uncert_growth_m` (a parameter for visualizing position uncertainty).

### `void draw_all_SAS()`
*   **Purpose:** Renders all SAS-related elements in the 3D OpenGL scene.
*   **Action:**
    *   Calls `setup_SAS_txBP()` (if not already done) to configure the SAS transmit beam pattern.
    *   Calculates `pos_uncert_radius` for visualizing position uncertainty around sub-array elements.
    *   Draws the acoustic path from the current subarray to the target if `SAS_show_path_to_target` is enabled.
    *   Iterates through each synthetic aperture element (`SAS_subarray[i]`):
        *   If visible, it translates and rotates to its simulated position and orientation.
        *   If `SAS_show_sub_array` is enabled (and it's the current, or adjacent subarrays), it draws the physical array model (`draw_SENSOTEK`) and optionally the transmit beam pattern (`draw_bp`) if `SAS_show_txBP` is enabled.
        *   If `SAS_show_syn_array` is enabled, it draws all physical array elements along the synthetic aperture.

### Helper Functions

*   **`void init_SAS_variables()`**: Initializes all global variables and parameters related to the SAS module to their default states. This includes default values for platform motion, SAS array dimensions, target position, and various display flags (e.g., `SAS_show_syn_array`, `SAS_show_sub_array`, `SAS_show_path_to_target`, `SAS_show_pos_uncert`, `SAS_show_txBP`, `SAS_show_interf`, `SAS_tx_setup`). It also defines the number of synthetic aperture elements (`no_SAS_sub_arrays`) and calls `calc_SAS_subarray()`.
*   **`void setup_SAS_txBP()`**: Configures the transmit beam pattern for the SAS system. It sets global beam pattern parameters (`Frequency`, `Along_Array_Length`, `Along_Array_Width`, `Across_Design_Steering`, `Along_Design_Steering`, `Calculation[]` for array shape) and then calls `recalc_bp()` and `setup_bp()` (external functions from the `bP_stuff` module) to generate the actual beam pattern data.
*   **`void calc_SAS_subarray()`**: Calculates the simulated position and orientation of each physical sub-array element along the synthetic aperture. This involves simulating the platform's trajectory over time, including sway and heave, to determine the `loc_x_m`, `loc_y_m`, `loc_z_m` for each sub-array element, as well as its pitch and heading.
*   **`void calc_SAS_slr_elev(float depth, float range)`**: Calculates the target's slant range (`SAS_target_slant_range_m`) and elevation angle (`SAS_target_elev_deg`) from its given depth and horizontal range.
*   **`int SAS_animate_SynArray()`**: Animates the formation of the synthetic array by stepping through each physical sub-array element, updating `current_SAS_sub_array`, redrawing the scene, and dumping RGB frames to create a video sequence.
*   **`int draw_phase_centre(float size, float uncert_radius)`**: Draws a representation of an acoustic phase center (typically a small cross), optionally with a transparent sphere indicating uncertainty around it.
*   **`int draw_SENSOTEK(float scaling, float pos_uncert_radius_m)`**: Draws a detailed model of a SENSOTEK-like SAS physical array, including its transmit (Tx) and receive (Rx) elements, and can display phase centers and uncertainty. This function helps visualize the physical hardware of the SAS system.

This module provides a rich and interactive platform for visualizing and understanding the complex principles of Synthetic Aperture Sonar, the impact of platform motion on array formation, and the resulting imaging capabilities and uncertainties in a dynamic 3D simulation environment.