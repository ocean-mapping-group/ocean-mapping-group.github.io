---
layout: default
title: work_proc.c
parent: BPdemo
nav_order: 15
---

# work_proc.c

## Description
`work_proc.c` is a source code file from the `bpdemo` application that contains the core function for the animation loop. It is not a standalone command-line tool.

The file defines the `plug_away` function, which is registered as an Xt "work procedure." This allows it to run in the background whenever the application is idle, driving the continuous animation of the phasor diagrams and wavefronts without blocking the user interface.

## Functionality

### `Boolean plug_away()`
*   **Purpose:** To execute a single step of the animation and ensure it continues to run.
*   **Action:** This function is called repeatedly by the application's main event loop when the "Go" button has been pressed. In each call, it performs the following steps:
    1.  **`advance_phase()`**: It calls this function to increment the simulation's global phase variable.
    2.  **`draw_main(...)`**: It calls the main drawing function for each of the visualization windows (`DA_main`, `DA_polar`, `DA_time`, `DA_options`), forcing them to redraw their content to reflect the new phase.
    3.  **`draw_threeD()`**: It also calls the drawing function for the 3D window if it exists.
*   **Return Value:** The function returns `False`. In the X Toolkit programming model, a work procedure that returns `False` is automatically re-registered to be called again. This creates the continuous loop necessary for animation. If it were to return `True`, the work procedure would be removed, and the animation would stop.

This simple function is the engine behind the dynamic, animated behavior of the `bpdemo` application.