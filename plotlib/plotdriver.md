---
layout: default
title: plotdriver
parent: Plotlib Tools
nav_order: 151
---
# plotdriver

## Description
`plotdriver.c` is the core module of the `plotlib` library responsible for parsing an intermediate plot metafile and dispatching commands to a specific plotting device driver. It acts as an interpreter, translating a generic sequence of plotting instructions into device-specific calls (e.g., to HPGL or a custom viewer).

This architecture allows `plotlib` to be device-independent: applications generate a single metafile format, and `plotdriver` (linked with the appropriate device driver) handles the actual rendering on the chosen output device.

## Global Variables

*   `plot_infile`: File pointer to the input plot metafile (defaults to `stdin`).
*   `plot_outfile`: File pointer to the output plot (defaults to `stdout`).
*   `plot_resolution`: Resolution setting (default 1).
*   `plot_rescale`: Boolean flag for rescaling.
*   `plot_scale_factor`: Scaling factor (default 1.0).
*   `plot_devnum`: Index of the current plotting device.
*   `penmap[MAXPENS]`: Array mapping `plotlib` pen numbers to device-specific pen numbers.
*   `plot_flip`: Boolean flag for plot rotation.
*   `retry`: Boolean flag to retry reading from `plot_infile` on EOF.
*   `textbuf[1024]`: Buffer for reading input lines.
*   `textptr`: Pointer within `textbuf` for token parsing.

## Functions

### `get_line(FILE *plot_infile)`
Reads a line from `plot_infile` into `textbuf`.
*   Handles potential `EOF` by retrying if `retry` is true, allowing for processing of continuously growing metafiles (like `tail -f`).

### `parse_token()`
Extracts the first token from `textbuf` (pointed to by `textptr`) and advances `textptr` past it.

### `get_token(FILE *plot_infile)`
Reads a line, parses its first token, and identifies it as a `plotlib` command (e.g., `PL_STR`, `PL_END`, `PL_MOV`).

### `get_value(float *v)`
Parses a floating-point value from `textptr` and stores it in `*v`.

### `get_coord(float *x, float *y)`
Parses two floating-point coordinates (`x`, `y`) from `textptr`.

### `get_string(char *s)`
Parses a quoted string from `textptr` into `*s`.

### `list_dev()`
Prints a list of recognized device names (`plot_devlist`).

## Main Logic (`main(int argc, char **argv)`)

1.  **Argument Parsing:**
    *   `[-res n]`: Sets `plot_resolution`.
    *   `[-win n]`: Sets `MAXWINDOW` (ignored in the provided snippet beyond parsing).
    *   `[-just_dump]`: Sets `just_dump` flag (purpose unclear from snippet).
    *   `[-dev plotname]`: Selects the plotting device by name (e.g., "hpgl", "viewmeta").
    *   `[-nomap]`: Disables pen mapping (uses default pen numbers).
    *   `[-debug]`: Enables verbose debugging output.
    *   `[-retry]`: Enables retrying file reads on EOF.
    *   `[-penmap filename]`: Specifies a custom pen map file.
    *   `[-rotate]`: Sets `plot_flip` to true.
    *   `[-rescale f]`: Sets `plot_rescale` and `plot_scale_factor`.
    *   Handles input (`plot_infile`) and output (`plot_outfile`) file arguments.
2.  **Pen Map Initialization:** Initializes `penmap` array (defaults to 1:1 mapping if no custom pen map is provided).
3.  **Metafile Processing Loop:**
    *   Reads `plotlib` commands (tokens) one by one from `plot_infile`.
    *   Uses a `switch` statement to call the corresponding device driver function (e.g., `plot_start`, `plot_end`, `plot_move`, `plot_line`, `plot_text`, `plot_pen`, `plot_textrot`, `plot_textsize`, `plot_clip`).
    *   Handles `PL_END` token to terminate processing and exit.

## Dependencies (external functions called by `main`)

The following functions are expected to be provided by the linked device driver module (e.g., `hpgl.c` or `viewmeta.c`):

*   `plot_start(float dx, float dy)`
*   `plot_end()`
*   `plot_rotate()`
*   `plot_move(float x, float y)`
*   `plot_line(float x, float y)`
*   `plot_text(char *text)`
*   `plot_textrot(float angle)`
*   `plot_pen(int pen)`
*   `plot_textsize(float x, float y)`
*   `plot_clip(float x0, float y0, float x1, float y1)`

## Notes
*   The `plotlib` library's overall design separates the generation of plotting commands (done by user applications) from their interpretation and rendering (`plotdriver.c` + device-specific backend).
*   The `plot_devlist` array defines the available output devices, and each entry (e.g., "hpgl", "viewmeta") corresponds to a set of `plot_*` functions provided by a linked module.
```
```