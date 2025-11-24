---
layout: default
title: pensort
parent: Plotlib Tools
nav_order: 149
---
# pensort

## Description
`pensort.c` is a utility that processes a `plotlib` metafile, which contains a sequence of plotting commands. Its primary function is to reorder these commands such that all drawing operations for a specific "pen" (color/style) are grouped together. This is a common optimization for physical plotters or some rendering pipelines, as it reduces the number of pen changes, thus potentially speeding up plotting.

The module separates the original metafile into temporary files, one for each pen used, and then appends these temporary files back into a single output metafile in a sorted order. It also attempts to reset the plotting state (like text rotation and size) when a pen is selected, ensuring consistent rendering.

## Functions

*   `file_append(FILE *a, FILE *b)`: Appends the contents of file `b` to file `a`. Reads `RUNSIZE` (16KB) chunks from `b` and writes them to `a`.
*   `reset_state(boolean text)`: Resets the plotting state for the current pen. Writes `MOV`, `TRT`, or `TSZ` commands to the `sep_file` as needed.
*   `plot_start(float dx, float dy)`: Initializes the pensorting process. Writes a `STR` (start) command to the main output file (`plot_outfile`).
*   `plot_end()`: Finalizes the pensorting process. Iterates through all possible pens, appends their temporary files to the main `plot_outfile`, writes an `END` command, and closes `plot_outfile`.
*   `plot_pen(int pen)`: Selects a plotting pen. If the pen changes, it redirects output to a temporary file associated with the selected pen.
*   `plot_rotate()`: (Placeholder function) Writes a `ROT` command to `plot_outfile`.
*   `plot_move(float x, float y)`: Records a pen movement. Updates `pen_x`, `pen_y` to store the new position.
*   `plot_line(float x, float y)`: Draws a line. Calls `reset_state(false)` to ensure correct pen position and writes an `LNE` (line) command to the current `sep_file`.
*   `plot_text(char *text)`: Draws text. Calls `reset_state(true)` to ensure correct pen position and text state, then writes a `TXT` (text) command to the current `sep_file`.
*   `plot_textrot(float angle)`: Sets text rotation. Updates `new_angle` and sets `angle_flag` for all pens.
*   `plot_textsize(float x, float y)`: Sets text size. Updates `new_x`, `new_y` and sets `size_flag` for all pens.
*   `plot_clip(float x0, float y0, float x1, float y1)`: Sets clipping window. Updates `clip_x0`, `clip_y0`, `clip_x1`, `clip_y1` and sets `clip_flag` for all pens.

## How It Works
`pensort` acts as a specialized `plotlib` device driver that intercepts plotting commands and reorders them before generating the final metafile. Instead of writing commands directly to the final output, it redirects them to temporary files, one for each pen. When the plot is finalized (`plot_end()`), it concatenates these temporary files back into a single output file, grouped by pen. This strategy minimizes physical pen changes on plotters, which can be a time-consuming operation. The module also manages internal state variables (like current pen position, text rotation, and size) and ensures these are correctly reset when a new pen is selected in the sorted output.

## Output Files
The module outputs a `plotlib` metafile (`plot_outfile`) with plotting commands sorted by pen.

## Dependencies
*   `plotdriver.h`: Defines the interface for `plotlib` device drivers.
*   `plotlib.h`: Defines general `plotlib` constants and global variables.
*   `hpgl.h`: (Included, but HPGL-specific functionality is not directly used by this pensorting logic; it processes `plotlib`'s intermediate metafile format).
*   Standard C library functions for file I/O and string manipulation.

## Notes
The actual sorting happens by redirecting output for each pen to a temporary file. When `plot_end()` is called, these temporary files are concatenated into the final output in a specific order (from `MAXPENS-1` down to 0, with `first_pen` appended last if it's not 0). The state (`pen_x`, `pen_y`, `new_angle`, `new_x`, `new_y`) is maintained globally, and flags (`pos_change`, `angle_flag`, `size_flag`) are used to ensure that these states are applied to each pen's temporary file when that pen is selected.