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

*   `get_line(FILE *plot_infile)`: Reads a line from `plot_infile` into `textbuf`. Handles potential `EOF` by retrying if `retry` is true.
*   `parse_token()`: Extracts the first token from `textbuf` (pointed to by `textptr`).
*   `get_token(FILE *plot_infile)`: Reads a line, parses its first token, and identifies it as a `plotlib` command (e.g., `PL_STR`, `PL_END`, `PL_MOV`).
*   `get_value(float *v)`: Parses a floating-point value from `textptr`.
*   `get_coord(float *x, float *y)`: Parses two floating-point coordinates (`x`, `y`) from `textptr`.
*   `get_string(char *s)`: Parses a quoted string from `textptr` into `*s`.
*   `list_dev()`: Prints a list of recognized device names (`plot_devlist`).

## Main Logic (`main(int argc, char **argv)`)
1.  **Argument Parsing:** Handles command-line options such as `[-res n]`, `[-dev plotname]`, `[-nomap]`, `[-debug]`, `[-retry]`, `[-penmap filename]`, `[-rotate]`, `[-rescale f]`. Configures input/output files.
2.  **Pen Map Initialization:** Initializes `penmap` array (defaults to 1:1 mapping if no custom pen map is provided).
3.  **Metafile Processing Loop:**
    *   Reads `plotlib` commands (tokens) one by one from `plot_infile`.
    *   Uses a `switch` statement to call the corresponding device driver function (e.g., `plot_start`, `plot_end`, `plot_move`, `plot_line`, `plot_text`, `plot_pen`, `plot_textrot`, `plot_textsize`, `plot_clip`).
    *   Handles `PL_END` token to terminate processing and exit.

## How It Works
`plotdriver.c` acts as the central orchestrator for `plotlib`'s device-independent plotting. An application using `plotlib` first generates a text-based "metafile" containing generic plotting commands. `plotdriver` then reads this metafile, parses each command, and dispatches it to a specific set of functions (a "device driver") that are linked at compile time. This allows the same metafile to be rendered on various output devices (e.g., HPGL plotters via `hpgl.c`, or an X-windows viewer via `viewmeta.c`) simply by linking with a different driver. The modular design ensures flexibility and extensibility.

## Output Files
The specific output files depend on the selected device driver. Typically, this is a device-specific plot file (e.g., `.hpgl` for HPGL, `.meta` for PostScript).

## Dependencies
*   `plotdriver.h`: Defines the interface for `plotlib` device drivers.
*   `plotlib.h`: Defines general `plotlib` constants and global variables.
*   `hpgl.h`: (Included for device list).
*   `viewmeta.h`: (Included for device list).
*   `penstat.h`: (Included for device list).
*   `unix.h`: (Included for device list).
*   Standard C libraries for file I/O and string manipulation.

## Notes
The `plotlib` library's overall design separates the generation of plotting commands (done by user applications) from their interpretation and rendering (`plotdriver.c` + device-specific backend). The `plot_devlist` array defines the available output devices, and each entry (e.g., "hpgl", "viewmeta") corresponds to a set of `plot_*` functions provided by a linked module. The `retry` flag is useful for processing real-time metafiles that are still being written to.