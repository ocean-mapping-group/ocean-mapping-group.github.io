---
layout: default
title: init_windows
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 13
---
# init_windows

## Description
`init_windows.c` is a Motif GUI source file responsible for initializing the X-windows graphical environment and setting up the necessary drawing contexts for the "Submetrix 2000 unraveller" application. It primarily initializes four `jX_win_param` drawing area structures (`DA1` to `DA4`), sets up the default colors and graphics contexts (GCs), and prepares `pixmap` buffers for off-screen drawing to ensure smooth and flicker-free updates of the graphical elements.

## How It Works
1.  **`init_windows()` function:**
    *   **Drawing Area Initialization:** Calls `jX_init_DA()` for each of the four global `jX_win_param` structures (`DA1` to `DA4`). These functions (presumably defined in `jX_win.h`) likely set default values and allocate memory for drawing area parameters.
    *   **Graphics Context (GC) Retrieval:** Obtains a default `GC` (`draw_gc`) from the X server, which is used for all subsequent drawing operations.
    *   **Color Initialization (`jX_init_colors()`):** Calls a function (presumably from `jX_win.h`) to initialize the application's color palette. The commented-out code suggests it sets up various named colors (red, yellow, green, blue, gray, orange) and a grayscale ramp (`jX_grey`).
    *   **Default GC Settings:** Sets the foreground color of `draw_gc` to white and the background to gray.
    *   **Font Setup:** Loads a default font ("6x10") and sets it for the `draw_gc`.
    *   **Pixmap Creation (Commented Out):** Although a block of code for creating pixmaps and XImages for each DA is commented out, it indicates the intended mechanism for double-buffering (drawing to an off-screen pixmap and then copying to the window) to avoid flickering. The actual implementation relies on individual `draw_view` or `draw_bathy` functions to create their own pixmaps/XImages when needed.
This file sets up the foundational graphical elements and resources required by the Motif-based user interface.
