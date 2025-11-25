---
layout: default
title: SYN_plate_select
parent: GL Tools
nav_order: 19
---

# SYN_plate_select

## Description
`SYN_plate_select.c` is a module within the `glSeis` (or `SYN` project) application, designed for the interactive selection, manipulation, and visualization of Digital Terrain Models (DTMs), referred to as "plates." It provides a dedicated graphical user interface (GUI) widget that empowers users to load, scale, rotate, translate, and define specific sub-regions of interest within different DTMs. It is not a standalone command-line tool.

This module is essential for visualizing and analyzing bathymetric data within the 3D simulation environment, offering flexibility in both global (full DTM) and local (sub-region) contexts.

## Functionality

### `void make_plate_select_widget()`
*   **Purpose:** Configures and creates the "Plate Select" control panel.
*   **Action:** Sets up a panel containing:
    *   **Sliders**: For adjusting various DTM transformation parameters:
        *   `Plate Azimuth (deg)`: Rotates the DTM around the Z-axis.
        *   `Plate Roll (deg)`: Tilts the DTM around the X-axis.
        *   `Plate Pitch (deg)`: Tilts the DTM around the Y-axis.
        *   `Plate Scale`: Uniformly scales the DTM.
        *   `Plate V.E.`: Controls the vertical exaggeration of the DTM.
    *   **Buttons**: A "Select" button (although DTM loading typically occurs upon clicking an item in the list graphic).
    *   **Graphic Areas**:
        *   A list-like display to select which DTM file (`platename`) from the loaded options is currently active.
        *   A 2D map graphic (`draw_plate_select_map`) providing an overview of the selected DTM, including an interactive bounding box to define a sub-region of interest.

### `int manage_plate_select_widget_events(XEvent event)`
*   **Purpose:** Handles all user interaction events (mouse, keyboard, button/slider input) within the "Plate Select" widget.
*   **Action:**
    *   **Quit Button:** Unmaps the widget's window and refreshes the main 3D scene.
    *   **Slider Interaction:** Updates global variables linked to the sliders (e.g., `plate_heading`, `plate_roll`, `plate_pitch`, `plate_scale`, `vert_exag`), then triggers `recalc_relative_plate_shifts()` (to adjust position based on scale/rotation), `scale_plate()` (to apply transformations to the DTM data), and `draw_all()` (to refresh the 3D scene).
    *   **Graphic Area Clicks (DTM List)**: Sets `current_plate` to the selected DTM's index, then loads the new DTM via `load_in_plate()`, prepares its map image with `load_up_plate_map()`, scales it with `scale_plate()`, and redraws the main scene and widget.
    *   **Graphic Area Clicks (2D Map)**:
        *   **Left-click (Button 1):** Defines the top-left (`plate_sub_minx`/`miny`) or bottom-right (`plate_sub_maxx`/`maxy`) corners of a sub-region bounding box, depending on whether it's the start or end of a drag.
        *   **Middle-click (Button 2):** Sets the `plate_focus_x`/`y` at the clicked location, then calls `recalc_relative_plate_shifts()` to adjust the plate's `plate_xshift`/`yshift` so this focus point is centered.
        *   **Right-click (Button 3):** Defines the `plate_sub_maxx`/`maxy` of a sub-region bounding box.
        *   After any map interaction, it triggers `draw_plate_select_map()` and `draw_all()` to update the graphical representation.
    *   **Keyboard Shortcuts:**
        *   `KEY_D`: Iterates through all loaded DTMs, loading each one, scaling it, refreshing the widget, redrawing the main scene, and dumping an RGB image of the scene.
        *   `KEY_UP`/`KEY_DOWN` (on DTM list): Selects the next/previous DTM in the list.
        *   `KEY_UP`/`KEY_DOWN`/`KEY_LEFT`/`KEY_RIGHT` (on 2D map): Scrolls the displayed sub-region bounding box.

### `void draw_plate_select_map()`
*   **Purpose:** Renders the 2D map graphic that shows an overview of the selected DTM.
*   **Action:** Clears its window, draws the `PLATE_image` (a greyscale representation of the DTM's intensity or color data) as a background, and overlays a black bounding box to indicate the currently selected sub-region. It also displays a blue cross/diamond at `plate_focus_x`/`y` and shows the current `plate_xshift`, `plate_yshift`, `plate_zshift` values as text.

### `void load_up_plate_map()`
*   **Purpose:** Prepares an XImage (`PLATE_image`) for the 2D map graphic from the currently loaded plate's intensity data.
*   **Action:** Iterates through the loaded `plate_inten` (intensity map) and puts pixels into the `PLATE_image`, scaling the intensity to greyscale values for display. It also calculates initial `plate_focus_x`/`y` based on current `plate_xshift`/`yshift`.

### `void recalc_relative_plate_shifts()`
*   **Purpose:** Re-calculates `plate_xshift` and `plate_yshift` based on `plate_focus_x`/`y` and `plate_scale`.
*   **Action:** This function ensures that when the user adjusts the focus point on the 2D map, the corresponding 3D translation of the plate in the main scene is accurately updated.

### `void init_plate_select_variables()`
*   **Purpose:** Initializes global variables and parameters related to plate selection and display.
*   **Action:** Sets default values for the sub-region bounding box (`plate_sub_minx`/`maxx`/`miny`/`maxy`) and allocates memory for the `PLATE_image` XImage used for the 2D map display.

### `void refresh_plate_select_widget_window (Window window)`
*   **Purpose:** Refreshes the display of the "Plate Select" widget's components.
*   **Action:** Redraws buttons, sliders, the DTM list (`jX_draw_list`), and the 2D DTM map (`draw_plate_select_map`) as needed (e.g., on `Expose` events or after parameter changes).

This module provides a robust and interactive environment for managing and visualizing Digital Terrain Models within `glSeis`, allowing users to explore and analyze bathymetric data with flexibility and detail in both global and local contexts.