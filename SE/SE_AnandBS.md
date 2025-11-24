---
layout: default
title: SE AnandBS
parent: SE Tools
nav_order: 6
---

# `SE_AnandBS.c` - Backscatter Analysis and Angular Response Curve Tool

`SE_AnandBS.c`, developed by Anand and JHC, is a specialized C program module integrated within the `SE` (Sonar Editor) suite. This X-windows graphical interface tool is designed for the comprehensive analysis of multibeam sonar backscatter data. Its primary function is to generate and visualize Angular Response Curves (ARCs) and associated metrics, processing raw backscatter snippets, applying various corrections, and presenting data through interactive plots to enhance the understanding of seabed acoustic properties and sonar system performance.

## Key Features and Functions

*   **GUI Event Management (`manage_AnandBS_widget_events`, `refresh_AnandBS_widget_window`, `manage_ARC_widget_events`, `refresh_ARC_widget_window`):**
    *   Manages user interactions for both the main AnandBS widget and the associated Angular Response Curve (ARC) widget.
    *   Handles standard X-windows events like `Expose` (for redrawing), `EnterNotify`/`LeaveNotify` (for button highlighting), `MotionNotify`/`ButtonRelease` (for rubber-banding and zooming), and `ButtonPress` (for general widget interaction).
    *   **Main AnandBS Widget Controls:**
        *   Buttons to toggle between displaying "Original" and "deTVG" (Time-Varying Gain corrected) backscatter data (`show_BS0`).
        *   Buttons to switch between displaying Ensonified Area, Bottom Target Strength (BTS), or One-Way Travel Time (OWTT) (`show_BS2`).
        *   Toggles for `show_statistics` and `show_BS_Stress` (backscatter stress).
        *   A button to toggle recalculation of R0 (normal incidence/crossover OWTT).
        *   Keyboard shortcuts facilitate panning, zooming, and resetting views, particularly in the beam trace window (`i == 3`).
    *   **ARC Widget Controls:**
        *   Buttons allow selection of "Original/deTVG BS" (`BS_type`), and different angular references: "SRA" (Sonar Referenced Angle), "VRA" (Vertically Referenced Angle), or "GRA" (Grazing Angle) (`Angle_type`).
        *   Navigation buttons ("<<" and ">>") allow users to cycle through and highlight selected sectors.
        *   A toggle button for drawing BS (Backscatter) coefficient values (`draw_BScoefficent`).
        *   Supports rubber-banding for interactive zooming and panning within the ARC graphic window.
