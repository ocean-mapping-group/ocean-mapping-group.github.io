---
layout: default
title: X_extra
parent: X11 / Motif / OpenGL Graphics Library (subr_graphics)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr_graphics/X_extra.c
category: X11 & GUI Widget Library
related_tools:
- jX_win
- jGL_draw
- omg_colours
- jview
- swathed
- svp_tool
module_name: X_extra
header_path: code/subr_graphics/X_extra.h
---

# X_extra

## Overview
`X_extra` (`X_extra.c`, `X_extra.h`, and `X_extra_globals.c`, totaling >4,000 lines), written by John Hughes Clarke (October 1990, continuously updated through 2016), is the core **X11 (`Xlib`) windowing, custom widget, colormap, and 2D world-coordinate plotting library** used by almost all interactive Ocean Mapping Group visualization programs (including `jview`, `swathed`, `svp_tool`, `get_area`, `weigh_grid` interactive mode, and `j_edit`).

Originally designed for 8-bit `PseudoColor` Sun/SGI workstations and later upgraded (`jX_get_PseudoColor_visual_and_colormap`, `jMOD_XCreateSimpleWindow`) to seamlessly support 24-bit and 16-bit `TrueColor` Linux X11 displays, `X_extra` provides a complete lightweight GUI toolkit (`jX_widget_params`) supporting interactive sliders (`jX_slider`), buttons, labels, progress bars, rubber-band zoom boxes, dynamic color table stretching, and scaled floating-point/double-precision 2D plotting (`jhc_line`, `jhc_text`, `jhc_fill_polygon`, `jhc_draw_labeled_axis`).

---

## Key Data Structures (`X_extra.h`)

### 1. `window_param`
Maps pixel dimensions and parent-window fractional layout to 2D real-world coordinates (`[x_min, x_max] x [y_min, y_max]`):

```c
typedef struct {
    int   width, height;         /* Drawable size in pixels excluding border */
    float x_min, y_min;          /* World coordinate minimum bounds */
    float x_max, y_max;          /* World coordinate maximum bounds */
    float x_size, y_size;        /* Fractional width/height of main window */
    int   x_border, y_border;    /* Border padding in pixels */
    float x_topleft, y_topleft;  /* Fractional top-left offset in main window */
} window_param;
```

### 2. `jX_widget_params`, `jX_slider` & `jX_slider_range`
Declarative layout specification for constructing composite X11 tool forms with up to `MAX_SLIDERS` (`100`) sliders, `MAX_BUTTONS` (`500`) buttons, and `MAX_GRAPHICS` (`100`) drawing canvases stacked horizontally (`JX_STACK_HORI`), vertically (`JX_STACK_VERT`), or at custom pixel offsets (`JX_STACK_CUSTOM`):

```c
typedef struct jX_slider {
    char *label;
    jX_slider_range range;       /* left, right, zero, step */
    int *ival;                   /* Bound int pointer (if dorf == JX_INT) */
    float *fval;                 /* Bound float pointer (if dorf == JX_FLOAT) */
    double *dval;                /* Bound double pointer (if dorf == JX_DOUBLE) */
    int dorf;                    /* JX_FLOAT (0), JX_DOUBLE (1), or JX_INT (2) */
} jX_slider;
```

---

## Global X11 State (`X_extra_globals.c`)

`X_extra_globals.c` instantiates the shared X11 display and window arrays declared `extern` in `X_extra.h` and `jX_win.h`:
- **Display & Visuals**: `Display *display`, `int screen`, `Visual *visual`, `XVisualInfo vinfo`, `unsigned int ddepth`, `int bitmap_pad`, `Colormap def_cmap, new_cmap`, `XColor def_cols[256], jhc_cols[256]`.
- **Window & Pixmap Arrays**: `Window main_window`, `icon_window[20]`, `graphic_window[20]` (`graphic_pixmap[20]`), `button_window[1000]`, `label_window[20]`, `range_window[20]`, `sub_window[1000]` (`sub_param[1000]`, `sub_pixmap[1000]`).
- **Graphics Contexts**: `GC icon_gc`, `GC draw_gc`, `GC image_gc`.
- **Sizing Mode**: `int jX_little` (`JX_NORMAL = 0` using `9x15` font, `JX_TINY = 4` using `6x10` font for compact laptop screens, `JX_LARGE = 8`).

---

## Public Functions

### 1. X11 Initialization, Visuals & Colormaps

