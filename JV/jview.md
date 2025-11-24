---
layout: default
title: jview
parent: JV Tools
nav_order: 1
---
# jview
## Description
`jview` is an X-windows-based interactive tool for visualizing, analyzing, and editing geospatial data. It orchestrates the entire application lifecycle, from startup configuration to user interaction handling and data processing.

## Usage
```bash
jview [OPTIONS] [<input_data_files...>]
```

## Arguments

### Data Loading
| Option | Description |
|---|---|
| `-mask` | Load a mask file. |
| `-spline_mask` | Load a spline-interpolated mask. |
| `-pgm` | Load a PGM image file. |
| `-dump_rot_coords` | Dump rotation coordinates. |
| `-svp` | Load Sound Velocity Profile (SVP) data. |
| `-sounding` | Load sounding data. |
| `-tide` | Load tide data. |
| `-watershed` | Load watershed data. |
| `-vector` | Load generic vector data. |
| `-omgedit` | Load OMG format editing data. |
| `-vectbin` | Load vector bin data. |
| `-gl` | Load GLoria data. |
| `-array` | Load array data. |
| `-oldarray` | Load old array data. |
| `-reclen` | Load record length data. |
| `-ios` | Load IOS format data. |
| `-survey_linefile` | Load a survey line file. |

### Display & View Options
| Option | Description |
|---|---|
| `-show_fft2d` | Show 2D FFT analysis widget. |
| `-show_wavfft` | Show WAV audio FFT analysis widget. |
| `-make_map_coords` | Make map coordinates. |
| `-decnav` | Use decimated navigation. |
| `-contval` | Contour value. |
| `-speed_knots` | Speed in knots. |
| `-zigzag` | Show zigzag pattern. |
| `-geomask` | Use georeferenced mask. |
| `-fillbox` | Fill box. |
| `-mcol` | Use multiple colormaps. |
| `-autoj` | Auto-justify display. |
| `-show_WCIM_header` | Show Water Column IM header. |
| `-linear` | Use linear scaling. |
| `-box_is_ellipse` | Box is an ellipse. |
| `-box_is_star` | Box is a star shape. |
| `-pickrot` | Pick rotation. |
| `-lookrot` | Look rotation. |
| `-current_box` | Current box. |
| `-concat` | Concatenate data. |
| `-concat_cumm` | Cumulative concatenation. |
| `-seis` | Show seismic data. |
| `-displacement` | Show displacement. |
| `-ticks` | Show ticks. |
| `-point` | Show points. |
| `-dot` | Show dots. |
| `-rascoord` | Show raster coordinates. |
| `-dm` | Use Degrees, Minutes format. |
| `-dms` | Use Degrees, Minutes, Seconds format. |
| `-lola` | Show Latitude/Longitude. |
| `-ship_location` | Ship location. |
| `-ship_orient` | Ship orientation. |
| `-ship_offset` | Ship offset. |
| `-ship_outline` | Show ship outline. |
| `-cmap` | Use custom colormap. |
| `-asciicmap` | Use ASCII colormap. |
| `-subimage` | Show subimage. |
| `-subimage2` | Show second subimage. |
| `-SUN` | Show sun illumination. |
| `-paintbox` | Paint box. |
| `-paint_color` | Paint color. |
| `-paint` | Paint. |
| `-noexpand` | Do not expand. |
| `-colstart` | Column start. |
| `-noscalebar` | No scalebar. |
| `-scalelabel` | Scale label. |
| `-skip` | Skip. |
| `-large_nav` | Large navigation. |
| `-navlook` | Navigation look. |
| `-navedit` | Navigation edit. |
| `-traces` | Show traces. |
| `-specbox` | Show spectral box. |
| `-nad27` | Use NAD27 ellipsoid. |
| `-area` | Show area. |
| `-forss` | For sidescan. |
| `-currents` | Show currents. |
| `-bigwinds` | Big winds. |
| `-currskip` | Current skip. |
| `-currdev` | Current deviation. |
| `-currscale` | Current scale. |
| `-ssedit` | Sidescan edit. |
| `-gaudy` | Gaudy display. |
| `-badread` | Bad read. |
| `-angresp` | Angular response. |
| `-smoothssnav` | Smooth sidescan navigation. |
| `-usesslut` | Use sidescan LUT. |
| `-sslook` | Sidescan look. |

### Debugging & Control
| Option | Description |
|---|---|
| `-die` | Exit immediately. |
| `-help` | Display help message. |

## How It Works
`jview` functions as the central command and control hub for an interactive geospatial data visualization and analysis system. It initializes the X-windows graphical environment, sets up its main window and various specialized modules (e.g., SVP editor, FFT2D tool, WAV audio analysis), and manages the entire application lifecycle. The `main` function parses command-line arguments to configure `jview`'s behavior, load specific data types, and activate various analysis modes. Upon startup, it enters a primary event loop (`process_x_events()`) which continuously monitors for user interactions (mouse clicks, keyboard presses, window events) and dispatches them to appropriate functions or widgets. Data processing, visualization, and editing are then handled by a multitude of internal functions and modules. `jview` employs an array of functionalities including data loading, preprocessing (e.g., zig-zag pattern generation, spline interpolation), various drawing and visualization routines (e.g., refreshing windows, drawing coordinate ticks, visualizing survey lines, plotting FFT results), and interactive editing and manipulation features (e.g., flagging navigation points, performing angular response analysis, displaying cross-sections). File I/O operations are handled for masks, image data, and configuration boxes. Upon exiting the main event loop, the application handles the saving of edited data and performs necessary resource cleanup.

## Output Files
`jview` is primarily an interactive visualization and editing tool, and thus does not produce standard batch output files on its own. However, through its interactive features and various sub-modules, it can:
*   Save edited data (masks, navigation, profiles, etc.) to their original or new files.
*   Capture X-window content to PGM or JHC image files (via `dump_current_window()`).
*   Generate scripts for copying spectral analysis box configurations (`write_out_specboxes()`).
*   Output specialized plot files through its plotting sub-modules.
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
