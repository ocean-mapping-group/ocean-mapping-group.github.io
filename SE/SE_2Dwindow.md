# `SE_2Dwindow.c` - 2D Bathymetry View and Editing Tool

`SE_2Dwindow.c` is a specialized C program that provides an interactive X-windows graphical interface for visualizing and editing 2D profiles of bathymetric data. As a core component of the `SE` (likely "Sonar Editor" or "Sounding Editor") suite, its primary function is to enable hydrographic data processors to meticulously examine individual soundings, interactively flag or unflag them based on various quality criteria, and assess overall data quality within a defined geographical area. This tool is instrumental in the manual cleaning and validation of multibeam bathymetry datasets.

## Key Features and Functions

*   **2D Data Visualization (`refresh_D2_main_window`):**
    *   Provides a dynamic and clear visual representation of 2D bathymetric profiles.
    *   Clears and redraws the main 2D plot window (`sub_window[23]`) to reflect current data and display settings.
    *   Draws horizontal grid lines with labels, adapting line intervals based on the current depth range for optimal readability.
    *   Dynamically sets the X-axis range (`sub_param[23].x_min`, `sub_param[23].x_max`) based on the chosen viewing direction (`D2_dirn` can be `NORTH`, `SOUTH`, `EAST`, or `WEST`), effectively rotating the profile view to align with specific survey lines or cross-sections.
    *   Displays informative text indicating whether amplitude detects, phase detects, or all detect types are currently being shown.
    *   Optionally overlays IHO (International Hydrographic Organization) quality bars, providing a visual reference for depth uncertainty and data compliance.
    *   Draws a context-rich scale bar for the X-axis (`draw_scale`).
    *   Optionally overlays a Digital Terrain Model (DTM) from `full_data` for comparative analysis, drawing profile lines from the DTM.
    *   Plots individual soundings (beams) from `D2x`, `D2y`, `D2z` (or `D2z_T`, `D2z_proc`, `D2z_Tproc` for tide-corrected or processed depths) using distinct shapes (`JHC_CROSS`, `JHC_DIAMOND`) and colors to denote their status or source.
    *   Soundings are colored based on a selected `colour_scheme` (`BY_SWATH` for line color, `BY_BD` for bottom detection type, `BY_FLAG` for flagged status) and their `D2_status` (flagged/unflagged).
    *   Includes a debug mode for detrending, which plots the calculated regression line across the soundings.
*   **Interactive Controls (`refresh_D2_button_windows`):**
    *   Manages the dynamic state and appearance of various button windows, updating their text and status based on user interactions.
    *   **Viewing Direction:** Buttons to toggle the `D2_dirn` (`SOUTH`, `NORTH`, `EAST`, `WEST`) to change the perspective of the 2D profile.
    *   **Data Correction Toggles:** Buttons to enable/disable the display of tide correction (`D2tide_flag`) and switch between observed (`OBS`) and processed (`PROC`) depth data (`obs_proc`).
    *   **Flagging Control:** Toggles to show/hide flagged soundings (`show_flagged`).
    *   **Action Buttons:**
        *   "PRINT" button: Triggers printing of the current view to a `D2_plot` file.
        *   "STATS" button: Initiates statistical calculations (`calc_stats`).
        *   "FLAG"/"UNFLAG" toggle (`D2_Sense`): Switches between flagging and unflagging modes for interactive editing.
        *   "SAVE" button: Triggers `dump_back_out_2D` to save all changes back to the original data files.
        *   "DTM." / "NoDTM." toggle (`show_dtm_flag`): Controls the overlay of the DTM.
        *   "AF" (Auto Flag): Automatically flags soundings based on their deviation from a terrain model (`auto_flag_distance`).
        *   **Color Scheme Selection:** Buttons to cycle through different `colour_scheme` options (`BY_SWATH`, `BY_BD`, `BY_FLAG`).
*   **Dynamic Memory Management:**
    *   `alloc_all_D2_memory(int novals)`: Dynamically allocates memory for all 2D data arrays, including coordinates (`D2x`, `D2y`), depths (`D2z`, `D2z_T`, `D2z_proc`, `D2z_Tproc`), detect types (`D2detect`), status flags (`D2_status`, `D2_changed`), and various identification numbers (`D2file`, `D2rec`, `D2beam`). The allocation size is precisely calculated based on the estimated `novals` (number of soundings).
    *   `free_all_D2_memory()`: Responsibly deallocates all dynamically allocated memory, setting pointers to `NULL` to prevent memory leaks.
*   **Efficient Data Loading and Filtering (`get_D2_profiles_inarea`, `count_profs_in`):**
    *   `count_profs_in()`: Provides an optimized method to estimate the number of soundings within a user-defined 2D area (defined by `left_x`, `right_x`, `top_y`, `bot_y`). It leverages `OMG_HDCS_read_summary` and `.100ping_bounds` index files to quickly identify 100-ping segments that intersect the area, significantly speeding up the data loading process.
    *   `get_D2_profiles_inarea()`: Loads the actual sounding data that falls within the specified 2D area.
        *   It reads `OMG_HDCS_summary_header` and `OMG_HDCS_bounds` from `.100ping_bounds` files.
        *   It processes `OMG_HDCS_profile` and `OMG_HDCS_beam` data, extracting relevant information for each sounding.
        *   Applies refraction corrections (`get_coeffs`, `set_up_ref_coefficients`) if `use_proc_flag == 1` is enabled.
        *   Populates the `D2x`, `D2y`, `D2z` (and processed variants) arrays with the extracted and corrected sounding data.
        *   Tracks `D2max` and `D2min` values for dynamic scaling of the depth axis.
        *   Displays a progress bar during the loading process for user feedback.
        *   Includes a detrending option (`use_proc_flag == 3`) that calculates a linear regression (X_slope, Y_slope) to flatten the profile.
        *   Automatically determines the most common heading (`D2_dirn`) for initial plotting if not explicitly set by the user.
        *   Optionally loads "random" soundings from external files (`rdmname`) if defined.
