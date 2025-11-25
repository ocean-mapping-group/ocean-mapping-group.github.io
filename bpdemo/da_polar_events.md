---
layout: default
title: da_polar_events.c
parent: BPdemo
nav_order: 6
---

# da_polar_events.c

## Description
`da_polar_events.c` is a source code file from the `bpdemo` application. It is not a standalone command-line tool. This file contains the event handler for the polar plot drawing area (`DA_polar`), which is one of the visualization windows in the GUI.

Its structure and purpose are very similar to `da_main_events.c`, but it is specifically tailored to handle user interactions within the polar plot widget.

## Functionality
The file's primary function, `da_polar_events`, is registered as the event handler for the `DA_polar` widget. It processes user input and windowing events that occur within that specific area.

### Event Handling
The function handles the following X11 events:

*   **`Expose`**: This event is sent when the polar plot window needs to be redrawn. The handler calls `expose_main()` to refresh the display of this specific widget.

*   **`MotionNotify`**, **`ButtonPress`**, and **`ButtonRelease`**: These events manage mouse interactions.
    *   **Left-clicking and dragging** (Button 1) allows the user to draw a "rubber band" selection box within the polar plot window.
    *   **Right-clicking** (Button 3) opens a context-sensitive popup menu (`da_polar_popup`) specific to the polar plot, which provides different display options for the phasor diagrams (e.g., "SUM", "Separate").

*   **`KeyPress`**: This event captures keyboard presses. However, unlike the main event handler, the `KeyPress` section in this file contains empty cases for the keys that control the simulation (e.g., arrow keys, `+`, `-`). This means that while the polar plot window can receive keyboard focus, it does not directly modify the simulation parameters. Its role is focused on display and mouse-based interaction.