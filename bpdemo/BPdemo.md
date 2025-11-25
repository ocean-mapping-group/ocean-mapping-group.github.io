---
layout: default
title: BPdemo.c
parent: BPdemo
nav_order: 2
---

# BPdemo.c

## Description
`BPdemo.c` is the main source file for the **Beam Pattern Phasor Summation Demo (`bpdemo`)** application. It is not a standalone command-line tool but rather the entry point for a graphical user interface (GUI) application built with the Motif (Xm) and X Toolkit (Xt) libraries.

This file is responsible for initializing the application, creating the main window, setting up all the primary GUI widgets (menus, buttons, drawing areas), and entering the main event loop to handle user interactions.

## Functionality
The `main` function in `BPdemo.c` serves as the application's entry point. Its key responsibilities include:

1.  **Initializing the GUI Toolkit:** It initializes the X Toolkit and creates an application context.
2.  **Creating the Main Window:** It calls the `create_main_widget` function to build the entire user interface.
3.  **Entering the Main Event Loop:** It calls `XtAppMainLoop()`, which listens for and dispatches events (e.g., button clicks, mouse movements, window exposes) to the appropriate callback functions.

### GUI Structure
The `create_main_widget` function constructs the main application window, which consists of:
*   A **main window shell** with the title "OMG/UNB Beam Pattern Phasor Summation".
*   A **menu bar** with the following menus:
    *   **File:** Contains an "Exit" option to close the application.
    *   **Settings:** Provides access to "Spacings," "Three D," and "Thresholds" dialogs (though some may be commented out).
    *   **Go:** A button to start the simulation/parsing.
    *   **Stop:** A button to stop the simulation/parsing.
    *   **Help:** Contains an "About" option to display the application's information window.
*   **Drawing Areas:** The main part of the interface is divided into four main drawing areas (`DrawingArea` widgets), each intended for a different visualization:
    *   `DA_main`: The primary display area.
    *   `DA_polar`: A smaller area for polar plots.
    *   `DA_time`: An area for time-series plots.
    *   `DA_options`: An area for displaying options or parameters.
*   **Event Handling:** It attaches event handlers to the drawing areas to manage user interactions like mouse clicks, motion, and window redraw events. Pop-up menus are also created for the main and polar drawing areas to provide context-sensitive options.

This file acts as the central hub of the `bpdemo` application, bringing together all the different UI components and linking them to their respective functionalities defined in other source files.