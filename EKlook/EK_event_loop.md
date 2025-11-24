---
layout: default
title: EK_event_loop (Module within EKlook)
parent: EKlook Tools
nav_order: 4
---
# EK_event_loop (Module within EKlook)

## Description
`EK_event_loop.c` defines the core event processing loop for the interactive `EKlook` X-window application. It is not a standalone command-line tool but rather a fundamental component that continuously monitors and responds to user interactions (mouse clicks, keyboard presses, window events) within the `EKlook` GUI. It dispatches events to various widgets (like FFT, POLAR, ZOOM, BOTTOM, POSMOTION widgets) for specialized handling, and manages interactions within the main `EKlook` window, such as zooming, scrolling through traces, and adjusting display parameters.

## Key Functionality and Interactions

| Interaction Type | Description | Controls / Bindings |
|---|---|---|
| **Event Dispatcher** | Continuously monitors for X events (e.g., mouse clicks, key presses, window exposures, motion notifications) and dispatches them to the relevant `EKlook` widgets (FFT, POLAR, ZOOM, BOTTOM, POSMOTION) for specific handling. Events not handled by a specific widget are processed by the main event loop. | |
| **Main Loop Control** | Manages the overall execution of the `EKlook` application's event loop. The application terminates upon detecting an 'Exit' command from a button or a specific key press. | `Q` or `ESC` (Key Press) |
| **Zooming and Region Selection (Main Image Window)** | Allows users to click and drag a rectangle in the main image window (`graphic_window[1]`). Upon button release, if sufficient movement occurred, this defines `zoomfirstsam`, `zoomlastsam`, `zoomfirsttrace`, and `zoomlasttrace`, updating the zoomed view. If a rubber-band selection has minimal movement, a single click sets `min_target_sample`. | Left Mouse Button (Click and Drag) |
| **Trace Navigation and Selection (Main Image Window)** | Sets the `currenttrace` to the trace number corresponding to the click location, updating displayed information and widget views. Increments/decrements the `currenttrace` variable, effectively scrolling through the available traces. | Middle Mouse Button (Click), Mouse Wheel (Scroll UP/DOWN), Arrow Keys (UP/DOWN) |
| **Display Adjustments (Histogram Window `graphic_window[2]`)** | Sets the `mindB` (minimum display dB value) based on the click's X-coordinate. Sets the `maxdB` (maximum display dB value) based on the click's X-coordinate. Sets the `trimdB` (trim dB value for target searching) based on the click's X-coordinate. Adjusts `mindB` or `maxdB` values by increments. | Left Mouse Button (Click), Right Mouse Button (Click), Middle Mouse Button (Click), Arrow Keys (LEFT/RIGHT) |
| **Toggle Display Options** | Toggles `showTrack` which can display the zoom window outline or bottom detection attempts. Handles clicks on various icon buttons (e.g., "Image", "Grey/Col.", "FFT", "Polar", "BD/ARC", "PosMotion") to map/unmap corresponding widget windows, toggle color schemes, or switch between detection modes. | `KEY_SPACE` (Main Image Window), Icon Buttons (Clicks) |

## How It Works
The `EK_event_loop` continuously monitors the X-server for user interactions and system events. When an event occurs, it first attempts to determine if a specialized widget (like the FFT or Polar display) should handle it. If not, it processes the event itself, updating core application state variables such as the `currenttrace`, zoom levels, or display thresholds. This central loop ensures that user actions are translated into real-time updates of the `EKlook` GUI and its underlying data processing.

## Notes
This module functions as the central nervous system for the `EKlook` graphical user interface. It does not accept direct command-line arguments for its operation, as its sole purpose is to manage and respond to interactive input within the running `EKlook` application. Its behavior is entirely dependent on the user's actions within the GUI.