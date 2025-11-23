# `SE_AUTOFLAGwin.c` - Automated Flagging Parameters Window for Sonar Editor

`SE_AUTOFLAGwin.c` is a specialized C program module within the `SE` (Sonar Editor) suite, designed to provide an X-windows graphical interface for configuring and applying automated flagging parameters to multibeam sonar data. This tool empowers users to define and customize rules for automatically identifying and marking (flagging) problematic soundings based on various criteria such as two-slope tests (both across-track and along-track), isolation from neighboring data points, and specific detection modes. It plays a crucial role in semi-automating and streamlining the data cleaning and quality control processes in hydrographic surveys.

## Key Features and Functions

*   **Memory Allocation (`allocate_autoflag_memory`):**
    *   Dynamically allocates memory for two integer arrays, `use_two_slope` and `use_beam`, each sized to `SE_NO_MAX` (presumably the maximum number of beams). These arrays likely store boolean flags that control whether specific two-slope tests or beam-level rejections are applied.
*   **Window Refreshing and Visualization (`refresh_autobox_windows`):**
    *   This function is responsible for redrawing and updating the visual state of specific sub-windows (widgets) within the autoflagging interface.
    *   **`sub_window[18]` (Two-Slope Beam Selection):** Visually represents the `no_beams` available. For each beam, it draws a red rectangle if the `use_two_slope[i]` flag is enabled (indicating that the two-slope test will be applied to that beam) and a green rectangle if disabled. On-screen instructions guide users to toggle these settings using mouse clicks.
    *   **`sub_window[19]` (Across-Track Two-Slope Limit):** Displays the current status of the across-track two-slope test. If `use_ACROSS_two` is enabled, it shows a red background with a line visually representing the `ACROSS_twoslopelimit`. If disabled, it shows a green background with a "Disabled" text label.
    *   **`sub_window[20]` (Beam Usage):** Similar to `sub_window[18]`, this window indicates which beams are marked for rejection. It shows a red rectangle if `use_beam[i]` is disabled (meaning that particular beam will be entirely rejected) and green if enabled.
    *   **`sub_window[21]` (Along-Track Two-Slope Limit):** Mirrors `sub_window[19]`, but specifically for the along-track two-slope test, displaying the status of `use_ALONG_two` and its `ALONG_twoslopelimit`.
    *   **`sub_window[55]` (Fore-Aft Gap Detection):** Indicates the enabled (red) or disabled (green) status of the `use_FOREAFT` flag, which is used to detect and flag soundings that are isolated along-track.
    *   **`sub_window[56]` (Left-Right Gap Detection):** Shows the enabled (red) or disabled (green) status of the `use_LEFTRIGHT` flag, which is used to detect and flag soundings isolated across-track.
*   **Automated Data Checking and Flagging Logic (`check_data`):**
    *   This is the core engine for applying the automated flagging rules to the sonar data.
    *   Initializes internal flags (`auto_check_across`, `auto_check_along`, `auto_foraft`, `auto_lefrig`) to zero before processing.
    *   **Pre-flagging/Beam Rejection:** Iterates through all beams and swaths, applying initial flags (`-ABS(box[j][i])`) to soundings if `!use_beam[j]` is set, effectively rejecting entire beams.
    *   **Across-Track Two-Slope Test (`use_ACROSS_two`):** For each sounding, it calculates the slope with valid neighbors before and after the sounding. If both `before_slope` and `after_slope` exceed `ACROSS_twoslopelimit` and have opposing signs (indicating a spike), or match the specified `spike_sense` (e.g., `UP_ONLY`, `DOWN_ONLY`), the sounding is automatically flagged.
    *   **Along-Track Two-Slope Test (`use_ALONG_two`):** Similar to the across-track test, but calculates slopes between adjacent pings along the track. It assumes a fixed along-track distance (e.g., 2.5 meters between pings for calculation).
    *   **Fore-Aft Neighbor Check (`use_FOREAFT`):** Flags soundings if they lack valid neighbors in both the preceding and succeeding pings along-track, indicating an isolated point.
    *   **Left-Right Neighbor Check (`use_LEFTRIGHT`):** Flags soundings if they lack valid neighbors to both their left and right across-track, also indicating an isolated point. Special handling is included for outermost beams.
    *   **"Any 2" Neighbors Test (`any_2`, `multi_pass`):** A more sophisticated test that flags a sounding if it has fewer than a specified number of valid neighbors (e.g., 2 out of 4 around it). This test can be applied iteratively in multiple passes (`multi_pass`) to progressively flag isolated points.
    *   If `pre_unflag` is enabled, previously flagged soundings can be unflagged (their absolute depth values restored), providing an "undo" mechanism.
    *   Returns the number of newly flagged soundings for user feedback.