*   **Data Loading and Processing (`load_AnandBS_data`):**
    *   Opens the original `.merged` file (`infile_ABS`) and its associated `.ss_data` (sidescan/backscatter data) file (`imagefile_ABS`).
    *   Reads `OMG_HDCS_summary_header` and `OMG_HDCS_profile_header` for the relevant swaths.
    *   Dynamically allocates memory for `BS_data_for_pings` (a 2D array of `BS_data` structs) to store processed backscatter data for all beams and samples.
    *   Iterates through each profile (ping) and each beam within the profile:
        *   Reads raw backscatter snippets from `imagefile_ABS` using `beam_data[j].offset` and `beam_data[j].no_samples`.
        *   Applies `get_TVG_params` to retrieve Time-Varying Gain (TVG) parameters for each profile.
        *   Calculates `grazing_angles` and `Verticaly_Referenced_Angle` (SRA or VRA) for each beam.
        *   Determines `owtt` (one-way travel time) for each sample within the snippet.
        *   Computes `BTS` (Bottom Target Strength) using `compute_BTS`.
        *   Calculates `deTVG_BS` (de-TVG'd backscatter) and `ensonifid_area` (ensonified area) using `adh_take_out_BTS_and_correct_for_area`.
        *   Stores `original_BS`, `deTVG_BS`, `BTS`, `owtt`, `ensonifid_area`, `grazing_angles`, `Verticaly_Referenced_Angle`, `sonar_relative_angle`, `unique_sector` into the `BS_data_for_pings` structure.
        *   Handles multi-sector sonar systems by loading `tx_sectors` and identifying `unique_sector`s based on various sonar parameters (e.g., `center_frequency`, `signal_length`, `waveform_id`).
    *   Calls `fill_in_BSvAngle()` after loading all data to populate scatter plot images.
*   **Backscatter Scatter Plot Generation (`draw_BSscatter_VRA`, `draw_BSscatter_GRA`, `fill_in_BSvAngle`, `make_image`):**
    *   **`draw_BSscatter_VRA()` / `draw_BSscatter_GRA()`:** Draw the primary scatter plots of backscatter intensity versus angle (VRA or GRA) in `graphic_window[0]` and `graphic_window[1]`.
        *   These functions overlay color-coded images derived from `bsva_scatterplots`, where colors represent the density of data points.
        *   They can optionally overlay individual data points (crosses) and statistical curves (average, sigma min/max) if `show_statistics == 1`.
        *   Axis labels are dynamically displayed.
    *   **`fill_in_BSvAngle()`:** Populates `bsva_scatterplots` (an array of `BSvA` structs) by stacking backscatter values against VRA/GRA.
        *   Calculates point density in 2D bins for the scatter plots.
        *   Computes statistics (`average_of_intensities`, `stdv_of_intensities`, `sigma_min`, `sigma_max`) for each angle bin.
    *   **`make_image(BSvA *bsva)`:** Creates an 8-bit image for a given `BSvA` struct, where pixel values represent the density of backscatter points at each angle/intensity combination, effectively visualizing the data distribution.
*   **Ensonified Area, BTS, OWTT Visualization (`draw_EnsonArea_VRA`, `draw_window3`):**
    *   **`draw_EnsonArea_VRA()`:** Plots ensonified area, BTS (Bottom Target Strength), or OWTT (One-Way Travel Time) against VRA in `graphic_window[2]`.
        *   Dynamically determines the appropriate Y-axis range based on the selected metric and the entire dataset.
        *   Calls `draw_window3` to render the plot.
    *   **`draw_window3()`:** A generic drawing function specifically for `graphic_window[2]` that plots individual points for the chosen metric (ensonified area, BTS, or OWTT) against VRA.
        *   Handles dynamic Y-axis scaling based on the data range.
        *   Plots different markers for pulse-length limited (cyan) and beamwidth limited (yellow) ensonified areas.
*   **Beam Trace and BTS Visualization (`draw_beam_trace`, `draw_BTS`):**
    *   **`draw_beam_trace()`:** Displays a beam trace plot (Beam Number vs. OWTT) in `graphic_window[3]`.
        *   Draws the TVG window markers (`owtt_to_normal_incidence`, `owtt_to_crossover`).
        *   Plots individual sample intensities as colored rectangles and highlights the center sample.
    *   **`draw_BTS()`:** Plots Bottom Target Strength (BTS) against OWTT in `graphic_window[4]`.
        *   Displays TVG window markers.
        *   Plots individual BTS values, highlighting specific scattering types (`WC_Spec_Lamb`).
        *   Overlays BSn/BSo (Normal and Oblique Incidence Backscatter) values derived from the profile header.
*   **Angular Response Curve (ARC) Tool (`make_ARC_widget`, `fill_in_ARC_Data`, `draw_ARC`, `draw_sectors`, `draw_unique_sector_in_ARC`, `init_ARC_variables`):**
    *   **`make_ARC_widget()`:** Initializes the X-windows for the ARC tool, setting up graphic windows, buttons, and slider parameters.
    *   **`fill_in_ARC_Data()`:** Populates `ARC_data_for_pings` by stacking backscatter values (Original, deTVG, and BS Coefficient) for each unique sector against GRA, VRA, and SRA.
        *   Calculates average backscatter for each angle bin.
    *   **`draw_ARC()`:** Determines the overall minimum and maximum backscatter values across all data to set the Y-axis range for the ARC plots. Calls `draw_sectors()`.
    *   **`draw_sectors()`:** Renders the ARC plot in `graphic_window[0]`.
        *   Draws grid lines and plots average backscatter values (Original, deTVG, or BS Coefficient) against the selected angle type (GRA, VRA, SRA) for all unique sectors.
        *   Displays labels for axes and sonar modes.
    *   **`fill_sector_chart()`:** Fills a tabular display (`graphic_window[1]`) showing detailed information for each unique sector encountered (ID, Frequency, Pulse Length, Waveform, Bandwidth, Swath).
    *   **`draw_unique_sector_in_ARC()`:** Highlights a currently selected unique sector in the ARC plot and its corresponding entry in the sector chart.
*   **Memory Management:**
    *   `allocate_BS_data_memory()`: Allocates memory for the `BS_data_for_pings` structure (a 2D array of `BS_data` structs).
    *   `free_BS_data_memory()`: Frees memory for `BS_data_for_pings`.
    *   `allocate_ARC_memory()`: Allocates memory for `ARC_data_for_pings`.
    *   `free_ARC_memory()`: Frees memory for `ARC_data_for_pings`.
    *   `allocate_sector_memory()`: Allocates memory for `define_sector_to_mode` and `unique_sectors_draw_marker`.
    *   `free_sector_memory()`: Frees memory for sector data.
*   **Helper Functions:** Includes various `adh_` (Anand's Helper) functions for detailed backscatter calculations, such as finding `range_to_center_sample`, `RX_beamwidth`, `OWTT_for_each_sample`, `take_out_BTS_and_correct_for_area`, `sampling_rate`, and `sector_pulse_length`. Other helpers include `get_mode_descriptor`, `compute_BTS`, `recalc_owtt_normal_incidence_crossover`, `convert_sector_to_mode`, and `find_first_or_second_swath`.

## Dependencies

*   **Standard C Libraries:** `stdio.h`, `string.h`, `math.h`, `stdlib.h`, `time.h` for fundamental operations.
*   **X11 Libraries:** `X11/keysym.h` for keyboard input.
*   `support.h`: General utility functions.
*   `array.h`: Likely custom array and image header (`JHC_header`) definitions.
*   `SE_global.h`: Global variables and definitions specific to the SE suite.
*   `SE_AnandBS.h`: Header for this module.
*   `SE_GEOwindows.h`: For geographical window parameters.
*   `OMG_HDCS_jversion.h`: For OMG HDCS data structures and I/O.
*   `simrad_tvg.h`: For Simrad-specific TVG (Time-Varying Gain) calculations.
*   `grazing_angle.h`: For grazing angle calculations.
*   `ensonification.h`: For ensonification area calculations.

## Purpose

`SE_AnandBS.c` is a critical and highly specialized tool for advanced backscatter data analysis, serving the following key purposes:

1.  **Backscatter Data Quality Control:** Provides detailed and interactive visualizations of backscatter data, enabling users to identify and diagnose issues such as system artifacts, calibration problems, or environmental noise.
2.  **Seabed Characterization and Classification:** Facilitates the in-depth study of seabed acoustic properties by analyzing how backscatter intensity varies with different angular references (Grazing Angle, Sonar Referenced Angle, Vertically Referenced Angle). This is fundamental for classifying seafloor types and understanding geological processes.
3.  **Sonar System Performance Evaluation:** Allows users to assess the effectiveness of TVG corrections, evaluate beam patterns, and analyze ensonification geometry, contributing to optimal sonar system calibration and setup.
4.  **Multi-Parameter Integrated Analysis:** Integrates various backscatter-related parameters (ensonified area, BTS, OWTT, SRA, VRA, GRA) into a cohesive visualization framework, providing a holistic view of the acoustic response.
5.  **Interactive Data Exploration:** Enables users to interactively explore complex backscatter datasets, zoom into regions of interest, and toggle different display modes to uncover hidden patterns and relationships.

This tool is invaluable for hydrographic data processors, marine geologists, and acoustic engineers who need to perform in-depth analysis of backscatter data for applications such as seabed classification, habitat mapping, and precise sonar system calibration and validation.
