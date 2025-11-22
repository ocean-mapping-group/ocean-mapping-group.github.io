---
layout: default
title: bathy_events
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 2
---
# bathy_events

## Description
`bathy_events.c` is a Motif GUI source file that implements the event handler for the bathymetry drawing area within the "Submetrix 2000 unraveller" application. This module is responsible for capturing and responding to user interactions (mouse movements, button presses, key presses) to enable interactive analysis and manipulation of the displayed bathymetry data. It allows users to select regions, access context menus, and dynamically adjust various data processing parameters.

## Interactive Mode
This module handles the following interactive features in the bathymetry drawing area:

*   **Mouse Motion (`MotionNotify`):** If a rubber-band selection is active (Button1 held down), it continuously updates the visual feedback of the rubber band.
*   **Button 1 Press (`ButtonPress`):** Initiates a rubber-band selection. The anchor point of the selection is set.
*   **Button 1 Release (`ButtonRelease`):** Finalizes the rubber-band selection.
*   **Button 2 Press (`ButtonPress`):** When pressed, it calculates and prints derived values (`MaxAcross_To_Use`, `MaxDepth_To_Use`, `Slant_Range_Fraction_To_Use`) based on the mouse click coordinates, likely to give interactive feedback on processing limits.
*   **Button 3 Press (`ButtonPress`):** Displays a popup menu (`bathy_popup`), providing context-sensitive options to the user.
*   **Key Presses (`KeyPress`):** Responds to various key presses:
    *   `q`: Quits the application.
    *   `g`: Toggles `show_gates` (likely a display option for some internal processing gates) and redraws the bathymetry.
    *   `m`: Toggles `apply_motion` flag, possibly for enabling/disabling motion compensation in processing.
    *   Arrow Keys (Left/Right): Allows for interactive adjustment of various processing parameters, such as `max_variance`, `min_binned`, `qua_thresh`, `amp_perc_thresh`, `water_depth_multiplier`, and `max_across_coverage`.
    *   `SPACE`: Toggles `show_raw` (likely a raw data display mode) and redraws the bathymetry.

## How It Works
The `bathy_events` function is registered as an event handler for the bathymetry drawing area widget.
1.  **Event Dispatch:** A `switch` statement on `event->type` dispatches to specific handlers for different X events.
2.  **Rubber Banding (`jX_rubber_band`):** Mouse motion events with Button1 pressed are used to draw a dynamic rubber band. The `DA10` structure (likely a global drawing area context) stores the state of the rubber band.
3.  **Parameter Adjustment:** Key presses (Left/Right arrow keys) check the mouse's vertical position within the drawing area to determine which parameter to adjust. For example, if the mouse is in a certain vertical band, pressing `KEY_LEFT` decrements `max_variance`. After adjustment, `handle_SUBX_block` and `draw_bathy` are called to reprocess and redraw the data with the new parameters.
4.  **Popup Menu (`XmMenuPosition`, `XtManageChild`):** Button3 press triggers the display of a Motif popup menu.
5.  **Coordinate Scaling (`jX_scaled_values`):** Mouse click coordinates are scaled to internal data units for parameter adjustment or display.
6.  **Redrawing (`draw_bathy`):** Many actions lead to a call to `draw_bathy`, which updates the visual representation of the bathymetry based on current data and parameters.
This module extensively uses global variables (`DA10`, `txInfo`, `current_side`, `max_variance`, `min_binned`, `qua_thresh`, etc.) to communicate and modify application state.
