---
layout: default
title: SYN_jGL_draw
parent: GL Tools
nav_order: 9
---

# jGL_draw.c

## Description
`jGL_draw.c`, located in the `code/subr_graphics` directory, is a generic OpenGL drawing utility file. It provides a comprehensive set of functions for rendering various 3D objects and managing the camera view within the `glSeis` application, and potentially other related OpenGL-based tools. This file serves as the graphical engine, handling low-level drawing primitives and higher-level models of sonar systems and environmental features. It is not a standalone command-line tool.

## Functionality

### View and Eye Position Management
*   **`void locate_eye(int where)`**: Sets the camera's position to predefined perspectives such as `EYE_ABOVE`, `EYE_AHEAD`, or `EYE_BESIDE` the scene.
*   **`void calc_eye_pos()`**: Computes the Cartesian coordinates (`eye_x`, `eye_y`, `eye_z`) of the camera based on its spherical coordinates (`eye_azi`, `eye_elev`, `eye_range`).
*   **`void move_the_view(float x, float y, float z, float ex, float ey, float ez)`**: Configures the OpenGL viewing frustum and camera position using `gluPerspective` and `gluLookAt` functions.

### Basic 3D Primitives
*   **`void draw_sphere(float xpos, float ypos, float zpos, float transp, float radius)`**: Draws a sphere at a specified 3D location, with a given radius and transparency.
*   **`void draw_rect_filled(...)`**: Draws a filled rectangle in 3D space.
*   **`void draw_arc_filled(...)`**: Draws a filled arc segment.
*   **`void draw_tapered_cylinder_filled(...)`**: Draws a cylinder that changes radius along its length.
*   **`void draw_cylinder_filled(...)`**: Draws a standard cylinder. Both cylinder functions allow specification of dimensions, color, transparency, and segmentation for visual smoothness.
*   **`void draw_shoe_box(float length, float width, float height, float red, float green, float blue)`**: Draws a simple rectangular box (cuboid).
*   **`void do_panel(float *v1, float *v2, float *v3, float *v4)`**: A lower-level utility to draw a quadrilateral given its four vertices, automatically computing normals for lighting.
*   **`void do_triangle(float *v1, float *v2, float *v3)`**: A lower-level utility to draw a triangle given its three vertices, with computed normals.

### Sonar and Sensor Models
The file includes functions to draw various detailed models of sonar systems, transducers, and their components:
*   **`void draw_EM1000()`**: Renders a model of an EM1000 multibeam sonar head.
*   **`void draw_Seabat(float tilt)`**: Draws a model of a Reson Seabat multibeam sonar.
*   **`void draw_Twin_Seabat(int num)`**: Draws a twin-head Seabat sonar configuration.
*   **`void draw_8101()` / `draw_8111()` / `draw_8125()`**: Models specific sonar transducers, typically used for profiling or imaging.
*   **`void draw_EM3000(float mount)` / `void draw_EM3000D()`**: Renders models of EM3000 series multibeam echosounders.
*   **`void draw_SMII()` / `void draw_two_row()` / `void draw_three_row()`**: Models various two-row and three-row array configurations for sonars.
*   **`void draw_Bathyscan()`**: Draws a model of a Bathyscan sonar.
*   **`void draw_disc()`**: Renders a simple disc model, often used to represent transducer elements.
*   **`void draw_SM2000()`**: Models an SM2000 sonar.
*   **`void draw_AcousticBeacon()`**: Draws a generic acoustic beacon.
*   **`void draw_SubbottomArray()`**: Renders a sub-bottom profiler array.
*   **`void draw_IandQ(int phase36th)`**: Visualizes the in-phase (I) and quadrature (Q) components of an acoustic signal as a helix in 3D, useful for signal analysis.
*   **`void draw_line_array(int transp)`**: Draws a generic linear transducer array, including visualizations of acoustic wavelengths and time-delay steering effects. This function has complex sub-modes for animating wave propagation and array shading.
*   **`void draw_T_array(float tilt, int style, float max_elev, float steer)`**: Draws a T-shaped array, commonly found in multibeam systems, and can visualize ray fans.
*   **`void draw_X_array()`**: Renders an X-shaped array, often used in Mills Cross array configurations.
*   **`void draw_30deg_Tpair()`**: Draws a pair of T-arrays, typically tilted at 30 degrees.

### Vehicle and Environmental Models
*   **`void draw_buoy(float scale)`**: Draws a detailed model of an oceanographic buoy, complete with solar panels, mast, and flotation.
*   **`void draw_M3(float scale)`**: Renders a model of an M3 multibeam sonar unit.
*   **`void draw_EM2040D()`**: Draws a model of an EM2040D multibeam sonar unit.
*   **`void draw_hugin(float tilt_option, int draw_sidescan)`**: Renders a model of a Hugin AUV (Autonomous Underwater Vehicle), including its sonar components and potentially sidescan sonar arrays.
*   **`void draw_ship()`**: Draws a generic ship model, which can be augmented with specific hull-mounted sonar transducer models.
*   **`void draw_boat()`**: A more detailed function to draw the hull of a generic boat.
*   **`void draw_ROV()`**: Draws a generic Remotely Operated Vehicle (ROV) model.

### Visualization Aids
*   **`void draw_axes()`**: Draws 3D coordinate axes in the scene, which can be aligned with the object's orientation.
*   **`void draw_cone(float steering_angle, int axis, float start_angle, float end_angle, int dobeams)`**: Renders a conical representation of a sonar beam. This function supports adjustable steering, axis alignment, and angular extent. It also handles the calculation and visualization of where the acoustic beams intersect the seafloor, generating a `swath_history`.
*   **`void draw_ek_profile(int flag)`**: Draws a 2D profile view that is relevant to echosounder (EK) geometry.
*   **`void draw_sea_surface()`**: Renders the sea surface, which can be either flat or dynamically perturbed by swells and waves, with the wave field calculated by `calc_sea_surface()`.

### OpenGL Setup and Utilities
*   **`void set_up_lighting()`**: Configures OpenGL's lighting environment, defining ambient, diffuse, and specular properties for multiple light sources.
*   **`void set_up_cylinder()` / `void set_up_sphere()`**: Initializes GLU (OpenGL Utility Library) quadric objects, which are used for efficiently drawing smooth cylinders and spheres.
*   **`short *get_normal(float *v1, float *v2, float *v3, short *normal)`**: Calculates the surface normal vector for a given triangle, crucial for correct lighting.
*   **`void setup_material_properties(int num, float red, float green, float blue)`**: Sets OpenGL material properties, including color, shininess, and transparency, for specific material indices.
*   **`void disable_transparency(int num)`**: Disables OpenGL blending for a specific material, effectively making it opaque.

This file acts as a foundational component of `glSeis`, providing the necessary graphical capabilities to render complex sonar systems, their operational environments, and the simulated outputs in an interactive 3D setting.
