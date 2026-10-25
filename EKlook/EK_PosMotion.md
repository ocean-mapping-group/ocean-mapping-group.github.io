---
layout: default
title: EK_PosMotion (Module within EKlook)
parent: EKlook Tools
nav_order: 7
tool_name: EK_PosMotion
source_path: code/EKlook/EK_PosMotion.c
category: EKlook
input_formats:
  - OMG_HDCS (.merged)
  - OMG Attitude (.orientation / .POS_orient)
  - JHC 8-bit Backdrop (.mos)
  - JHC Float Area Maps (.r4)
output_formats:
  - Interactive 2D Map, 3D OpenGL Cone & Attitude Plots
related_tools:
  - EKlook
  - EK_funcs
---

# EK_PosMotion (Module within EKlook)

## Description
`EK_PosMotion` (`code/EKlook/EK_PosMotion.c`) is an interactive GUI module within the [`EKlook`](EKlook.md) application. It manages the **"Position-Motion EK-Trace Window,"** providing an integrated 2D plan-view map of the vessel track and ray-traced bottom footprint over an 8-bit multibeam backdrop (`-backdrop`), an interactive 3D OpenGL view of the vessel, tilted transducer, and acoustic beam cone, and synchronized time-series plots of Roll, Pitch, Heave, and Heading from multiple attitude sensors.

## Interactive Controls

| Control | Description |
|---|---|
| **Buttons** | |
| `Centre on Ping` | Toggles automatic centering of the 2D map and attitude time-series plots on the currently selected ping (`currenttrace`). |
| `Look at C/M/B` | Cycles the 3D OpenGL camera target between the vessel origin (**C**entre), mid-water ray (**M**iddle), and seafloor strike point (**B**ottom). |
| `Next Area` | Cycles through the geographic area `.r4` mapsheets loaded via `-areas`. |
| `Show Backdrop` | Toggles the 8-bit background orthomap (`-backdrop`) in the 2D plan view. |
| **Sliders** | |
| `Async. Motion Latency (s)` | Adjusts the time latency offset (in seconds) applied to asynchronous motion streams (`MRU0` vs. `POS MV`). |

## Visualizations

*   **Geographic Map View:** Displays the ship track, selected ping marker, ray-traced bottom strike point, elliptical beam footprint outline, and `.r4` area boundaries over the 8-bit multibeam backdrop.
*   **3D OpenGL View:** Renders the 3D vessel frame, mounted EK transducer cone, and seafloor strike vector (interactive camera controls via arrow keys, `+`/`-`, and `7`/`8`/`9` view presets).
*   **Attitude Time-Series Plots:** Four synchronized panels for **Roll**, **Pitch**, **Heave**, and **Heading**, overlaying `.merged` Tx attitude against `.orientation` and `.POS_orient` records.
