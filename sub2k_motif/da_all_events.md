---
layout: default
title: da_all_events
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 6
---
# da_all_events

## Description
`da_all_events.c` is a Motif GUI source file that implements a generic event handler for all drawing areas (`DA1`, `DA2`, `DA3`, `DA4`) within the "Submetrix 2000 unraveller" application. This module centralizes the processing of various X events, allowing for interactive features such as rubber-band selection, context-menu display, and dynamic adjustment of processing parameters directly from the user interface. It determines which drawing area (DA) triggered the event and uses that context to modify global application state and refresh the display.

## Interactive Mode
This module handles the following interactive features for drawing areas:

*   **Mouse Motion (`MotionNotify`):** If a rubber-band selection is active (Button1 held down), it continuously updates the visual feedback of the rubber band within the active drawing area (`theDA`).
*   **Button 1 Press (`ButtonPress`):** Initiates a rubber-band selection within the active DA.
*   **Button 1 Release (`ButtonRelease`):** Finalizes the rubber-band selection within the active DA.
*   **Button 3 Press (`ButtonPress`):** Displays a popup menu (`da_all_popup`), providing context-sensitive options to the user within the active DA.
*   **Key Presses (`KeyPress`):** Responds to various key presses, primarily for adjusting parameters:
    *   `XK_KP_Add`, `XK_KP_Subtract`: Adjusts `qua_thresh` (quality threshold) if `RTS_ANGDIFFS` is the current `display_state` of the active DA.
    *   `XK_Up`, `XK_Down`: Adjusts `port_pc` (port amplitude percentage threshold) and `stbd_pc` (starboard amplitude percentage threshold) if `RTS_LOG_AMPL` is the current `display_state` of the active DA. It also adjusts `qua_thresh` if `RTS_ANGDIFFS` is the `display_state`.
    *   `XK_space`: If `RTS_ANGLE` is the `display_state`, it toggles the `method` for phase-to-angle conversion between method 1 and 2 (and updates `qua_thresh` accordingly) and re-primes lookup tables (`prime_LUTs`).

## How It Works
The `da_all_events` function is registered as an event handler for multiple drawing area widgets.
1.  **Event Source Identification:** Upon an event, it first determines which `DrawingArea` (DA1-DA4) triggered the event by comparing `event->xany.window` with the `window` member of each `jX_win_param` structure. The `theDA` pointer is then set to the corresponding `jX_win_param` structure.
2.  **Event Dispatch:** A `switch` statement on `event->type` dispatches to specific handlers for different X events.
3.  **Rubber Banding (`jX_rubber_band`):** Mouse motion events with Button1 pressed are used to draw a dynamic rubber band. The `theDA` structure stores the state of the rubber band.
4.  **Parameter Adjustment:** Key presses check the `display_state` of the `theDA` to determine which global processing parameters (e.g., `qua_thresh`, `port_pc`, `stbd_pc`, `method`) to modify. After modification, `handle_SUBX_block()` (not shown in this file, but implied for reprocessing) and `draw_view()`/`expose_view()` are typically called to update the display.
5.  **Popup Menu (`XmMenuPosition`, `XtManageChild`):** Button3 press triggers the display of a Motif popup menu (`da_all_popup`).
6.  **Coordinate Scaling (`jX_scaled_values`):** (Though not explicitly called in the keypress handlers for parameter adjustment, it's a common helper function in `jX_win` for mapping screen coordinates to data coordinates).
7.  **Redrawing (`expose_view`):** `Expose` events trigger a call to `expose_view`, which is responsible for redrawing the contents of the drawing area.
This module extensively uses global variables to communicate and modify application state across different parts of the GUI and processing logic.
