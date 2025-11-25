---
layout: default
title: SYN_TCtrajectory
parent: GL Tools
nav_order: 25
---

# SYN_TCtrajectory

## Description
`SYN_TCtrajectory.c` is a module within the `SYN` project (likely `synSwath`), located in the `gl/` directory. Its purpose is to simulate and visualize the trajectory of a "TC" (Towed Cable) or similar underwater vehicle/instrument, integrate hydrophone data, and analyze associated acoustic ray paths and signal characteristics. It provides a graphical user interface (GUI) to load trajectory and hydrophone data, adjust display parameters, visualize signal strength and time shifts in various 2D profiles, and animate the towed body's movement. It is not a standalone command-line tool.

This module is a comprehensive tool for studying the dynamics of towed underwater systems, their acoustic interactions with hydrophones, and the propagation of signals in a dynamic 3D environment.

## Functionality

### `void make_TCtraj_widget()`
*   **Purpose:** Configures and creates the "TCtraj Display Control" panel.
*   **Action:** Sets up a panel containing:
    *   **Sliders**: For adjusting display parameters such as `Point Size`, `scan step`, `Vertical Fix Step` (for vertical markers on the trajectory), `No Puppys` (number of simulated secondary towed bodies), and `PercentSlowerPerPuppy` (to simulate speed variations for puppies).
    *   **Buttons**: To trigger animation (`Animate TC`), toggle `show hydrophones`, and to select specific acoustic frequencies for real data plotting (e.g., `20 kHz` through `80 kHz`). Also, a "show TC train" button toggles the visibility of the trajectory.
    *   **Graphic Areas**: Multiple graphic windows for displaying various 2D profile plots and lists:
        *   `Distance v. Depth`: 2D profile of the trajectory.
        *   `Speed v. Distance`: 2D profile of the towed body's speed along its path.
        *   `Speed v. Time`: 2D profile of the towed body's speed over time.
        *   `Model Noise v. Time`: 2D profile of modeled acoustic signal drop (dB) over time for different frequencies.
        *   `Actual Noise v. Time`: 2D profile of real hydrophone signal measurements (dB) over time for different frequencies.
        *   `LIST_HPHONE`: A list of loaded hydrophones and real data files, with visibility toggles.
        *   `LIST_TRAJ`: A list of loaded TC trajectories, with visibility toggles.

### `int manage_TCtraj_widget_events(XEvent event)`
*   **Purpose:** Handles all user interactions (button clicks, slider movements, keyboard input) within the TCtrajectory widget.
*   **Action:**
    *   **Quit Button:** Unmaps the widget's window and redraws the main scene.
    *   **Button Clicks:** Triggers animations (`Animate TC`), toggles `show hydrophones` and `show TC train`, and selects specific frequency plots for real data.
    *   **Graphic Area Clicks**:
        *   Clicking in the `Distance v. Depth` graphic (profile 0) can set `showTClocation` to navigate the trajectory display.
        *   Clicking in `LIST_HPHONE` toggles visibility (`show_Hydrophone`, `show_RealData`) and selects the `current_RealData` for more detailed analysis.
        *   Clicking in `LIST_TRAJ` toggles the visibility (`visible`) of individual trajectories (`TCtraj_param[i].visible`).
        *   Middle-click in profile 0 can update `showTClocation`.
    *   **Slider Interaction**: Updates display parameters (e.g., `TCtraj_size`, `noPuppys`, `PercentSlowerPerPuppy`, `TCtraj_vertical_fix_step`) and redraws the scene.
    *   **Keyboard Shortcuts**:
        *   `KEY_UP`/`KEY_DOWN`: Adjusts `Model_Signal_maxdB`/`mindB` or `Data_Signal_maxdB`/`mindB` in the profile plots. Also adjusts `RD_dBshift` for selected frequency buttons.
        *   `KEY_LEFT`/`KEY_RIGHT`: Navigates `showTClocation` (current point on trajectory), adjusts time ranges (`ViewedTimeStart`, `ViewedTimeEnd`) in profile plots, or adjusts `RD_Tshift` for selected frequency buttons. Also adjusts `TCtraj_vertical_fix_step`, `noPuppys`, `PercentSlowerPerPuppy`.
        *   `KEY_PLUS`/`KEY_MINUS` (PgUp/PgDown): No specific action in this snippet for graphics 0.
        *   `KEY_SPACE`: Toggles frequency visibility for real data or hydrophone/trajectory visibility.

