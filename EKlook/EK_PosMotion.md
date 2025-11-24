---
layout: default
title: EK_PosMotion (Module within EKlook)
parent: EKlook Tools
nav_order: 7
---
# EK_PosMotion (Module within EKlook)

## Description
`EK_PosMotion` is a module within the `EKlook` interactive application, primarily responsible for managing the "Position-Motion EK-Trace window" (a graphical user interface element). This module provides a comprehensive visualization of the EK echosounder's position and motion, allowing users to analyze and understand the vessel's trajectory, attitude (roll, pitch, heading, heave), and the corresponding bottom strike points and footprints in 2D (geographic map) and 3D views. It supports the integration and comparison of multiple motion sources (e.g., primary navigation, asynchronous motion data).

## Interactive Controls

This module exposes the following interactive controls within the `EKlook` application:

| Control | Description | Related Variable |
|---|---|---|
| **Buttons** | | |
| `Centre on Ping` | Toggles whether the geographic and time series plots are automatically centered on the currently selected ping (`currenttrace`). | |
| `Look at C/M/B` | Cycles the 3D view's focus point between the vessel's origin ("Centre"), the mid-point between the vessel and the bottom strike ("Middle"), and the actual bottom strike point ("Bottom"). | |
| `Next Area` | If multiple geographic areas are loaded (via `-areas` in `EKlook`), this cycles through them, updating the geographic display. | |
| `Show Backdrop` | Toggles the display of a background orthomap in the geographic view (if loaded). | |
| **Sliders** | | |
| `Async. Motion Latency (s)` | Allows adjustment of a time latency (in seconds) applied to asynchronous motion data, essential for aligning data from different sensors in the time series plots. | |

## Visualizations

The module provides several integrated visualization panels within `EKlook`:

*   **Geographic Map View:**
    *   Displays the vessel's track, with individual pings marked.
    *   Shows the calculated bottom strike points and their corresponding footprint outlines.
    *   Can overlay a geographic backdrop image for context.
    *   Allows interactive zooming and panning.
    *   Input geographic areas (from `-areas`) can be displayed.
*   **3D View:**
    *   Provides a dynamic 3D representation of the vessel model, the EK transducer, and its effective beam pattern cone.
    *   Displays the bottom strike vector.
    *   Users can control the camera's perspective (azimuth, elevation, range) to view the scene from different angles.
    *   Various elements like coordinate axes, vessel model, and beam pattern can be toggled on/off.
*   **Time Series Plots:**
    *   Individual plots for **Roll**, **Pitch**, **Heave**, and **Heading**.
    *   Displays motion data from the main merged file (TxNav) and can overlay data from separate primary orientation files (e.g., `MRU0`) and asynchronous motion data (e.g., `POS MV`) for visual comparison and latency assessment.
    *   Allows interactive zooming along the time axis and scaling along the value axis.

## Key Bindings (within the module's graphic windows)

*   **Mouse Wheel (Scroll UP/DOWN):**
    *   Geographic Map: Zooms the map in/out.
    *   Time Series Plots: Zooms the time axis in/out.
*   **Left Mouse Drag (Rubber Banding):**
    *   Geographic Map: Defines a rectangular region to zoom into.
    *   Time Series Plots: Defines a time range to zoom into.
*   **Middle Mouse Click:**
    *   Geographic Map / Time Series Plots: Identifies the closest ping to the click location, updates `currenttrace`, and re-centers all associated displays.
*   **Keyboard Shortcuts (within 3D view):**
    *   `+` / `-` (Keypad or `+`/`-` keys): Zooms the 3D view camera in/out (`eye_range`).
    *   `Arrow Keys (LEFT/RIGHT)`: Adjusts the 3D camera's azimuth (`eye_azi`).
    *   `Arrow Keys (UP/DOWN)`: Adjusts the 3D camera's elevation (`eye_elev`).
    *   `0`, `1`, `2`: Toggles OpenGL lights (light0, light1, light2).
    *   `7`, `8`, `9`: Pre-sets common camera views (Top-Down, Side-On, Head-On).
    *   `S`: Toggles the display of the vessel (boat) model.
    *   `B`: Toggles the display of the beam pattern cone.
    *   `A`: Toggles the display of the coordinate axes.
    *   `Z`: Resets the zoom/pan in the geographic map, resets the time series plot ranges, or toggles full rendering in the 3D view.
    *   `W`: Dumps animation frames for the plan view (debug functionality).

## How It Works
The `EK_PosMotion` module visualizes the vessel's position and motion by processing navigation and attitude data from the EK echosounder. It projects this data into both a 2D geographic map and a dynamic 3D view. Interactive controls allow users to adjust views, compare motion data from different sensors, and analyze the impact of motion on bottom strike points. The module continuously updates its displays based on incoming data and user input.

## Notes
The `EK_PosMotion` module is an integral part of the `EKlook` graphical user interface, focusing on interactive analysis and visualization of position and motion data. It does not accept any command-line arguments. Its functionality is accessed and controlled entirely through the `EKlook` GUI.