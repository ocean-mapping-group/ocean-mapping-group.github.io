---
layout: default
title: plotlib
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/plotlib.c
category: Visualization, GUI & Plotting
related_tools:
- viewmeta
- plotdriver
- hpgl
- plotSVP
- plotProf
- plotBP
- plotTides
- lineplot
module_name: plotlib
header_path: code/subr/plotlib.h
---

# plotlib

## Overview & Purpose

`plotlib` (authored by Guy Carpenter, September 1989) is the Ocean Mapping Group's device-independent 2D vector plotting library. Scientific and diagnostic tools across the OMG repository call `plotlib` routines to emit an ASCII vector metafile of floating-point drawing primitives (`STR`, `MOV`, `LNE`, `TXT`, `PEN`, `CLP`, etc.), which can then be rendered on screen or converted to PostScript/HPGL by backend drivers in `code/plotlib/` (such as `viewmeta`, `plotdriver`, `hpgl`, `pensort`, and `penstat`).

## Key Data Structures, Constants & Macros

### Types & Global State
- `boolean`: `typedef unsigned char boolean` with `false` (`0x00`) and `true` (`0xff`).
- Internal Module State (`plotlib.c`):
  - `FILE *plot_file`: Active file stream for the output ASCII metafile.
  - `boolean plot_opened`: Guards against duplicate `plot_open` calls or drawing before opening a metafile.
  - `short pen_number`: Caches the currently active pen number (`0` indicates no pen selected) to suppress redundant `PEN` commands.

### Metafile Command Protocol
Every `plotlib` function writes a single line-oriented ASCII command to `plot_file`:
- `STR <dx> <dy>`: Initializes the plot canvas dimensions.
- `END`: Terminates the plot stream.
- `ROT`: Rotates the coordinate axes by 90 degrees (landscape/portrait toggle).
- `MOV <x> <y>`: Moves the pen to `(x, y)` with the pen up.
- `LNE <x> <y>`: Draws a straight line segment from the current position to `(x, y)` with the pen down.
- `TXT "<string>"`: Draws a null-terminated text label at the current position.
- `TRT <angle>`: Sets the text rotation angle in degrees.
- `TSZ <x> <y>`: Sets the character width (`x`) and height (`y`) in centimeters.
- `PEN <pen>`: Selects pen/color index `<pen>`.
- `CLP <x0> <y0> <x1> <y1>`: Sets the rectangular clipping window in centimeters.

## Public Functions & Signatures

### Canvas & State Control
- `int plot_open(float dx, float dy, char *metafile)`
  - Opens `metafile` for writing. If `metafile` is `NULL` or empty, automatically generates the first unused filename matching `"plotfile_%d"` (`plotfile_0`, `plotfile_1`, ...) using `access()`. Writes `"STR %.3f %.3f\n"` with dimensions `(dx, dy)` and flushes the stream. Returns `1` on success, `0` on failure.
- `int plot_close()`
  - Writes `"END\n"`, closes `plot_file`, and resets `plot_opened = false`.
- `int plot_rotate()`
  - Emits `"ROT\n"` to rotate the plot coordinate axes.
- `int plot_pen(int pen)`
  - Emits `"PEN %d\n"` and updates `pen_number` if `pen != pen_number`.
- `int plot_clip(float x0, float y0, float x1, float y1)`
  - Sorts `(x0, x1)` and `(y0, y1)` so that `x0 <= x1` and `y0 <= y1`, then emits `"CLP %.3f %.3f %.3f %.3f\n"`.

### Vector & Text Primitives
- `int plot_move(float x, float y)`
  - Emits `"MOV %.3f %.3f\n"` (pen-up move).
- `int plot_line(float x, float y)`
  - Emits `"LNE %.3f %.3f\n"` (pen-down line draw).
- `int plot_text(char *text)`
  - Emits `"TXT \"%s\"\n"`.
- `int plot_textrot(float angle)`
  - Emits `"TRT %.3f\n"` to set text baseline angle in degrees.
- `int plot_textrunrise(float run, float rise)`
  - Computes the slope angle in degrees from `(run, rise)` using `atan(rise / run) * 180.0 / 3.14159` (handling vertical `run == 0.0` and negative `run` quadrants) and calls `plot_textrot(angle)`.
- `int plot_textsize(float x, float y)`
  - Emits `"TSZ %.3f %.3f\n"` to configure character cell width and height (cm).

### Higher-Order Symbol Helpers
- `void plot_diamond(float x, float y, float rad)`
  - Draws a closed 4-vertex diamond centered at `(x, y)` with half-width/radius `rad` using `plot_move` and four `plot_line` calls.
- `void plot_cross(float x, float y, float rad)`
  - Draws a `+` crosshair centered at `(x, y)` with arm radius `rad` and returns the pen to `(x, y)`.

## How It Fits Into the OMG Architecture

`plotlib` is used by over 35 plotting and diagnostic tools across `code/plot/` (`plotBP`, `plotAngular`, `plotSwath`, `plotTides`, `plotRoll`, `plotDelayHeave`, `plotFoot`, `plotDump`, `plot2D`, `asciiplot`), `code/ray/` (`plotSVP`, `traceRay`, `plotSOLN`), `code/grid/` (`plotProfile`, `plotADCPgridcurrents`), `code/sidescan/` (`mapmos`, `binplot`), `code/vers/` (`lineplot`), and `code/plotlib/` (`viewmeta`, `plotdriver`, `hpgl`).
