---
layout: default
title: SYN_LLZ
parent: GL Tools
nav_order: 13
---

# SYN_LLZ

## Description
`SYN_LLZ.c` is a module within the `glSeis` application, primarily designed for the visualization and interactive analysis of "LLZ" (likely "Localized Layer Z" or similar) data. This data typically consists of 3D point clouds, often derived from multibeam echosounders or other remote sensing platforms, and may include additional attributes like backscatter intensity and quality factors. It is not a standalone command-line tool.

The module provides a comprehensive set of tools for loading, filtering, interactively manipulating, and displaying these 3D point clouds within the `glSeis` OpenGL environment, often in conjunction with an underlying Digital Terrain Model (DTM).

## Functionality

### `void read_LLZ()`
*   **Purpose:** Loads LLZ data from external files into the application.
*   **Action:** Reads point data which can be of two types:
    *   An older format containing basic latitude, longitude, and depth (`llztype[i] == 0`).
    *   A newer, "multi-detect" format that includes additional attributes such as backscatter intensity (`BS`) and a quality factor (`If_Q_factor`) (`llztype[i] == 1`).
*   **Data Handling:** Dynamically allocates and reallocates memory for `geobeam` structures to store the loaded LLZ points.
*   **Navigation Overlay:** Can optionally read a companion navigation file (`.nav`) to display navigation tracks alongside the LLZ points.

### `void init_LLZ_variables()`
*   **Purpose:** Initializes global variables and parameters related to LLZ data visualization.
*   **Action:** Sets default values for display settings (e.g., `LLZ_size` for point rendering size, `LLZ_col` for color, `LLZ_scan_step` for animation speed, `LLZ_max_quality_factor`, `LLZ_min_BS_value` for filtering). It also initializes the bounding box limits (`LLZ_min_x`, `LLZ_max_x`, `LLZ_min_y`, `LLZ_max_y`) for data display. Crucially, it creates an XImage (`DTM_image`) from the `plate_inten` (DTM intensity) for display in the LLZ widget's graphic window.

### `void draw_LLZ()`
*   **Purpose:** Renders the loaded LLZ point cloud data in the 3D OpenGL scene.
*   **Action:**
    *   Each LLZ point is drawn as a cross, with its color potentially varying based on the dataset.
    *   **Filtering:** Points can be filtered based on their 2D location (within `LLZ_min_x`, `LLZ_max_x`, `LLZ_min_y`, `LLZ_max_y`), quality factor, and backscatter intensity.
    *   **Ghost Mode:** If `LLZ_show_ghosts` is enabled, points outside the active display bounding box are rendered with reduced visibility to provide context.
    *   **Vertical Exaggeration:** Applies `vert_exag` to the Z-coordinate for enhanced vertical relief.

### `void scale_LLZ()`
*   **Purpose:** Transforms the geographical coordinates of LLZ points into the OpenGL scene's local coordinate system.
*   **Action:** Projects latitude/longitude to a local (x,y) plane using `Project()` and then scales these coordinates (`scale_xyz`) to fit within the normalized 3D viewing volume, taking into account the DTM's properties and vertical exaggeration.

### `void make_LLZ_widget()`
*   **Purpose:** Creates the graphical user interface for the "LLZ Display Control" panel.
*   **Action:** Sets up a panel containing:
    *   **Sliders:** To adjust visualization parameters such as `Point Size`, `scan step` (for animations), `Max Quality Factor` (for filtering multi-detect data), and `Min BS Level (dB)` (for backscatter filtering).
    *   **Buttons:** To trigger animations (`spin azimuth`, `scan up/down`, `scan left/right`), toggle the display of "ghost" points (`show ghosts`), control the spinning plane of the "spin azimuth" animation (`spin in plane`), and save/load LLZ visualization settings (`dump Geometry`, `load Geometry`).
    *   **Graphic Windows:**
        *   An interactive 2D map displaying the underlying DTM, on which a yellow bounding box indicates the current LLZ display limits (`draw_select_LLZ`).
        *   A list-like display showing the loaded LLZ datasets, where their visibility can be toggled (`draw_list_LLZ`).

### `int manage_LLZ_widget_events(XEvent event)`
*   **Purpose:** Handles all user interaction events (mouse, keyboard, button/slider input) within the LLZ control widget.
*   **Action:**
    *   **Mouse Interaction (Graphic Window):** Supports rubber-banding in the DTM map to define the `LLZ_min_x`, `LLZ_max_x`, `LLZ_min_y`, `LLZ_max_y` bounding box for filtering displayed LLZ points. Also allows clicking on items in the LLZ list graphic to toggle their visibility.
    *   **Buttons:** Executes actions such as triggering animated camera movements (`spin azimuth`), animating the bounding box (`scan up/down`, `scan left/right`), toggling ghost point display, and saving/loading geometry settings.
    *   **Sliders:** Updates linked global variables for display parameters and triggers redraws of the scene.
    *   **Keyboard Shortcuts:**
        *   Arrow keys (`KEY_UP`, `KEY_DOWN`, `KEY_LEFT`, `KEY_RIGHT`): Allow incremental movement of the DTM map's bounding box and the camera's `lookat` point. Also adjusts slider values for `Max Quality Factor` and `Min BS Level`.
        *   `KEY_PLUS`/`KEY_MINUS`: Adjusts the camera's `lookat_Z` position.
        *   `KEY_SPACE`: Toggles the visibility of a selected LLZ dataset in the list graphic.

### `void refresh_LLZ_widget_window(Window window)`
*   **Purpose:** Refreshes the display of the LLZ widget's components.
*   **Action:** Redraws buttons, sliders, the DTM map (`draw_select_LLZ`), and the LLZ dataset list (`draw_list_LLZ`) as needed (e.g., on `Expose` events or after parameter changes).

### Animation and View Control
*   **`void spin azimuth()` (triggered by button):** Animates the camera's azimuth rotation, optionally adjusting the elevation to maintain a perspective relative to the scene if `LLZ_how_to_spin` is enabled. Dumps frames (`dump_rgbfile`) for video creation.
*   **`void scan up/down()` / `void scan left/right()` (triggered by buttons):** Animates the display bounding box across the DTM, simulating a scanning motion. Dumps frames for video creation.
*   **`void draw_select_LLZ()`**: Renders the DTM map in one of the widget's graphic windows, overlaying the currently defined yellow bounding box and a red/yellow cross indicating the camera's `lookat` point.
*   **`void draw_list_LLZ()`**: Displays a list of all loaded LLZ datasets in a graphic window, using colored rectangles to indicate whether each dataset is currently visible (green) or hidden (red).

### Configuration Save/Load
*   **`int dump_LLZ_Geometry()`**: Saves the current LLZ visualization settings (eye position, various flags, slider values, bounding box coordinates, and camera look-at point) to a text file for later retrieval.
*   **`int load_LLZ_Geometry()`**: Loads previously saved LLZ visualization settings from a text file, restoring the application's visual state.

This module is a powerful tool within `glSeis` for the interactive exploration, filtering, analysis, and presentation of localized 3D point cloud survey data, enabling users to gain insights into complex bathymetric and backscatter patterns.