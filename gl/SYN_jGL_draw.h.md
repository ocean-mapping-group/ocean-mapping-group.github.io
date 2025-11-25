---
layout: default
title: jGL_draw.h
parent: GL Tools
nav_order: 10
---

# jGL_draw.h

## Description
`jGL_draw.h` is a critical header file that serves as the primary interface for 3D rendering and visualization within the `glSeis` application and potentially other related OpenGL-based graphical tools. It declares a comprehensive set of OpenGL drawing functions, global variables, and constants that manage the graphical state and parameters of the simulated environment.

## Key Components

### 1. Included Header Files
The file includes necessary libraries and custom headers:
*   Standard OpenGL/GLX/GLU headers: `<GL/glx.h>`, `<GL/glu.h>`, `<GL/gl.h>`.
*   `unistd.h`: For POSIX operating system API functions.
*   `gl/image.h`: (Specifically for SGI systems) likely for image handling.
*   `DCM_rthand.h`: For Direction Cosine Matrix and attitude handling.
*   `support.h`: General utility functions.
*   `bP_stuff.h`: For beam pattern related functionalities.

### 2. Macros and Constants
A range of macros and constants are defined for clarity and configuration:
*   `X`, `Y`, `Z`: Standard Cartesian coordinate indices.
*   `MAX_ANGLE`, `ANGLE_SHIFT`: Used in angular calculations and increments.
*   **Camera Look-at Points**: `CENTRE`, `PLATE`, `SONAR`, `ANTENNA`, `MIDDLE`, `BOTTOM`, `CUSTOM` specify various points of interest in the scene for the camera.
*   **Standard Camera Eye Positions**: `EYE_ABOVE`, `EYE_AHEAD`, `EYE_BESIDE` define common viewpoints.

### 3. Global Variables
A diverse set of global variables manage the application's graphical state and simulation parameters:
*   **GLU Objects**: `GLUquadricObj *qobj_cyl`, `*qobj_sph`, `*qobj_disk` are pointers to GLU quadric objects used for drawing smooth spheres, cylinders, and disks.
*   **Lighting**: `int light[10]` controls the state of multiple light sources, and `GLfloat light_pos_variable[4]` defines the position of a movable light.
*   **Stabilization Flags**: `int roll_stabilised`, `pitch_stabilised`, `yaw_stabilised`, `mech_pitch_stabilised` indicate which motion components are stabilized.
*   **Window/View Properties**: `int glwin_width`, `glwin_height`, `float glwin_aspect` store OpenGL window dimensions; `double eye_range`, `eye_x`, `eye_y`, `eye_z`, `eye_horiz`, `eye_azi`, `eye_elev` define the camera's position and orientation.
*   **Object Attitude/Position**: `double object_heading`, `object_pitch`, `object_roll`, `object_heave`, `object_surge`, `object_sway` represent the current 3D pose of the main simulated object.
*   **Look-at/View Target**: `int lookat` defines the current camera focus mode; `float lookat_X`, `lookat_Y`, `lookat_Z` specify the coordinates of the look-at point; `int show_hull_transducer` is a flag to display a specific hull transducer.
*   **Rendering Flags**: `int full_render`, `render_res`, `low_res_flag`, `rays_flag`, `show_barrel_RC` control various rendering modes and features.
*   **Sonar Model Parameters**: `float barrel_rcbeam_angle` (specific to certain sonar models), `float nominal_depth` (a reference depth).
*   **Widget/Interactivity State**: `int conesteer_widget_mapped` indicates if a cone steering widget is active.
*   **Sonar/Receiver Display**: `int show_receive`, `SHOW_RECEIVE_FAN` are flags for controlling the display of receive arrays or fans.
*   **Plate Nudging**: `float plate_zshift`, `plate_xshift`, `plate_yshift`, `plate_znudge`, `plate_xnudge`, `plate_ynudge` are used to adjust the position of a simulated seafloor plate.
*   **Swath History**: `fvect swath_history[HIST_LEN][180]` stores historical swath data for visualization of the sonar coverage.
*   **Wobble Simulation**: `int add_wobble`, `float wobble_roll`, `wobble_pitch`, `wobble_yaw` define parameters for simulating platform motion.
*   **Time Series/Signal Visualization**: `int noIQs`, `float IQphase[10]`, `IQampli[10]`, `int currentIQ_36th` are for visualizing In-phase/Quadrature (IQ) signal components.
*   **Array Properties**: `int tx_OR_rc` (transmit or receive mode), `float virtual_ARRAY_shift`, `int SHOW_ARRAY_WAVELENGTHS`, `SHOW_FOCAL_LENGTH`, `SHOW_TIME_DELAY`, `SHOW_SHADING`, `float anim_phase_frac`, `float focal_length`, `int focal_points[5]`, `float Mills_Tx_X`, `Mills_Tx_Y`, `Mills_Tx_Z`, `Mills_scaling`, `Mills_Tx_Azi` are parameters for sonar array and beam pattern display, including time delay animation effects.
*   **Material Properties**: `jGL_matprop matprops[6]` is an array of structures defining material properties (diffuse, ambient, specular, shininess, transparency) for different objects, along with `int no_matprops`, `int current_material`, and `char *mat_name[6]` for material names.
*   **Sea Surface Parameters**: `double swell_wl`, `swell_azi`, `swell_amp`, `swell_phase`, `waves_wl`, `waves_azi`, `waves_amp`, `waves_phase`, `double wave_depth`, `int flat_flag`, `internal_wave`, `internal_wave_view`, `float sea_surface[100][100]` are parameters for simulating and drawing the sea surface.
*   **EK Profile Parameters**: `double ek_depth`, `ek_length`, `em_depth`, `em_radius` are variables related to echosounder (EK) profile visualization.

