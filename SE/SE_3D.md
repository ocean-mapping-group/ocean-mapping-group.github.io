# `SE_3D.c` - 3D OpenGL Visualization and Watercolumn Editing Tool

`SE_3D.c` is a specialized C program functioning as a core component of the `SE` (likely "Sonar Editor" or "Sounding Editor") suite. It provides a highly interactive 3D OpenGL visualization and editing environment tailored for multibeam sonar data, with a particular emphasis on watercolumn scatterers and bathymetric information. This tool allows users to explore sonar data from diverse perspectives, dynamically adjust display parameters, and interact directly with a three-dimensional representation of the seafloor and the watercolumn.

## Key Features and Functions

*   **OpenGL Initialization and Drawing (`draw_SE3D`):**
    *   Initializes the OpenGL context, clearing color and depth buffers to prepare for each new frame.
    *   Retrieves real-time vessel attitude data (roll, pitch, heading, heave) and sonar center coordinates (`SE3D_cen`) for the currently selected swath.
    *   Conditionally draws 3D axes if `show_AXES` is enabled, providing spatial orientation.
    *   Draws a 3D boat model (`draw_boat`) if `show_BOAT` is enabled, scaling and orienting it based on current vessel attitude and a `nominal_depth` for realistic representation.
    *   **3D Bottom Track Visualization (`show_3D_BTRK`):**
        *   Configures material properties (e.g., color, shininess) for the bottom track.
        *   If `show_solid_bottom` is enabled, the seafloor is rendered as a continuous, solid mesh of panels (`do_panel`) connecting adjacent `SE3D_pos` (3D position) points.
        *   Otherwise, individual bottom track points are rendered as discrete crosses, suitable for sparse data or detailed inspection.
        *   Draws small spheres at the sonar's reference point (`SE3D_cen`) for each swath, indicating sensor locations.
    *   **3D Watercolumn Visualization (`show_3D_WC`):**
        *   Iterates through selected swaths (`k`) and individual acoustic beams (`i`) within each swath.
        *   Calculates `beam_angle` and `tx_steer` for each watercolumn sample, crucial for determining the acoustic path geometry.
        *   Utilizes `calc_nonorthogonal_cones` (or `calc_nonorthogonal_cones2`) to accurately determine the 3D vector (`LL_beam_vect`) of the acoustic path in space.
        *   Filters watercolumn samples based on `idB_thresh` (intensity threshold) and `max_range` (influenced by `R0_multiplier` and `R0_width`), allowing users to focus on specific return strengths and ranges.
        *   Plots individual watercolumn scatterers as either crosses or spheres, color-coded based on their depth or intensity for enhanced interpretability.
        *   Transforms coordinates by incorporating sonar location offsets (`parameters[current_file].sonar[0].Xloc`, `Yloc`), vessel heading, and `nominal_depth`.
    *   **3D Target Visualization (`show_TARGETS`):**
        *   Iterates through a `target_list` and plots identified targets as distinct crosses in 3D, integrating their positions with watercolumn points and seafloor.
    *   **3D DTM (Digital Terrain Model) Visualization (`show_3D_DTM`):**
        *   If a DTM is loaded (`locr4_flag`) and a sub-area is selected (`got_a_subwindow`), it renders the DTM as a solid surface (`paint_DTM`).
        *   The DTM is typically drawn with a yellowish material property for contrast.
        *   The drawing order (nested `i`, `j` loops) is dynamically optimized based on `eye_azi` (camera azimuth) to minimize overdrawing and improve rendering performance.
    *   Employs `glXSwapBuffers` to swap front and back buffers, ensuring smooth and flicker-free animation.
