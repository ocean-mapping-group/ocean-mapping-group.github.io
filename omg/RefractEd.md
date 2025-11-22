---
layout: default
title: RefractEd
parent: OMG Tools
nav_order: 53
---
# RefractEd

## Description
`RefractEd` (Refraction Editor) is an interactive X-Windows based utility designed for visualizing and analyzing raytracing through sound velocity profiles (SVPs). It allows users to input SVPs, perform raytracing calculations, and visually compare the effects of different SVPs or constant velocity assumptions on beam paths and depth errors.

The tool provides a graphical interface to:
*   Display input SVPs.
*   Show ray paths for isovelocity, first SVP, and second SVP scenarios.
*   Plot vertical depth errors between these scenarios.
*   Interact with the SVP to modify velocities, observing the real-time impact on raytracing results.

## Usage
```bash
RefractEd <datafile> [-v] [-SUN] [-std16] [-raw <filename>] [-raw <filename2>]
```

## Arguments

| Option | Description |
|---|---|
| `<datafile>` | **Required (unless `-raw` is used).** The path to an SVP file in a specific format (e.g., depths and velocities). |
| `-raw <filename>` | Specifies a raw SVP filename for the first SVP. Can be used twice for two raw SVPs. |
| `-v` | Enable verbose output. |
| `-SUN` | Special flag for SUN workstations (installs colormap instead of setting it). |
| `-std16` | Uses a standard 16-layer SVP format (specific parsing logic). |

## Interactive Features
*   **Raytracing Visualization:** Displays ray paths through the water column for:
    *   **Isovelocity:** Rays traced with a constant sound velocity (e.g., 1500 m/s).
    *   **First SVP:** Rays traced with the first loaded SVP.
    *   **Second SVP:** Rays traced with the second loaded SVP (if two are provided).
*   **Depth Error Plots:** Shows vertical depth differences between the various raytracing scenarios, allowing users to quantify the impact of refraction.
*   **SVP Editing:** Users can interactively modify the sound velocity profile (e.g., by clicking and dragging points on the graphical display), and the raytracing results will update dynamically.
*   **Zooming/Panning:** Standard X-Windows controls for zooming into and panning across the plots.
*   **Output Dumps:** Can dump raytracing lookup tables (grazing angle, beam angle, time of flight) to files.

## How It Works
1.  **SVP Loading:** Loads sound velocity profiles either from a single data file or from one or two raw SVP files (using `-raw`). It can handle different SVP formats (`-std16`).
2.  **SVP Interpolation:** Interpolates the input SVPs into a set of equi-spaced depth layers (`layerthick`).
3.  **Raytracing Calculation:** For each ray (defined by `startangle` and `finishangle` with `anglestep`), it traces its path through the water column using Snell's Law. It calculates `across`, `deep`, and `Ttime` (two-way travel time) for each layer. This is done for isovelocity and the loaded SVPs.
4.  **Error Calculation:** Computes vertical depth differences (`Depth_difference`) between the raytraced depths of different scenarios.
5.  **X-Windows Interface:**
    *   Initializes an X-Windows display with several graphical windows for SVP, ray path, and error plots.
    *   Sets up a custom colormap.
    *   Enters an event loop to handle user interactions (mouse clicks, movements, key presses, window exposures).
    *   Redraws relevant graphical elements in response to user input or window events.
6.  **Lookup Table (LUT) Dumping:** The `dump_LUTs` function (though not explicitly called in `main`'s event loop in the provided snippet) is designed to write out lookup tables for grazing angle, beam angle, and time of flight into JHC image header (`.r4`) files.

## Files Generated (if `dump_LUTs` is called)
*   `.gra` (Grazing Angle Lookup Array)
*   `.bea` (Beam Angle Lookup Array)
*   `.tim` (Time of Flight Lookup Array)
