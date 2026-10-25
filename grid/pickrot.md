---
layout: default
title: pickrot
parent: Grid Tools
tool_name: pickrot
source_path: code/grid/pickrot.c
category: gridding
input_formats: ["ASCII waypoint/navigation track (-way)", "JHC_header rotated UTM box headers"]
output_formats: ["JHC_header rotated UTM mapsheet header (-out)"]
related_tools: ["make_blank", "make_bases", "edhead", "weigh_grid"]
---

# pickrot

## Overview

`pickrot` is an interactive X11 graphical utility for visually positioning, sizing, and rotating a **Rotated UTM (`projection = 4`)** mapsheet bounding box over plotted vessel navigation tracks or waypoint lines (`-way`). Once the user adjusts the box center, width, height, and rotation angle using the mouse and keyboard, quitting (`q` or `d`) writes the 1024-byte `OMG1` `JHC_header` to the file specified by `-out`.

---

## Syntax & CLI Options

```bash
pickrot [OPTIONS] [-way <wayfile>] -out <new_box.header> [<existing_box_headers...>]
```

| Option | Description | Default |
|---|---|---|
| `-out <filename>` | **Required.** Output filename for the newly defined 1024-byte `JHC_header` rotated UTM mapsheet (`projection = 4`). | None |
| `-way <filename>` | Input ASCII waypoint/track file beginning with `Emin Emax`, `Nmin Nmax`, `no_way`, followed by `east north` coordinate pairs. | None |
| `-East <Emin> <Emax>` | Explicitly set Easting display bounds (meters) when `-way` is not used or to override bounds. | From `-way` (`0.0 0.0`) |
| `-North <Nmin> <Nmax>` | Explicitly set Northing display bounds (meters). | From `-way` (`0.0 0.0`) |
| `-width <meters>` | Initial width (`rect_width[0]`) of the editable rotated mapsheet box in meters. | `1000.0` |
| `-height <meters>` | Initial height (`rect_height[0]`) of the editable rotated mapsheet box in meters. | `1000.0` |
| `-angle <deg>` | Initial rotation angle (`angle[0]`, stored in `header.ymax`) in degrees. | `0.0` |
| `-pixel <mpp>` | Grid pixel size in meters per pixel (`xstep` and `ystep`) used to compute `dx = width / pixel` and `dy = height / pixel`. | `10.0` |
| `<existing_box_headers...>` | Up to 49 existing rotated UTM (`projection == 4`) `JHC_header` files to display in cyan for reference when laying out adjacent tiles. | None |

---

## Interactive X11 Controls

| Input | Action |
|---|---|
| **Left Mouse Drag (Button 1)** | Rubber-band zoom into a sub-area (`Sub_Area` window). |
| **Middle Mouse Click (Button 2)** | Reposition the center (`Ecen[0]`, `Ncen[0]`) of the active blue mapsheet box to the cursor location. |
| **Left / Right Arrow Keys** | Decrease / increase mapsheet width (`rect_width[0]`) by `100 m`. |
| **Down / Up Arrow Keys** | Decrease / increase mapsheet height (`rect_height[0]`) by `100 m`. |
| **`+` / `-` Keys** | Rotate mapsheet angle (`angle[0]`) by $+0.5^\circ$ / $-0.5^\circ$. |
| **`r` Key** | Refresh the current window. |
| **`x` Key** | Close the zoomed sub-window. |
| **`q` or `d` Key** | Exit X11 session and write the final `JHC_header` (`projection = 4`, `xmin = Ecen`, `ymin = Ncen`, `ymax = angle`, `xstep = ystep = pixel`) to `-out`. |

---

## Examples

**Interactively align a 2 m resolution rotated UTM mapsheet along a survey track:**
```bash
pickrot -way survey_utm_track.way -width 4000 -height 1500 -angle 35.0 -pixel 2.0 -out channel_rot.blank
```

---

## Workflow Context

- **Next Step:** Pass the header written by `pickrot` into [`make_blank`](make_blank.md) (`-area <header>`) or `tor4` to allocate the full pixel array before gridding with [`weigh_grid`](weigh_grid.md).
