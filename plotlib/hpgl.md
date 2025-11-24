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

*   `plot_start(float dx, float dy)`: Initializes the HPGL plotting device. Sets up scaling factors and offsets, and initializes the HPGL plotter.
*   `plot_end()`: Finalizes the HPGL plot. Lifts the pen, sends the plotter to home position, and initializes the plotter.
*   `plot_rotate()`: Rotates the plot by 90 degrees. Sends `RO90;IP;IW0,0,11100,16160;` command.
*   `plot_move(float x, float y)`: Moves the plotting pen to a new absolute position without drawing. Converts `plotlib` coordinates to HPGL device units.
*   `plot_line(float x, float y)`: Draws a line from the current pen position to a new absolute position. Ensures the pen is down and sends `PA<x>,<y>;` command.
*   `plot_text(char *text)`: Draws a text string at the current pen position. Sends `LB<text>\3;` command.
*   `plot_textrot(float angle)`: Sets the orientation of text. Calculates direction vectors and sends `DI<x_direction>,<y_direction>;` command.
*   `plot_pen(int pen)`: Selects the plotting pen. Maps the `plotlib` pen number to an HPGL pen number.
*   `plot_textsize(float x, float y)`: Sets the size of the text characters. Sends `SI<width_scale>,<height_scale>;` command.
*   `plot_clip(float x0, float y0, float x1, float y1)`: Defines a clipping window for plotting. Sends `IW<x0>,<y0>,<x1>,<y1>;` command.

## How It Works
The `hpgl.c` module implements the device driver interface required by the `plotlib` library for HPGL output. When `plotlib` functions are called by an application, they generate intermediate, device-independent commands. `hpgl.c` intercepts these commands and translates them into the specific HPGL instruction set. This involves:
1.  **Coordinate Transformation:** Converting `plotlib`'s internal floating-point coordinates (typically in centimeters) to HPGL's integer device units.
2.  **State Management:** Maintaining the current pen position, pen status (up/down), and other drawing attributes to optimize the generated HPGL output and ensure correct rendering.
3.  **Command Generation:** Writing the appropriate HPGL commands (e.g., `PA` for Plot Absolute, `PD` for Pen Down, `LB` for Label) to the designated output file.

## Output Files
The module outputs HPGL commands to a file, which can then be sent to an HPGL-compatible plotter or software.

## Dependencies
*   `plotdriver.h`: Defines the interface for `plotlib` device drivers.
*   `plotlib.h`: Defines general `plotlib` constants and global variables.
*   `hpgl.h`: Defines HPGL-specific constants and macros.

## Notes
The `plotlib` library's design allows for modular device drivers. `hpgl.c` is one such driver, specifically tailored for HPGL output devices. The `posknown` and `pendown` flags are used internally to optimize HPGL command generation, minimizing redundant instructions and improving plotting efficiency. The coordinate scaling and mapping between `plotlib` units and HPGL units are handled internally by the driver.