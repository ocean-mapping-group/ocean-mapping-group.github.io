---
layout: default
title: warning.c
parent: BPdemo
nav_order: 14
---

# warning.c

## Description
`warning.c` is a source code file from the `bpdemo` application. It is not a standalone command-line tool. This file's purpose is to create the "Warning" dialog box that appears when a user attempts to exit the application.

## Functionality
The file contains a single function, `create_warning`, which is responsible for constructing the GUI components of the warning dialog using the Motif widget toolkit.

### `void create_warning(Widget parent)`
*   **Purpose:** To create the exit-confirmation dialog window during the application's initialization.
*   **Action:**
    1.  It creates a `DialogShell` widget, which serves as the top-level window for the dialog, with the title "Warning!".
    2.  Inside this shell, it creates a `MessageBox` widget (`warning_box`) to hold the content.
    3.  A `Label` widget is added to display the confirmation message: "The configuration file has not been saved.\nDo you really want to exit?".
    4.  Two `PushButton` widgets are added to the dialog:
        *   An **"Exit"** button, which is connected to the `really_quit` callback function (defined in `callbacks.c`). Clicking this will terminate the application.
        *   A **"Return"** button, which is connected to the `dont_quit` callback function (defined in `callbacks.c`). Clicking this will close the warning dialog and return the user to the application.

This dialog is created when the application starts but remains hidden. It is only displayed when the user triggers the `quit` function, serving as a confirmation step to prevent accidental data loss or closure.