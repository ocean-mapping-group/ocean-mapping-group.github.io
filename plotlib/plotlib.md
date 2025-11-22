---
layout: default
title: plotlib
parent: Plotlib Tools
nav_order: 152
---
# plotlib

## Description
`plotlib.c` implements the core `plotlib` API functions that generate an intermediate, device-independent metafile. These functions take plotting commands (like moving the pen, drawing lines, or placing text) and translate them into a series of text-based commands that are written to a file. This metafile can then be interpreted by a separate `plotdriver` (linked with a specific device backend like HPGL or a screen viewer) to produce the final graphical output.

This design decouples the plotting logic from the rendering device, making `plotlib` applications portable across different output systems.

## Global Variables

*   `plot_file`: A `FILE` pointer to the output metafile.
*   `plot_opened`: A boolean flag indicating whether a plot file is currently open.
*   `pen_number`: The currently selected pen number.

## Functions

### `plot_open(float dx, float dy, char *metafile)`
Opens a new plot file and initializes the plotting context.
*   **`dx`, `dy`:** The desired drawing area width and height in `plotlib` units (centimeters).
*   **`metafile`:** The name of the metafile to create. If `NULL` or empty, a unique name like `plotfile_N` is generated.
*   Writes a `STR` (start) command to the metafile, indicating the plot dimensions.

### `plot_close()`
Closes the current plot file.
*   Writes an `END` command to the metafile.

### `plot_rotate()`
Records a request to rotate the plot by 90 degrees.
*   Writes a `ROT` command to the metafile.

### `plot_move(float x, float y)`
Moves the plotting pen to an absolute position without drawing.
*   **`x`, `y`:** Target coordinates in `plotlib` units.
*   Writes a `MOV` command with the coordinates to the metafile.

### `plot_line(float x, float y)`
Draws a line from the current pen position to a new absolute position.
*   **`x`, `y`:** Target coordinates in `plotlib` units.
*   Writes an `LNE` command with the coordinates to the metafile.

### `plot_text(char *text)`
Draws a text string at the current pen position.
*   **`text`:** The null-terminated string to draw.
*   Writes a `TXT` command with the string to the metafile.

### `plot_textrot(float angle)`
Sets the orientation of text.
*   **`angle`:** Rotation angle in degrees.
*   Writes a `TRT` command with the angle to the metafile.

### `plot_textrunrise(float run, float rise)`
Sets text orientation based on a run and rise vector.
*   **`run`, `rise`:** X and Y components of the text direction vector.
*   Calculates the angle from `run` and `rise` and calls `plot_textrot()`.

### `plot_pen(int pen)`
Selects the plotting pen.
*   **`pen`:** The desired pen number.
*   If the pen number changes, writes a `PEN` command with the new pen number to the metafile.

### `plot_textsize(float x, float y)`
Sets the size of the text characters.
*   **`x`, `y`:** Character width and height scaling factors (in `plotlib` units).
*   Writes a `TSZ` command with the size parameters to the metafile.

### `plot_clip(float x0, float y0, float x1, float y1)`
Defines a clipping window for plotting.
*   **`x0`, `y0`, `x1`, `y1`:** Coordinates of the clipping window in `plotlib` units.
*   Sorts the coordinates to ensure `x0 <= x1` and `y0 <= y1`.
*   Writes a `CLP` command with the clipping window coordinates to the metafile.

### `plot_diamond(float x, float y, float rad)`
Draws a diamond shape.
*   **`x`, `y`:** Center coordinates.
*   **`rad`:** Radius of the diamond.
*   Uses `plot_move` and `plot_line` to draw the diamond.

### `plot_cross(float x, float y, float rad)`
Draws a cross shape.
*   **`x`, `y`:** Center coordinates.
*   **`rad`:** Radius of the cross.
*   Uses `plot_move` and `plot_line` to draw the cross.

## Dependencies
*   `plotlib.h`: Defines the API and global variables for `plotlib`.
*   `support.h`: (Implied, for `access()` and `sprintf()` usage).

## Notes
*   All coordinates and sizes are in centimeters.
*   The output metafile contains simple text commands that are human-readable.
*   The `plot_file` stream must be successfully opened by `plot_open` for any plotting commands to be written.
```
```