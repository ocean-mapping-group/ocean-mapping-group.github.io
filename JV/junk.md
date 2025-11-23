# `junk.c` - JView World Vector Shoreline (WVS) Plotting Module

This C file is responsible for drawing World Vector Shoreline (WVS) data onto the map display within the `jview` application. It dynamically selects an appropriate coastline dataset based on the current map's scale, projects the geographical coordinates to screen coordinates, and then renders the coastline segments. Despite its seemingly arbitrary filename, this module provides essential geographical context for data visualization in `jview`.

## Key Functions

*   **`draw_wvs(int window)`:**
    *   This is the primary function responsible for rendering WVS data.
    *   **Pre-condition Check:** It first verifies the `plot_shoreline` global flag. If this flag is false, the function returns immediately without drawing any coastlines.
    *   **Dynamic Dataset Selection:** The function intelligently determines which of six available WVS datasets (e.g., `wvsfull.dat`, `wvs250k.dat`, `wvs1.dat`, `wvs3.dat`, `wvs12.dat`, `wvs43.dat`) to use. This selection is based on the current `map_width` and `map_height` (derived from `sub_param` or `graphic_param` and `map_header.xstep`), which effectively represents the geographical extent currently visible in the map window. This dynamic selection ensures that an appropriate level of detail is displayed: coarser data for large-scale views and finer detail for zoomed-in areas, optimizing rendering performance and visual clarity.
    *   **Geographical Query Loop:** It iterates through a grid of latitude (`startlat` to `endlat`) and longitude (`startlon` to `endlon`) coordinates that encompass the current map view. For each grid cell, it queries for coastline data.
    *   **WVS Data Retrieval (`wvsrtv`):** The external function `wvsrtv` (presumably from a dedicated World Vector Shoreline retrieval library) is called to fetch coastline segments (stored in `latray`, `lonray`, and `segray`) for the specified geographical tile and chosen WVS dataset.
    *   **Filtering Single-Point Islands:** The code includes a condition (`nseg > 2 || latray[0] != latray[1] || lonray[0] != lonray[1]`) to filter out single-point "islands." These appear to be artifacts generated during the decimation process of the WVS data and are not intended to be drawn as part of continuous coastlines.
    *   **Projection and Drawing:** For each valid and non-single-point coastline segment retrieved:
        *   The latitude (`this_lat`) and longitude (`this_lon`) coordinates are transformed into the map's display coordinates (`segx`, `segy`) using the `Project` function.
        *   These projected segments are then drawn as lines onto the specified X-windows graphic `window` using the `jhc_line` function, typically rendered in `YELLOW` color.
    *   **Resource Cleanup:** After all coastlines have been processed and drawn, `wvsrtv("clean", ...)` is called to free any dynamically allocated memory or resources associated with the WVS retrieval process.

## Dependencies

This module relies on several global variables and external functions within the `jview` project and potentially external libraries:

*   `JV_global.h`: Provides access to essential global variables such as `plot_shoreline` (to control WVS drawing), `min_latitude`, `max_latitude`, `min_longitude`, `max_longitude` (defining the current map view extent), `sub_param`, `graphic_param` (for window dimensions and parameters), and `map_header.xstep` (for map scaling).
*   `wvsrtv`: An external function, likely part of a dedicated World Vector Shoreline library, used for retrieving coastline data segments based on geographical coordinates and selected dataset.
*   `Project`: A crucial function responsible for transforming geographical coordinates (latitude and longitude) into the Cartesian coordinates of the map display.
*   `jhc_line`: A graphics primitive function from the `jview`'s drawing library, used to draw lines on an X-windows display.

## Purpose

Despite its informal filename, `junk.c` serves a critical function in the `jview` application by accurately and efficiently visualizing shorelines. Its ability to adapt the level of coastline detail to the current map zoom ensures that geographical context is always present and rendered appropriately, which is vital for users analyzing marine, coastal, or other geographically referenced datasets.
