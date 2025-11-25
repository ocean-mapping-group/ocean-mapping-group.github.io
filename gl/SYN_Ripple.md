---
layout: default
title: SYN_Ripple
parent: GL Tools
nav_order: 21
---

# SYN_Ripple

## Description
`SYN_Ripple.c` is a module within the `SYN` project (likely `synSwath`), located in the `gl/` directory. Its primary function is to simulate and visualize various ripple and dune geometries on the seafloor. It's designed to explore the impact of these complex bottom morphologies on acoustic backscatter, particularly at near-normal incidence, which is crucial for understanding sonar performance and seafloor characterization. It provides an interactive GUI widget to define intricate ripple patterns and observe their 3D representation. It is not a standalone command-line tool.

This module allows users to generate and manipulate detailed models of seafloor ripples, making it a valuable tool for research and educational purposes in marine acoustics and geology.

## Functionality

### `void make_RIP_widget()`
*   **Purpose:** Configures and creates the "Ripple/Dune Geometry Control" panel, which is the user interface for this module.
*   **Action:** Sets up a panel containing:
    *   **Sliders**: A comprehensive set of sliders for defining detailed ripple morphology:
        *   `Ripple Scaling`: Overall scaling factor for the ripple field.
        *   `Ripple Wavelength (m)`: The fundamental wavelength (distance between crests) of the ripples.
        *   `Ripple Amplitude Aspect`: A ratio determining the height of the ripples relative to their wavelength.
        *   `Phase (deg)`: A phase shift that controls the starting point of the ripple pattern.
        *   `Azimuth (deg)`: The orientation (direction) of the ripple crests.
        *   `Peakedness`: Controls whether the ripple crests or troughs are sharper (+1.0 for peaked crests, -1.0 for peaked troughs).
        *   `Asymmetry`: Defines the slope asymmetry of the ripples (e.g., for dunes, +1.0 for a vertical lee slope, -1.0 for a vertical stoss slope).
        *   `Angularity`: Controls the shape transition from sinusoidal (0.0) to planar (+1.0).
        *   `Sinuosity Length m`: The wavelength of any cross-flow sinuosity in the ripple crests.
        *   `Sinuosity Aspect`: A ratio defining the amplitude of the cross-flow sinuosity relative to its length.
    *   **Buttons**: To toggle the display of `show Normals` (surface normals) and `show Rays` (visualizing acoustic rays interacting with the surface).
    *   **Graphic Areas**: Two graphic windows are typically included, likely for 2D visualizations of ripple profiles, spectral characteristics, or ray interaction, though their specific content is not explicitly detailed in this snippet.

### `int manage_RIP_widget_events(XEvent event)`
*   **Purpose:** Handles all user interaction events (button clicks, slider movements, keyboard input) within the Ripple widget.
*   **Action:**
    *   **Quit Button:** Unmaps the widget's window.
    *   **Button Clicks:** Toggles display flags (`RIP_show_normals`, `RIP_show_rays`).
    *   **Slider Interaction**: Updates global variables linked to the sliders (e.g., `Ripple_Wavelength_m`, `Ripple_Amplitude_Aspect`). Importantly, changes to related parameters (like wavelength or amplitude aspect) automatically update dependent variables (e.g., `Ripple_Amplitude_m`). Similarly, sinuosity parameters update `Ripple_Sinuosity_Offset_m`. After any parameter change, it calls `calc_RIP_surface()` to re-calculate the ripple DTM, and then `draw_all_RIP()` and `draw_all()` to update the 3D display.
    *   **Keyboard Shortcuts**: `KEY_Z` resets the selected slider's value to a default. Arrow keys (`KEY_LEFT`, `KEY_RIGHT`) incrementally adjust slider values.

### `void alloc_RIP_plate()`
*   **Purpose:** Dynamically allocates memory for the Digital Terrain Model (DTM) grid that will store the generated ripple surface.
*   **Action:** Frees any existing memory allocated for the DTM, sets `plate_header` dimensions (width `RIP_x`, height `RIP_y`, pixel size `RIP_pixel_m`), and then allocates new memory for `plate_coords` (3D coordinates), `plate_bs` (backscatter strength), `plate_depth` (depth values), `plate_time`, `plate_phase`, `plate_color` (8-bit color map), and `plate_inten` (8-bit intensity map). This effectively creates a fresh DTM grid tailored for the ripple model.

### `float calc_ripple_profile(float wave_fraction, float peakedness, float angularity, float asymmetry)`
*   **Purpose:** Calculates the normalized height of a ripple at a given fractional position along its wavelength, incorporating various morphological parameters.
*   **Action:** Starts with a basic cosine wave, then modifies it to introduce `peakedness` (by adding a sine wave of double the wavelength). While `angularity` and `asymmetry` are passed as arguments, their direct impact on the height calculation isn't fully shown in the provided snippet's `normalized_height` formula, suggesting they might be used elsewhere or in more complex versions of the profile calculation.

### `void calc_RIP_surface()`
*   **Purpose:** Generates the 3D ripple surface (DTM) based on the current widget parameters.
*   **Action:** Iterates through each grid cell (i,j) of the allocated DTM (`plate_header.dx` by `plate_header.dy`). For each cell, it calculates:
    *   Its radial distance and bearing relative to the origin.
    *   Its relative bearing to the `Ripple_Azimuth_deg`.
    *   The `dist_propagated` and `lambda_fraction` for the ripple wave component.
    *   The `local_ripple_ht` (height) using `calc_ripple_profile()`.
    *   This height is stored in `*(plate_depth + ...)` and also used to generate a greyscale color/intensity map (`*(plate_color + ...)`, `*(plate_inten + ...)`), which reflects the ripple amplitude.
    *   Finally, it calls `scale_plate()` (an external function) to transform the newly calculated DTM into the OpenGL scene's coordinate system, making it ready for 3D rendering.

### `void init_RIP_variables()`
*   **Purpose:** Initializes all global variables and parameters related to the Ripple module to their default states.
*   **Action:** Sets default values for `RIP_seafloor_depth_m`, `RIP_pixel_m`, `RIP_x`, `RIP_y`, and all ripple morphology parameters (e.g., wavelength, amplitude aspect, phase, azimuth, peakedness, asymmetry, angularity, sinuosity).

### `void draw_all_RIP()`
*   **Purpose:** Placeholder for OpenGL drawing calls specific to the ripple surface.
*   **Action:** While currently empty in the provided snippet, this function would typically contain or orchestrate the OpenGL commands to render the ripple surface if its drawing was not fully handled by `draw_plate()` (which renders the generic `plate_depth` DTM). It might set specific material properties or transformations unique to the ripple visualization.

### `void refresh_RIP_widget_window (Window window)`
*   **Purpose:** Refreshes the display of the Ripple widget's components.
*   **Action:** Redraws buttons, sliders, and the graphic windows as needed, ensuring the widget remains responsive and up-to-date with parameter changes.

This module provides a powerful and interactive platform for visualizing and exploring the complex geometries of seafloor ripples and dunes, and offers a fundamental way to study their potential acoustic characteristics within the `SYN` simulation environment.