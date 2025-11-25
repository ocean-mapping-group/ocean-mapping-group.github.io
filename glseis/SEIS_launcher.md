---
layout: default
title: SEIS_launcher
parent: GLSEIS Tools
nav_order: 4
---

# SEIS_launcher

## Description
`SEIS_launcher.c` is a source code file from the `glSeis` application. It is not a standalone command-line tool. This file is responsible for creating and managing the main **launcher widget**, which acts as the primary control panel for the application.

This launcher window contains buttons to open other specialized visualization windows and sliders to control the global parameters of the main 3D view.

## Functionality

### `void make_launcher_widget()`
This function is called at startup to define and create the launcher window.
*   It sets the title of the window to "glSeis Widget App. launcher".
*   It defines the buttons that will be present in the window, including "Terrains," "Seismics," and "Water Col." These buttons are intended to launch other, more specialized, windows.
*   It configures four primary sliders, each linked to a global variable that controls the main 3D camera:
    1.  **vertical exaggeration:** Controls the `vert_exag` variable.
    2.  **View Azimuth:** Controls the `eye_azi` variable (horizontal rotation).
    3.  **View Elevation:** Controls the `eye_elev` variable (vertical rotation).
    4.  **View Range:** Controls the `eye_range` variable (zoom).
*   It then calls a lower-level function (`jX_setup_widget`) to construct the actual X11 widgets.

### `int manage_launcher_widget_events(XEvent event)`
This is the dedicated event handler for the launcher window. It processes user interactions that occur within the control panel.
*   **Button Clicks:** When a button like "Water Col" is clicked, this function is responsible for making the corresponding window visible (e.g., by calling `XMapWindow` and `XRaiseWindow`).
*   **Slider Interaction:** When a user clicks on a slider, this function calculates the new value based on the click position, updates the corresponding global variable (e.g., `eye_azi`), recalculates the camera position (`calc_eye_pos`), updates the 3D view (`move_view`), and redraws the main scene (`draw_all`).
*   **Keyboard Shortcuts:**
    *   **`Z` key:** Resets the value of the slider that currently has focus to its default (e.g., sets vertical exaggeration to 1, or resets camera position).
    *   **`A` key:** Triggers a pre-scripted animation that rotates the camera around the scene and saves out a sequence of image frames (`.ppm`), useful for creating movies.

### `void refresh_..._window()`
These functions are responsible for redrawing the launcher window itself, including its buttons and sliders, whenever an `Expose` event occurs.