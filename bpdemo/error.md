---
layout: default
title: error.c
parent: BPdemo
nav_order: 11
---

# error.c

## Description
`error.c` is a source code file from the `bpdemo` application. It is not a standalone command-line tool. This file's purpose is to create a reusable "Error" dialog box for the application's GUI.

## Functionality
The file contains a single function, `create_ErrorShell`, which is responsible for constructing the GUI components of the error dialog using the Motif widget toolkit.

### `void create_ErrorShell(Widget parent)`
*   **Purpose:** To create the error dialog window during the application's initialization.
*   **Action:**
    1.  It creates a `DialogShell` widget, which serves as the top-level window for the dialog, with the title "Error".
    2.  Inside this shell, it creates a `MessageBox` widget to hold the content.
    3.  A `Label` widget (`ErrorLabel`) is added to the message box. This label is designed to display the specific error message text. When the dialog is created, it is initially populated with the system error message obtained from `strerror(errno)`.
    4.  An "OK" `PushButton` is added to the dialog.
    5.  A callback, `OKCallback` (defined in `callbacks.c`), is attached to the "OK" button, which allows the user to close the dialog by clicking it.

This dialog is not displayed immediately upon creation. Another function, `display_error()` (from `callbacks.c`), is responsible for updating the `ErrorLabel` with a current error message and then managing (displaying) the `ErrorBB` widget to make it visible to the user when an error occurs.