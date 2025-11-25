---
layout: default
title: SYN_NONORTHO
parent: GL Tools
nav_order: 17
---

# SYN_NONORTHO

## Description
The NONORTHO (Non-Orthogonal Cones) module is a conceptual component within the `SYN` project (likely `synSwath`), accessible through the `glSeis` application. It is designed to visualize and test different algorithms for calculating the common beam vector resulting from non-orthogonal transmit and receive transducer arrays. It is not a standalone command-line tool, but rather an interactive feature within the graphical simulation environment.

This module is crucial for understanding the complex geometric relationships and potential solutions when sonar arrays are not aligned orthogonally, which can occur due to mounting constraints or specific design choices.

## Functionality

### `void make_NONORTHO_widget()`
*   **Purpose:** Configures and creates the "Non Orthogonal Cones Algorithm Tester" control panel.
*   **Action:** Sets up a panel with:
    *   **Sliders:** A comprehensive set of sliders to define the mounting angles (Roll, Pitch, Yaw) and orientations (Roll, Pitch, Yaw) for both the Transmit (TX) and Receive (RC) arrays. This allows users to precisely configure non-orthogonal array geometries and platform motion.
        *   `TX mount ROLL`, `TX mount PITCH`, `TX mount YAW`
        *   `RC mount ROLL`, `RC mount PITCH`, `RC mount YAW`
        *   `TX orient ROLL`, `TX orient PITCH`, `TX orient YAW`
        *   `Rc Delta ROLL`, `Rc Delta PITCH`, `Rc Delta YAW` (representing the relative orientation of the receiver to the transmitter)
    *   **Buttons:** To toggle the display of `CONES` (representing the non-orthogonal beam pattern) and `PLANE` (representing the plane of commonality between the TX and RC arrays). Also, buttons to select different calculation algorithms: `JOHN`, `OTTO`, `DOUG`, `TIMK`. These buttons trigger the execution of different mathematical approaches to solve the non-orthogonal beam problem.

### Event Handling (Part of `SYN_event_loop.c` / `synSwath.c`)
The `NONORTHO_widget`'s events are handled by the main application's event loop, which dispatches specific actions:
*   **Button Clicks:**
    *   Toggles `show_nonortho_cones` (global flag): Controls the visibility of the non-orthogonal beam cones.
    *   Toggles `show_nonortho_plane` (global flag): Controls the visibility of the plane of commonality.
    *   Selects the `calc_formula` (global enum): Chooses which algorithm to use for calculating the common beam vector (e.g., `JOHN`, `OTTO`, `DOUG`, `TIMK`).
    *   Triggers `draw_all()` to refresh the 3D scene after changes.
*   **Slider Interaction:** Updates the corresponding global attitude variables (`Tx_mount`, `Rc_mount`, `Tx_orient`, `Rc_dorient`) and refreshes the scene. It also re-calculates `Rc_orient` based on `Tx_orient` and `Rc_dorient`.

### `void draw_nonortho_beam_vector()`
*   **Purpose:** Renders the calculated common beam vector and related visualization aids in the 3D OpenGL scene.
*   **Action:**
    *   Draws the `LL_beam_vect` (common beam vector) as a line, with a small sphere at its end.
    *   If `beam_vector` (global flag) is set to `2` or `3`, it draws arcs to indicate the beam's azimuth and depression angles.
    *   If `beam_vector` is set to `3`, it draws a rectangle to visualize the "instantaneous plane of refraction solution."
    *   Optionally, draws the TX and RC array vectors.
    *   If `show_nonortho_plane` is enabled and `calc_formula` is `JOHN`, it draws a translucent blue rectangle representing the plane of commonality.
    *   It also contains logic for drawing refracted ray paths based on `ref_coeff`.

### Core Calculation Logic (Implicitly called via `calc_formula`)
While not explicitly a single function in `SYN_NONORTHO.c`, the module relies on external functions for its core calculations, which are selected via `calc_formula`:
*   `calc_nonorthogonal_cones()`: (Likely implements the "JOHN" algorithm) A function to calculate the common beam vector for non-orthogonal arrays.
*   `OTTO_calc_nonorthogonal_cones()`: (Implements the "OTTO" algorithm) Another function for the common beam vector calculation.
*   Other functions for "DOUG" and "TIMK" algorithms (their specific implementations are not detailed in this module's scope but are part of the larger `SYN` project).

This NONORTHO module provides a powerful and interactive platform for researchers and students to explore, compare, and validate different algorithms for handling complex non-orthogonal sonar array geometries in a dynamic 3D simulation environment.