| Function | Signature | Description |
|---|---|---|
| `start_x` | `void start_x(void)` | Connects to the X server (`XOpenDisplay`), selects the optimal visual (`jX_get_PseudoColor_visual_and_colormap`), primes color palettes (`prime_palettes`, `do_colormap`), creates `main_window`, `icon_window[]`, and `graphic_window[]`, enables X11 event masks, and initializes `icon_gc`, `draw_gc`, and `image_gc`. |
| `jX_get_PseudoColor_visual_and_colormap` | `void jX_get_PseudoColor_visual_and_colormap(void)` | Queries `XMatchVisualInfo` for an 8-bit `PseudoColor` visual first, falling back cleanly to 24-bit `TrueColor` (`bitmap_pad = 32`) or 16-bit `TrueColor` on modern displays. |
| `jMOD_XCreateSimpleWindow` | `Window jMOD_XCreateSimpleWindow(Display *dpy, Window parent, int x, int y, unsigned int w, unsigned int h, unsigned int bw, unsigned long border, unsigned long bg)` | Wrapper around `XCreateWindow` that binds `vinfo.depth`, `vinfo.visual`, and `new_cmap` so child windows never fail with `BadMatch` when the root window visual differs from `vinfo`. |
| `do_colormap` / `do_colormap_palette` / `load_colormap` / `make_CnCmap` | `void do_colormap(int type)` | Populates `jhc_cols[0..255]` (`SIXTEEN_PLUS`, `EIGHT_PLUS`, `ZERO_PLUS`, `GREY_PLUS`) with UI bevel colors (`X_WHITE`..`X_FRONT_NW`), primary colors (`BLACK`..`WHITE` at `COL_OFFSET=8`), and linearly/logarithmically stretched data palettes between `col_min` and `col_max`. |
| `terminate_x` | `void terminate_x(char *error_msg)` | Frees X11 resources, prints `error_msg` if non-NULL, and exits cleanly. |

### 2. Widget & Form Management (`jX_*`)

| Function | Signature | Description |
|---|---|---|
| `jX_setup_widget` | `void jX_setup_widget(jX_widget_params *params)` | Automatically computes pixel geometry and creates a complete form window containing title bar, Quit button, interactive slider bars, action buttons, and 2D graphics subwindows. |
| `jX_is_any_win` / `jX_is_win` | `int jX_is_any_win(jX_widget_params *params, int *type, Window *window)` | Translates an X11 event `Window` ID into a widget category (`JX_SLIDER`, `JX_GRAPHIC`, `JX_BUTTON`, `JX_QUIT`) and returns the 0-based index of the clicked control. |
| `jX_redraw_slider` / `jX_update_slider_variable` | `int jX_redraw_slider(jX_widget_params *params, int slider_no)` | Updates the bound `int`/`float`/`double` pointer for a slider and renders its 3D bevelled thumb bar and numeric readout. |
| `jX_make_button` / `jX_make_label` | `void jX_make_button(Window win, int num, int x, int y, int w, int h, char *label)` | Creates individual button or label subwindows. |
| `jX_draw_list` / `jX_draw_progress` | `void jX_draw_progress(int window, float percent, char *message)` | Renders scrollable selection lists and animated completion progress bars. |

### 3. World-Coordinate 2D Drawing (`jhc_*`)
Note: Passing a positive `sub_window` index draws into `graphic_window[sub_window]`; passing a negative index (`-sub_window`) targets `sub_window[abs(sub_window)]` (or its backing pixmap when `color < 0`):

| Function | Signature | Description |
|---|---|---|
| `jhc_window_value` / `jhc_window_dvalue` | `void jhc_window_value(int sub_win, float x, float y, short *ix, short *iy)` | Converts world coordinates `(x, y)` (`float` or `double`) into pixel coordinates `(*ix, *iy)`. |
| `jhc_scaled_values` / `jhc_scaled_dvalues` | `void jhc_scaled_values(int x, int y, int sub_win, float *rx, float *ry)` | Inverse conversion from mouse pixel `(x, y)` to world coordinates `(*rx, *ry)`. |
| `jhc_line` / `jhc_dline` | `void jhc_line(int sub_win, float x0, float y0, float x1, float y1, int color)` | Draws a line segment in world coordinates. |
| `jhc_text` / `jhc_dtext` | `void jhc_text(int sub_win, float x, float y, char *text, int color)` | Draws a text string at world coordinates `(x, y)`. |
| `jhc_shape` / `jhc_dshape` | `void jhc_shape(int sub_win, float x, float y, short isize, int shape, int color)` | Plots a marker symbol (`JHC_CROSS`, `JHC_DIAMOND`, `JHC_SQUARE`, `JHC_BOX`) of pixel radius `isize`. |
| `jhc_fill_rect` / `jhc_draw_polygon` / `jhc_fill_polygon` | `void jhc_fill_rect(int sub_win, float x0, float y0, float x1, float y1, int color)` | Draws or fills rectangles and arbitrary polygons in world coordinates. |
| `jhc_draw_labeled_axis` | `int jhc_draw_labeled_axis(int box_no, int XorY, int fontsize, int nodecplaces, int side, float axisval, float minval, float maxval, float step)` | Automatically draws and labels tick marks along an X or Y axis in world coordinates. |
| `j_rubber_band` | `void j_rubber_band(int old_x0, int old_y0, int anchor_x0, int anchor_y0, int new_x0, int new_y0, int start, Window win)` | Non-destructively saves/restores underlying `XImage` scanlines to animate interactive red rubber-band selection rectangles. |
