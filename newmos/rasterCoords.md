---
layout: default
title: rasterCoords
parent: Mosaicking Tools
nav_order: 5
module_name: rasterCoords
source_path: code/newmos/rasterCoords.c
category: Backscatter & Sidescan Mosaicking
related_tools: ["mos2", "afont", "cache", "j_proj"]
---

# rasterCoords

## Overview
`rasterCoords` (`code/newmos/rasterCoords.c`, originally written by Guy Carpenter and John Hughes Clarke, August 22, 1991) is a collection of legacy JCU/OMG `mosaic` raster-annotation routines preserved in `code/newmos/` for burning **geographic coordinate grid ticks, border degree/minute or UTM coordinate labels, and geographic polyline vectors** directly into `.mos` and `.ran` paged cache buffers (`moscache` and `rancache`).

Using the Hershey/vfont raster font engine ([`afont`](../subr/afont.md)) and the paged tile cache ([`cache`](../subr/cache.md)), these functions draw graticule ticks and text labels with maximum autoseam priority (`TICK_WEIGHT = 0`, `LABEL_WEIGHT = 0`) and black pixel intensity (`TICK_COLOR = 1`, `LABEL_COLOR = 1`) so that coordinate annotations are never overwritten by subsequent sidescan swaths.

---

## Constants & Target Destinations

Defined in `rasterCoords.c`:

| Constant | Value | Description |
|---|---|---|
| `TICK_SIZE` | `80` | Tick half-length scaling factor (`dx = (x1 - x0) / 80`, minimum `1` pixel). |
| `TICK_COLOR` / `LABEL_COLOR` | `1` | Pixel DN value (`1` = black) written into `moscache`. |
| `TICK_WEIGHT` / `LABEL_WEIGHT` | `0` | Priority weight (`0` = highest possible weight) written into `rancache` when `autoseam_flag` is active. |
| `IN_BOTH` | `0` | Draw line pixels into both `moscache` (`.mos`) and `rancache` (`.ran`). |
| `IN_MOSAIC` | `1` | Draw line pixels into `moscache` (`.mos`) only. |
| `IN_RANGE` | `2` | Draw line pixels into `rancache` (`.ran`) only. |

---

## Functions

| Function | Signature | Description |
|---|---|---|
| `MosaicGrid` | `void MosaicGrid(double interval)` | Draws a regular geographic or UTM coordinate graticule at spacing `interval` across the mosaic (`[min_lon, max_lon] x [min_lat, max_lat]`). Projects each grid intersection `(lon, lat)` via `(*Project)(lon, lat, &x0, &y0)`, writes cross-hair ticks of radius `(dx, dy)` into `moscache` (and `rancache` if `autoseam_flag` is set), loads `grid_font = "std"` via `af_loadfont()`, and renders horizontal latitude labels along the left/right borders and vertical (`af_setdirection(1)` / `3`) longitude labels along the top/bottom borders. Supports `mercator_proj` (DMS labels via `dmsstring`) and `utm_proj` (meter labels); skips `rotutm_proj`. |
| `dmsstring` | `char *dmsstring(double val, char *label)` | Formats a decimal degree latitude or longitude `val` into a static 8-character Degrees-Minutes-Hemisphere string `"%3d°%2d'%c"` (using ASCII `176` for the degree symbol and `label[0]`/`label[1]` for `'S'`/`'N'` or `'W'`/`'E'`, rounded to the nearest arc-minute). |
| `labelfn` | `void labelfn(int x, int y, unsigned char z)` | Callback registered with `af_setfunction(labelfn)` so [`afont`](../subr/afont.md)'s `aprintf()` writes glyph pixels at `(x, y)` into `moscache` with `LABEL_COLOR` (`1`) and `rancache` with `LABEL_WEIGHT` (`0`). |
| `Draw_Line` | `void Draw_Line(int x0, int y0, int x1, int y1, int color, int where)` | Rasterizes a straight line segment from `(x0, y0)` to `(x1, y1)` with pixel value `color` into `moscache` (`IN_MOSAIC`), `rancache` (`IN_RANGE`), or both (`IN_BOTH`). |
| `DrawVectors` | `void DrawVectors(char *name, int color)` | Opens an ASCII `<lat> <lon> <depth>` polyline file `name`, projects consecutive vertices into mosaic pixel coordinates `(x, y)`, clips segments to `[min_x, max_x] x [min_y, max_y]`, and draws them into `moscache` (`IN_MOSAIC`) via `Draw_Line()`. |

---

## Architectural Role
`rasterCoords.c` is kept in `code/newmos/` as a reference module from the original JCU `mosaic` program. In modern OMG workflows, coordinate grids, coastlines, and vector overlays are rendered dynamically at display time in [`jview`](../viz/jview.md) or PostScript plotting tools rather than permanently burned into the `.mos` raster pixels.
