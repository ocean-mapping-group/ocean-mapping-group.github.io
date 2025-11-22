---
layout: default
title: penstat
parent: Plotlib Tools
nav_order: 150
---
# penstat

## Description
`penstat.c` is a utility that processes a `plotlib` metafile (a sequence of plotting commands) and generates statistics about the plotting operations. It calculates metrics such as the number of pen-up/pen-down movements, pen changes, text characters, and the total distance the pen travels both while drawing and while moving without drawing.

This tool is useful for analyzing the efficiency of a `plotlib` generated plot, which can be critical for optimizing plotting time on physical plotters or for understanding the complexity of a graphical output.

## Functions

### `plot_start(float dx, float dy)`
Initializes the statistics gathering process.
*   **`dx`, `dy`:** Overall plot dimensions (ignored by this module as it only gathers statistics, not performs actual plotting).
*   Resets internal counters and flags (`pen_x`, `pen_y`, `pen_down`, `pen_number`).

### `plot_end()`
Finalizes the statistics gathering and prints the results.
*   If the pen is currently down, increments `pen_ups`.
*   Prints a summary report to `plot_outfile` detailing:
    *   Number of pen-downs
    *   Number of pen-ups
    *   Number of pen changes
    *   Number of text characters
    *   Total distance drawn (pen down) in cm
    *   Total distance moved (pen up) in cm

### `plot_pen(int pen)`
Records a pen change.
*   **`pen`:** The requested pen number.
*   If the pen number changes, increments `pen_changes` and updates `pen_number`.

### `plot_rotate()`
(Empty function) This statistic module does not need to process rotation.

### `plot_move(float x, float y)`
Records a pen movement without drawing.
*   **`x`, `y`:** Target coordinates.
*   If the pen moves to a new position:
    *   If the pen was down, increments `pen_ups`.
    *   Calculates the distance moved using `DIST` macro and adds it to `pen_moved`.
    *   Updates `pen_x`, `pen_y`, and sets `pen_down` to false.

### `plot_line(float x, float y)`
Records a pen movement while drawing.
*   **`x`, `y`:** Target coordinates.
*   If the pen draws to a new position:
    *   If the pen was up, increments `pen_downs`.
    *   Calculates the distance drawn using `DIST` macro and adds it to `pen_drawn`.
    *   Updates `pen_x`, `pen_y`, and sets `pen_down` to true.

### `plot_text(char *text)`
Records text drawing.
*   **`text`:** The text string.
*   Adds the length of the string to `text_chars`.

### `plot_textrot(float angle)`
(Empty function) This module does not need to process text rotation.

### `plot_textsize(float x, float y)`
(Empty function) This module does not need to process text size.

### `plot_clip(float x0, float y0, float x1, float y1)`
(Empty function) This module does not need to process clipping.

## Dependencies
*   `plotdriver.h`: Defines the interface for `plotlib` device drivers.
*   `plotlib.h`: Defines general `plotlib` constants and global variables.
*   `support.h`: (Implied, for `DIST` macro).
*   `penstat.h`: Defines `penstat`-specific constants (e.g., global variables for statistics).

## Notes
*   This module implements the `plotlib` driver interface to intercept plotting commands and tally statistics.
*   The `plot_outfile` global variable is used to print the final statistics report.
```
```