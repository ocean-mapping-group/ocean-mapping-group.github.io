# `JV_initialise.c` - JView Initialization Module

This C file is solely dedicated to the initialization of a wide array of global variables that govern the behavior, state, and appearance of the `jview` application. It systematically sets default values for flags, counters, and parameters across various functional domains of `jview`, ensuring a consistent and predictable starting environment for the program.

## Key Functions

*   **`initialise_JV_variables()`:**
    *   This is the sole and primary function implemented in this module. It performs extensive initialization tasks, including:
        *   **Memory Clearing:** Resets arrays such as `boxname` (for pick-rotation boxes) and `specboxname` (for spectral analysis boxes) to ensure they are empty at startup using `memset`.
        *   **Debugging and Display Flags:** Initializes `JEVENT_debug` to `0` (disabled), `verbose_flag`, `decnav`, `large_nav`, `mcol_flag`, `autoj_flag`, `nad27_flag`, `float_flag`, `interp_flag`, `concat_profile`, `concats`, `got_an_fft`, `SHOW_SWATH_GEOMETRY`, `AR_flag`, `gaudy_flag`, `badread`, `rotate_flag`, `skip`, `blank_flag`, `traces_flag`, `mask_flag`, `geomask_flag`, `zigzag_flag`, `spline_mask`, `reclen_flag`, `gloria_flag`, `bpick_flag`, `ios_flag`, `tick_flag`, `vector_flag`, `view_vectors`, `displacement_flag`, `dot_flag`, `point_flag`, `RC_flag`, `dm_flag`, `rascoord_flag`, `sounding_flag`, `digit_flag`, `vectbin_flag`, `navedit_flag`, `noexpand_flag`, `rejectnav_flag`, `omgedit_flag`, `flag_sense`, `area_flag`, `forss_flag`, `current_flag`, `bigwinds`, `pickrot_flag`, `pickrot_arrow`, `editrot_flag`, `box_flag`, `show_parallels`, `show_nodes`, `box_is_ellipse`, `box_is_star`, `fillbox`, `linear_flag`, `cmap_flag`, `paint_flag`, `SUN_flag`, `array_flag`, `oldarray_flag`, `blowup_flag`, `subimage_flag`, `cenbox_flag`, `ssedit_flag`, `sslook_flag`, `smoothssnav`, `usesslut`, `noss`, `pgm_flag`, `print_box_coords`, `make_map_coords`, `shift_dn_flag`, `init_dn_shift`, `show_fft2d`, `survey_lines_flag`, `survey_planning_mode`, `ship_outline` to their default (usually `0` or `1`) states. `scalebar_flag` is set to `1`.
        *   **Tide Parameters:** Sets `tide_flag` (off), `the_mintide` (1000), `the_maxtide` (-1000), `mintide` (0), `maxtide` (10.0), `tiderange` (10.0), and extreme initial values for `tide_start`, `tide_end`, `tide_view_start`, `tide_view_end`.
        *   **Side-scan FFT and Zoom:** Initializes `do_SSfft` (off), `sszoomfactor` (1), `sscentre_x` (512), `sscentre_y` (400), `current_ssfile` (0), `current_ssping` (200), `ss_alongtrack_zoom` (1), `nohalfsstraces` (400), `use_other_freq` (0), `halfzoom` (200).
        *   **Rotation and Shift Values:** Sets `rot_angle` (0) and `Shift_Fraction` (0.75).
        *   **Map and Input Management:** Initializes `no_rubber_band` (0), `show_WCIM_header` (0), `init_str` (0), `max_sub` (850), `no_in` (0), `current_map` (0), `last_accessed_map` (0), `numnav` (0).
        *   **DTM and Angular Response (AR) Analysis:** Sets default `azi` (45.0), `elev` (45.0), `exag` (1.0), `ViewType` (`DEPTH_VIEW`), `ship_location` (0.5), `ship_locationZ` (1.0), `def_width` (500.0), `def_height` (500.0), `def_angle` (0.0). For AR, `plot_AR` (on), `no_AR_plots` (0), `no_angresps` (0), `BSo` (-30.0), `BSn_BSo` (10.0), `Lamb_Power` (2.0), `Angle_Change` (25.0).
        *   **Display Options:** Initializes `show_class` (on), `show_ss` (on), `show_bs` (on), `show_resid` (on), `reduce_bp` (off), `show_raw` (off), `show_separate` (on) for AR plots.
        *   **Picking/Selection Box Parameters:** Sets `boxstep` (100.0), `no_boxes` (0), `current_box` (0), `no_auto_boxes` (0), `no_spec_boxes` (0).
        *   **Speed and Color Settings:** `speed_knots` (8.0), `colors` (8), `bin_cmap` (1), `paintbox` (2), `paint_color` (255).
        *   **Counters:** Initializes `omgi_count`, `mask_count`, `vect_count`, `tot_count`, `current_hist`. `vectbin_count` array is cleared.
        *   **Survey Planning Parameters:** Initializes `survey_line_list_filename` (NULL), `survey_line_spacing` (1000.0), `survey_line_spacing_increment` (10.0).
        *   **Ship Model Parameters:** Initializes `ship_lat`, `ship_lon`, `ship_count`, `ship_outline` to `0`.

**Dependencies:**

*   `JV_initialise.h`: This module's own header file, which likely contains the function prototype for `initialise_JV_variables()`.
*   `JV_global.h`: Crucial for providing the declarations of all the global variables that are being initialized within this file.

**Purpose:**

`JV_initialise.c` is fundamental to the stability and correct operation of the `jview` application. By centralizing the initialization of hundreds of global variables, it ensures that the application always starts from a well-defined and consistent state, preventing potential crashes or unpredictable behavior due to uninitialized memory or incorrect default settings. This systematic approach also significantly aids in the maintainability and debugging of the `jview` codebase.
