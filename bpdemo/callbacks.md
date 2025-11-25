---
layout: default
title: callbacks.c
parent: BPdemo
nav_order: 4
---

# callbacks.c

## Description
`callbacks.c` is a source code file from the `bpdemo` application. It is not a standalone command-line tool. This file contains the implementation of various callback functions that are triggered by user interactions with the application's GUI, such as clicking buttons or selecting menu items.

These functions act as the "glue" between the user interface (defined in `BPdemo.c`) and the application's logic, defining what happens when a user performs a specific action.

## Functionality

The key callback functions defined in this file include:

### Dialog Management
*   **`void OKCallback(Widget w, ...)`**: A generic callback for "OK" buttons on dialogs. It closes the dialog by unmanaging its parent widget.
*   **`void about()`**: Displays the "About" dialog box, which shows application information.
*   **`void display_error()`**: Displays a pre-defined error dialog box, populating it with the current system error message.
*   **`void display_threeD()`**: Displays the 3D visualization window by managing its form widget and calling an initialization function (`init_threeD`).

### Application Control
*   **`void quit()`**: This function is called when the "Exit" menu item is selected. It presents a warning dialog to confirm if the user really wants to quit.
*   **`void really_quit()`**: If the user confirms the exit action in the warning dialog, this function is called to terminate the application via `exit(0)`.
*   **`void dont_quit()`**: If the user cancels the exit action, this function is called to close the warning dialog and return to the application.

### Display and Interaction
*   **`void change_display_state(Widget w, ...)`**: This function is linked to the popup menu on the main drawing area. When the user selects a different visualization mode, this callback updates the global `display_state` variable and triggers a redraw of the main drawing area to reflect the new state.

These functions are essential for the interactivity of the `bpdemo` application, connecting the user's actions to the program's behavior.