---
layout: default
title: RT steve play
parent: RT Tools
nav_order: 5
---

# `RT_steve_play.c` - Real-Time Sonar Data Unraveling, Monitoring, and Logging Tool

`RT_steve_play.c` (located in an "old" directory, suggesting a legacy or specialized version) is an exceptionally comprehensive and complex C program designed for real-time processing, visualization, and logging of data originating from various multibeam and singlebeam sonar systems. This application functions as a robust real-time monitor, displaying incoming data through an interactive X-windows graphical user interface (GUI) and simultaneously writing processed data to standardized Ocean Mapping Group (OMG) HDCS files and other ancillary formats. It serves as a critical tool for on-the-fly quality control and preliminary data processing during marine surveys.

## Key Features and Functions

*   **Real-time Data Processing & Monitoring:**
    *   Reads, unpacks, and processes proprietary telegrams from a wide array of sonar types, including Simrad EM-series (EM100, EM1000, EM120, EM300, EM3000, EM3002, EM1002), Reson SeaBat, and Elac systems.
    *   Dynamically displays processed acoustic data, vessel attitude, navigation, and line-running parameters within an interactive X-windows graphical user interface.
    *   Provides instant feedback on the operational status and data quality of the ongoing survey.
*   **Comprehensive Command-line Argument Parsing (`main` function):** Offers extensive control over program execution, input/output, processing, and display settings.
    *   **Sonar Type Specification:** A **mandatory** flag (e.g., `-em100`, `-reson`, `-elac`) is used to specify the exact sonar system being processed. This dynamically configures default processing parameters via the `set_tooltype_variables` function.
    *   **Input/Output (I/O) Control:**
        *   `-out <prefix>`: Defines a custom output file prefix for all generated OMG files.
        *   `-prefix <directory>`, `-suffix <extension>`: Specifies directory prefixes and file extensions for input files, enabling flexible and automated file discovery.
        *   `-WRITE`: Explicitly enables the writing of processed data to various output files.
        *   `-ascii_dump`: Activates ASCII output format for debugging or specialized text-based data analysis.
        *   `-background`: Runs the program without displaying the graphical interface (implicitly enables `WRITE_flag` and disables `view_flag`).
        *   `-line <name>`: Specifies a particular line name for processing, often used to organize survey data.
    *   **Data Processing Parameters:**
        *   `-recalc_AAZ`: Triggers the recalculation of across-track angles.
        *   `-tide <file>`: Specifies an external tide file for applying tidal corrections to depth data.
        *   `-ignore_not_Y2K`: Instructs the program to ignore non-Y2K compliant timestamps, allowing processing of older datasets.
        *   `-2motions`: Indicates that two motion sensors are present, requiring dual-sensor processing.
        *   `-suppress_sk`: Suppresses the display of skipped pings, reducing visual clutter in real-time.
        *   `-scramblenav (-refcoord <lat> <lon>)`: A specialized option to "scramble" navigation data, typically used for testing or specific data manipulation, often requiring a reference coordinate.
        *   `-force_swap`: Forces byte swapping for data interpretation, handling endianness differences.
        *   `-declin <value>`: Specifies the magnetic declination for heading corrections.
        *   `-custom_mask <file>`: Loads a custom beam mask from a specified file, overriding default beam masking patterns.
    *   **Display & Visualization Control (when `view_flag` is active):**
        *   `-v`: Increases the verbosity level for more detailed console output.
        *   `-check`, `-date_check`: Activates various data consistency and date checks.
        *   `-phase`: Enables the storage and display of phase data alongside amplitude.
        *   `-onetype`: Processes only one type of sonar telegram, useful for isolating specific data streams.
        *   `-playback`: Enables a playback mode for reviewing recorded data.
        *   `-paintss`, `-paintbathy`: Specifies whether to render sidescan imagery or bathymetry data in the main display window.
        *   `-SUN`: Activates sun-illumination rendering for bathymetry, enhancing topographic visualization.
        *   `-ATdist`, `-sspixel`, `-ssshift`: Controls various side-scan display parameters, such as across-track distance, pixel size, and shift.
        *   `-yrange <min> <max>`: Sets the Y-axis range for plots.
        *   `-depth`, `-reflect`: Explicitly enables or disables depth and reflectivity processing/display.
        *   `-navcockup`, `-debug_nav`: Flags for specific navigation debugging and error identification.
        *   `-utm <meridian>`: Enables Universal Transverse Mercator (UTM) projection, requiring a central meridian.
        *   `-scale <factor>`: Applies a scaling factor to the entire X-windows display.
        *   `-signal <min> <max>`, `-stretch <min> <max>`: Controls the signal range and stretching for visual display.
        *   `-auto`: Activates auto-logging and automatic switching to new input files.
        *   `-packdown`, `-version<N>`: Controls the OMG file version and data packing strategy.
        *   `-vector <file> <length>`, `-navi <file> <color>`, `-targ <file> <color>`: Allows loading and displaying external vector fields, additional navigation tracks, and target/waypoint data.
        *   `-flipNE`, `-dont_addRP`, `-oldEM100_ampl`: Specific flags for display orientation, roll/pitch application, and legacy EM100 amplitude handling.
