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

*   `plot_start(float dx, float dy)`: Initializes the statistics gathering process. Resets internal counters and flags (`pen_x`, `pen_y`, `pen_down`, `pen_number`).
*   `plot_end()`: Finalizes the statistics gathering and prints the results. Prints a summary report to `plot_outfile` detailing pen movements, pen changes, text characters, and total distances.
*   `plot_pen(int pen)`: Records a pen change. If the pen number changes, increments `pen_changes` and updates `pen_number`.
*   `plot_rotate()`: (Empty function) This statistic module does not need to process rotation.
*   `plot_move(float x, float y)`: Records a pen movement without drawing. Calculates the distance moved and adds it to `pen_moved`.
*   `plot_line(float x, float y)`: Records a pen movement while drawing. Calculates the distance drawn and adds it to `pen_drawn`.
*   `plot_text(char *text)`: Records text drawing. Adds the length of the string to `text_chars`.
*   `plot_textrot(float angle)`: (Empty function) This module does not need to process text rotation.
*   `plot_textsize(float x, float y)`: (Empty function) This module does not need to process text size.
*   `plot_clip(float x0, float y0, float x1, float y1)`: (Empty function) This module does not need to process clipping.

## How It Works
`penstat` implements the `plotlib` device driver interface, but instead of rendering, it acts as an observer. It intercepts each `plotlib` command (e.g., pen movements, line draws, text prints, pen changes) and updates internal counters and accumulators. For pen movements and line draws, it calculates the Euclidean distance covered. At the end of the plot processing (`plot_end()`), it presents a summary report of all these accumulated statistics.

## Output Files
The module prints a statistics report to `plot_outfile` (standard output by default).

## Dependencies
*   `plotdriver.h`: Defines the interface for `plotlib` device drivers.
*   `plotlib.h`: Defines general `plotlib` constants and global variables.
*   `support.h`: (Implied, for `DIST` macro).
*   `penstat.h`: Defines `penstat`-specific constants (e.g., global variables for statistics).

## Notes
This tool is useful for analyzing and optimizing plotting routines. For example, a high number of pen changes can indicate inefficient plotting, while a large `pen_moved` distance (compared to `pen_drawn`) can highlight excessive pen-up movements, both of which can impact plotting speed on physical devices. This module demonstrates the flexibility of the `plotlib` driver architecture.