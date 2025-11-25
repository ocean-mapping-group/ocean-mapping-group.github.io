---
layout: default
title: SYN_ROT
parent: GL Tools
nav_order: 22
---

# SYN_ROT

## Description
The ROT (Rotation Sequence) module is a conceptual component within the `SYN` project (likely `synSwath`), accessible through the `glSeis` application. Its primary purpose is to allow users to visualize and compare different Euler angle rotation sequences used to represent 3D orientations (attitude). This is crucial for understanding the complexities of attitude representation in navigation and sensor data processing. It is not a standalone command-line tool, but rather an interactive feature within the graphical simulation environment.

This module helps users comprehend how the order of rotations (yaw, pitch, roll) affects the final orientation of an object, which is a common source of error and confusion in real-world systems.

## Functionality

### `void make_ROT_widget()`
*   **Purpose:** Configures and creates the "Rotation Sequence Selection" control panel.
*   **Action:** Sets up a panel with:
    *   **Buttons:** A series of buttons, each labeled with a different Euler angle rotation sequence (e.g., "Y-P-R (Tate Bryant)", "Y-P-R0 (HIPPY)", "Y-R-P", "P-R-Y", "R-P-Y", "R-Y-P", "P-Y-R"). Selecting a button changes the global `rotation_sequence` variable.
    *   **Graphic Area:** A placeholder graphic window (its specific use is not detailed in the snippet but could be for a textual display of the active sequence or a visual aid).

### Event Handling (Part of `SYN_event_loop.c` / `synSwath.c`)
The `ROT_widget`'s events are handled by the main application's event loop, which dispatches specific actions:
*   **Button Clicks:**
    *   When a rotation sequence button is pressed, the global `rotation_sequence` variable is updated to the corresponding enumeration value (e.g., `ROT_YPR_TB`, `ROT_HIPPY`, `ROT_YRP`, etc.).
    *   `update_ROT_sequence()` is called to refresh the graphic display within the widget.
    *   `draw_all()` is called to refresh the main 3D scene, applying the newly selected rotation sequence to the simulated object.
*   **Quit Button:** Unmaps the widget's window.

### `void update_ROT_sequence()`
*   **Purpose:** Updates the graphical display within the `ROT_widget` to reflect the currently selected rotation sequence.
*   **Action:** Displays a text string indicating the active `rotation_sequence` (e.g., "rotation sequence is now Tate Bryant Y-P-R") in the widget's graphic area.

### `void do_rotations_in_sequence()` (Implemented in `jGL_draw.c`)
*   **Purpose:** Applies the currently selected Euler angle rotation sequence to the OpenGL transformation matrix.
*   **Action:** This function takes the global `heading`, `pitch`, and `roll` values and applies a series of `glRotatef()` calls in the order defined by the `rotation_sequence` variable. For example:
    *   **`ROT_YPR_TB` (Tate Bryant Y-P-R):** `glRotatef(heading, Z_AXIS); glRotatef(pitch, Y_AXIS); glRotatef(roll, X_AXIS);`
    *   **`ROT_HIPPY` (HIPPY Y-P-R, body-fixed roll):** `glRotatef(heading, Z_AXIS); glRotatef(pitch, Y_AXIS); glRotatef(roll, BODY_X_AXIS_ROTATED_BY_PITCH);`
    *   And similarly for `ROT_YRP`, `ROT_PRY`, `ROT_RPY`, `ROT_RYP`, `ROT_PYR`.

This ROT module provides a powerful and interactive platform for illustrating the fundamental differences between various Euler angle rotation conventions, enabling users to visually grasp their impact on 3D object orientation in a dynamic simulation.
