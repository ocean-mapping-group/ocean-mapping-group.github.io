---
layout: default
title: SEIS_initialise
parent: GLSEIS Tools
nav_order: 3
---

# SEIS_initialise

## Description
`SEIS_initialise.c` is a source code file containing the initialization routine for the `glSeis` application. It is not a standalone command-line tool. Its sole purpose is to define and call the `initialise_SEIS_variables()` function, which sets the default values for all major global variables used throughout the application.

This function ensures that `glSeis` starts in a consistent and predictable state before any data is loaded or user interaction occurs.

## Functionality

### `void initialise_SEIS_variables()`
This function is called once at the beginning of the `main` function in `SEIS_launcher.c` to set up the initial environment. It configures the following aspects of the application:

*   **General Flags:**
    *   `record_flag` and `frame_no` are reset for video frame recording.
    *   Debugging and verbosity flags (`JEVENT_debug`, `verbose_flag`) are turned off.

*   **Window and Rendering Settings:**
    *   Sets the default `window_name` to "OMG/UNB GL_Seis".
    *   Defines the attributes for requesting an OpenGL rendering context, with options for both `FAST` (double-buffered) and `SLOW` (single-buffered) modes.
    *   Sets the initial window dimensions to 900x900 pixels.

*   **3D Camera (Viewpoint) Settings:**
    *   `eye_range`: Sets the initial distance of the camera from the focal point (zoom level).
    *   `eye_azi`: Sets the initial azimuth (horizontal rotation) of the camera.
    *   `eye_elev`: Sets the initial elevation (vertical angle) of the camera.
    *   `focal_x`, `focal_y`, `focal_z`: Sets the point in 3D space that the camera looks at, initialized to the origin (0,0,0).

*   **Lighting and Display:**
    *   Defines the default position for a dynamic light source.
    *   `axes_flag`: Set to `1` by default, meaning the 3D coordinate axes are visible on startup.

*   **Plate (DTM) Display Settings:**
    *   `plate_flag`: Initialized to `0`, meaning the DTM is not displayed by default, even if loaded.
    *   `vert_exag`: Sets the default vertical exaggeration for the DTM to `4.0`.
    *   Initializes all DTM position shifts, rotation (`plate_heading`), and scaling factors to default values.