*   **Window Management (`view_autobox`):**
    *   Initializes and creates the main `Auto-Flag Parameters` X-window and all its child windows (graphic areas and interactive buttons).
    *   Configures `sub_param` structures with precise window dimensions and positions for various display elements: beam slope application, across/along two-slope limits, beam usage, fore-aft/left-right flags.
    *   Creates interactive buttons using `jX_make_button` for actions such as "Unflag ON/OFF", "Amp/Phase" (detection mode), "1-pass" (multi-pass count), "UP/DOWN" (spike sense), "Any 2 ON/OFF", and "Apply" (to apply the flagging rules).
    *   Sets window attributes and input masks to enable comprehensive user interaction.
*   **Parameter Configuration Save/Load (`dump_auto_parameters`, `parse_auto_parameters`):**
    *   `dump_auto_parameters(char *name)`: Saves the current autoflagging parameters (e.g., two-slope limits, detection modes, pass count, neighbor checks) to a specified configuration file for persistence.
    *   `parse_auto_parameters(char *name)`: Reads autoflagging parameters from a configuration file, updating global variables and settings accordingly. It recognizes various keywords (e.g., "UNFLAG_ON", "ACROSS_TWO_SLOPE_ON", "BEAM") to configure the tool.
*   **Helper Functions:**
    *   `ABS(val)`: A macro to return the absolute value of its argument.
    *   `recalc_good_bounds()`: Recalculates good data bounds (likely for the main SE window).
    *   `refresh_coreSE_window()`: Refreshes specific parts of the main SE window.

## Dependencies

*   **Standard C Libraries:** `string.h`, `stdlib.h` for basic string manipulation, memory allocation, and general utilities.
*   `SE_global.h`: Contains global variables and definitions that are shared across the entire `SE` suite.
*   `SE_AUTOFLAGwin.h`: The specific header file for this module, containing declarations for its global variables and function prototypes.
*   `SE_mainwin.h`: Provides access to variables and functions used by the main Sonar Editor window, such as `no_beams`, `graphic_window`, and `refresh_coreSE_window`.
*   `X_extra.h`: A custom library providing X-windows drawing utilities (`jhc_fill_rect`, `jhc_text`, `jhc_load_font`, `jhc_line`, `jMOD_XCreateSimpleWindow`, `jX_make_button`) for graphical rendering.
*   `support.h`: Custom utility functions for general tasks, including error and warning reporting.

## Purpose

`SE_AUTOFLAGwin.c` delivers essential and powerful functionality for semi-automating the quality control of hydrographic multibeam sonar data. Its primary purposes are to:

1.  **Automate Outlier Detection:** Systematically identify and flag soundings that deviate significantly from neighboring data, appear as isolated points, or form unnatural spikes, based on robust, user-defined parameters.
2.  **Improve Data Cleaning Efficiency:** Substantially reduce the manual effort and time required to clean large datasets by applying consistent and configurable flagging rules, thereby accelerating the processing workflow.
3.  **Enhance Data Quality and Integrity:** Contribute directly to the production of higher quality bathymetric products by more efficiently and reliably identifying and marking erroneous soundings.
4.  **Flexible and Adaptable Configuration:** Offer users the ability to precisely tailor flagging parameters to suit specific survey environments, characteristics of different sonar types, and unique data conditions.

This tool is invaluable for hydrographic data processors, allowing them to rapidly and consistently apply initial quality control steps to raw multibeam data, thereby significantly streamlining the overall processing workflow and improving the reliability of final bathymetric products.
