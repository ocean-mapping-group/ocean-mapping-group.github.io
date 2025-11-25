---
layout: default
title: SYN_RefFrame
parent: GL Tools
nav_order: 20
---

# SYN_RefFrame

## Description
`SYN_RefFrame.c` is a module within the `SYN` project (likely `synSwath`), located in the `gl/` directory. Its core purpose is to simulate and visualize the complex spatial arrangement of various sensors and their associated reference frames on a mobile platform (e.g., a ship, Remotely Operated Vehicle (ROV), or Autonomous Underwater Vehicle (AUV)). It provides an interactive graphical user interface (GUI) widget that enables users to configure the precise lever arms (positions) and angular offsets (orientations) of multiple sensors relative to the platform's primary reference point, typically its center of gravity. It is not a standalone command-line tool.

This module is fundamental for understanding how sensor integration and spatial referencing impact data acquisition and processing in marine environments.

## Functionality

### `void make_RF_widget()`
*   **Purpose:** Configures and creates the "Reference Frame - Sensor Layout" control panel.
*   **Action:** Sets up a panel that includes:
    *   **Sliders**: For adjusting parameters of the currently selected sensor (`current_RF_sensor`), including: `Separation` (for multi-element sensors like GPS antenna pairs), `X Location`, `Y Location`, `Z Location` (lever arms relative to the platform's origin), and `AZIMUTH OFFSET`, `PITCH OFFSET`, `ROLL OFFSET` (angular misalignments).
    *   **Buttons**: To toggle the display of `levers` (visualization of lever arms), adjust the `transparency` of the main platform object, and to quickly load predefined sensor configurations for "default ship", "ROV", or "AUV" platforms. Additional buttons toggle `sensor coords` (local axis systems for each sensor), `show history` (sensor trajectory history), and `show offsets` (visualization of relative offsets).
    *   **Graphic Area**: A list-like display that allows the user to select which specific sensor's properties are being modified.

### `int manage_RF_widget_events(XEvent event)`
*   **Purpose:** Handles all user interaction events (mouse, keyboard, button/slider input) within the RF (Reference Frame) widget.
*   **Action:**
    *   **Quit Button:** Unmaps the widget, resets the global `lookat` parameter to `CENTRE`, sets `ship_flag` to a default (e.g., a ship model), and redraws the main 3D scene.
    *   **Button Clicks:** Toggles various display flags (e.g., `RF_show_levers`, `RF_transparency`, `RF_what_to_show`, `show_sensor_history`, `show_sensor_offset`), loads predefined sensor configurations for different platform types (ship, ROV, AUV), and triggers `draw_all()` to refresh the scene.
    *   **Graphic Area Clicks (Sensor List)**: Sets `current_RF_sensor` to the index of the clicked sensor in the list, and then updates the sliders to reflect its properties.
    *   **Slider Interaction**: Updates the corresponding global `RF_props` variables (e.g., `RF_props[current_RF_sensor].x`, `RF_props[current_RF_sensor].pitch_offset`) and redraws the scene.
    *   **Keyboard Shortcuts**:
        *   `KEY_PLUS`/`KEY_MINUS`: Adjusts the `transparency` of the main object or `aziPatch` (a parameter for azimuth offset, possibly for fine-tuning).
        *   `KEY_X`: Toggles the `show_beams` flag for the selected sensor (if it's a sonar).
        *   `KEY_L`: Toggles `wobble_with_sonar` (a flag to apply platform wobble to the sensor's relative motion).
        *   `KEY_P`: Toggles `showPatch` (a flag for visualizing something like an attitude patch).
        *   `KEY_G`: Toggles `ghost_RF` (for displaying a ghost outline of the RF).
        *   `KEY_W`: Triggers `wobble_sensor()` for the currently selected sensor, applying a perturbation.
        *   `KEY_F`: Sets `LOOKAT_FOCUS` to the currently selected sensor, centering the camera view on it.
        *   Arrow keys (`KEY_UP`/`KEY_DOWN`/`KEY_LEFT`/`KEY_RIGHT`): Adjusts `surgePatch` (X-offset) or `swayPatch` (Y-offset) for the selected sensor or incrementally adjusts slider values.
        *   `KEY_Z`: Zeros the currently selected slider value or toggles the `lookat` mode between `ANTENNA` and `CENTRE`.
        *   `KEY_SPACE`: Toggles the visibility (`visible`) of a selected sensor.

### `void draw_RF(int ghost)`
*   **Purpose:** Renders the platform and all configured sensors in the 3D OpenGL scene.
*   **Action:**
    *   Draws the main platform object (ship, ROV, AUV) in its current pose (position and orientation) based on `ship_flag`.
    *   Iterates through each configured sensor (`RF_props[i]`). If a sensor is `visible`:
        *   Translates and rotates the sensor to its configured position and orientation relative to the platform.
        *   If `RF_show_levers` is enabled, it draws small lines (cylinders) representing the lever arm from the platform's origin to the sensor.
        *   If `RF_what_to_show` allows, it draws the sensor's local coordinate axes (`draw_sensor_axis()`).
        *   It then draws the specific sensor model (e.g., `draw_EM1000`, `draw_MRU`, `draw_disc`, `draw_ADCP`, `draw_AcousticBeacon`, `draw_line_array`, `draw_SubbottomArray`) based on `RF_props[i].type`.
        *   Sonars can optionally display their beam patterns if `RF_props[i].show_beams` is enabled.
        *   The `ghost` parameter, combined with `ghost_RF`, allows rendering a "ghost" version of the RF at a previous position.

### Helper Functions
*   **`void init_RF_variables()`**: Initializes all global variables and parameters related to the RF module. It sets default display flags, initializes arrays for sensor history (`sensor_history`), and pre-configures a list of sensors (`RF_names`, `RF_props`) with their types, default positions, and offsets for different platform types (ship, HUGIN AUV, ROV) based on the `ship_flag`.
*   **`int wobble_sensor(int sensor)`**: Simulates a sinusoidal wobble or perturbation in the orientation of a specific sensor's angular offsets. It can also apply this wobble to other sonars on the platform if `wobble_with_sonar` is enabled, and redraws the scene for each step to create a visual animation.
*   **`int draw_sensor_axis()`**: A utility function that draws 3D coordinate axes (X, Y, Z) to visually represent a sensor's local reference frame.
*   **`int draw_sensor_history()`**: Renders a trail of markers showing the historical trajectory of each visible sensor in the scene.
*   **`int draw_sensor_offset()`**: Draws lines illustrating the X, Y, and Z offsets from a primary reference point (e.g., a GPS antenna) to another sensor.
*   **`int locate_sensors_and_shift()`**: Updates the historical positions of all sensors. This function is typically called at each simulation step to log the sensor's trajectory relative to the platform's movement for the `show_sensor_history` display.
*   **`void refresh_RF_widget_window (Window window)`**: Refreshes the display of the RF widget's components as needed.

This module provides a powerful interactive tool within `glSeis` for understanding, configuring, and visualizing the intricate details of sensor integration and spatial referencing on mobile platforms, which is fundamental to accurate navigation, positioning, and data acquisition in dynamic marine environments.