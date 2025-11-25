---
layout: default
title: SYN_global
parent: GL Tools
nav_order: 7
---

# SYN_global.h

## Description
`SYN_global.h` is a critical header file for the `glSeis` application, serving as a central repository for global variable declarations, constant definitions, and function prototypes. It provides the shared context and data structures that are used across various modules of the OpenGL-based simulation and visualization framework. This file is included by almost all other `.c` files in the `glSeis` project.

## Key Components

### 1. Included Header Files
The file includes several other header files that provide essential functionalities and data structures:
*   `support.h`: General utility functions.
*   `X_extra.h`: X Window System related extensions.
*   `bP_stuff.h`: Beam pattern related definitions and functions.
*   `DCM_rthand.h`: DCM (Direction Cosine Matrix) and attitude handling.
*   `matrix.h`, `array.h`: Matrix and array operations.
*   `beam_foot.h`, `backscatter.h`: Beam footprint and backscatter calculations.
*   `stdtime.h`, `swapio.h`: Time handling and byte swapping utilities.
*   `j_non_ortho_cones.h`: Definitions for non-orthogonal cone handling.
*   `jGL_draw.h`: OpenGL drawing primitives and functions.

### 2. Macros and Constants
A comprehensive set of macros and constants are defined, categorizing various aspects of the application:
*   **General Flags/Modes**: `FAST`, `SLOW`, `VT_PHASE`, `VT_INT`, `VT_TIME` (view types), `SKIP_NODE`.
*   **Graphic Window Identifiers**: `WIN_ROLL`, `WIN_PITCH`, `WIN_HEADING`, `WIN_HEAVE`, `WIN_CONE_ROLL`, `WIN_CONE_PITCH`, `WIN_MIN_dB`, `BUTTON_V`, `EYE_AZI`, `EYE_ELEV`, `PLATE_EXAG` (used to identify specific graphical display areas).
*   **Sector Definitions**: `PORT_SECTOR`, `STBD_SECTOR`, `CENTRE_SECTOR`.
*   **Bottom Detection Types**: `PHASE`, `INTEN`.
*   **Echosounder (EK) Phase Directions**: `EKPHASEPS`, `EKPHASEFA`, `EKPHASE045`, `EKPHASE315`.
*   **MRU (Motion Reference Unit) Settings**: `NED_NONE`, `NED_MRU` (position types); `RPY_NONE`, `RPY_MRU`, `RPY_ACCEL`, `RPY_ANGRATE` (orientation types).
*   **Maximum Array Sizes**: `MAX_NO_TIME_SERIES` (for time series data), `RAY_MEAN`, `RAY_LEVELS`, `RAY_INDEXES` (for Rayleigh distribution lookup).
*   **Cone Model Types**: Defines various single, twin, and multi-sector cone models (e.g., `SINGLE_1_SECTOR`, `TWIN_4_SECTOR`, `MULTI_EM710_2ROW_3_SECTOR`), used for simulating different sonar geometries.

### 3. Global Variables
A large number of global variables are declared, managing the entire state of the `glSeis` application. These variables control:
*   **Application State & Flags**: Debugging flags (`JEVENT_debug`), visibility toggles (`show_nonortho_cones`, `water_flag`, `axes_flag`, `bp_flag`, `plate_flag`, `rays_flag`, `show_Sphere`), simulation modes (`auto_load`, `multibeam`, `animate_flag`, `record_flag`).
*   **Geometric & Physical Parameters**: Ship/platform attitude (`Tx_mount`, `Rc_mount`, `Tx_orient`, `Rc_orient`, `Rc_dorient`, `object_roll`, `object_pitch`, `object_heading`, `object_heave`), MRU data (`MRU_angR`, `MRU_accelX`, `MRU_magR`), sound speed (`sound_speed`), various offsets and scales for displayed objects and plates.
*   **Simulation & Animation Control**: Time-series parameters (`time_res`, `interp_nodes`, `Time_Series`, `Phase_Series`), beam pattern characteristics (`Tr_missteer`, `Rc_missteer`, `beam_ball`, `bp_scale`), animation intervals (`ping_interval`, `frames_per_ping`), and perturbation values for platform wobble (`roll_scale`, `pitch_scale`).
*   **Data Structures**: Arrays for time series (`Time_Series`, `Phase_Series`), look-up tables (`lut_TS`, `rayleigh_TS`, `RayLUT`), widget parameter structures (`jX_widget_params BP_widget`, `material_widget`, etc.), plate data (`plate_coords`, `plate_normals`, `plate_bs`, `plate_phase`, `plate_rgb`), and geographical beam/ping data (`geobeam`, `geoping`).
*   **X Window System Elements**: Pointers to `Display`, `Window`, `Pixmap`, `Colormap`, `GC`, `Screen`, `Visual` for managing the graphical user interface.

### 4. Function Prototypes
The file declares a multitude of function prototypes for functions defined in various `.c` files throughout the project. These cover:
*   **3D Rendering & Visualization**: Functions to calculate and draw beam patterns, normals, cones, error ellipses, and various 3D objects (`calc_3dbp`, `draw_bp`, `draw_all`, `draw_error_ellipse`).
*   **GUI Widget Management**: Functions to create and manage various control widgets (`make_BP_widget`, `make_material_widget`).
*   **Seabed Interaction & Backscatter Modeling**: Functions to calculate angular response, incident beam patterns, shadows, and apply noise/multiples (`calc_angular_response`, `find_shadows`, `apply_noise`).
*   **Digital Terrain Model (DTM) / Plate Handling**: Functions for loading, scaling, drawing, and manipulating the simulated seafloor plate (`load_in_plate`, `draw_plate`, `scale_plate`).
*   **Utilities & Event Processing**: Functions for printing data, refreshing windows, setting up X, checking events, and managing simulation flow (`print_angular_response`, `refresh_window`, `check_for_stop`, `ping_away`).

In essence, `SYN_global.h` acts as the backbone of the `glSeis` application, centralizing all global definitions and declarations necessary for its complex simulation and visualization capabilities.