*   **Event Handling (`manage_SE3D_widget_events`):**
    *   Processes various X-windows events (Expose, EnterNotify, LeaveNotify, MotionNotify, ButtonRelease, ButtonPress, KeyPress) to enable user interaction.
    *   **Expose events:** Trigger `refresh_SE3D_widget_window` to redraw the display.
    *   **Mouse Motion/Button events:** Manage button highlighting, rubber-banding for selections, and general 3D navigation.
    *   **ButtonPress events:** Toggle display flags (`show_3D_WC`, `show_3D_BTRK`, `show_solid_bottom`, `show_beyond_first_arrival`, `show_3D_DTM`), or trigger actions like loading/dumping geometry.
    *   **Slider Interaction:** Updates slider variables (`jX_update_slider_variable`) and redraws sliders (`jX_redraw_slider`) for continuous adjustments of parameters like `selected_swath`.
    *   **KeyPress events:** Provides extensive keyboard shortcuts for:
        *   **Rendering control:** Toggling `full_render` (full OpenGL rendering), `GL_LIGHT0`, `GL_LIGHT1`, `GL_LIGHT2` states.
        *   **Camera control:** Adjusting `eye_elev` (elevation), `eye_azi` (azimuth), `eye_range` (distance), and `lookat_X`, `lookat_Y`, `lookat_Z` (look-at point) for precise camera positioning.
        *   **Display toggles:** `show_AXES`, `show_BOAT`, `add_delays`.
        *   **Predefined views:** Setting `locate_eye` to predefined positions (e.g., `EYE_ABOVE`, `EYE_BESIDE`, `EYE_AHEAD`).
        *   **DTM detail:** Adjusting `DTM_skip` (DTM rendering resolution).
        *   **Automated actions:** Triggering `dump_out_AZI_rotation` (dumps images during rotation), `SE3D_dump_3d_screen` (single screenshot), `KEY_W` (sequence of watercolumn images), `KEY_C` (sequence of images for `dB_thresh` values).
*   **Camera and View Control:**
    *   `calc_eye_pos()`: Computes the camera's eye position in 3D space based on `eye_azi`, `eye_elev`, and `eye_range` parameters.
    *   `move_view()`: Invokes `gluLookAt()` to correctly set the camera's position and orientation, ensuring it points towards a specified `lookat_X`, `lookat_Y`, `lookat_Z` point.
    *   `locate_eye(int type)`: Instantly repositions the camera to predefined perspectives (e.g., `EYE_ABOVE`, `EYE_BESIDE`, `EYE_AHEAD`).
*   **Geometry Management:**
    *   `proj_3D(double lon, double lat, float depth, float *x, float *y, float *z)`: Transforms geographical coordinates (latitude, longitude, depth) into the program's internal 3D OpenGL coordinate system. This involves normalizing values by `nominal_depth` and centering them around `SE3D_av_lat`, `SE3D_av_lon`.
*   **Configuration Save/Load:**
    *   `dump_WC3D_Geometry()`: Persists the current 3D viewer configuration (camera position, display flags, intensity thresholds, nominal depth, etc.) to a file named "WC_3D_Geometry".
    *   `load_WC3D_Geometry()`: Retrieves and applies a previously saved configuration from the "WC_3D_Geometry" file.
*   **Automated Image Dumping:**
    *   `dump_out_AZI_rotation()`: Automates the process of rotating the 3D view around the azimuth and capturing sequential screenshots to PPM files (`3dim_azi_XXX.ppm`), useful for creating animations.
    *   `SE3D_dump_3d_screen()`: Captures and saves the current 3D OpenGL view to a single PPM file.
*   **DTM Painting (`paint_DTM`):**
    *   Renders individual panels of an overlaid DTM within the 3D view.
    *   Calculates 3D coordinates for each DTM grid cell corner using `proj_3D`.
    *   Colors DTM panels based on the `colormap_flag` (either using sidescan image data or sun-illuminated data).
    *   Utilizes `do_panel` to draw each quadrilateral.
