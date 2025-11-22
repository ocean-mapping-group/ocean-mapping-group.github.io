---
layout: default
title: traceRay
parent: Ray Tools
nav_order: 173
---
# traceRay

## Description
`traceRay` is a utility for visualizing ray paths through a sound velocity profile (SVP). It takes an SVP file, models the water column as a series of constant velocity layers, and then traces a set of acoustic rays at specified outgoing angles. The tool then generates a PostScript plot of these ray paths, showing their trajectory (horizontal range vs. depth) through the water column.

This tool is useful for understanding sound propagation behavior in different oceanographic conditions and for visualizing how SVP variations affect ray bending.

## Usage
```bash
traceRay -pro <svp_handle> [-fishdep <val>] [-layerthick <val>] [-spacing <step> <start> <finish>] [-range <val>] [-depth <val>] [-verbose]
```

## Arguments

| Option | Description |
|---|---|
| `-pro <svp_handle>` | **Required.** Base name for the sound velocity profile file.
    *   Expected input: `<svp_handle>.RAWPROF` (default), `<svp_handle>.svp` (`-simradsvp`), or `<svp_handle>.profile` (another format). |
| `-fishdep <val>` | Depth of the transducer/fish (meters). | `50.0` |
| `-layerthick <val>` | Thickness of the constant velocity layers in the water column model (meters). | `20.0` |
| `-spacing <step> <start> <finish>` | Defines the angular spacing for ray tracing:
    *   `step`: Angular step (degrees).
    *   `start`: Starting beam angle (degrees).
    *   `finish`: Finishing beam angle (degrees). | `0.01 0 89` |
| `-range <val>` | Maximum horizontal range for plotting (meters). | `22500.0` |
| `-depth <val>` | Maximum vertical depth for plotting (meters). | `5000.0` |
| `-verbose` | Enable verbose output. |
| `-simradsvp` | Input SVP file is in Simrad SVP format (`.svp`). |
| `-NEWsvp` | Input SVP file is in a "NEW" raw format (`.RAWPROF`). |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting various ray tracing and plotting parameters.
2.  **SVP Reading (`read_in_*()` functions):**
    *   Opens the input SVP file specified by `-pro` and the format flags (`-simradsvp`, `-NEWsvp`).
    *   Calls one of the `read_in_raw`, `read_in_NEW_raw`, or `read_in_svp` functions to load the raw sound velocity profile data (`rawvel`, `rawdep`).
    *   If `std16_flag` or `NEW_flag` is set, `make_equisvp()` is called to interpolate the raw SVP into an equi-spaced layered model (`veldep`).
3.  **Plot Setup:**
    *   Initializes a `plotlib` PostScript output (`svp_plot.meta`).
    *   Sets up plot dimensions (`dx`, `dy`), X/Y axis ranges (`xmin`, `xmax`, `ymin`, `ymax`), and labels (`vellabel`, `depthlabel`, `rangelabel`).
    *   Draws the main plot frame and legends.
    *   Plots the sound velocity profile (velocity vs. depth) as a line in a dedicated panel.
4.  **Ray Tracing Loop:**
    *   Iterates through each `outangle` from `startangle` to `finishangle` with `anglestep`.
    *   For each `outangle`:
        *   Initializes `posx`, `posz`, `ttime`, and `rangle`.
        *   Sets the initial pen position for plotting the ray.
        *   **Layer-by-Layer Propagation:** Traces the ray through the water column layers:
            *   Updates `posx`, `posz`, and `ttime` based on the ray's path through the current layer's velocity.
            *   Converts `posx` and `posz` to screen coordinates (`xpos`, `ypos`).
            *   Draws a line segment from the previous point (`oldxpos`, `oldypos`) to the current point (`xpos`, `ypos`), visualizing the ray path.
            *   Applies Snell's Law to calculate the new `rangle` for the next layer.
            *   Handles cases where the ray goes beyond `maxrange` or becomes horizontal.
5.  **Cleanup:** Closes the input SVP file and `plotlib` output.

## Output
*   A PostScript metafile (`svp_plot.meta`) visualizing the SVP and the traced ray paths.

## Helper Functions

*   `read_in_raw()`: Reads SVP data in a raw format (depth, velocity pairs).
*   `read_in_NEW_raw()`: Reads SVP data in another "NEW" raw format.
*   `make_equisvp()`: Interpolates raw SVP data to create an equi-spaced layered velocity profile (`veldep`).
*   `read_in_svp()`: Reads SVP data from a custom `.profile` format.
```
```