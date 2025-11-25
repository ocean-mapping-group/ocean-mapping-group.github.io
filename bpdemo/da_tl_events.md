---
layout: default
title: da_tl_events.c
parent: BPdemo
nav_order: 7
---

# da_tl_events.c

## Description
`da_tl_events.c` is a source code file from the `bpdemo` application that serves as the event handler for the time-series drawing area (`DA_time`). It is not a standalone command-line tool. This file is responsible for capturing and responding to user input that occurs within the time-series visualization window. "tl" in the filename likely stands for "time-line".

## Functionality
The file's main function, `da_tl_events`, is registered as the event handler for the `DA_time` widget. It is structured similarly to the other event handlers in the application, using a `switch` statement to process different X11 events.

### Event Handling

*   **`Expose`**: This event triggers a redraw of the time-series window by calling `expose_main()`.

*   **`MotionNotify`**, **`ButtonPress`**, and **`ButtonRelease`**: These events manage mouse interactions, primarily allowing the user to draw a "rubber band" selection box with the left mouse button. The right-click action for a popup menu is commented out in this file, so it has no effect.

*   **`KeyPress`**: This event captures keyboard shortcuts when the time-series window has focus. This event handler provides unique controls compared to the other drawing areas:
    *   **`+` (Numpad):** Increases the spacing between transducer elements (`element_spacing`).
    *   **`-` (Numpad):** Decreases the spacing between transducer elements.
    *   **`Space` Bar:** Advances the animation by a single phase step, similar to the main window.
    *   The **arrow keys** are recognized but have no specific action implemented in this handler.

When a parameter is changed via a key press (e.g., element spacing), the core simulation functions (`calc_element_positions` and `calc_beam_pattern`) are called, and all visualization areas are subsequently redrawn to reflect the updated simulation state. This file gives the user direct, interactive control over the element spacing parameter from the time-series view.