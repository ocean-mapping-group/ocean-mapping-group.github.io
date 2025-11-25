---
layout: default
title: temp.c
parent: GLSEIS Tools
nav_order: 10
---

# temp.c

## Description
`temp.c` is a small source code file from the `glSeis` application. It is not a standalone command-line tool. This file contains a single utility function, `draw_axes`, which is responsible for rendering a 3D coordinate axis system (X, Y, and Z axes) in the main OpenGL window.

The name "temp.c" suggests it may have been a temporary file for testing drawing functions, but it provides a core piece of the visualization framework.

## Functionality

### `void draw_axes()`
*   **Purpose:** To draw a visual representation of the X, Y, and Z axes at the origin of the 3D world space. This is a common feature in 3D applications to help the user maintain a sense of orientation.
*   **Action:**
    1.  **Debug Output:** The function first prints the current orientation and position of the "object" (likely the sonar) to the console for debugging purposes.
    2.  **Draw X-axis:** It draws a red cylinder along the positive X-axis, with a red cone at the end to serve as an arrowhead.
    3.  **Draw Y-axis:** It rotates the coordinate system and draws a magenta-colored cylinder and cone along the positive Y-axis.
    4.  **Draw Z-axis:** It rotates again and draws a blue cylinder and cone along the positive Z-axis.
*   **Implementation:** The function uses OpenGL transformation commands (`glPushMatrix`, `glScalef`, `glRotatef`, `glTranslatef`) to position and orient each axis. The actual drawing of the shapes is delegated to custom external functions (`draw_cylinder_filled` and `draw_tapered_cylinder_filled`).

This function is called whenever the scene needs to be redrawn and the `axes_flag` is enabled, providing a persistent and helpful reference for navigating the 3D data.