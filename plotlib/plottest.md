---
layout: default
title: plottest
parent: Plotlib Tools
nav_order: 154
---
# plottest

## Description
`plottest.c` is a simple test program for the `plotlib` library. It demonstrates basic usage of `plotlib` functions to open a plot, draw some lines, display text, and close the plot. It serves as a quick functional check of the `plotlib` installation and its ability to generate a metafile.

## Usage
```bash
plottest
```

## Arguments
None.

## How It Works
1.  **Initialization:** The `main` function is called.
2.  **`plot_open()`:** Calls `plot_open()` to initialize a plot. It requests a plot area of 10000x10000 units and lets `plotlib` generate a default filename for the metafile.
3.  **Plotting Commands:**
    *   `plot_pen(1)`: Selects pen number 1.
    *   `plot_textrot(0)`: Sets text rotation to 0 degrees.
    *   `plot_move(5000, 5000)`: Moves the pen to coordinates (5000, 5000).
    *   `plot_text("hello mom")`: Writes "hello mom" at the current position.
    *   `plot_pen(2)`: Selects pen number 2.
    *   `plot_move(0, 0)`: Moves to (0, 0).
    *   `plot_line(10000, 0)`: Draws a line to (10000, 0).
    *   `plot_line(10000, 10000)`: Draws a line to (10000, 10000).
    *   `plot_pen(3)`: Selects pen number 3.
    *   `plot_line(0, 10000)`: Draws a line to (0, 10000).
    *   `plot_line(0, 0)`: Draws a line to (0, 0).
    *   `plot_move(5000, 5000)`: Moves to (5000, 5000).
    *   `plot_textrot(90)`: Sets text rotation to 90 degrees.
    *   `plot_pen(4)`: Selects pen number 4.
    *   `plot_text("hello dad")`: Writes "hello dad".
    *   `plot_pen(5)`: Selects pen number 5.
    *   `plot_textrot(180)`: Sets text rotation to 180 degrees.
    *   `plot_text("hello world")`: Writes "hello world".
4.  **`plot_close()`:** Calls `plot_close()` to finalize and close the plot file.

## Output Files
*   A `plotlib` metafile (e.g., `plotfile_0`) containing the commands to draw a rectangle with text at various orientations.

## Dependencies
*   `plotlib.h`: For `plotlib` functions.
*   Standard C library functions for input/output.

## Notes
This program serves as a minimal working example and regression test for the `plotlib` library, ensuring that basic plotting functionality is correctly implemented. It generates a metafile that can then be viewed or converted by `plotdriver` and its associated device drivers.