---
layout: default
title: omg_colours
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/omg_colours.c
category: Visualization & Color Palettes
related_tools:
- jview
- swathed
- r4toz
- X11 plotting & image generation utilities
module_name: omg_colours
header_path: code/subr/omg_colours.h
---

# `omg_colours` — Standard OMG Color Table Palettes & HSV-to-RGB Conversion Library

## Overview & Purpose in the OMG Architecture

`omg_colours` (`code/subr/omg_colours.c`, `code/subr/omg_colours.h`) defines the standard 8-bit indexed color lookup tables (`red_pal`, `green_pal`, `blue_pal`), discrete overlay color index constants (`BLACK` through `WHITE`), palette initialization routine (`prime_palettes`), and HSV-to-RGB color space converter (`hsv_to_rgb`) used by OMG's X11 graphical user interfaces and raster rendering tools.

In 8-bit indexed X11 displays and OMG raster images (`JHC_header.rgb_cmap`), pixel intensities `0..255` are mapped through 256-entry RGB lookup tables across multiple selectable palettes (`NO_PALS = 3`), such as linear grayscale (`palette 0`) for sidescan/backscatter and the classic **LDGO (Lamont-Doherty Geological Observatory) bathymetric rainbow** (`palette 1`, progressing from black at `0`, blue $\rightarrow$ green $\rightarrow$ yellow $\rightarrow$ red $\rightarrow$ purple, and white at `255`).

---

## Key Constants & Global Arrays (`code/subr/omg_colours.h`)

### Discrete Overlay Color Indices
Offset by `COL_OFFSET` (`8`) to avoid colliding with system X11 colormap slots `0..7`:
- `COL_OFFSET` (`8`)
- `BLACK` (`8`), `RED` (`9`), `GREEN` (`10`), `BLUE` (`11`), `CYAN` (`12`), `YELLOW` (`13`), `MAGENTA` (`14`), `WHITE` (`15`)

### Global Palette Arrays
- `NO_PALS` (`3`): Number of supported 256-color palettes.
- `unsigned char red_pal[256][NO_PALS]`, `green_pal[256][NO_PALS]`, `blue_pal[256][NO_PALS]`: Global 256 × 3 RGB lookup tables storing 8-bit (`0..255`) red, green, and blue intensities for each palette index.

---

## Public Functions & Signatures

- `int prime_palettes()`
  Populates the global `red_pal`, `green_pal`, and `blue_pal` lookup tables:
  - **Palette `0` (Linear Grayscale)**: Sets `red_pal[i][0] = green_pal[i][0] = blue_pal[i][0] = i` for all `i` in `0..255`.
  - **Palette `1` (LDGO Bathymetric Color Ramp)**:
    - Index `0`: Black `(0, 0, 0)`.
    - Indices `1..63`: Blue to Green transition (`red = 0`, `green` ramps up in steps of 16, `blue` ramps down).
    - Indices `64..127`: Green to Yellow transition (`red` ramps up, `green = 240`, `blue = 0`).
    - Indices `128..191`: Yellow to Red transition (`red = 240`, `green` ramps down, `blue = 0`).
    - Indices `192..254`: Red to Purple/Magenta transition (`red = 240`, `green = 0`, `blue` ramps up).
    - Index `255`: White `(255, 255, 255)`.

- `void hsv_to_rgb(int *r, int *g, int *b, double h, double s, double v)`
  Converts a color specified in cylindrical **Hue-Saturation-Value (HSV)** coordinates:
  - `h`: Hue angle in degrees $[0.0, 360.0)$ (automatically wrapped via `while (h >= 360.0) h -= 360.0`).
  - `s`: Saturation in $[0.0, 1.0]$ (if `s == 0.0`, outputs achromatic grayscale `*r = *g = *b = floor(255.999 * v)`).
  - `v`: Value (brightness) in $[0.0, 1.0]$.
  Computes the 6-sector (`i = floor(h / 60.0)`) piecewise linear RGB components and scales them to 8-bit integers `(*r, *g, *b)` in `[0..255]`.

---

## How It Fits Into the OMG Architecture

`omg_colours` provides consistent color-table initialization and HSV-to-RGB sun-illuminated relief shading across OMG's visualization and image export programs (`jview`, `swathed`, `r4toz`, and X11 display utilities).
