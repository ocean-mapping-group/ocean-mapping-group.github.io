# `jview.c` - Core JView Application Manager

This `jview.c` file serves as the central command and control hub for the `jview` application, an X-windows-based interactive tool for visualizing, analyzing, and editing geospatial data. It orchestrates the entire application lifecycle, from startup configuration to user interaction handling and data processing.

## Key Features and Functions

*   **Application Entry Point (`main` function):**
    *   Parses a wide range of command-line arguments to configure `jview`'s behavior and input data sources. These arguments enable diverse functionalities such as loading specific data types, setting display options, and activating various analysis modes.
    *   Initializes numerous global variables and application modules (e.g., SVP editor, FFT2D tool, WAV audio analysis) by calling functions like `initialise_JV_variables()` and `init_SVP()`.
    *   Sets up the X-windows graphical environment (`set_up_X()`, `set_up_CMAP()`).
    *   Creates and maps specialized widgets if their respective flags (`show_fft2d`, `show_wavfft`) are enabled.
    *   Enters the primary event loop (`process_x_events()`) to continuously monitor and respond to user interactions.
*   **Command-Line Argument Parsing:**
    *   Supports an extensive set of command-line flags for flexible application configuration, including:
        *   **Data Loading:** `-mask`, `-spline_mask`, `-pgm`, `-dump_rot_coords`, `-svp`, `-sounding`, `-tide`, `-watershed`, `-vector`, `-omgedit`, `-vectbin`, `-gl`, `-array`, `-oldarray`, `-reclen`, `-ios`, `-survey_linefile`.
        *   **Display & View Options:** `-show_fft2d`, `-show_wavfft`, `-make_map_coords`, `-decnav`, `-contval`, `-speed_knots`, `-zigzag`, `-geomask`, `-fillbox`, `-mcol`, `-autoj`, `-show_WCIM_header`, `-linear`, `-box_is_ellipse`, `-box_is_star`, `-pickrot`, `-lookrot`, `-current_box`, `-concat`, `-concat_cumm`, `-seis`, `-displacement`, `-ticks`, `-point`, `-dot`, `-rascoord`, `-dm`, `-dms`, `-lola`, `-ship_location`, `-ship_orient`, `-ship_offset`, `-ship_outline`, `-cmap`, `-asciicmap`, `-subimage`, `-subimage2`, `-SUN`, `-paintbox`, `-paint_color`, `-paint`, `-noexpand`, `-colstart`, `-noscalebar`, `-scalelabel`, `-skip`, `-large_nav`, `-navlook`, `-navedit`, `-traces`, `-specbox`, `-nad27`, `-area`, `-forss`, `-currents`, `-bigwinds`, `-currskip`, `-currdev`, `-currscale`, `-ssedit`, `-gaudy`, `-badread`, `-angresp`, `-smoothssnav`, `-usesslut`, `-sslook`.
        *   **Debugging/Control:** `-die`, `-help`.
*   **Application Termination and Cleanup:**
    *   Upon exiting the main event loop, handles the saving of edited data (masks, navigation, OMG profiles, DN shifts, pick-rotation boxes, spectral analysis boxes) to disk.
    *   Performs resource cleanup, including terminating the X-windows environment (`terminate_x()`) and closing all open input files.
*   **Data Preprocessing and Calculation Functions:**
    *   `calc_zig_zag(float zig_spacing, float zig_orthogonal)`: Generates a zigzag survey pattern based on user-defined parameters, converting units and calculating coordinates in the projection space.
    *   `calc_mask_spline()`: Uses GSL (GNU Scientific Library) for cubic spline interpolation to create a smoother representation of a user-defined mask.
    *   `sum_geomask_travelled()`: Calculates the total geographical distance along a geomask and provides estimated travel times.
    *   `get_subimage(int window)`: Retrieves a specific subset of the main image data for display within a sub-window, managing memory allocation and image expansion. A historical "double free" bug related to `raw_image` was noted in comments.
    *   `calc_fft()`: Performs a 1D FFT on a selected profile. It detrends the data using a least-squares fit, applies a tapering window, and then uses the `four1` (Numerical Recipes) FFT routine.
    *   `get_Xsection()`: Extracts a 2D profile from a DTM along a defined line, interpolates data gaps, and prepares it for plotting and output.
    *   `get_SUBsection()`: Similar to `get_Xsection`, but specifically for a sub-section of a profile, optimized for localized analysis and FFT functions.