### 4. Function Prototypes
The header declares a wide range of functions, covering:
*   **3D Drawing Primitives**: `draw_sphere`, `set_up_sphere`, `set_up_cylinder`, `draw_rect_filled`, `draw_arc_filled`, `draw_cylinder_filled`, `draw_tapered_cylinder_filled`, `draw_shoe_box`.
*   **View/Camera Control**: `locate_eye`, `move_the_view`, `calc_eye_pos`.
*   **Object/Sonar Models**: `draw_appropriate_object`, `draw_ROV`, `draw_hugin`, `draw_8125`, `draw_8101`, `draw_8111`, `draw_SM2000`, `draw_EM2040D`, `draw_M3`, `draw_buoy`, `draw_ship`, `draw_boat`, `draw_IandQ`, `draw_line_array`, `draw_transverse_array`, `draw_T_array`, `draw_X_array`, `draw_30deg_Tpair`, `draw_disc`, `draw_EM3000D`, `draw_EM3000`, `draw_two_row`, `draw_three_row`, `draw_SMII`, `draw_Bathyscan`, `draw_AcousticBeacon`, `draw_SubbottomArray`, `draw_EM1000`, `draw_Seabat`, `draw_Twin_Seabat`.
*   **Specialized Drawing**: `draw_axes`, `draw_cone`, `draw_ek_profile`, `draw_sea_surface`.
*   **Normal/Panel Calculation**: `short *get_normal(float *v1, float *v2,float *v3, short *normal)`, `void do_panel(float *v1, float *v2, float *v3, float *v4)`, `void do_triangle(float *v1, float *v2, float *v3)`.
*   **Material Management**: `set_up_lighting`, `disable_transparency`, `setup_material_properties`.
*   **Ray Tracing**: `do_ray_fan`.
*   **Rotation**: `do_rotations_in_sequence`.
*   **Initialization/Calculation**: `init_ek_profile`, `calc_ek_profile`, `init_sea_surface`, `calc_sea_surface`.

In summary, `jGL_draw.h` provides the complete API for `glSeis` to construct and interact with its complex 3D visual environment. It centralizes declarations for everything from basic geometric shapes to detailed sonar and vehicle models, as well as environmental elements like the sea surface, ensuring consistent graphical representation throughout the application.
