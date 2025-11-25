---
layout: default
title: SYN_LBL
parent: GL Tools
nav_order: 12
---

# SYN_LBL

## Description
`SYN_LBL.c` is a module within the `glSeis` application, specifically designed for simulating and visualizing Long Baseline (LBL) acoustic positioning systems. It is not a standalone command-line tool.

This module allows users to interactively define an LBL transponder array, place a mobile target within this array, observe acoustic ranges, and visualize the positioning geometry in a 3D OpenGL environment. It also supports the simulation of a surface vessel ("barge") affecting the relative target position.

## Functionality

### `void make_LBL_widget()`
*   **Purpose:** Configures and creates the graphical user interface for the "LBL Transponder Array Control" panel.
*   **Action:** Sets up a panel containing:
    *   **Buttons:** To toggle the display of `spheres` (representing transponders or range spheres), `rays` (acoustic paths from transponders to target), `P. depth` (a horizontal plane at the target's depth), the `target` itself, and a simulated `barge` (surface vessel).
    *   **Sliders:** For adjusting parameters of the currently selected LBL transponder (e.g., `Tracking Range`, `X Location`, `Y Location`, `Z Location`) and the mobile target (`TARGET X`, `TARGET Y`, `TARGET Z`).
    *   **Graphic Area:** A list-like display that allows the user to select which specific transponder's properties are currently being modified by the sliders.

### `int manage_LBL_widget_events(XEvent event)`
*   **Purpose:** Handles all user interaction events (button clicks, slider movements, keyboard input) within the LBL control widget.
*   **Action:**
    *   **Button Clicks:** Toggles display flags (`LBL_show_spheres`, `LBL_show_rays`, `LBL_show_Pdepth`, `LBL_show_target`, `show_BARGE`) and then triggers `draw_all()` to refresh the main 3D scene.
    *   **Graphic Area Clicks:** Updates `current_LBL` to change the active transponder. The sliders then reflect the properties of this newly selected transponder. The display is refreshed.
    *   **Slider Interaction:** Modifies the values of linked global variables (e.g., `LBLprops[current_LBL].range`, `LBLprops[current_LBL].x`, `LBL_target[]`), and then redraws the scene to reflect these changes.
    *   **Keyboard Shortcuts:**
        *   Arrow keys (`KEY_LEFT`, `KEY_RIGHT`): Allow incremental adjustment of slider values.
        *   `KEY_SPACE`: Toggles the visibility of a transponder selected in the graphic area.

### `void draw_LBL()`
*   **Purpose:** The main OpenGL drawing function responsible for rendering all components of the LBL system in the 3D scene.
*   **Action:**
    *   Draws each LBL transponder as a small sphere with an attached cylindrical marker.
    *   If `LBL_show_rays` is enabled, it draws lines (representing acoustic rays) connecting each visible transponder to the target.
    *   If `LBL_show_spheres` is active, it draws translucent spheres around each transponder. The radius of these spheres corresponds to the calculated range to the target, visually representing the range uncertainty or the geometric basis of the LBL solution.
    *   If `LBL_show_Pdepth` is enabled, a horizontal plane is drawn at the target's depth.
    *   Renders the `LBL_target` itself. Optionally, this target can be drawn as a detailed model of a Hugin AUV.
    *   Optionally, a simulated `barge` (surface vessel) is drawn. If `show_BARGE` is active, the target's coordinates are dynamically updated to be relative to the barge's motion, using a Direction Cosine Matrix (DCM) rotation (`DCM_unrotate`).
    *   Continuously calculates and updates `LBLprops[i].range` (the range from each transponder to the target).

### `void init_LBL_variables()`
*   **Purpose:** Initializes all global variables and parameters related to the LBL system to their default states.
*   **Action:** Sets initial display flags (e.g., `LBL_show_spheres = 1`), defines a default target position (`LBL_target`), sets the initial number of transponders (`no_LBLs`), and assigns default names to the transponders. If a custom LBL file (`LBLname`) is provided, it loads transponder positions and target coordinates from that file.

### `void refresh_LBL_widget_window(Window window)`
*   **Purpose:** A standard refresh function for the LBL widget's display.
*   **Action:** Handles `Expose` events to redraw buttons, sliders, and the list-like graphic area that displays the transponder names.

This module provides an interactive and visually intuitive environment within `glSeis` for studying LBL acoustic positioning principles, exploring transponder array geometries, and simulating target tracking scenarios.