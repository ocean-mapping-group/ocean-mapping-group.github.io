---
layout: default
title: file
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 12
---
# file

## Description
`file.c` is a Motif GUI source file that provides high-level file management functions for the "Submetrix 2000 unraveller" application. It contains wrapper functions for opening Submetrix 2000 raw data files (`.sxr` or `.sxi` formats) and placeholder functions for operations like creating, writing, and closing files. The actual low-level handling of the Submetrix data format is delegated to functions provided by the `j_SUB2K` library.

## Functions

### `int create_file(char *filename)`
This function is a placeholder and currently only prints a message indicating that raw files cannot be created directly by this part of the application. It's commented out to prevent creation.

### `int open_file(char *filename)`
Opens a Submetrix 2000 raw data file.
*   `filename`: The path to the `.sxr` or `.sxi` file to open.
*   It calls `open_SUBX_files(filename, filename)` (from `j_SUB2K`) to perform the actual file opening and initialization of internal Submetrix data structures.
*   Sets the global `opened` flag to `TRUE`.
*   **Returns:** `1` on success.

### `void write_file()`
This function is a placeholder and currently only prints a message. The application likely performs continuous background writing or doesn't have a direct "save current view" equivalent in this module.

### `void close_file()`
Closes the currently opened Submetrix 2000 data files.
*   Calls `close_SUBX_files()` (from `j_SUB2K`) to perform the necessary cleanup and file closing.

## How It Works
This module acts as an interface between the Motif GUI's file selection dialogs and the core Submetrix 2000 data handling library (`j_SUB2K`). When a user selects to open a file through the GUI, `file.c`'s `open_file` function is invoked. This, in turn, calls the specialized `j_SUB2K` functions to parse the Submetrix file. The placeholder `create_file` and `write_file` functions indicate that this particular GUI application focuses on reading and processing existing raw data rather than creating or modifying these raw files directly through its interface.