### `void draw_TCtraj()`
*   **Purpose:** Renders the Towed Cable trajectory in the 3D scene.
*   **Action:**
    *   Draws each visible trajectory (`TCtraj_param[i].visible`) as a continuous line, with vertical fix step lines if `TCtraj_vertical_fix_step` is enabled.
    *   Highlights the `headTClocation` (current animation point) with a sphere.
    *   If `noPuppys` are defined, it draws scaled spheres for each "puppy" trailing the main trajectory, with their positions calculated based on `PuppySpeedScale`.

### `void draw_Hydrophone()`
*   **Purpose:** Renders hydrophone locations and their ray paths to the trajectory in 3D.
*   **Action:** Draws each visible hydrophone as a sphere with a cross marker. If `TCtraj_show_raypaths` is enabled, it draws lines (rays) from the hydrophone to each point along the trajectory (up to a certain slant range).

### `void draw_profile_TCtraj(int profile)`
*   **Purpose:** Draws various 2D profile plots within the widget's graphic areas.
*   **Action:** For each specified `profile` (0-4), it sets up the drawing area (`jX_set_up_drawing_area`) and plots:
    *   **`profile == 0` (Distance v. Depth):** The trajectory's depth profile.
    *   **`profile == 1` (Speed v. Distance):** The towed body's speed along the trajectory.
    *   **`profile == 2` (Speed v. Time):** The towed body's speed over time.
    *   **`profile == 3` (Model Noise v. Time):** Modeled acoustic signal loss (dB) from the trajectory to hydrophones (e.g., 20 kHz, 80 kHz).
    *   **`profile == 4` (Actual Noise v. Time):** Real hydrophone measurement data (dB) over time for different frequencies, with applied `RD_dBshift` and `RD_Tshift`.

### Helper Functions

*   **`void read_TCtraj()`**: Loads trajectory points (distance, latitude, longitude, depth) from a specified file.
*   **`void read_Hydrophone()`**: Loads hydrophone locations (latitude, longitude, depth) from files. For each hydrophone, it calculates ray path parameters (horizontal range, height, slant range, azimuth, elevation) from the hydrophone to each point on the main trajectory.
*   **`void read_RealData()`**: Loads real hydrophone measurement data (time and dB values for different frequencies) from files.
*   **`void calc_Speed_Time()`**: Calculates speed and cumulative arrival time along the trajectory based on user-defined speed distribution over distance (`SpeedDist`). It also finds the closest point of approach for each hydrophone to the trajectory.
*   **`void calc_dBDrop()`**: Calculates the modeled acoustic dB drop (signal loss) for specific frequencies (e.g., 20 kHz and 80 kHz) from the trajectory to hydrophones, considering range and absorption.
*   **`void scale_TCtraj()` / `void scale_Hydrophone()`**: Transforms geographical coordinates of trajectory points and hydrophones into the OpenGL scene's coordinate system for 3D rendering.
*   **`void show_RD_shifts()`**: Prints the currently applied time and dB shifts for real data, used for debugging or user feedback.
*   **`void refresh_TCtraj_widget_window (Window window)`**: Refreshes the display of the TCtrajectory widget's components.
*   **`int find_closest_node_at_time (float time)`**: Finds the trajectory node (point) closest to a given time.

This module provides a comprehensive and interactive environment for simulating, visualizing, and analyzing underwater towed body trajectories, hydrophone acoustics, and associated data in a dynamic 3D context, which is invaluable for system design, mission planning, and data interpretation.