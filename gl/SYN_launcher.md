---
layout: default
title: SYN_launcher
parent: GL Tools
nav_order: 11
---

# SYN_launcher

## Description
`SYN_launcher.c` is a module within the `glSeis` application that functions as a graphical "Widget App. launcher." It provides a centralized control panel within the `glSeis` environment from which users can open, manage, and interact with various specialized simulation and visualization widgets. It is not a standalone command-line tool.

The primary purpose of this module is to streamline the user interface, offering quick and organized access to the diverse functionalities of `glSeis`.

## Functionality

### `void make_launcher_widget()`
*   **Purpose:** Configures and creates the "Widget App. launcher" control panel.
*   **Action:** Sets up a panel containing a series of buttons. Each button is labeled with the name of a specific `glSeis` control widget (e.g., "beam pattern", "mat. props.", "currents", "ADCP", "Internal Wave", "SAS Geometry", "EK Geometry", etc.). It also defines a dummy graphics window, likely for layout consistency.

### `int manage_launcher_widget_events(XEvent event)`
*   **Purpose:** Handles all user interaction events (primarily button presses) within the launcher widget.
*   **Action:**
    *   When a button on the launcher panel is pressed, the function identifies which widget the button corresponds to.
    *   It then checks if the target widget's window is already visible (mapped).
    *   If the target widget is already mapped, it brings that widget's window to the foreground using `XRaiseWindow()`.
    *   If the target widget is not yet mapped, it makes its window visible using `XMapWindow()`, waits for it to be exposed, sets its `mapped` flag, and then calls `draw_all()` to refresh the main 3D scene. For some widgets (e.g., "cone in cone", "Internal Wave"), it also initializes specific display parameters upon launch.
    *   Handles the "quit" button for the launcher itself, unmapping its window (`XUnmapWindow()`) and setting its `mapped` flag to 0.

### `void refresh_launcher_widget_window(Window window)`
*   **Purpose:** A standard refresh function for the launcher widget's graphical elements.
*   **Action:** Primarily responds to `Expose` events to redraw the button labels and other visual components of the launcher panel, ensuring it remains visually responsive.

This module significantly contributes to the modularity and user-friendliness of `glSeis`, enabling users to selectively activate and control different simulation and visualization components without overwhelming the main application window with numerous concurrent control panels.