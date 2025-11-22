---
layout: default
title: callbacks
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 4
---
# callbacks

## Description
`callbacks.c` is a Motif GUI source file that defines a collection of callback functions. These functions are triggered by various user interactions (e.g., button clicks, menu selections, dialog confirmations) within the "Submetrix 2000 unraveller" application. This module orchestrates the application's responses to user input, handling tasks such as dismissing dialogs, applying data processing settings, managing file operations, and updating the display.

## How It Works
The functions in `callbacks.c` are typically registered with specific Motif widgets using `XtAddCallback`. When a user interacts with a widget, the corresponding callback function is invoked.

### Generic Callbacks
*   **`OKCallback(Widget w, XtPointer client_data, XtPointer xt_call_data)`:** A general-purpose callback for "OK" or "Close" buttons in dialogs. It simply unmanages the parent widget, effectively closing the dialog.

### Data Processing Callbacks
*   **`change_data_compression(Widget w, XtPointer client_data, XtPointer xt_call_data)`:** This callback is likely triggered by buttons in a popup menu (e.g., from `bathy_window.c`). It sets global flags (`linear_ss`, `sqrtss`, `tvgss`) to control the data compression method (linear, logarithmic, square root, or TVG) applied to the displayed bathymetry.
*   **`change_display_state(Widget w, XtPointer client_data, XtPointer xt_call_data)`:** Updates a global `display_state` array based on `client_data` and a `DA_down` variable, presumably controlling how different drawing areas (DA1-DA4) are rendered.

### Thresholds Dialog Callbacks (for `ThresholdForm`):
*   **`ThresholdOKCallback(...)`, `ThresholdApplyCallback(...)`:** These read values from text input widgets (`ThresholdText1` to `ThresholdText5`) representing `athresh`, `pthresh`, `oftotal`, `nobelow`, and `firstsam` (parameters for bottom picking and quality control). They then update corresponding global variables. `ThresholdOKCallback` also unmanages the dialog.
*   **`ThresholdCancelCallback(...)`:** Closes the Thresholds dialog without applying changes.

### Spacings Dialog Callbacks (for `SpacingForm`):
*   **`SpacingOKCallback(...)`, `SpacingApplyCallback(...)`:** These read values from text input widgets (`SpacingText1` to `SpacingText6`) representing transducer spacing parameters (`PORT_NOMINAL_SPACING`, `PORT_AB_AC_ratio`, `PORT_AB_AD_ratio`, `STBD_NOMINAL_SPACING`, `STBD_AB_AC_ratio`, `STBD_AB_AD_ratio`). They update global variables and then call `calc_row_spacings()` and `prime_LUTs()` to re-calculate internal look-up tables based on the new spacings. `SpacingOKCallback` also unmanages the dialog.
*   **`SpacingCancelCallback(...)`:** Closes the Spacings dialog without applying changes.

### Menu/Button Action Callbacks:
*   **`about()`:** Displays the "About" dialog box (`AboutBB`).
*   **`display_error()`:** Displays an error message dialog (`ErrorBB`) with details from `strerror(errno)`.
*   **`display_spacings()`:** Manages and displays the Spacings configuration dialog (`SpacingForm`).
*   **`display_thresholds()`:** Manages and displays the Thresholds configuration dialog (`ThresholdForm`).
*   **`display_bathy()`:** Manages and displays the main bathymetry window (`BathyForm`) and initializes its display using `init_bathy()`.
*   **`open_callback()`, `file_selection()`:** Initiates the file selection dialog (`FSBox`) for opening files.
*   **`save()`, `save_as()`:** Handles saving the current configuration or data. `save_as()` first prompts for a new filename.
*   **`file_select_ok(...)`:** The callback for the "OK" button in the file selection dialog. It retrieves the selected filename. If saving, it calls `create_file()` (if new) and `write_file()`. If opening, it calls `open_file()`, updates the main window's title, and redraws all drawing areas (`draw_view`).
*   **`file_select_cancel()`:** Dismisses the file selection dialog.
*   **`quit()`, `really_quit()`, `dont_quit()`:** Handle application exit, potentially prompting the user to save unsaved changes (`warning_box`). `really_quit()` performs the actual cleanup and exit.
This file demonstrates a typical event-driven programming model in GUI applications, where discrete user actions trigger specific functions to update the application's state and display.
