---
layout: default
title: da_main_events.c
parent: BPdemo
nav_order: 5
---

# da_main_events.c

## Description
`da_main_events.c` is a source code file from the `bpdemo` application that acts as the event handler for the main drawing area widget (`DA_main`). It is not a standalone command-line tool. This file is responsible for capturing and responding to all user interactions that occur within this primary visualization window, including mouse movements, clicks, and keyboard presses.

## Functionality
The file contains a single primary function, `da_main_events`, which is registered as the event handler for the `DA_main` widget. This function uses a `switch` statement to process different types of X11 events.

### Event Handling

*   **`Expose`**: This event is triggered whenever the window or a part of it becomes visible and needs to be redrawn. The handler calls `expose_main()` to refresh the contents of the drawing area.

*   **`MotionNotify`**: This event fires when the mouse is moved within the window. Its primary use here is to update a "rubber band" selection box if the user is dragging the mouse with the left button held down.

*   **`ButtonPress` and `ButtonRelease`**: These events handle mouse clicks.
    *   **Button 1 (Left-click):** Pressing initiates a rubber-band selection box, and releasing finalizes it.
    *   **Button 2 (Middle-click):** Currently recognized but has no action associated with it.
    *   **Button 3 (Right-click):** Opens a context-sensitive popup menu (`da_main_popup`) at the cursor's location, allowing the user to change visualization modes.

*   **`KeyPress`**: This handles keyboard shortcuts when the drawing area has focus, providing real-time control over the simulation parameters:
    *   **`+` (Numpad):** Increases the number of transducer elements.
    *   **`-` (Numpad):** Decreases the number of transducer elements.
    *   **`Left Arrow`:** Decreases the beam steering angle by 5 degrees.
    *   **`Right Arrow`:** Increases the beam steering angle by 5 degrees.
    *   **`Space` Bar:** Advances the animation by a single phase step.

After a parameter is changed via a key press, the relevant calculation functions (e.g., `calc_element_positions`, `calc_beam_pattern`) are called, and all drawing areas are updated to reflect the new state of the simulation. This file is central to the interactive nature of the `bpdemo` tool.