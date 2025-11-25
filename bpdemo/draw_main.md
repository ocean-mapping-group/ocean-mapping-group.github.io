---
layout: default
title: draw_main.c
parent: BPdemo
nav_order: 9
---

# draw_main.c

## Description
`draw_main.c` is a source code file from the `bpdemo` application that contains all the core drawing and rendering logic. It is not a standalone command-line tool. This file is responsible for translating the numerical state of the beam pattern simulation into the graphical representations displayed in the various windows of the GUI.

It uses a set of custom drawing functions (prefixed with `jX_`) to render lines, rectangles, and polygons onto off-screen pixmaps, which are then copied to the screen.

## Functionality

### `void draw_main(jX_win_param *DA, int type)`
This is the primary rendering function. It is called whenever a part of the GUI needs to be redrawn. It checks which drawing area (`DA`) it is being asked to draw and what `type` of display is requested, then executes the appropriate drawing code.

*   **If Drawing Area is `DA_main`**:
    *   This is the main visualization window.
    *   It sets the coordinate system and clears the background.
    *   It draws the individual transducer elements at the bottom.
    *   It can draw the beam pattern in polar coordinates (if the "log BP" toggle is on).
    *   It can draw the individual wavefronts as "wiggles" arriving at the array (if the "wiggles" toggle is on).
    *   It draws a line indicating the current beam steering angle.

*   **If Drawing Area is `DA_polar`**:
    *   This window displays the phasor diagrams.
    *   It can draw the individual phasor vector for each element.
    *   It can draw the vector sum of all phasors.
    *   It can display the final amplitude as a bar graph.
    *   The exact visualization depends on the state of the toggle buttons in its popup menu (`pt_sum`, `pt_indiv`, `pt_amplitude`).

*   **If Drawing Area is `DA_time`**:
    *   This window displays the time-domain view of the signals.
    *   It draws the sinusoidal wave received at each element over time, clearly showing the phase shifts between them.

*   **If Drawing Area is `DA_options`**:
    *   This section appears to be a placeholder, as it only fills the area with a solid red color.

### `void expose_main(jX_win_param *DA)`
This is a helper function called by the event handlers when an `Expose` event occurs. Its only job is to copy the pre-rendered image from the off-screen pixmap (where `draw_main` does its work) to the visible window on the screen. This double-buffering technique ensures smooth, flicker-free updates and animations.