---
layout: default
title: SYN_animate
parent: GL Tools
nav_order: 2
---

# SYN_animate

## Description
`SYN_animate.c` is a source code file within the `glSeis` application, specifically designed to handle animations and dynamic drawing routines for the simulated environment. It is not a standalone command-line tool.

This module orchestrates time-series playback, "wobble" animations of the simulated platform, and the drawing of various echo and pulse visualizations in 2D and 3D.

## Functionality

### `void bound_BD_series()`
*   **Purpose:** Determines the time boundaries for displaying echo time-series data, particularly for bottom detection (BD) series.
*   **Action:** It calculates `first_pulse_data` and `last_pulse_data`, which define the start and end indices of the relevant portion of the time-series array. It can either use fixed ranges or dynamically find the extent of valid data. It also calculates `pulse_location`, which represents a central point within the echo envelope.

### `void make_pulse_animation()`
*   **Purpose:** Creates an animation of the sonar pulse propagating through time-series data.
*   **Action:** It iterates through a defined range of the time series, updates `pulse_location` for each step, calls `draw_all()` to re-render the 3D scene, and can optionally dump RGB frames to create a video. It is primarily used to visualize the pulse's movement over the echo envelope.

### `void draw_pulse_hemisphere(float radius, int method)` and `void draw_pulse_hemisphere_bounds(float radius, int method, ...)`
*   **Purpose:** Renders a 3D translucent hemisphere in the OpenGL scene, representing the sonar's ensonified volume.
*   **Action:** These functions use OpenGL primitives (`GL_QUADS`) to draw a spherical segment. The `radius` parameter controls its size, and the `method` parameter allows for different rendering styles (e.g., by transmit steering, receive steering, or general). It uses a defined transparency for visualization.

### `void draw_2D_trace_echo()`
*   **Purpose:** Draws a 2D representation of an echo trace (time-series) in an OpenGL overlay.
*   **Action:** It plots the intensity (backscatter) and phase information of an echo. It scales the data within a specified range and highlights specific points like the current `pulse_location` and detected bottom detections. It includes basic drawing of amplitude envelopes and phase curves.

### `void wobble_platform(int doroll, int dopitch, int doazi, int doheave)`
*   **Purpose:** Generates a cyclical animation where the simulated vessel/sensor platform's orientation (roll, pitch, azimuth, heave) is dynamically varied.
*   **Action:** It iterates through a full angular cycle, applying sinusoidal perturbations to the platform's specified motion parameters. For each step, it recalculates related parameters, redraws the 3D scene, and can save animation frames. This is used to visually demonstrate the effects of platform motion.

This module is crucial for providing dynamic, interactive, and visually informative simulations within the `glSeis` application.