*   **Drawing and Visualization Functions:**
    *   `refresh_window(Window window)`: The primary function for redrawing various graphical elements. It acts as a dispatcher, calling specific drawing routines based on the window type (main image, colormap, sub-windows, etc.).
    *   `refresh_all_subwindows()`: Iterates and refreshes all active sub-windows.
    *   `draw_coord_ticks(int sub_window)`: Draws geographical coordinate tick marks (latitude/longitude) on the map display.
    *   `draw_vectbins(int sub_window)`: Renders binned vector data.
    *   `draw_survey_lines(int sub_window)`: Visualizes survey lines, highlighting selected lines and labeling start/end points.
    *   `draw_ship(int sub_window)`: Draws a loaded ship outline.
    *   `draw_vectors(int sub_window)`: Displays various types of vector data, including point data with labels and line segments.
    *   `draw_mask(int sub_window)`: Renders user-defined mask polygons, including spline-interpolated versions.
    *   `draw_zigzag(int sub_window)`: Visualizes generated zigzag survey patterns.
    *   `draw_omgi(int sub_window)`: Draws OMG (Ocean Mapping Group) format profile data points, indicating their status (flagged/unflagged).
    *   `draw_AR(int sub_window)`: Plots angular response data, highlighting selected areas and model fits.
    *   `draw_ssss(int sub_window)`: Draws side-scan (SSSS) fixes and related patterns.
    *   `draw_navi(int sub_window)`: Renders navigation tracks and, optionally, current vectors.
    *   `draw_fft2d_box(int window)`: Draws a box on the main display indicating the region chosen for 2D FFT analysis.
    *   `plot_box(int window)`: Plots user-defined rectangular analysis boxes, including support for ellipses, star patterns, parallel survey lines, and node points.
    *   `plot_fft()`: Visualizes the results of a 1D FFT, typically plotting logarithmic amplitude versus logarithmic period, and fitting a power-law trend.
    *   `plot_Av_response()`: Plots average angular response curves.
    *   `plot_Resid_response()`: Plots residuals from angular response model fits.
    *   `plot_thumbnail()`: Displays a small graphical summary of along-track variability for angular response.
    *   `plot_Model_Response()`: Plots theoretical angular response models.
    *   `plot_Av_sigma()`: Plots the average standard deviation of backscatter.
    *   `plot_tide_box()`: Displays tide data and current vectors within a dedicated window.
    *   `plot_useprof_box()`: Lists and highlights currently selected input files.
    *   `draw_scale(int window)`: Draws a dynamic scale bar on various windows.
*   **Interactive Editing and Data Manipulation Functions:**
    *   `flag_nav(float anchor_x, float anchor_y, float toe_x, float toe_y)`: Flags or unflags navigation points within a user-defined rectangular region.
    *   `flag_omg(float anchor_x, float anchor_y, float toe_x, float toe_y)`: Flags or unflags OMG profile data points.
    *   `do_AR_plot(float anchor_x, float anchor_y, float toe_x, float toe_y)`: Initiates angular response analysis for data within a selected region.
    *   `do_histo(int anchor_x, int anchor_y, int toe_x, int toe_y)`: Calculates and displays histograms for 8-bit image data within a selected area.
    *   `do_paint(int sub_wind, int anchor_x, int anchor_y, int toe_x, int toe_y)`: Allows painting (modifying pixel values) within a selected region of a sub-window.
    *   `view_crosssection(int decimate, int x, int y)`: Displays horizontal and vertical cross-sections of the main image.
    *   `shift_subimage(int window, int direction)`: Shifts the displayed content of a sub-window.
    *   `smooth_sub_window(int sub_win)`: Applies a smoothing filter to the image data in a sub-window.
    *   `check_if_inabox(int x_loc, int y_loc)`: Determines if a click is within a pick-rotation box.
    *   `check_if_inaspecbox(int x_loc, int y_loc)`: Determines if a click is within a spectral analysis box.
    *   `filt_bpicks(int win, int type)`: Applies median or average filtering to "bpick" data.
    *   `make_new_box()`: Creates a new pick-rotation box.
