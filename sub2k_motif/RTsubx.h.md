---
layout: default
title: RTsubx.h
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 15
---
# RTsubx.h

## Description
`RTsubx.h` is a C header file that serves as a central definition file for global variables, constants, and data structures used throughout the "Submetrix 2000 unraveller" Motif GUI application. It declares the `jX_win_param` structures that manage the drawing areas, defines boolean flags and display state identifiers, and provides external declarations for functions that operate on these global elements. This header ensures consistent access to shared application state and display modes across different source files of the GUI.

## Global Variables Declared Extern
*   `jX_win_param DA1, DA2, DA3, DA4, DA10;`: Structures defining parameters for up to five drawing areas, including their associated Motif widgets, window IDs, dimensions, and drawing contexts.
*   `int DA_down;`: Indicates which drawing area is currently active or has received the last event.
*   `int display_state[4];`: An array storing the current display mode (e.g., `RTS_AB_PHASE`, `RTS_LOG_AMPL`) for each of the four main drawing areas.
*   `int save_flag;`: A flag indicating whether a save operation is in progress.
*   `int new;`: A flag indicating if the current file is new (needs a "Save As").
*   `int saved;`: A flag indicating if the current file has been saved.
*   `int show_gates;`: A flag to control the display of gate lines in the bathymetry view.
*   `int show_raw;`: A flag to control the display mode of raw data versus processed data.

## Constants

### Debugging & Boolean Flags
*   `#define DEBUG 0`: Debugging flag (0 for disabled).
*   `#define TRUE 1`: Boolean true.
*   `#define FALSE 0`: Boolean false.

### Display States / Data Types
These constants define the various types of data or processing results that can be displayed in the drawing areas, used to control the rendering logic in `draw_view.c`.
*   `#define RTS_NOTHING 0`
*   `#define RTS_AB_PHASE 1`
*   `#define RTS_AC_PHASE 2`
*   `#define RTS_AD_PHASE 3`
*   `#define RTS_LOG_AMPL 4`
*   `#define RTS_SIDESCAN 5`
*   `#define RTS_ANGLE 6`
*   `#define RTS_ANGDIFFS 7`
*   `#define RTS_BC_PHASE 8`
*   `#define RTS_CD_PHASE 9`
*   `#define RTS_AB_BC_PHASE 10`
*   `#define RTS_SLR_SIDES 11`
*   `#define RTS_SLR_BATHY 12`
*   `#define RTS_ORIENT 13`

## External Functions Declared
*   `extern int recalc_and_draw();`: Function to trigger reprocessing and redrawing of data.
