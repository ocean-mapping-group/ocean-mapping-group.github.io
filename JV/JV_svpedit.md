# `JV_svpedit.c` - JView Sound Velocity Profile (SVP) Editor Module

This C file implements the functionality for interactive editing and visualization of Sound Velocity Profiles (SVPs) within the `jview` application. It provides a dedicated X-windows-based interface that allows users to inspect, navigate, and modify SVP data, which is a critical component for accurate bathymetric data processing and correction.

## Key Features and Functions

*   **GUI Management (`manage_SVP_events`, `refresh_SVP_window`):**
    *   `manage_SVP_events`: Serves as the central event handler for the SVP editing widget. It processes all relevant X-events (`Expose`, `EnterNotify`, `LeaveNotify`, `KeyPress`, `ButtonPress`, `MotionNotify`, `ButtonRelease`) that occur within the SVP display windows and their associated control buttons.
    *   `refresh_SVP_window`: Ensures that the visual state of a specified SVP display window or button is kept up-to-date by triggering a redraw.

*   **SVP Navigation and Display Controls:**

    *   **Keyboard Shortcuts (within `manage_SVP_events`'s `KeyPress` handler):**
        *   `KEY_UP`, `KEY_DOWN`: Allow users to dynamically adjust the vertical viewing range (`max_svp_depth_view` and `min_svp_depth_view`) of the SVP plots, providing vertical zoom/pan capabilities on the depth axis.
        *   `KEY_LEFT`, `KEY_RIGHT`: Enable adjustment of the horizontal viewing ranges for `speed`, `temperature`, and `salinity` axes (`min_svp_speed_view`, `max_svp_speed_view`, etc.), facilitating horizontal zoom/pan on the respective parameter plots.
    *   **Button Controls (within `manage_SVP_events`'s `ButtonPress` handler):**
        *   `button_window[15]` (Previous SVP): Navigates to and displays the preceding SVP in the currently loaded list by decrementing `current_svp`.
        *   `button_window[16]` (Next SVP): Advances to and displays the subsequent SVP in the list by incrementing `current_svp`.
        *   `button_window[17]` (Reset View): Invokes `reset_svp_view` to restore all SVP viewing ranges (depth, speed, temperature, salinity) to their default, unscaled states.
        *   `button_window[18]` (Write SVPs): Triggers `write_out_svps` to save any SVPs that have been edited back to their respective disk files.

*   **Interactive SVP Editing and Flagging (within `manage_SVP_events`'s `ButtonRelease` handler):**
    *   **Rubber-banding Selection:** When a mouse button (left, middle, or right) is held down and the mouse is dragged across an SVP plot, `j_rubber_band` is used to define a rectangular selection region.
    *   **Flagging Data Points (Left-click - `button1` release):** Releasing the left mouse button after a rubber-banding selection on the speed, temperature, or salinity plots calls `flag_svp(FLAG_SVP, ...)`. This function marks individual SVP data points (`raw_zv`) as flagged if they fall within the selected depth and parameter range.
    *   **Unflagging Data Points (Right-click - `button3` release):** Similar to flagging, but `flag_svp(UNFLAG_SVP, ...)` is called to clear the flagged status of data points within the selected region.
    *   **Zooming Plot (Middle-click - `button2` release):** Releasing the middle mouse button after a rubber-banding selection adjusts the current plot's view to magnify the selected region.

*   **SVP Data Management (`init_SVP`, `load_up_svp_nav`, `search_for_closest_svp`, `flag_svp`, `reset_svp_view`, `write_out_svps`):**
    *   `init_SVP`: Initializes various global flags and variables pertinent to SVP handling, such as `svp_field_flag` (indicating whether SVP data is active), `num_watercolumns`, `svplook_flag`, `num_valid_watercolumns`, and `current_svp`. It also clears arrays used for storing SVP filenames and their edited status, and resets all viewing range variables to an "unset" state.
    *   `load_up_svp_nav`: Processes the geographical coordinates (latitude and longitude) of each loaded water column (SVP). It projects these coordinates onto the application's current map projection (`Project`) and stores the resulting map coordinates in `svp_array` for spatial display.
    *   `search_for_closest_svp`: Given a pixel coordinate (`xpick`, `ypick`) from the main display, this function efficiently identifies the loaded SVP that is geographically closest to that point. It updates `current_svp` to the index of the closest SVP and provides console output with relevant information.
    *   `flag_svp`: A core function that modifies the `flag` status of individual data points (`raw_zv`) within the currently selected SVP. Flagging is applied based on whether a data point's depth and specified parameter (speed, temperature, or salinity) fall within a defined range.
    *   `reset_svp_view`: Resets all viewing range variables (`min_svp_speed_view`, `max_svp_depth_view`, etc.) to their default "unset" values, effectively restoring the automatic scaling of the SVP plots.
    *   `write_out_svps`: Iterates through all loaded SVPs and writes any that have been modified (`svp_edited` flag set) back to their respective files on disk using the `jWC_write` function. It also handles internal format version promotion if the SVP data needs to be updated during the write process.

*   **SVP Visualization (`plot_svp`, `draw_svp`):**
    *   `plot_svp`: The main rendering function for SVP data. It clears the dedicated SVP display windows, configures the coordinate systems for the speed-depth, temperature-depth, and salinity-depth plots, draws appropriate grid lines and labels, and then plots the individual data points for the `current_svp`. Data points that have been flagged are prominently highlighted in red. This function also displays textual information about the currently viewed SVP file.
    *   `draw_svp`: A helper function, typically called by `refresh_SVP_window`, that draws simplified markers for SVP locations on a larger map (e.g., `graphic_window[0]`) and highlights the currently selected SVP to provide context within the broader survey area.

## Dependencies

This module relies on several internal libraries and header files, which provide the foundational components for its operation:

*   `JV_global.h`: Contains global variables and common definitions used across the entire `jview` application suite.
*   `JV_svpedit.h`: This module's own header file, which declares the function prototypes and data structures specific to SVP editing functionalities.
*   **GUI and Graphics Functions:** Includes `jX_is_win`, `jhc_scaled_values`, `j_rubber_band`, `hilite_window`, `write_icon`, `jhc_shape`, `jhc_line`, `jhc_text` for managing GUI elements, drawing primitives, and text rendering.
*   **Projection and Time Utilities:** `Project` (for geographic projection) and `stdtime_nicetime` (for time formatting).
*   **Water Column (SVP) I/O:** `jWC_write` (for writing SVP data).

## Usage

`JV_svpedit.c` is indispensable for quality control and refinement of Sound Velocity Profile data within the `jview` application. It empowers users to visually analyze SVP casts, identify and flag anomalous data points, adjust viewing parameters, and save corrected profiles, thereby ensuring the highest possible accuracy for subsequent bathymetric data processing steps.
