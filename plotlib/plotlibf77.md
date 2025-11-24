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

*   `make_cstring(char *string, int len)`: A helper function to convert a Fortran string (fixed-length, potentially space-padded) into a null-terminated C string.
*   `plot_open_(float *dx, float *dy, char *metafile, int len)`: Fortran interface for `plot_open`. Calls the C `plot_open` function after converting the Fortran string.
*   `plot_rotate_()`: Fortran interface for `plot_rotate`. Calls the C `plot_rotate` function.
*   `plot_close_()`: Fortran interface for `plot_close`. Calls the C `plot_close` function.
*   `plot_move_(float *x, float *y)`: Fortran interface for `plot_move`. Calls the C `plot_move` function.
*   `plot_line_(float *x, float *y)`: Fortran interface for `plot_line`. Calls the C `plot_line` function.
*   `plot_text_(char *text, int len)`: Fortran interface for `plot_text`. Calls the C `plot_text` function after converting the Fortran string.
*   `plot_textrot_(float *angle)`: Fortran interface for `plot_textrot`. Calls the C `plot_textrot` function.
*   `plot_pen_(int *pen)`: Fortran interface for `plot_pen`. Calls the C `plot_pen` function.
*   `plot_textsize_(float *x, float *y)`: Fortran interface for `plot_textsize`. Calls the C `plot_textsize` function.

## How It Works
`plotlibf77.c` provides a compatibility layer between Fortran 77 programs and the C `plotlib` library. Fortran compilers often use different calling conventions (e.g., passing arguments by reference, appending underscores to function names) and string representations (fixed-length, space-padded). The wrapper functions in `plotlibf77.c` (e.g., `plot_open_`) handle these differences by:
1.  **Matching Calling Conventions:** Accepting pointers to Fortran variables.
2.  **String Conversion:** Using `make_cstring` to convert Fortran strings into C-compatible null-terminated strings before passing them to the underlying C `plotlib` functions.
This allows Fortran applications to generate `plotlib` metafiles without needing direct knowledge of C interfacing, promoting code reuse across different programming languages.

## Output Files
The module generates `plotlib` metafiles via the underlying C `plotlib` library.

## Dependencies
*   `plotlib.h`: Defines the C API for `plotlib`.
*   Standard C library functions for string manipulation and memory management.

## Notes
Fortran compilers typically append an underscore (`_`) to external function names when generating object code. This module uses this convention (e.g., `plot_open_`) to match the Fortran calls. Fortran CHARACTER variables are fixed-length and often space-padded. `make_cstring` is crucial for converting these to null-terminated C strings correctly. The implementation of `make_cstring` uses a static buffer, which means it is not re-entrant and not thread-safe. This is a common pattern in older Fortran-C interfaces.