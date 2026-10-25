---
layout: default
title: jX_win
parent: Graphics & X11/OpenGL Libraries (subr_graphics)
module_name: jX_win
source_path: code/subr_graphics/jX_win.c
header_path: code/subr_graphics/jX_win.h
category: Motif & X11 Drawing Library
related_tools: ["X_extra", "jGL_draw", "swathed", "jview", "glSeis"]
---

# jX_win

## Overview
`jX_win` (`jX_win.c` / `jX_win.h`, written by John Hughes Clarke, July 1999) is the **OSF/Motif (`XmDrawingArea`) and `Xt` Intrinsics window/pixmap plotting library** in `subr_graphics/`. Created as a structured, per-widget upgrade to the global-array architecture of [`X_extra`](X_extra.md), `jX_win` encapsulates all state for an individual Motif drawing canvas—its `Widget`, X11 `Window`, offscreen backing `Pixmap`, `XImage` pixel buffer, world-coordinate bounds, and mouse rubber-band state—inside a self-contained `jX_win_param` struct.

This design allows complex Motif applications (`swathed`, `glSeis`, `synSwath`, and Motif-based interactive editors) to manage any number of independent 2D canvases with double-buffered pixmap rendering and world-coordinate plotting.

---

## Core Data Structure: `jX_win_param`

Defined in `jX_win.h`:
```c
typedef struct {
    Widget        widget;                       /* Motif XmDrawingArea widget */
    Pixmap        pixmap;                       /* Offscreen backing pixmap for expose redraws */
    Window        window;                       /* X11 Window ID (XtWindow(widget)) */
    Window        root;                         /* Root window ID */
    Font          font;                         /* Active X11 font */
    GC            draw_gc;                      /* Graphics context */
    Colormap      cmap;                         /* Colormap handle */
    XImage       *ximage;                       /* Direct-pixel ZPixmap image buffer */
    unsigned char *data;                        /* Raw pixel byte array (width * height * bitmap_pad/8) */

    float         x_min, y_min;                 /* World-coordinate minimum bounds */
    float         x_max, y_max;                 /* World-coordinate maximum bounds */
    unsigned int  width, height, depth, border_width; /* Canvas pixel geometry */
    int           x_org, y_org;                 /* Window origin */
    int           rubber;                       /* Rubber-band active flag */
    int           button1_down, button2_down, button3_down; /* Mouse button states */
    int           start, anchor_x, anchor_y, old_x, old_y;  /* Rubber-band tracking coords */
} jX_win_param;
```

---

## Global Variables (`jX_win.h` / `X_extra_globals.c`)

- `XtAppContext app_context` — Motif/Xt application context.
- `unsigned long white, black, red, yellow, green, blue, gray, orange` — Pre-allocated X11 color pixel values initialized by `jX_init_colors()`.
- `int colors[MAX_COLORS]` (`MAX_COLORS = 6`) — Array of the 6 primary named colors (`"Red"`, `"Yellow"`, `"Green"`, `"Blue"`, `"Slate Gray"`, `"Orange"`).
- `int jX_grey[256]` — 256-entry grayscale lookup table (16 allocated gray levels replicated across 16 steps each).

---

## Public Functions

### Conventions for Window vs. Backing Pixmap Drawing
In all `jX_win` drawing functions (`jX_line`, `jX_point`, `jX_fill_rect`, `jX_text`, `jX_draw_polygon`, `jX_fill_polygon`), the sign of the `color` parameter controls the target drawable:
- **`color >= 0`**: Draws directly into the visible X11 window (`wp->window`) using foreground pixel `color`.
- **`color < 0`**: Draws into the offscreen backing pixmap (`wp->pixmap`) using foreground pixel `abs(color)`, allowing fast flicker-free updates that can later be blitted to `wp->window` via `XCopyArea`.

| Function | Signature | Description |
|---|---|---|
| `jX_init_colors` | `void jX_init_colors(void)` | Queries the default colormap, allocates the 6 named primary colors (`red`, `yellow`, `green`, `blue`, `gray`, `orange`) plus `white`, `black`, and the 256-entry `jX_grey[]` ramp, and initializes `draw_gc` with the `"6x10"` font. |
| `jX_init_DA` | `void jX_init_DA(jX_win_param *wp)` | Initializes a realized Motif `XmDrawingArea` widget (`wp->widget`): retrieves `wp->window = XtWindow(wp->widget)`, queries window pixel geometry via `XGetGeometry`, creates the offscreen backing `wp->pixmap`, allocates `wp->data`, and binds a `ZPixmap` `wp->ximage` (`MSBFirst`) for direct raster blitting. |
| `jX_window_value` | `void jX_window_value(jX_win_param *wp, float x, float y, short *ix, short *iy)` | Converts world coordinates `(x, y)` in `[x_min, x_max] x [y_min, y_max]` into canvas pixel coordinates `(*ix, *iy)` (with Y inverted so `y_min` is at the bottom of the canvas). |
| `jX_scaled_values` | `void jX_scaled_values(jX_win_param *wp, int x, int y, float *rx, float *ry)` | Converts mouse pixel coordinates `(x, y)` into world coordinates `(*rx, *ry)`. |
| `jX_line` | `void jX_line(jX_win_param *wp, float x0, float y0, float x1, float y1, int color)` | Draws a line segment between `(x0, y0)` and `(x1, y1)` in world coordinates (falls back to a 1x1 `XFillRectangle` if both endpoints map to the same pixel). |
| `jX_point` | `void jX_point(jX_win_param *wp, float x, float y, int color)` | Plots a single clipped pixel at world coordinate `(x, y)` via `XDrawPoint`. |
| `jX_fill_rect` | `void jX_fill_rect(jX_win_param *wp, float x0, float y0, float x1, float y1, int color)` | Fills a rectangle between world corners `(x0, y0)` and `(x1, y1)`. |
| `jX_text` | `void jX_text(jX_win_param *wp, float x, float y, char *text, int color)` | Renders `text` at world coordinate `(x, y)` using `XDrawString`. |
| `jX_draw_polygon` | `void jX_draw_polygon(jX_win_param *wp, float *x, float *y, int count, int color)` | Draws a closed polygon outline of `count` (`<= 100`) vertices in world coordinates. |
| `jX_fill_polygon` | `void jX_fill_polygon(jX_win_param *wp, float *x, float *y, int count, int color)` | Fills a convex polygon of `count` (`<= 100`) vertices in world coordinates via `XFillPolygon`. |
| `jX_load_font` | `void jX_load_font(int height_in_pixels)` | Selects an X11 medium font (`6`, `8`, `10`, `12`, `14`, `16`, `18`, `25`, `30`, `40`, `50`, or `60` pt) matching `height_in_pixels` and updates `draw_gc`. |
| `jX_rubber_band` | `void jX_rubber_band(int old_x0, int old_y0, int anchor_x0, int anchor_y0, int new_x0, int new_y0, int start, jX_win_param *wp)` | Saves and restores 1-pixel `XImage` border strips (`top_line`, `bot_line`, `lef_line`, `rig_line`) to animate a red rubber-band selection box (`start = 0` init, `1` move, `2` erase) over `wp->window`. |
