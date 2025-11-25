---
layout: default
title: SYN_event_loop
parent: GL Tools
nav_order: 6
---

# SYN_event_loop

## Description
`SYN_event_loop.c` is the central event handling module for the `glSeis` application, an OpenGL-based simulation and visualization tool. It is responsible for processing all user interactions (keyboard, mouse, window events) from the X Window System and dispatching them to the appropriate handlers. It is not a standalone command-line tool.

This module is critical for the interactivity and responsiveness of the `glSeis` application, allowing users to control simulation parameters and visualization modes in real-time.

## Functionality

### `void process_x_events()`
This is the core event loop function that continuously retrieves and processes X events:
*   **Event Dispatching**: Events are first passed to `parse_which_widget()` to check if they belong to a specific GUI widget. If not, the event is handled by a general `switch` statement based on its type.
*   **Window Management**:
    *   Handles `ConfigureNotify` events for the main OpenGL window (`the_gl_win`) to update its dimensions on resize.
    *   Processes `UnmapNotify` and `Expose` events to ensure proper rendering and redrawing of windows.
*   **Mouse Interaction**:
    *   **`MotionNotify`**: Detects mouse movement, especially when a button is held down. It enables functionalities such as:
        *   Adjusting platform parameters (`object_roll`, `object_pitch`, `object_heading`, `object_heave`) by dragging in corresponding graphic windows.
        *   Modifying cone steering angles (`cone_roll`, `cone_pitch`).
        *   Changing the minimum viewable power (`MIN_VIEWABLE_POWER`).
        *   Performing rubber-banding for interactive zooming in 2D plots (e.g., bottom detection windows).
    *   **`ButtonPress` / `ButtonRelease`**: Manages clicks and releases of mouse buttons for various controls:
        *   **Main Buttons**: Toggles rendering styles (wireframe/full), auto-loading data, water surface visibility, beam pattern display, axes, coupling, beam vectors, seafloor plate visibility, ray tracing, and cone visualization.
        *   **Object Buttons**: Allows selection of different ship/sonar models (`ship_flag`) and controls the scaling of displayed objects.
        *   **Plate Display Buttons**: Changes the visualization type for the seafloor plate (phase, intensity, time), provides options to center or edge the plate, and adjusts plate resolution.
        *   **Angular Response (AR) Buttons**: Toggles the display of Angular Response, Bottom Type (BT), shading, noise, multiples, and Rayleigh fading.
        *   **Animation Buttons**: Triggers calculations for simplified beam patterns, toggles stabilization features (roll, pitch, yaw, mechanical pitch), dumps plate data, starts/stops continuous animation (`ping_away()`), and initiates frame recording.
        *   **Non-Ortho Buttons**: Controls the display of non-orthogonal cones/planes and allows selection of different calculation formulas.
        *   **Rotation (ROT) Buttons**: Enables selection of various rotation sequences (e.g., Tate Bryant Y-P-R, HIPPY Y-P-R).
        *   **Beamfootprint (BF) Select Buttons**: Triggers the generation of mock beamfootprints.
        *   **MRU Buttons**: Controls the display of accelerations, angular rates, magnetic field, residual accelerations, beach ball display, and adjusts MRU position/orientation.
        *   **Cone Steer Buttons**: Allows selection of different multi-sector cone models and toggles history drawing.
        *   **BP Buttons**: Selects beam pattern calculation models (continuous line, discrete line, circular disc) and geometry types (multibeam, bathy sidescan, simple sidescan).
        *   **Bottom Detection Window**: Handles mouse clicks for picking pulse locations and for resetting or changing the X-scale of time-series plots.
*   **Keyboard Interaction (`KeyPress`)**: Responds to a wide array of keyboard shortcuts, offering granular control over the simulation and visualization:
    *   **View Control**: Keys `7`, `8`, `9` for top, side, and front views; `5` to change the camera's look-at point; arrow keys for rotating the eye, nudging the plate/objects, and adjusting sphere/cone parameters; `+`/`-` keys for zooming in/out and modifying perturbation/viewable power parameters.
    *   **Toggle Flags**: `SPACE` key toggles reference frame, sample location visibility, 2D phase/amplitude plots, MRU at RP, and array wavelengths. `F` toggles focal length display. `E` activates/deactivates error ellipses. `K` cycles through EK flags and bottom detection plot types. `H` cycles through bottom detection plot types and hemisphere visibility. `M` dumps RGB files and cycles bottom detection plot types. `6` cycles through hull transducer displays. `0`/`1`/`2` toggle individual lights. `L` loads beam pattern files. `T` switches to transmit view, toggles taper display, or triggers a time delay animation. `G` runs scripts, starts animation, or controls ghostship display. `V` toggles frame recording. `R` switches to receive view or toggles receiver fan display. `B` switches to transmit/receive (TR\_AND\_RC) view or controls barrel RC beam angle. `A` triggers animations for eye/plate azimuth rotation, swept beams, IQ animation, or a Furuno searchlight. `J` toggles MRU updating. `W` triggers platform wobble animations or oscillates BP parameters. `C` toggles cone display. `I` toggles internal wave display or calculates incident beam patterns. `Y` toggles beam pattern display. `P` toggles plate display, prints angular response, or prints time series. `S` toggles shading in time delay animation, shows/hides a sphere, or cycles through ship models. `X` toggles ADCP beam pattern display.
    *   **Reset**: `Z` resets object/cone/slider parameters or toggles full render mode.
    *   **Quit**: `Q` exits the application.

### `int parse_which_widget(XEvent event)`
This is a crucial routing function that examines the window associated with an event. It attempts to match the event's window to a specific widget (e.g., `plate_select_widget`, `currents_widget`, `LBL_widget`, `M3_widget`, `SAS_widget`, `EK_widget`, `RIP_widget`, `IW_widget`, `LLZ_widget`, `navSect_widget`, `TCtraj_widget`, `launcher_widget`, `ADCP_widget`, `RF_widget`) and then calls that widget's dedicated event handler. This design aims to modularize the event loop and improve code organization.

### `int manage_MAIN_events(XEvent event)`
Handles events specifically targeted at the main application window, primarily `ConfigureNotify` events which occur when the window is resized.

### `int manage_ICON_events(XEvent event)`
Manages events originating from the main icon bar, which typically includes buttons for exiting the application, loading beam pattern files, and launching other specialized widgets.

This extensive module vividly demonstrates the highly interactive and configurable nature of the `glSeis` application, providing users with fine-grained control over simulation parameters and various visualization modes.