---
layout: default
title: afont
parent: Subr Tools
grand_parent: code
nav_order: 1
---
# afont

## Description
`afont.c` is a C utility library designed for rendering text onto a 2D array, which typically represents an image buffer or graphical display. It utilizes a custom "vector font" format, allowing for flexible text drawing with control over font selection, foreground color, drawing destination, and text orientation. This low-level text rendering engine is likely used by other modules in the GEMINI project for annotating plots, images, or graphical user interfaces.

## Global Variables
*   `unsigned char *afont_array`: Pointer to the 2D array where characters are drawn.
*   `int afont_dx, afont_dy`: Dimensions (width and height) of `afont_array`.
*   `unsigned char afont_color`: The color to use for drawing characters.
*   `boolean afont_loaded`: Flag indicating if a font has been loaded.
*   `char *afont_deffont`: Default font name to load if none is specified.
*   `af_function *afont_fn`: Pointer to the drawing function (`af_arraywrite` by default).
*   `struct header afont_head`: Font file header structure.
*   `struct dispatch afont_disp[256]`: Character dispatch table (stores character metrics and data offsets).
*   `unsigned char *afont_data`: Raw font bitmap data.
*   `int afont_dxx, afont_dyx, afont_dxy, afont_dyy`: Transformation matrix components for text direction.
*   `int afont_ysense`: Y-axis direction sense (e.g., positive down or up).

## Functions

### `void af_setysense(char dy)`
Sets the Y-axis direction sense for drawing.
*   `dy`: Character indicating Y-axis sense (e.g., positive down).

### `void af_setdest(unsigned char *array, int dx, int dy)`
Sets the destination 2D array and its dimensions for text drawing.
*   `array`: Pointer to the `unsigned char` array.
*   `dx`: Width of the array.
*   `dy`: Height of the array.

### `void af_setfunction(af_function *fn)`
Sets a custom drawing function to be used instead of the default `af_arraywrite`.
*   `fn`: Pointer to the custom `af_function`.

### `void af_setcolor(unsigned char color)`
Sets the foreground color for text drawing.
*   `color`: The 8-bit color value.

### `void af_setdirection(unsigned char direction)`
Sets the text drawing direction (e.g., right, up, left, down) by modifying an internal transformation matrix.

### `void af_loadfont(char *fontname)`
Loads a specified vector font file into memory.
*   `fontname`: The name of the font file (e.g., "std").
*   Reads the font header, character dispatch table, and raw character bitmap data from the font file.

### `void af_arraywrite(int x, int y, unsigned char z)`
The default drawing function that writes a single pixel (`z`) at `(x, y)` in the `afont_array`.

### `void aprintc(int x, int y, unsigned char ch)`
Draws a single character (`ch`) at a given `(x, y)` coordinate.
*   `x, y`: Starting coordinates for the character.
*   `ch`: The ASCII value of the character to draw.

### `void af_textsize(int *dx, int *dy, char *msg, ...)`
Calculates the dimensions (width `dx` and height `dy`) that a given formatted string (`msg`) would occupy if drawn.
*   `dx, dy`: Pointers to store the calculated width and height.
*   `msg`: Format string (like `printf`).
*   `...`: Variable arguments for the format string.

### `void aprintf(int x0, int y0, char *msg, ...)`
Prints a formatted string (`msg`) starting at a given `(x0, y0)` coordinate.
*   `x0, y0`: Starting coordinates for the string.
*   `msg`: Format string (like `printf`).
*   `...`: Variable arguments for the format string.

## How It Works
The `afont` library operates by loading a font definition, which includes a header, a dispatch table for each character, and raw bitmap data for the characters themselves.
1.  **Font Loading:** `af_loadfont` reads a font file. The `header` contains overall font information, `dispatch` entries for each character store its dimensions (left, right, up, down extents) and an offset into the `afont_data` (bitmap data).
2.  **Drawing Destination:** `af_setdest` (or `af_setfunction`) defines where the pixels will be drawn (either directly into a `unsigned char` array or via a custom function).
3.  **Drawing Characters:**
    *   `aprintc` is the core character drawing function. It retrieves the character's metrics and bitmap data from the loaded font's `dispatch` table.
    *   It then iterates through the character's bitmap, translating its local coordinates to the global coordinates of the `afont_array`, accounting for the current `afont_dxx`, `afont_dyx`, `afont_dxy`, `afont_dyy` (direction matrix).
    *   For each 'on' pixel in the character's bitmap, it calls the `afont_fn` (which defaults to `af_arraywrite`) to draw the pixel at the calculated coordinates with `afont_color`.
This approach provides fine-grained control over text rendering, useful for specialized graphical outputs common in scientific and engineering applications.