*   **File I/O and Utility Functions:**
    *   `dump_out_mask()`: Saves mask data to a file.
    *   `get_8bit_data(char *data, int offset, int length)`: Reads 8-bit image data from files.
    *   `write_out_subarea(int window)`: Writes a selected sub-area of an image to a new file.
    *   `stretch8bit(unsigned char *val, int min, int max)`: Adjusts 8-bit image data for display contrast.
    *   `write_out_specboxes()`: Saves spectral analysis box statuses and generates copy scripts.
    *   `write_out_boxes()`: Saves pick-rotation box configurations.
    *   `dump_current_window(Window window, int subwin, char *filename, int format)`: Captures X-window content to PGM or JHC image files.
    *   `read_PGM_header(FILE *infile, int *image_head_rows, int *image_head_cols)`: Reads PGM file headers.
*   **Data Loading Specifics:**
    *   `load_up_AR()`: Loads Angular Response data.
    *   `load_up_OMG()`: Loads OMG format profile data.
    *   `load_up_vectbins()`: Loads binary vector data.
    *   `load_displacements()`: Loads displacement vectors.
    *   `load_ship_outline()`: Loads ship outline data.
    *   `load_up_vectors()`: Loads generic vector data (ASCII).
    *   `load_up_traces()`: Loads seismic reflector traces.
    *   `load_up_SSnav()`: Loads side-scan navigation data, using or compiling a lookup table (LUT).
    *   `load_up_nav()`: Loads navigation data from various sources.
    *   `search_for_closest_ssss()`: Finds the closest side-scan fix.
    *   `search_for_closest_navi()`: Finds the closest navigation point.
*   **Display Setup Functions:**
    *   `view_SVP_box()`: Sets up windows for the Sound Velocity Profile (SVP) editor.
    *   `view_DTM_box()`: Configures windows for DTM analysis tools.
    *   `view_AR_box()`: Sets up windows for Angular Response analysis.
    *   `view_SSVIEW_box()`: Configures windows for the Sidescan Strip Investigation Tool.
    *   `view_tide_box()`: Sets up windows for the Tide Phase Window.
    *   `view_useprof_box()`: Configures windows for the MapSheet Selection Window.

## Dependencies

`jview.c` is highly dependent on a custom set of libraries and header files that define global variables, data structures, and utility functions specific to the `jview` project and its underlying graphical and numerical capabilities. These include:

*   `JV_global.h`: Core global definitions.
*   `JV_initialise.h`: For initial application setup.
*   `JV_svpedit.h`: For SVP editor functionalities.
*   `JV_play_WAV.h`: For WAV audio analysis functionalities.
*   `JV_FFT2D.h`: For 2D FFT analysis functionalities.
*   `nbstereo.h`: Likely for specialized navigation or projection.
*   `gsl/gsl_errno.h`, `gsl/gsl_spline.h`: GNU Scientific Library for numerical routines, specifically for splines.
*   Numerous internal `jhc_` (J.H.C. utility), `jcu_` (J.C.U. utility), `jMOD_` (Maury modifications), `OMG_HDCS_`, `nav_`, `Project`, `inv_proj`, `stdtime_`, `get_2D_profile`, `read_PGM_header`, `Analyze_SSpatch`, `find_inflexions`, `characterise_BS_curve`, `fit_jack_par`, `do_RG_simple_model`, `unrotate`, `get360azi` and various other custom functions for graphics, data handling, numerical computations, and specialized data format I/O.

## Purpose

`jview.c` serves as the comprehensive control center for a sophisticated geospatial visualization and analysis system. Its monolithic structure integrates a vast array of functionalities, enabling users to interactively load, view, process, analyze, and save diverse types of geographical and acoustic data within an X-windows environment. It is a critical component for scientific data exploration, quality control, and specialized mapping tasks.
