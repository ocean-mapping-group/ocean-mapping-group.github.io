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

*   `plot_open(float dx, float dy, char *metafile)`: Opens a new plot file and initializes the plotting context. Writes a `STR` (start) command to the metafile, indicating the plot dimensions.
*   `plot_close()`: Closes the current plot file. Writes an `END` command to the metafile.
*   `plot_rotate()`: Records a request to rotate the plot by 90 degrees. Writes a `ROT` command to the metafile.
*   `plot_move(float x, float y)`: Moves the plotting pen to an absolute position without drawing. Writes a `MOV` command with the coordinates to the metafile.
*   `plot_line(float x, float y)`: Draws a line from the current pen position to a new absolute position. Writes an `LNE` command with the coordinates to the metafile.
*   `plot_text(char *text)`: Draws a text string at the current pen position. Writes a `TXT` command with the string to the metafile.
*   `plot_textrot(float angle)`: Sets the orientation of text. Writes a `TRT` command with the angle to the metafile.
*   `plot_textrunrise(float run, float rise)`: Sets text orientation based on a run and rise vector. Calculates the angle from `run` and `rise` and calls `plot_textrot()`.
*   `plot_pen(int pen)`: Selects the plotting pen. If the pen number changes, writes a `PEN` command with the new pen number to the metafile.
*   `plot_textsize(float x, float y)`: Sets the size of the text characters. Writes a `TSZ` command with the size parameters to the metafile.
*   `plot_clip(float x0, float y0, float x1, float y1)`: Defines a clipping window for plotting. Writes a `CLP` command with the clipping window coordinates to the metafile.
*   `plot_diamond(float x, float y, float rad)`: Draws a diamond shape. Uses `plot_move` and `plot_line` to draw the diamond.
*   `plot_cross(float x, float y, float rad)`: Draws a cross shape. Uses `plot_move` and `plot_line` to draw the cross.

## How It Works
`plotlib.c` provides the high-level API for applications to create graphical output. Each `plot_*` function translates a generic plotting action into a simple text-based command (e.g., `STR` for start, `MOV` for move, `LNE` for line, `TXT` for text). These commands are written sequentially to an output metafile (`plot_file`). This metafile serves as an intermediate, device-independent representation of the plot. A separate program (`plotdriver`) then reads this metafile and, by linking with a specific device driver (like `hpgl.c` or `viewmeta.c`), converts these generic commands into device-specific instructions for actual rendering. This modular design ensures that applications using `plotlib` do not need to be modified for different output devices.

## Output Files
The module outputs a text-based metafile containing generic `plotlib` commands.

## Dependencies
*   `plotlib.h`: Defines the API and global variables for `plotlib`.
*   `support.h`: (Implied, for `access()` and `sprintf()` usage).
*   Standard C library functions for file I/O and string manipulation.

## Notes
All coordinates and sizes are in centimeters. The output metafile contains simple text commands that are human-readable. The `plot_file` stream must be successfully opened by `plot_open` for any plotting commands to be written. The library includes convenience functions (`plot_diamond`, `plot_cross`) for drawing common shapes. The design emphasizes portability and separation of concerns between plotting logic and rendering.