*   **Widget Initialization (`view_SE3D_widget`):**
    *   Creates the main `3D WaterColumn ViewTool` X-window and all its associated child windows (graphic areas, buttons, sliders).
    *   Initializes the `SE3D_widget` structure with window parameters, button strings, and slider variables (e.g., eye elevation, azimuth, range, dB thresholds, selected swath, number of watercolumns to plot, R0 multipliers, ambient lighting).
    *   Sets up the OpenGL context for the primary graphic window.
    *   Handles the creation and initial values of buttons and sliders.
    *   Initializes OpenGL lights and material properties for realistic rendering.
    *   Establishes average latitude/longitude and `nominal_depth`.
    *   Calls `SE3D_calc_locations()` and `draw_SE3D()` to render the initial 3D view.
*   **Helper Functions:**
    *   `SE3D_calc_locations()`: Computes the 3D coordinates (`SE3D_pos`, `SE3D_cen`) for all soundings and sonar centers.
    *   `SE3D_check_for_stop()`: Monitors for user interrupts or stop flags to allow graceful exit from rendering loops.

## Dependencies

`SE_3D.c` relies on an extensive set of standard and custom header files, highlighting its deep integration within a specialized hydrographic software framework:

*   **Standard C Libraries:** `string.h`, `math.h`, `stdio.h` for fundamental string, mathematical, and input/output operations.
*   **OpenGL/GLX Libraries:** `GL/glx.h`, `GL/glu.h`, `GL/gl.h` provide the core functionality for 3D graphics rendering.
*   **X11 Libraries:** `X11/keysym.h` for advanced keyboard input handling.
*   `support.h`: Custom utility functions for general-purpose tasks like error handling.
*   `array.h`: Likely contains custom array and image header (`JHC_header`) definitions.
*   `j_EM_watercol.h`: Defines data structures for watercolumn data.
*   `j_non_ortho_cones.h`: Provides functions for calculating non-orthogonal cone intersections, essential for modeling acoustic beam paths.
*   `SE_global.h`: Contains global variables and definitions specific to the overall `SE` suite.
*   `SE_GEOwindows.h`: For geographical window parameters.
*   `SE_mainwin.h`: Provides access to `max_good_depth`.
*   `SE_WaterColumn.h`: For watercolumn-related parameters and configurations.
*   `SE_3D.h`: The specific header file for this module, declaring its global variables and function prototypes.
*   `SE_TOOLBOXwin.h`: Provides access to `colormap_flag`.
*   `jGL_draw.h`: Custom OpenGL drawing utilities (`draw_axes`, `draw_boat`, `do_panel`, `setup_material_properties`).
*   `X_extra.h`: Custom X-windows drawing utilities (`jX_is_win`, `jX_update_slider_variable`, `jX_redraw_slider`, `hilite_window`, `write_icon`, `j_rubber_band`, `jhc_scaled_values`).

## Purpose

`SE_3D.c` is a highly sophisticated and invaluable tool essential for advanced hydrographic and oceanographic data analysis due to its capabilities in:

1.  **Immersive Data Exploration:** Providing an intuitive and flexible 3D environment for exploring complex multibeam bathymetry and watercolumn data, allowing users to gain deeper insights into data characteristics.
2.  **Enhanced Quality Control and Editing:** Enabling detailed, three-dimensional inspection of individual sonar returns, which facilitates the identification and correction of subtle outliers, artifacts, or systematic errors that might be difficult to discern in 2D views.
3.  **Sensor Performance Analysis:** Offering a visual representation of acoustic beam paths and watercolumn scatterers, which helps in understanding sonar performance, beam coverage, and data acquisition characteristics.
4.  **DTM Validation:** The ability to overlay and interact with a Digital Terrain Model (DTM) allows for visual validation of bathymetric models against raw sounding data, identifying discrepancies or confirming model accuracy.
5.  **Target Identification and Characterization:** Viewing targets in 3D relative to the seafloor and watercolumn aids significantly in their identification, localization, and characterization.
6.  **High-Quality Presentation and Reporting:** Generating high-quality 3D renderings and animated sequences directly from the visualization, which are crucial for scientific presentations, reports, and outreach.

This tool is indispensable for hydrographic data processors, scientists, and engineers who require advanced visualization capabilities to thoroughly analyze, validate, and effectively present complex multibeam sonar datasets.