*   **X-windows Graphical Interface Management:**
    *   `set_up_X()`: Initializes the entire X-windows environment, meticulously defining the layout and dimensions of numerous graphical widgets, including:
        *   Main geographical view.
        *   Colormap and End-Of-File (EOF) indicator.
        *   Text information display.
        *   Depth/sun-encoded and reflectivity images.
        *   Side-scan imagery.
        *   Azimuth, speed, tide, and backscatter widgets.
        *   Along/across track profiles, side-scan scale, labels, and various interactive buttons/icons.
    *   `set_up_CMAP()`: Initializes the colormap used for all graphical displays.
    *   `set_up_MINMAX()`: Establishes the logical minimum and maximum coordinates for each graphical widget, defining the data range displayed.
    *   `refresh_window()`, `re_draw_box()`: Manages the efficient updating and redrawing of specific graphical components.
    *   `update_plot()`, `update_bathy()`, `paint_bathy()`, `paint_ampl()`, `paint_ss()`: Functions dedicated to rendering data onto the X-windows display.
    *   `check_for_stop()`: Monitors for user input to gracefully terminate the program.
    *   `shift_view()`, `zoom_view()`, `check_for_edge()`: Provides interactive control for panning, zooming, and automatic view adjustments based on vessel position, crucial for real-time tracking.
*   **Data Input/Output Operations:**
    *   `load_up_data()`: Loads 8-bit image data into memory for efficient display rendering.
    *   `load_up_selected_area()`, `initialise_without_area()`: Handles the loading of predefined geographical survey areas or initializes default views when no specific area file is provided.
    *   `dumpout_file()`: Efficiently flushes (writes) modified image data from memory back to the corresponding image files, optimizing I/O by only writing changed scan lines.
    *   `setup_outputfiles()`: Initializes and opens all necessary OMG output files, including `.nav`, `.orientation`, `.merged`, `.svp`, `.param`, `.depth`, `.reflect`, `.merged.ss_data`, `.merged.ph_data`, and others. It also initializes `OMG_HDCS_summary_header` structures for these files.
*   **Automated File Management:**
    *   `look_for_new_logged_file()`: A critical function for the "auto" mode, continuously monitors designated log files (`log.lines`, `event.log`) or the file system for newly created input data files. Upon detection, it automatically switches to and begins processing the new file via `next_file()`.
    *   `next_file()`: Manages the lifecycle of input files, closing the current file, opening the next, and re-initializing all output files accordingly.
*   **Ancillary Data Handling & Visualization:**
    *   `load_tide()`, `calc_tide()`: Loads tidal data from a specified file and calculates real-time tidal corrections, which are then applied to depth measurements.
    *   `load_up_vectors()`, `load_up_nav()`, `load_up_targets()`: Functions to load and display external vector fields, additional navigation tracks, and target/waypoint data on the graphical interface.
    *   `view_attitude()`, `plot_beam_masks()`, `change_mask()`: Provides functionality for visualizing vessel attitude, plotting beam masks (indicating active beams or data quality), and dynamically modifying these masks.
    *   `view_line_running()`, `plot_line_running()`, `calculate_line_params()`, `shift_run_line()`: Implements tools for displaying and interacting with planned survey lines, including across-track deviation and along-track progress.
