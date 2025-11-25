---
layout: default
title: SYN_internal_wave
parent: GL Tools
nav_order: 8
---

# SYN_internal_wave

## Description
`SYN_internal_wave.c` is a module within the `glSeis` application, dedicated to simulating and visualizing the intricate effects of internal ocean waves on acoustic beam propagation and the resulting accuracy of seafloor mapping. It is not a standalone command-line tool.

This module integrates an internal wave model, advanced ray tracing algorithms for stratified water columns, and interactive 3D visualization to demonstrate how these oceanographic phenomena can distort sonar measurements.

## Functionality

### `void make_IW_widget()`
This function constructs the GUI control panel for the Internal Wave simulation. This panel includes:
*   **Toggle Buttons:** To control the display of the internal `wave` itself, different `seafloor` representations (actual vs. erroneously mapped), acoustic `rays`, interface `crosses`, interface `normals`, a `fan` of rays, a `profile` view, specific `beam` highlighting, different `lookat` points (sonar, interface, seabed), `actual/erron` beam comparison, `demo interface` (a local slope demonstration), `single or multiple steps` (for the layering model), `dump surface` data, and `phase_at_intercept`.
*   **Sliders:** To adjust:
    *   **Internal Wave Parameters**: `iwave wl` (wavelength), `iwave height` (amplitude), `iwave azimuth`, `iwave phase`.
    *   **Water Column Structure**: `velocline depth` (thermocline/pycnocline depth), `Seafloor Depth`, `Sound Speed Change` (across the velocline), `Sonar Depth`, `# velocline sub layers`, `velocline thickness`.
    *   **Simulation & Visualization Controls**: `HighLight Beam`, `HighLight Swath` (for selecting a specific beam/ping to highlight), `NO_IW_PINGS`, `NO_IW_BEAMS` (number of pings and beams simulated).

### `int manage_IW_widget_events(XEvent event)`
This is the event handler for the Internal Wave control widget, managing all user interactions:
*   **Button Clicks:** Toggles various display flags (`IW_show_wave`, `IW_show_seafloor`, `IW_show_rays`, etc.), changes the camera's `lookat` target, activates a local slope demonstration (`demo_local_slope`), switches between single-layer and multi-layer ray tracing models (`use_sub_layers`), initiates data dumping (`IW_dump_surface`), and toggles `phase_at_intercept`.
*   **Slider Interaction:** Updates global variables linked to the sliders, which in turn triggers recalculations of the sound speed profile (`update_velocline_sublayers()`), ping spacing (`calc_ping_spacing()`), and acoustic ray paths (`trace_beams()`), followed by a `draw_all()` call to refresh the 3D scene.
*   **Keyboard Shortcuts:**
    *   `KEY_A`: Triggers animations that cycle through `iwave phase`, `iwave azimuth`, or `velocline offset` (interface offset), dumping RGB frames for video creation.
    *   `KEY_Z`: Resets the focused slider to a default value or resets camera nudges.
    *   `KEY_PLUS`/`KEY_MINUS`: Adjusts the number of beams highlighted (`beams_to_side`).
    *   Arrow keys: Adjust slider values or nudge the camera's look-at point.

### `void draw_IW()`
This is the primary OpenGL drawing function for visualizing the internal wave simulation:
*   **Internal Wave Surface**: Renders the dynamic 3D surface of the internal wave itself (`draw_internal_wave()`).
*   **Seafloor**: Draws the seafloor, potentially showing both the "actual" and the "erroneously mapped" seafloor.
*   **Acoustic Ray Paths**: Visualizes the propagation of acoustic rays from the sonar through the water column. It can differentiate between paths calculated assuming a flat interface (the "assumed" path) and those calculated through the perturbed internal wave interface (the "actual" path).
*   **Highlighting**: Highlights specific beams and pings based on user selection.
*   **Interface Details**: Draws crosses at interface intercepts and displays interface normal vectors.
*   **Local Slope Demonstration**: Can render a local slope plane (`draw_local_slope()`) to illustrate the impact of local interface tilt.

### Core Ray Tracing & Modeling Functions

*   **`void trace_beams()`**: Orchestrates the ray tracing process by calling one of two main simulation models:
    *   **`void trace_beams_one_layer()`**: Simulates ray propagation through a simplified two-layer water column separated by a single internal wave perturbed interface. It calculates both the "assumed" acoustic path (what a sonar would measure if the interface were flat) and the "actual" path (considering the perturbed interface).
    *   **`void trace_beams_sub_layers()`**: Models ray propagation through a more complex water column with multiple sub-layers, each potentially having a different sound speed and an internal wave perturbed interface. This model provides more detailed calculations for "actual" propagation, an "ideal" path through a flat layered structure, and the "assumed" (erroneous) seafloor strike point based on flat layers but actual travel time.

*   **`void find_beam_strike(fvect start, fvect beam, fvect *strike, ...)` / `void find_specific_layer_beam_strike(layer_attrib *la, ...)`**: These functions are fundamental to the ray tracing. They determine the 3D intersection point (`strike`) of an acoustic beam with a given surface (which can be wavy). They do this by iteratively checking the beam's elevation against the surface's elevation and then calculate the local normal vector and tangential vectors (`dx`, `dy`) at the strike point. `find_specific_layer_beam_strike` extends this to layer-specific attributes.

*   **`void calc_refracted_vector(Traced_Beam *tb, int debug)` / `void calc_refracted_vector_layer_upper_interface(per_layer *layer, int debug)`**: These functions implement Snell's Law to calculate how an acoustic ray's direction changes (refracts) when it crosses an interface between two different sound speed layers. They account for the local tilt of the interface, providing the new beam vector. `calc_refracted_vector_layer_upper_interface` operates on a per-layer structure.

*   **`int refract_at_specific_interface(float elev_in, float *elev_out, float speed_above, float speed_below, int debug)`**: A simpler implementation of Snell's Law, calculating the refracted elevation angle given the incident elevation angle and the sound speeds in the two media.

*   **`float height_at_location(float x_metres, float y_metres)` / `float height_at_layer_location(layer_attrib *ab, float x_metres, float y_metres)`**: These functions calculate the height (depth) of the internal wave perturbed interface at a given (x,y) location in meters. They incorporate internal wave parameters like wavelength, amplitude, azimuth, and phase. `height_at_layer_location` uses per-layer attributes for more detailed modeling.

### Utility Functions

*   **`void calc_ping_spacing()`**: Computes the along-track horizontal distance between successive pings based on the simulated vessel's speed and ping rate.
*   **`int update_velocline_sublayers()`**: Dynamically updates the water column's sound speed profile model. This includes calculating the sound speeds and depths for each sub-layer of the velocline and generating an `IW_svp_model.jwc` file (a standard SVP format).
*   **`void IW_dump_surface()`**: Exports the current simulation parameters and the calculated seafloor strike points (from both single-layer and multi-layer models) to XYZ files for external analysis or playback.
*   **`void init_IW_variables()`**: Initializes all global variables and parameters related to the internal wave simulation to their default starting states.
*   **`int change_view_target(int target)`**: Adjusts the camera's look-at point in the 3D scene (e.g., to the sonar, interface, or seabed) and applies user-defined nudges.

This module is a comprehensive tool for exploring and understanding the complex interplay between oceanographic internal waves and acoustic bathymetry, highlighting the potential for mapping errors in such dynamic environments.