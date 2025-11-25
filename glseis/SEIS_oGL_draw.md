---
layout: default
title: SEIS_oGL_draw
parent: GLSEIS Tools
nav_order: 5
---

# SEIS_oGL_draw

## Description
`SEIS_oGL_draw.c` is a small source code file from the `glSeis` application. It is not a standalone command-line tool. This file acts as a simple wrapper or intermediary, connecting the main application's camera and view parameters to a more generic OpenGL drawing library (likely `jGL_draw.c`).

Its primary purpose is to translate the application's specific camera state into a call that updates the OpenGL viewport.

## Functionality

The file contains a single function:

### `void move_view()`
*   **Purpose:** To update the camera position in the 3D scene. This function is called whenever the viewpoint changes, for example, after the user presses an arrow key or adjusts a camera slider.
*   **Action:**
    1.  It reads the global variables that define the camera's state: the coordinates of the focal point (`focal_x`, `focal_y`, `focal_z`) and the position of the camera's "eye" relative to that focal point (`eye_x`, `eye_y`, `eye_z`).
    2.  It calculates the absolute world coordinates of the camera.
    3.  It then passes these calculated focal point and eye coordinates to a generic function, `move_the_view()`. This function (defined externally) is responsible for making the actual low-level OpenGL call (typically `gluLookAt()`) that updates the model-view matrix and repositions the camera in the 3D scene.

This function serves to decouple the main application logic from the specific OpenGL implementation details, which are handled by the generic drawing library.