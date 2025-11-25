---
layout: default
title: do_parse.c
parent: BPdemo
nav_order: 8
---

# do_parse.c

## Description
`do_parse.c` is a source code file from the `bpdemo` application that controls the execution of the main simulation/animation loop. It is not a standalone command-line tool.

This file provides the functions to start and stop a background "work procedure," which is the standard mechanism in X Toolkit (Xt) applications for running continuous tasks like animations without freezing the user interface.

## Functionality

The file defines two key functions that are linked to the "Go" and "Stop" buttons in the main menu:

### `void go_parse()`
*   **Purpose:** To start the continuous simulation/animation.
*   **Action:** This function is the callback for the "Go" button. It calls `XtAppAddWorkProc` to register a function named `plug_away` as a background work procedure. The `plug_away` function (defined elsewhere) contains the logic for a single step of the animation. Once registered, the application will call `plug_away` repeatedly whenever it is idle.
*   It also sets a global `running` flag to `1` to indicate that the simulation is active.

### `void stop_parse()`
*   **Purpose:** To stop the continuous simulation/animation.
*   **Action:** This function is the callback for the "Stop" button. It calls `XtRemoveWorkProc` to unregister the background work procedure that was started by `go_parse()`. This effectively pauses the simulation.
*   It sets the global `running` flag to `0`.

In summary, this file implements the essential start/stop control for the `bpdemo`'s dynamic behavior.