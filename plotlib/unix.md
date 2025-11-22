---
layout: default
title: unix
parent: Plotlib Tools
nav_order: 155
---
# unix

## Description
`unix.c` provides the backend functions for the `plotlib` library to generate UNIX plot command files. It acts as a filter, converting `plotlib`'s generic drawing commands (like `plot_move`, `plot_line`, `plot_text`) into the specific format understood by UNIX plot utilities (e.g., `plot(5)`).

This module enables applications using `plotlib` to produce graphical output compatible with traditional UNIX plotting tools. It includes helper functions for coordinate scaling and managing the plot state.

## Global Variables

*   `posknown`: A boolean flag indicating whether the current pen position is known.
*   `oldx`, `oldy`: Stores the previous X and Y coordinates of the pen.
*   `plopen`: A flag indicating if the plot device is open.

## Helper Functions

### `postx(float x)`
Scales a `plotlib` X-coordinate to a UNIX plot X-coordinate.

### `posty(float y)`
Scales a `plotlib` Y-coordinate to a UNIX plot Y-coordinate.

### `wnum(short x)`
Writes a short integer `x` to `plot_outfile` as two bytes.

## Functions (Implementing `plotlib` Driver Interface)

### `plot_start(float dx, float dy)`
Initializes the UNIX plot device.
*   **`dx`, `dy`:** The desired drawing area width and height (ignored beyond opening the plot).
*   Calls `openpl(plot_outfile)` to open the plot.

### `plot_end()`
Finalizes the UNIX plot.
*   Calls `closepl()` to close the plot.

### `plot_rotate()`
(Empty function) UNIX plot drivers don't typically handle rotation directly.

### `plot_move(float x, float y)`
Moves the plotting pen to a new absolute position without drawing.
*   **`x`, `y`:** Target coordinates in `plotlib` units.
*   Calls `move(postx(x), posty(y))` to move the pen.

### `plot_line(float x, float y)`
Draws a line from the current pen position to a new absolute position.
*   **`x`, `y`:** Target coordinates in `plotlib` units.
*   If the position is not known, calls `move` first.
*   Calls `cont(postx(x), posty(y))` to draw a line.

### `plot_text(char *text)`
Draws a text string.
*   **`text`:** The string to draw.
*   Calls `label(text)` to draw the text.

### `plot_textrot(float angle)`
(Empty function) Text rotation is not typically handled directly by this UNIX plot driver.

### `plot_pen(int pen)`
(Empty function) Pen selection is not typically handled directly by this UNIX plot driver.

### `plot_textsize(float x, float y)`
(Empty function) Text size is not typically handled directly by this UNIX plot driver.

### `plot_clip(float x0, float y0, float x1, float y1)`
(Empty function) Clipping is not typically handled directly by this UNIX plot driver.

## Internal UNIX Plot Functions (mimicking `plot(5)`)

*   `openpl(char *fname)`: Opens the plot device, initializes internal state, and sets up scaling.
*   `move(short x, short y)`: Writes a 'm' command and coordinates to move the pen.
*   `cont(short x, short y)`: Writes an 'n' command and coordinates to draw a line.
*   `line(short x1, short y1, short x2, short y2)`: Writes an 'l' command and coordinates to draw a line segment.
*   `point(short x, short y)`: Writes a 'p' command and coordinates to draw a point.
*   `closepl()`: Flushes `plot_outfile`.
*   `label(char *string)`: Writes a 't' command and the string for text.
*   `space(short x1, short y1, short x2, short y2)`: Writes an 's' command and coordinates to define the coordinate space.
*   `linemod(char *mode)`: Writes an 'f' command and mode for line type.
*   `wnum(short x)`: Writes a short integer as two bytes.
*   `erase()`: Writes an 'e' command to erase the plot.
*   `circle(short x, short y, short r)`: Writes a 'c' command and parameters to draw a circle.
*   `arc(short x, short y, short x0, short y0, short x1, short y1)`: Writes an 'a' command and parameters to draw an arc.

## Dependencies
*   `plotdriver.h`: Defines the interface for `plotlib` device drivers.
*   `plotlib.h`: Defines general `plotlib` constants and global variables.
*   `support.h`: (Implied, for utility functions).

## Notes
*   The coordinate scaling (`postx`, `posty`) is hardcoded for specific dimensions (20.4cm x 26.6cm to 2500x3250 device units).
*   Many `plotlib` features (like pen selection, text rotation, text size, clipping) are not fully implemented, reflecting the simplicity of the underlying UNIX plot format.
```
```