*   **Core Processing Loops (`log_RESON_data`, `log_SUBMETRIX_data`, `log_ELAC_data`, `log_data`):** These sonar-specific functions are the operational core of the real-time processing. They are responsible for reading raw sonar telegrams, applying essential corrections (e.g., tidal, motion, sound velocity), extracting bathymetry and imagery, and writing the processed data to the configured output files.
*   **Event Handling:** Utilizes `process_x_events()` to manage user interactions (e.g., button clicks, keyboard input) and integrates an `interrupt_flag` mechanism for graceful program termination.

## Dependencies

`RT_steve_play.c` relies on an extensive set of custom and standard header files, underscoring its role as part of a larger, integrated software suite developed by the Ocean Mapping Group. Key dependencies include:

*   **Standard C Libraries:** `stdio.h`, `ctype.h`, `string.h`, `math.h`, `unistd.h` (for POSIX systems), `malloc.h` (often via `stdlib.h`) for basic I/O, string manipulation, mathematical operations, and system calls.
*   `support.h`: Provides general utility functions (e.g., `error`, `warning`, `usage`, `strtoint`, `strtodbl`).
*   `interrupt.h`: For signal handling and program interruption.
*   `stdtime.h`: Standardized time conversion utilities.
*   **Geographical Libraries:** `j_area.h`, `mercator.h`, `wgs.h`, `j_proj.h` for geographical projections, area management, and WGS84 conversions.
*   `array.h`: Defines custom array and image header (`JHC_header`) definitions.
*   **Acoustic Processing:** `backscatter.h`, `Echo_calib.h`, `j_ang_resp.h` for acoustic backscatter analysis, echo calibration, and angular response calculations.
*   **X-windows Graphics:** `X_extra.h`, `jX_win.h` for custom X-windows drawing primitives and window management.
*   **Sonar-Specific Libraries:** `Simrad_em12.h`, `RESON_UNB.h`, `UNB_ELAC.h` providing data structures and parsing routines specific to various sonar systems.
*   **OMG Data Formats:** `OMG_HDCS_jversion.h` for OMG HDCS data structures and I/O routines.
*   `jcu_nav.h`: Navigation data structures and I/O.
*   **Internal RT Headers:** `RT_unravel.h`, `RT_ancil_data.h` containing internal definitions for real-time unraveling logic and ancillary data management.

## Purpose

`RT_steve_play.c` is an exceptionally powerful and indispensable real-time system with multiple critical purposes within hydrographic and oceanographic applications:

1.  **Real-time Quality Control:** It enables surveyors and researchers to monitor incoming sonar data, assess vessel dynamics, and evaluate data quality directly during acquisition, facilitating immediate operational adjustments.
2.  **On-the-fly Data Processing:** The program applies essential corrections (e.g., tidal, motion, sound velocity) as data is acquired, significantly reducing post-processing time and improving real-time data accuracy.
3.  **Robust Data Logging:** It consistently creates standardized OMG HDCS files (merged bathymetry, navigation, attitude, imagery), ensuring data integrity and compatibility for subsequent rigorous post-processing, archiving, and analysis.
4.  **Navigational Guidance:** Provides crucial visual aids for line following, monitoring vessel speed, and managing course over ground, directly supporting efficient and precise survey operations.
5.  **Multi-Sonar System Support:** Its modular design, featuring specific `log_*_data` functions and `set_tooltype_variables` configurations, ensures adaptability and compatibility across a wide range of commonly used multibeam and singlebeam sonar systems.

This tool is invaluable for hydrographic surveyors, oceanographers, and marine researchers who require immediate feedback and robust data logging capabilities during sonar data acquisition, contributing significantly to the efficiency and accuracy of marine surveys and scientific campaigns.
