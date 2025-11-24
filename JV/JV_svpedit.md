---
layout: default
title: JV_svpedit (Module within jview)
parent: JV Tools
nav_order: 6
---
# JV_svpedit (Module within jview)

## Description
`JV_svpedit.c` implements the functionality for interactive editing and visualization of Sound Velocity Profiles (SVPs) within the `jview` application. It provides a dedicated X-windows-based interface that allows users to inspect, navigate, and modify SVP data, which is a critical component for accurate bathymetric data processing and correction.

## Key Features and Functions

*   **GUI Management (`manage_SVP_events`, `refresh_SVP_window`):**
    *   `manage_SVP_events`: Serves as the central event handler for the SVP editing widget. It processes all relevant X-events (`Expose`, `EnterNotify`, `LeaveNotify`, `KeyPress`, `ButtonPress`, `MotionNotify`, `ButtonRelease`) that occur within the SVP display windows and their associated control buttons.
    *   `refresh_SVP_window`: Ensures that the visual state of a specified SVP display window or button is kept up-to-date by triggering a redraw.
*   **SVP Navigation and Display Controls:**
    *   **Keyboard Shortcuts (within `manage_SVP_events`'s `KeyPress` handler):** `KEY_UP`, `KEY_DOWN` (adjust vertical viewing range), `KEY_LEFT`, `KEY_RIGHT` (adjust horizontal viewing ranges for speed, temperature, and salinity axes).
    *   **Button Controls (within `manage_SVP_events`'s `ButtonPress` handler):** `button_window[15]` (Previous SVP), `button_window[16]` (Next SVP), `button_window[17]` (Reset View), `button_window[18]` (Write SVPs).
*   **Interactive SVP Editing and Flagging (within `manage_SVP_events`'s `ButtonRelease` handler):**
    *   **Rubber-banding Selection:** `j_rubber_band` is used to define a rectangular selection region.
    *   **Flagging Data Points (Left-click - `button1` release):** Calls `flag_svp(FLAG_SVP, ...)` to mark individual SVP data points as flagged if they fall within the selected region.
    *   **Unflagging Data Points (Right-click - `button3` release):** Calls `flag_svp(UNFLAG_SVP, ...)` to clear the flagged status of data points within the selected region.
    *   **Zooming Plot (Middle-click - `button2` release):** Adjusts the current plot's view to magnify the selected region.
*   **SVP Data Management (`init_SVP`, `load_up_svp_nav`, `search_for_closest_svp`, `flag_svp`, `reset_svp_view`, `write_out_svps`):**
    *   `init_SVP`: Initializes various global flags and variables pertinent to SVP handling.
    *   `load_up_svp_nav`: Processes geographical coordinates of each loaded water column.
    *   `search_for_closest_svp`: Identifies the loaded SVP that is geographically closest to a given pixel coordinate.
    *   `flag_svp`: Modifies the `flag` status of individual data points within the currently selected SVP.
    *   `reset_svp_view`: Resets all viewing range variables to their default values.
    *   `write_out_svps`: Iterates through all loaded SVPs and writes any modified ones back to disk.
*   **SVP Visualization (`plot_svp`, `draw_svp`):**
    *   `plot_svp`: The main rendering function for SVP data, clearing windows, configuring coordinate systems, drawing grids/labels, and plotting data points (highlighting flagged points).
    *   `draw_svp`: A helper function that draws simplified markers for SVP locations on a larger map.

## How It Works
The `JV_svpedit` module operates as an interactive editor within `jview`, allowing users to load, display, and modify Sound Velocity Profile data. It manages GUI elements like buttons and sliders to control navigation through SVPs, adjust display ranges, and apply edits. User interactions (mouse clicks, keyboard input) are captured by event handlers, which then trigger functions to update the SVP data, recalculate visualizations, and save changes. This module is tightly integrated with `jview`'s core event loop and global state, ensuring that SVP edits are reflected across the application and can be persistently stored.

## Dependencies

*   `JV_global.h`: Contains global variables and common definitions used across the entire `jview` application suite.
*   `JV_svpedit.h`: This module's own header file, which declares the function prototypes and data structures specific to SVP editing functionalities.
*   **GUI and Graphics Functions:** Includes `jX_is_win`, `jhc_scaled_values`, `j_rubber_band`, `hilite_window`, `write_icon`, `jhc_shape`, `jhc_line`, `jhc_text` for managing GUI elements, drawing primitives, and text rendering.
*   **Projection and Time Utilities:** `Project` (for geographic projection) and `stdtime_nicetime` (for time formatting).
*   **Water Column (SVP) I/O:** `jWC_write` (for writing SVP data).

## Notes
`JV_svpedit.c` is indispensable for quality control and refinement of Sound Velocity Profile data within the `jview` application. It empowers users to visually analyze SVP casts, identify and flag anomalous data points, adjust viewing parameters, and save corrected profiles, thereby ensuring the highest possible accuracy for subsequent bathymetric data processing steps.