*   **Interactive Editing Functions:**
    *   `flag_2D_values(float rx1, float rx2, float ry1, float ry2)`: Allows users to interactively flag or unflag soundings within a user-defined rectangular selection box (`rx1`, `rx2`, `ry1`, `ry2`).
        *   Based on the `D2_Sense` mode (`FLAG_2D` or `UNFLAG_2D`), it modifies the `D2_status` and `D2_changed` flags of affected soundings.
        *   Flags are assigned specific numerical values (e.g., `16` for auto-flagged soundings) to indicate their origin.
*   **Persistent Data Saving (`dump_back_out_2D`):**
    *   Saves all interactive changes made in the 2D window back to the original `.merged` OMG HDCS files.
    *   It iterates through all `no2Dpos` soundings, checking their `D2_changed` status.
    *   If a sounding has been modified, it rereads the original profile and beams from the file, updates the status of the specific modified beam, and writes the changes back using `OMG_HDCS_put_raw_beams`.
    *   Optimizes I/O by only writing profiles that have had changes.
    *   Generates a `changes_2D` log file detailing the modifications.
*   **Data Analysis and Statistics (`calc_stats`):**
    *   Calculates essential statistical parameters, including the mean and standard deviation of depths for soundings within the current view that are not flagged (or are explicitly shown if `show_flagged` is set).
    *   Performs an advanced analysis by calculating the mean and standard deviation of deviations from an overlaid DTM for each individual beam, outputting these statistics to a `beamstats.2D` file.
*   **Printing and Reporting (`print_2D`):** Dumps the current 2D view data to a text file named `D2_plot`, including coordinates, depth, file ID, and plotting shape for external visualization or reporting.
*   **GUI Initialization (`view_2Dbox`):**
    *   Sets up the main `2D Beam View ToolKit` X-windows, meticulously defining dimensions and positions for the primary plot area and various interactive control buttons.
    *   Initializes parameters for all control buttons (e.g., direction, tide, flagged, observed/processed, print, DTM toggle, statistics, flag/unflag, save, auto-flag, color scheme).
    *   Creates and configures all associated sub-windows, setting appropriate input masks for user interaction.
*   **Image Dumping (`dump_the_2D_window`):**
    *   Captures the visual content of a specified X-window as an image.
    *   Converts the captured image to PPM (Portable Pixmap) format and saves it to a file, providing a quick way to create screenshots or static reports.
    *   Handles both 8-bit and 24-bit TrueColor displays, extracting RGB pixel values as needed.

## Dependencies

`SE_2Dwindow.c` relies on a robust set of custom and standard header files, indicating its deep integration within a larger hydrographic data processing framework:

*   **Standard C Libraries:** `string.h`, `stdio.h`, `math.h`, `malloc.h` (often implicitly via `stdlib.h`) for fundamental operations like string manipulation, file I/O, mathematical functions, and dynamic memory allocation.
*   `support.h`: Provides essential custom utility functions (e.g., `error`, `warning`, `usage`, `strtoint`, `strtodbl`).
*   `ref_coeffs.h`: Defines structures (`ref_coeff`) and functions (`read_ref_coeff_file`, `get_coeffs`, `set_up_ref_coefficients`) for handling refraction coefficients.
*   `SE_global.h`: Contains global variables and definitions specific to the `SE` (Sonar Editor) suite.
*   `X_extra.h`: Provides custom X-windows drawing utilities (`jhc_line`, `jhc_text`, `jhc_fill_rect`, `jhc_shape`, `jhc_load_font`, `draw_scale`, `jX_draw_progress`, `jMOD_XCreateSimpleWindow`).
*   `SE_2Dwindow.h`: The header file for this specific module, likely containing declarations for its global variables and function prototypes.
*   `SE_GEOwindows.h`: Contains definitions related to geographical navigation and display (e.g., `nav_x`).
*   `OMG_HDCS_jversion.h`: Crucial for OMG HDCS data structures (`OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, `OMG_HDCS_beam`, `OMG_HDCS_bounds`) and associated I/O functions.

## Purpose

`SE_2Dwindow.c` is a highly interactive and essential component for the rigorous quality control and manual editing of multibeam bathymetric data. Its primary purposes are to:

1.  **High-Resolution Data Inspection:** Offer a detailed 2D cross-section view of soundings within a specific area, enabling precise inspection of individual beam returns and their relationship to the seafloor.
2.  **Manual Data Cleaning:** Provide users with interactive tools to flag or unflag erroneous soundings, a crucial step for refining bathymetric models, removing outliers, and enhancing data accuracy.
3.  **Terrain Model Integration:** Support the comparison of individual soundings against a DTM or terrain model, facilitating the identification of systematic errors, sensor biases, or real seafloor features.
4.  **Refraction & Processing Visualization:** Allow for the visualization of the effects of refraction and other processing corrections on depth data, helping users understand and validate the applied algorithms.
5.  **Data Quality Assessment:** Offer statistical analysis (mean, standard deviation) of depth data and deviations from terrain models, providing quantitative measures for data quality assessment.
6.  **Graphical Reporting:** Enable the generation of printable outputs of the 2D view for documentation, reports, and presentations.

This tool is invaluable for hydrographic data processors, allowing them to perform detailed quality control and editing tasks that are critical for generating high-accuracy bathymetric charts and models required for navigation, scientific research, and engineering projects.
