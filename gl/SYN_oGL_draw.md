---
layout: default
title: SYN_oGL_draw
parent: GL Tools
nav_order: 18
---

# SYN_oGL_draw

## Description
`SYN_oGL_draw.c` is a module within the `SYN` project (likely `synSwath`), specifically responsible for managing the 3D camera view (position and orientation) within the OpenGL simulation environment. It is not a standalone command-line tool.

This module provides the core logic for controlling how the user perceives the simulated scene, allowing for various "look-at" modes that dynamically adjust the camera based on different points of interest and the overall state of the simulation.

## Functionality

### `void move_view()`
*   **Purpose:** Sets the camera's position, orientation, and perspective in the 3D OpenGL scene. This function acts as the central control point for camera navigation within the `SYN` application.
*   **Action:**
    1.  **Retrieves Global State:** Accesses global variables that define the simulated object's current pose (`object_roll`, `object_pitch`, `object_heading`, `object_heave`), the camera's current perspective settings (`eye_x`, `eye_y`, `eye_z`, `eye_azi`, `eye_elev`, `eye_range`), and the current `lookat` mode.
    2.  **Determines Look-at Target:** Based on the `lookat` global variable, it calculates the (x, y, z) coordinates of the point the camera should focus on:
        *   **`lookat == ANTENNA`**: The target is a specific antenna position (read from `RF_props[LOOKAT_FOCUS]`), transformed from the object's body frame to the geographical frame, considering the object's attitude and heave.
        *   **`lookat == PLATE`**: The target is defined by the plate's current position and nudges (`plate_xshift`, `plate_yshift`, `plate_zshift`, `plate_xnudge`, `plate_ynudge`, `plate_znudge`).
        *   **`lookat == CENTRE`**: The target is the origin (0,0,0) of the scene.
        *   **`lookat == MIDDLE`**: The target is (0,0,0.5), representing the middle depth.
        *   **`lookat == BOTTOM`**: The target is (0,0,1.0), representing the bottom of the normalized depth range.
        *   **`lookat == CUSTOM`**: The target is explicitly set by `lookat_X`, `lookat_Y`, `lookat_Z`.
    3.  **Calculates Camera Position:** The camera's eye position (`ex`, `ey`, `ez`) is then calculated relative to the chosen look-at target, using the global `eye_x`, `eye_y`, `eye_z` values (which represent the camera's position relative to the target when the target is at the origin).
    4.  **Applies OpenGL Transformations:** Finally, it calls `move_the_view()` (a function declared in `jGL_draw.h` and implemented in `jGL_draw.c`) passing the calculated eye and target coordinates. This function, in turn, uses `gluPerspective()` to set the viewing frustum and `gluLookAt()` to position and orient the camera in the OpenGL world.

This module is a critical part of the application's visualization core, enabling users to interactively navigate the complex simulated environment, inspect different components, and analyze data from various strategic perspectives.