---
layout: default
title: SEIS_event_loop
parent: GLSEIS Tools
nav_order: 2
---

# SEIS_event_loop

## Description
`SEIS_event_loop.c` is the core event-handling module for the `glSeis` interactive OpenGL visualization application. It is not a standalone command-line tool. This file contains the main event loop that continuously listens for and processes user input (keyboard presses, mouse actions) and windowing system events (e.g., resizing, exposure).

This module is responsible for the application's interactivity, translating user actions into changes in the 3D scene, such as camera movement, display toggles, and application state changes.

## Functionality
The file contains two primary functions that work together to manage the application's event loop.

### `int parse_which_widget(XEvent event)`
This function acts as a dispatcher. When an event occurs, `parse_which_widget` checks which part of the GUI the event belongs to (e.g., the main launcher window, the watercolumn display window). If it belongs to a specialized widget, it calls that widget's own event handler (e.g., `manage_launcher_widget_events`). This modular approach keeps the code for different UI components separate.

### `process_x_events()`
This is the main event loop. It runs continuously, fetching events from the X server queue.
1.  It first calls `parse_which_widget` to see if the event should be handled by a sub-component.
2.  If the event is not handled by a sub-component, it is processed here. This function primarily handles events for the main OpenGL window (`the_gl_win`).

#### Key Handlers in `process_x_events()`
*   **`ConfigureNotify`**: Updates the application's internal record of the main window's width and height when it is resized.
*   **`Expose`**: Handles window redraw requests by calling the appropriate refresh function.
*   **`KeyPress`**: This is the most significant part of the handler, providing extensive keyboard controls for navigating and controlling the 3D scene:
    *   **Camera Views**:
        *   `7`: Top-down view.
        *   `8`: Side-on view.
        *   `9`: Ahead view.
    *   **Camera Movement**:
        *   `Arrow Keys`: Rotate the camera's azimuth (Left/Right) and elevation (Up/Down).
        *   `+` / `-` (or `PageUp` / `PageDown`): Zoom the camera in and out by adjusting its range.
    *   **Display Toggles**:
        *   `0`, `1`, `2`: Toggle the status of OpenGL lights (GL_LIGHT0, GL_LIGHT1, GL_LIGHT2).
        *   `A`: Toggles the visibility of the coordinate axes.
        *   `P`: Toggles the visibility of the loaded DTM "plate".
        *   `Z`: Toggles between a full, high-quality render and a faster, simplified one.
    *   **Application Control**:
        *   `V`: Toggles a recording flag, likely for saving animation frames.
        *   `M`: Dumps the current view to an RGB image file.
        *   `Q` or `ESC`: Exits the application.

After any action that changes the scene (like camera movement), this function calls `draw_all()` to re-render the OpenGL view and refreshes any relevant UI elements in the launcher widget.