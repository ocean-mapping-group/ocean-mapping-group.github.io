---
layout: default
title: SYN_navSect
parent: GL Tools
nav_order: 16
---

# SYN_navSect

## Description
`SYN_navSect.c` is a module for the `glSeis` application, specifically designed for the visualization and interactive analysis of navigation sections ("navSects") and ADCP (Acoustic Doppler Current Profiler) data. It is commonly used in multibeam survey planning, post-processing, and for visualizing oceanographic current models. It is not a standalone command-line tool.

This module provides functionalities to load and display navigation tracks, ADCP current profiles (both as 2D depth-vs-ping curtains and in 3D vector fields), and outputs from oceanographic models ("Model Epochs"), integrating these into the `glSeis` 3D environment and complementing them with 2D map and curtain views.

## Functionality

### Data Loading Functions
*   **`void read_navSect()`**:
    *   **Purpose:** Loads navigation tracks (survey lines) into the application.
    *   **Action:** For each navigation section, it reads binary `.nav` files (JCU_BINNAV_RECLEN format) to extract time, latitude, and longitude for each ping. It also calculates a simple smoothed navigation track. If `navSect_is_ADCP` is enabled, it proceeds to load associated ADCP data.
*   **`int load_adcpSect(int sectno)`**:
    *   **Purpose:** Loads ADCP (Acoustic Doppler Current Profiler) current profiles and associated motion data for a specified navigation section.
    *   **Action:** Reads `.N.r4`, `.E.r4`, and `.D.r4` files for North, East, and Downward velocity components respectively. It also loads a `.motion` file (OMG_HDCS_summary_attitude format) to get attitude (roll, pitch, heading) for each ping. It calculates the mean and standard deviation for each velocity component.
*   **`int load_modelEpoch(int epochno)`**:
    *   **Purpose:** Loads current or other physical model outputs for a specific "epoch" (time slice) for visualization.
    *   **Action:** Reads navigation positions from a `.curr` file and detailed depth profiles (temperature, salinity, sound speed, U/V/W velocities) from a `.prof` file for each node in the model.

### Initialization Functions
*   **`void init_navSect_variables()`**: Sets default values for visualization parameters, including `navSect_size`, `navSect_col`, `trim_height`, `plot_around_radius_m`, ADCP display flags, averaging factors, and initializes XImages for the map and curtain graphics.
*   **`int setup_adcpSect_params()`**: Sets default display flags for ADCP visualization, such as `ADCP_show_beampatts` (beam patterns) and `ADCP_show_bins`.
*   **`int get_default_mapImage_bounds()`**: Calculates initial bounding box coordinates for the map display based on the loaded plate (DTM) header dimensions.

### Drawing Functions
*   **`void draw_navSect()`**:
    *   **Purpose:** Renders navigation tracks and ADCP data in the 3D scene.
    *   **Action:** Draws each point of the active navigation sections as a cross (color-coded per section). Filters these points by a user-defined bounding box on the map. Displays vertical "fix step" lines along the track. For ADCP-enabled sections, it draws the selected ADCP ping (and optionally surrounding pings for a "caterpillar" effect) with its orientation and current profiles.
*   **`void draw_ModelEpoch(int epoch)`**:
    *   **Purpose:** Renders model output nodes and their associated current profiles in 3D.
    *   **Action:** Draws each model node and, if current data is present, displays its vertical current profile as a scaled and oriented vector field (using `draw_Current_Profile`).
*   **`void draw_select_navSect()`**:
    *   **Purpose:** Draws the 2D map graphic within the widget's interface.
    *   **Action:** Displays the underlying DTM as a background image, overlays the navigation section tracks, and highlights the current zoom bounding box and the 3D view's look-at point.
*   **`void draw_Curtain_navSect()`**:
    *   **Purpose:** Draws the 2D curtain plot graphic within the widget's interface.
    *   **Action:** Visualizes ADCP current profiles (N, E, or D velocity components vs. depth and ping number) as a color-scaled image. It applies averaging if `use_Average` is enabled and displays mean/sigma values. Also draws a vertical line indicating the currently selected ping and horizontal lines representing the seabed and trimmed height.
*   **`void draw_list_navSect()`**: Displays a list of loaded navigation sections in a graphic window, indicating their visibility status.
*   **`void draw_list_ModelEpoch()`**: Displays a list of loaded model epochs in a graphic window, showing their time ranges.

### Coordinate Scaling Functions
*   **`void scale_navSect()`**: Transforms geographical coordinates (latitude, longitude) of navSect points into the OpenGL scene's coordinate system, projecting them onto the DTM, and calculates their 3D locations (including depth from DTM).
*   **`void scale_modelEpochs()`**: Performs similar scaling for model epoch nodes, including projecting them onto the DTM and calculating their 3D scene coordinates.

### Widget Management Functions
*   **`void make_navSect_widget()`**:
    *   **Purpose:** Creates the graphical user interface for the "navSect Display Control" panel.
    *   **Action:** Sets up sliders (e.g., for `trim_height`, `ping step`, `Vertical Fix Step`, `ADCP Current Exag`, `Pixel Trim Radius`, `Plate Vert Exag`, `Averaging Factor`), buttons for display toggles and animations, and initializes four graphic windows for the map, navSect list, curtain plot, and model epoch list.
*   **`int manage_navSect_widget_events(XEvent event)`**:
    *   **Purpose:** Handles all user interactions within the navSect widget.
    *   **Action:** Processes mouse events (rubber-banding for map zoom, middle-click to select/center on pings, clicking on lists to toggle visibility), button presses (toggling display modes, enabling recording, changing view focus), slider adjustments, and keyboard shortcuts (resetting zoom, panning map, stepping through pings, adjusting `lookat_Z` or `calc_curr.depth`).
*   **`void refresh_navSect_widget_window(Window window)`**: Refreshes the display of the widget's components as needed.

### Animation and Navigation Functions
*   **`int centre_on_adcpPing(int pingno)`**: Centers the 3D view on a specific ADCP ping and updates the active display bounding box if `plot_around_ping` is enabled.
*   **`int load_adcpPing(int pingno)`**: Loads the ADCP current profile for a specific ping into the `curr_prof` structure for plotting, calculating magnitudes, azimuths, and depressions.
*   **`int aver_adcpSect(int sectno)`**: Applies an along-track averaging filter to the ADCP velocity components based on `avFactor`.
*   **`int ping_ADCP_away()`**: Animates through ADCP pings, updating the display for each ping and optionally dumping frames to create video sequences.

### Image Handling Functions
*   **`int loadup_relevant_mapImage()`**: Loads intensity data from the underlying DTM (`plate_inten`) into an XImage (`DTM_image`) for display in the map graphic window.
*   **`int loadup_relevant_CurtainImage()`**: Loads ADCP velocity component data (N, E, or D) into an XImage (`CUR_image`) for display in the curtain plot graphic window.
*   **`int dump_adcp_frame()`**: Dumps multiple RGB image files (3D view, map, curtain plot) for the current ADCP ping.
*   **`int dump_one_subwindow(int subwin, char *string)`**: A utility function to dump the content of a specific sub-window to a PPM image file.

This module is a highly specialized and powerful tool within `glSeis` for the detailed analysis, visualization, and presentation of navigation tracks and ADCP current data in complex 2D and 3D contexts, aiding in the interpretation of dynamic oceanographic processes and their impact on acoustic surveys.