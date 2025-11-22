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

### `file_append(FILE *a, FILE *b)`
Appends the contents of file `b` to file `a`.
*   Reads `RUNSIZE` (16KB) chunks from `b` and writes them to `a`.

### `reset_state(boolean text)`
Resets the plotting state for the current pen.
*   If `pos_change` is true, it writes a `MOV` (move) command to the `sep_file` to set the pen position.
*   If `text` is true and certain flags are set (angle or size), it writes `TRT` (text rotate) or `TSZ` (text size) commands to reset text state for the current pen.

### `plot_start(float dx, float dy)`
Initializes the pensorting process.
*   **`dx`, `dy`:** Overall plot dimensions.
*   Initializes `sepfile` array (to `NULL`), `sepflag` array (to `0`), indicating no files are open and no state flags are set.
*   Writes a `STR` (start) command to the main output file (`plot_outfile`).

### `plot_end()`
Finalizes the pensorting process.
*   Iterates through all possible pens (`MAXPENS`).
*   For each pen that has an associated temporary file (`sepfile[i]`), it appends the content of that temporary file to the main `plot_outfile`.
*   Writes an `END` command and closes `plot_outfile`.

### `plot_pen(int pen)`
Selects a plotting pen. This is the core pensorting logic.
*   **`pen`:** The requested pen number.
*   If the requested `pen` is already the current `pen_number`, it does nothing.
*   If `pen` is 0, it directs output to the main `plot_outfile`.
*   If `sepfile[pen]` is not yet open:
    *   Creates a new temporary file (using `mkstemp`) for this pen.
    *   Writes a `PEN` command to this temporary file.
    *   Writes `TRT` (text rotate) and `TSZ` (text size) commands to set initial text state (if not already set for this pen).
*   Sets `sep_file` to point to the file stream associated with the selected pen.
*   Updates `pen_number` and sets `pos_change` to true.

### `plot_rotate()`
(Placeholder function) Writes a `ROT` command to `plot_outfile`.

### `plot_move(float x, float y)`
Records a pen movement.
*   **`x`, `y`:** Target coordinates.
*   Sets `pos_change` to true and updates `pen_x`, `pen_y` to store the new position.
*   (Note: The actual `MOV` command is deferred until `reset_state` is called before a drawing/text operation).

### `plot_line(float x, float y)`
Draws a line.
*   **`x`, `y`:** Target coordinates.
*   Calls `reset_state(false)` to ensure correct pen position before drawing.
*   Updates `pen_x`, `pen_y` and writes an `LNE` (line) command to the current `sep_file`.

### `plot_text(char *text)`
Draws text.
*   **`text`:** The text string.
*   Calls `reset_state(true)` to ensure correct pen position and text state before drawing.
*   Writes a `TXT` (text) command to the current `sep_file`.

### `plot_textrot(float angle)`
Sets text rotation.
*   **`angle`:** Rotation angle.
*   Updates `new_angle` and sets `angle_flag` for all pens, indicating that text rotation state needs to be reset when a pen is next selected.

### `plot_textsize(float x, float y)`
Sets text size.
*   **`x`, `y`:** Text size parameters.
*   Updates `new_x`, `new_y` and sets `size_flag` for all pens, indicating that text size state needs to be reset when a pen is next selected.

### `plot_clip(float x0, float y0, float x1, float y1)`
Sets clipping window.
*   **`x0`, `y0`, `x1`, `y1`:** Clipping window coordinates.
*   Updates `clip_x0`, `clip_y0`, `clip_x1`, `clip_y1` and sets `clip_flag` for all pens.

## Dependencies
*   `plotdriver.h`: Defines the interface for `plotlib` device drivers.
*   `plotlib.h`: Defines general `plotlib` constants and global variables.
*   `hpgl.h`: (Included, but HPGL-specific functionality is not directly used by this pensorting logic; it processes `plotlib`'s intermediate metafile format).

## Notes
*   The actual sorting happens by redirecting output for each pen to a temporary file. When `plot_end()` is called, these temporary files are concatenated into the final output in a specific order (from `MAXPENS-1` down to 0, with `first_pen` appended last if it's not 0).
*   The state (`pen_x`, `pen_y`, `new_angle`, `new_x`, `new_y`) is maintained globally, and flags (`pos_change`, `angle_flag`, `size_flag`) are used to ensure that these states are applied to each pen's temporary file when that pen is selected.
```
```