---
layout: default
title: X11 / Motif / OpenGL Graphics Library (subr_graphics)
parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 2
has_children: true
---

# Graphics & X11/OpenGL Libraries (`subr_graphics/`)

The `code/subr_graphics/` directory contains the shared graphical user interface (GUI), 2D world-coordinate plotting, raster image display, and 3D OpenGL visualization libraries used across all interactive Ocean Mapping Group applications (`jview`, `swathed`, `svp_tool`, `glSeis`, `synSwath`, `get_area`, `j_edit`, `pb_sim`, etc.).

Separating X11 (`-lX11`), OSF/Motif (`-lXm -lXt`), and OpenGL (`-lGL -lGLU`) rendering routines into `subr_graphics/` allows non-graphical command-line batch tools in the OMG suite to link purely against [`subr/`](../subr/) without requiring X11 or OpenGL libraries at link or run time.

---

## Library Modules

| Module | Source Files | Primary Technology | Role in the OMG Architecture |
|---|---|---|---|
| [`X_extra`](X_extra.html) | `X_extra.c`<br>`X_extra.h`<br>`X_extra_globals.c` | Pure `Xlib` (`<X11/Xlib.h>`, `<X11/Xutil.h>`) | **Core X11 Window, Colormap, Widget & 2D Plotting Toolkit**: Manages X server connections (`start_x`), 8-bit `PseudoColor` and 16/24-bit `TrueColor` visuals (`jX_get_PseudoColor_visual_and_colormap`), dynamic 256-entry colormaps (`do_colormap`), declarative form widgets (`jX_setup_widget` with sliders, buttons, labels, and progress bars), rubber-band zoom boxes, and `float`/`double` world-coordinate 2D plotting (`jhc_line`, `jhc_text`, `jhc_shape`, `jhc_draw_labeled_axis`). |
| [`jX_win`](jX_win.html) | `jX_win.c`<br>`jX_win.h` | OSF/Motif (`<Xm/Xm.h>`) + `Xlib` | **Motif `XmDrawingArea` Canvas & Double-Buffered Pixmap Library**: Encapsulates per-widget window, backing `Pixmap`, and `ZPixmap` `XImage` buffers inside `jX_win_param` (`jX_init_DA`). Supports world-coordinate plotting (`jX_line`, `jX_point`, `jX_fill_rect`, `jX_text`, `jX_fill_polygon`) into either the live window (`color >= 0`) or the offscreen pixmap (`color < 0`), plus non-destructive rubber-band selection (`jX_rubber_band`). |
| [`jGL_draw`](jGL_draw.html) | `jGL_draw.c`<br>`jGL_draw.h` | OpenGL (`<GL/gl.h>`, `<GL/glu.h>`, `<GL/glx.h>`) | **3D OpenGL Acoustic Geometry, Array & Platform Scene Engine**: Provides spherical camera controls (`calc_eye_pos`, `move_the_view`), 6-layer material/transparency management (`jGL_matprop`), 3D transducer array and near-field/time-delay beamforming animations (`draw_line_array`, `draw_T_array`, `draw_IandQ`), 3D transmit/receive steering cones (`draw_cone`), 15+ vessel/ROV/AUV/multibeam head models (`draw_appropriate_object`), and animated 3D ocean surface waves (`draw_sea_surface`). |

---

## Architectural Relationships

1. **Color Palette Integration with `subr/omg_colours`**:
   `X_extra` delegates raw RGB/HSV palette table initialization (`red_pal`, `green_pal`, `blue_pal`, `prime_palettes()`, `hsv_to_rgb()`) to [`omg_colours`](../subr/omg_colours.html) in `subr/` (so batch PostScript/SUN-raster tools can use the same colormaps without X11), while `X_extra` binds those RGB palettes into X11 `Colormap` hardware cells (`jhc_cols[256]`).
2. **Global Symbol Consolidation (`X_extra_globals.c`)**:
   Modern GCC (`-fno-common`) requires a single definition for shared globals. `X_extra_globals.c` defines all shared X11 state (`display`, `visual`, `vinfo`, `main_window`, `sub_window[]`, `draw_gc`, `jhc_cols[]`, `app_context`, `jX_grey[]`) declared `extern` across both `X_extra.h` and `jX_win.h`.
3. **3D Vector & Beam-Pattern Integration**:
   `jGL_draw` links directly with [`DCM_rthand`](../subr/DCM_rthand.html) (`fvect`, `fmatx`) and [`bP_stuff`](../subr/bP_stuff.html) (`Along_Shading`, `no_elements`, `Frequency`) to render physically accurate 3D array shading, element delays, and non-orthogonal cone intersections in `synSwath`, `swathed`, and `glSeis`.
