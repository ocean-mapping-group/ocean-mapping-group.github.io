---
layout: default
title: RTsubx
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 14
---
# RTsubx

## Description
`RTsubx.c` is the main application file for the "Submetrix 2000 unraveller," a Motif-based graphical user interface (GUI) application designed for processing and visualizing Submetrix 2000 sonar data. This file is responsible for initializing the X Window System environment (using Xt Intrinsics), creating the primary application window, setting up its menu bar and various drawing areas, and instantiating all necessary dialog boxes (e.g., About, File Selection, Spacings, Thresholds, Bathy). It acts as the central orchestrator, connecting the GUI elements to the underlying Submetrix 2000 data processing logic.

## How It Works
1.  **Xt Initialization:**
    *   `XtSetLanguageProc()`: Sets up the language procedure.
    *   `XtToolkitInitialize()`: Initializes the Xt Intrinsics toolkit.
    *   `XtAppCreateApplicationContext()`: Creates an application context.
    *   `XtOpenDisplay()`: Opens a connection to the X display server.
2.  **Screen Depth Determination:** Determines the screen's color depth (`ddepth`) and sets `bitmap_pad` accordingly (for 8, 16, or 24-bit displays).
3.  **Main Widget Creation (`create_main_widget()`):** This function, defined within `RTsubx.c`, constructs the main application window:
    *   Creates an `ApplicationShell` (`main_widget`) as the top-level window.
    *   Creates a main `XmForm` widget (`widget8`) to manage the layout.
    *   Creates an `XmMenuBar` (`widget9`) at the top.
    *   **File Menu:** Sets up a "File" cascade button (`FileButton`) with a pulldown menu (`widget14`) containing "New", "Open", "Save", "Save As", and "Exit" options. Callbacks (`open_callback`, `save`, `save_as`, `quit`) are attached.
    *   **Settings Menu:** Sets up a "Settings" cascade button (`SettingButton`) with a pulldown menu (`widget20`) containing "Spacings", "Bathy", and "Thresholds" options. Callbacks (`display_spacings`, `display_bathy`, `display_thresholds`) are attached.
    *   **Go/Stop Buttons:** Creates "Go" (`GoButton`) and "Stop" (`StopButton`) cascade buttons, with callbacks (`go_parse`, `stop_parse`) to control the background data parsing.
    *   **Help Menu:** Sets up a "Help" cascade button (`HelpMenu`) with an "About" option (`widget23`), which calls the `about()` function.
    *   **Drawing Areas (`DA1` to `DA4`):** Creates four `XmFrame` widgets (widgetf1-f4) and within each, an `XmDrawingArea` widget (`DA1.widget` to `DA4.widget`). These drawing areas are arranged vertically within the main form.
    *   **Drawing Area Popup Menu:** Creates a popup menu (`da_all_popup`) for the drawing areas, allowing users to select different display types (e.g., "AB phase", "Log Ampl", "Sidescan", "Angle", "AngleDif", "Orientation"). Callbacks (`change_display_state`) are attached.
    *   **Event Handlers:** Attaches `da_all_events` as an event handler to each of the four drawing areas to manage interactive events.
4.  **Widget Realization:** `XtRealizeWidget(main_widget)` makes the entire widget hierarchy visible on the screen.
5.  **Initial Display Setup:**
    *   Sets initial `display_state` for each drawing area.
    *   Calls `init_windows()` to initialize drawing contexts.
    *   Initializes `current_side` to `SUBX_UNASSIGNED`.
    *   Calls `expose_view()` for each DA to perform initial drawing.
6.  **Dialog Box Creation:** Creates instances of all necessary dialog shells and message boxes (e.g., `create_BathyShell`, `create_SpacingShell`, `create_ThresholdShell`, `create_AboutShell`, `create_FileSelectionBox`, `create_CantSaveShell`, `create_ErrorShell`, `create_warning`).
7.  **Data Processing Initialization:** Calls `init_jSUBX_vals()`, `prime_Alignments()`, `set_values()`, `calc_row_spacings()`, `prime_IQ()`, `prime_LUTs()` to initialize the internal data structures and processing parameters for handling Submetrix 2000 data.
8.  **Event Loop:** `XtAppMainLoop(app_context)` enters the main X event loop, where the application waits for and processes user events.
9.  **Exit:** Exits gracefully when the application is terminated.
This file brings together all the GUI and processing components to form a functional interactive application for Submetrix 2000 data.
