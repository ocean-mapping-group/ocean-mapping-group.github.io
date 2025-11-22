---
layout: default
title: hpgl
parent: Plotlib Tools
nav_order: 148
---
# hpgl

## Description
`hpgl.c` provides the backend functions for the `plotlib` library to generate HPGL (Hewlett-Packard Graphics Language) plot command files. It translates generic plotting commands (like `plot_move`, `plot_line`, `plot_text`) into specific HPGL instructions.

This module acts as a device driver for `plotlib`, enabling any application that uses `plotlib` to output its graphical results in the HPGL format, which is commonly used by pen plotters and some graphics software.

## Functions

### `plot_start(float dx, float dy)`
Initializes the HPGL plotting device.
*   **`dx`, `dy`:** The desired drawing area width and height in `plotlib` units.
*   Sets up scaling factors and offsets based on `plotlib`'s configuration.
*   Initializes the HPGL plotter.
*   Applies rotation if `plot_flip` is set.

### `plot_end()`
Finalizes the HPGL plot.
*   Lifts the pen if it's down (`PU;`).
*   Sends the plotter to home position (`SP0;PA0,0;`).
*   Initializes the plotter (`IN;`).

### `plot_rotate()`
Rotates the plot by 90 degrees.
*   Sends `RO90;IP;IW0,0,11100,16160;` command to the HPGL plotter.

### `plot_move(float x, float y)`
Moves the plotting pen to a new absolute position without drawing.
*   **`x`, `y`:** Target coordinates in `plotlib` units.
*   Converts `plotlib` coordinates to HPGL device units using `HPGL_XCOORD` and `HPGL_YCOORD` macros.
*   Sends `PA<x>,<y>;` (Plot Absolute) command.
*   Ensures the pen is up (`PU;`) before moving if it was down.

### `plot_line(float x, float y)`
Draws a line from the current pen position to a new absolute position.
*   **`x`, `y`:** Target coordinates in `plotlib` units.
*   Converts `plotlib` coordinates to HPGL device units.
*   Ensures the pen is down (`PD;`) before drawing if it was up.
*   Sends `PA<x>,<y>;` (Plot Absolute) command.

### `plot_text(char *text)`
Draws a text string at the current pen position.
*   **`text`:** The string to draw.
*   Sends `LB<text>\3;` (Label) command.
*   Resets `posknown` flag as text drawing can change the pen's perceived position.

### `plot_textrot(float angle)`
Sets the orientation of text.
*   **`angle`:** Rotation angle in degrees.
*   Calculates direction vectors and sends `DI<x_direction>,<y_direction>;` (Direction) command.

### `plot_pen(int pen)`
Selects the plotting pen.
*   **`pen`:** Pen number from `plotlib`'s internal mapping.
*   Maps the `plotlib` pen number to an HPGL pen number using `penmap[]`.
*   Sends `SP<pen_number>;` (Select Pen) command if the pen needs to change.

### `plot_textsize(float x, float y)`
Sets the size of the text characters.
*   **`x`, `y`:** Character width and height scaling factors (relative to `plotlib` units).
*   Sends `SI<width_scale>,<height_scale>;` (Size) command.

### `plot_clip(float x0, float y0, float x1, float y1)`
Defines a clipping window for plotting.
*   **`x0`, `y0`, `x1`, `y1`:** Coordinates of the clipping window in `plotlib` units.
*   Sends `IW<x0>,<y0>,<x1>,<y1>;` (Input Window) command if coordinates are provided, or `IW;` to disable clipping.

## Dependencies
*   `plotdriver.h`: Defines the interface for `plotlib` device drivers.
*   `plotlib.h`: Defines general `plotlib` constants and global variables.
*   `hpgl.h`: Defines HPGL-specific constants and macros, such as `HPGL_PENS`, `HPGL_XCOORD`, `HPGL_YCOORD`.

## Notes
*   The `plot_outfile` global variable (defined in `plotlib.h` and opened in `plotlib.c`) is used for all HPGL output.
*   `plot_scale_factor`, `plot_devres`, `plot_resolution`, and `plot_devinit` are global variables/arrays from `plotlib` that configure the output.
*   `penmap` is an array that maps `plotlib`'s generic pen numbers to specific HPGL pen numbers.
*   `posknown` and `pendown` flags are used to optimize HPGL output by minimizing redundant `PA` and `PU/PD` commands.
```
```