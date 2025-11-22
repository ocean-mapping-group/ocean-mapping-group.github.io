---
layout: default
title: plotlibf77
parent: Plotlib Tools
nav_order: 153
---
# plotlibf77

## Description
`plotlibf77.c` provides a Fortran 77 interface to the `plotlib` library. It acts as a wrapper, allowing Fortran programs to call the `plotlib` functions to generate plot metafiles. This module handles the necessary type conversions and string manipulations required to bridge the Fortran calling conventions with the C `plotlib` API.

This enables existing Fortran applications to leverage `plotlib` for their plotting needs without needing to rewrite them in C.

## Functions

### `make_cstring(char *string, int len)`
A helper function to convert a Fortran string (fixed-length, potentially space-padded) into a null-terminated C string.
*   **`string`:** Pointer to the Fortran string.
*   **`len`:** Length of the Fortran string.
*   Returns a pointer to a static C string buffer.

### `plot_open_(float *dx, float *dy, char *metafile, int len)`
Fortran interface for `plot_open`.
*   **`dx`, `dy`:** Pointers to Fortran REAL variables for plot dimensions.
*   **`metafile`:** Pointer to a Fortran CHARACTER variable for the metafile name.
*   **`len`:** Length of the `metafile` CHARACTER variable.
*   Calls the C `plot_open` function after converting the Fortran string.

### `plot_rotate_()`
Fortran interface for `plot_rotate`.
*   Calls the C `plot_rotate` function.

### `plot_close_()`
Fortran interface for `plot_close`.
*   Calls the C `plot_close` function.

### `plot_move_(float *x, float *y)`
Fortran interface for `plot_move`.
*   **`x`, `y`:** Pointers to Fortran REAL variables for coordinates.
*   Calls the C `plot_move` function.

### `plot_line_(float *x, float *y)`
Fortran interface for `plot_line`.
*   **`x`, `y`:** Pointers to Fortran REAL variables for coordinates.
*   Calls the C `plot_line` function.

### `plot_text_(char *text, int len)`
Fortran interface for `plot_text`.
*   **`text`:** Pointer to a Fortran CHARACTER variable for the text string.
*   **`len`:** Length of the `text` CHARACTER variable.
*   Calls the C `plot_text` function after converting the Fortran string.

### `plot_textrot_(float *angle)`
Fortran interface for `plot_textrot`.
*   **`angle`:** Pointer to a Fortran REAL variable for the rotation angle.
*   Calls the C `plot_textrot` function.

### `plot_pen_(int *pen)`
Fortran interface for `plot_pen`.
*   **`pen`:** Pointer to a Fortran INTEGER variable for the pen number.
*   Calls the C `plot_pen` function.

### `plot_textsize_(float *x, float *y)`
Fortran interface for `plot_textsize`.
*   **`x`, `y`:** Pointers to Fortran REAL variables for text size.
*   Calls the C `plot_textsize` function.

## Dependencies
*   `plotlib.h`: Defines the C API for `plotlib`.

## Notes
*   Fortran compilers typically append an underscore (`_`) to external function names when generating object code. This module uses this convention (e.g., `plot_open_`) to match the Fortran calls.
*   Fortran passes arguments by reference, so all C function parameters are pointers to the Fortran variables.
*   Fortran CHARACTER variables are fixed-length and often space-padded. `make_cstring` is crucial for converting these to null-terminated C strings correctly.
```
```