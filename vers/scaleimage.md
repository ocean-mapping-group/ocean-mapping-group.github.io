---
layout: default
title: scaleimage
parent: Version Control & Build Stamps (vers)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
tool_name: scaleimage
source_path: code/vers/scaleimage.c
category: Cartographic & Map Plotting
related_tools:
- lineplot
- jview
- X_extra
- CnCcolorMap
---

# scaleimage

## Overview
`scaleimage` (`code/vers/scaleimage.c`, written by John E. Hughes Clarke, September 1991) is an interactive X11 cartographic layout and raster-to-plotter composition tool ("Versatec Plotting Editor"). It loads an 8-bit OMG raster image (`JHC_header` format, such as a sun-illuminated bathymetry `.sun`, color-coded depth `.8bit`, or sidescan `.mos` file), projects it to a user-specified map scale, overlays vector contours, navigation tracks, graticules, scale bars, sun-illumination spheres, depth colorbars, title blocks, and custom logos, and allows interactive placement of map widgets in an X11 window before outputting the final plot.

---

## Usage

```bash
scaleimage [OPTIONS] <imagefile>
```

---

## Command-Line Options

### Color Palettes, Masking & Image Controls

| Option | Description |
|---|---|
| `<imagefile>` | **Required.** Input 8-bit OMG raster file with a `JHC_header`. |
| `-grey` / `-col` / `-pseudo` | Select grayscale (`col_offset=257`), standard color (`513`), or pseudocolor (`769`) palette mapping. |
| `-cmap <cmapfile>` | Load a custom 256-entry 8-bit RGB colormap file. |
| `-set <actual_dn> <target_dn>` | Remap pixel value `<actual_dn>` to `<target_dn>` in the lookup table (repeatable). |
| `-mask <maskfile>` | Mask out pixels using a companion `JHC_header` raster mask file. |
| `-color_mask <file> <mode>` | Apply a secondary color mask raster using under-colormap `<mode>` (`1` = grey, `2` = pseudo, `3` = color). |
| `-rotate` | Rotate the output map layout by 90 degrees. |
| `-SUN` | Flag input image as sun-illuminated shaded relief. |
| `-chunk <rows>` | Number of raster scanline rows painted per batch (default `300`). |

### Map Graticule, Layout & Multi-Copy Tiling

| Option | Description |
|---|---|
| `-linear <dx_cm> <dy_cm>` | Use linear Cartesian scaling with explicit width `<dx_cm>` and height `<dy_cm>` in centimeters (skips interactive Mercator scale prompt). |
| `-grid <label_min> <tick_min>` | Set graticule label and tick spacing (default `15` and `5`). |
| `-scalebar <length> <step>` | Draw a distance scale bar of `<length>` subdivided by `<step>`. |
| `-vcopy <n>` / `-hcopy <n>` | Tile `<n>` vertical and/or horizontal copies of the map across the plotter sheet. |
| `-vspace <cm>` / `-hspace <cm>` | Vertical and horizontal spacing (cm) between tiled copies (default `30` cm). |
| `-small <factor>` | Scale map legend widgets (title, depth bar, illumination rose, logo) by `<factor>`. |

### Cartographic Widgets & Vector Overlays

| Option | Description |
|---|---|
| `-tit1 "<title1>"` / `-tit2 "<title2>"` | Primary and secondary title strings for the interactive Title Box widget (defaults to `header.label_1`). |
| `-illum <azi> <elev> <exag>` | Enable the 3D Sun-Illumination hemisphere widget displaying sun azimuth, elevation, and vertical exaggeration (auto-populated from `header.sun_*` if present). |
| `-depthbar <min> <max> <step>` | Enable the Depth Colorbar scale widget spanning `<min>` to `<max>` meters with labels every `<step>` meters. |
| `-custom <logofile>` | Load an OMG raster logo image into a movable Custom Logo widget. |
| `-vector <file> <color>` | Overlay an ASCII vector file in pen `<color>` (up to 10 files). |
| `-vectbin <file> <linecol> <labcol>` | Overlay a binary vector contour file (`bin_vect`) with line color `<linecol>` and label color `<labcol>`. |
| `-label <file> <color>` | Overlay positioned ASCII text labels in pen `<color>` (with `-fix_size <cm>` for symbol size). |
| `-verbose` | Enable verbose diagnostic output. |

---

## Interactive X11 Interface
Once the image and metadata are loaded, `scaleimage` opens a `650 x 650` main drawing canvas (`Versatec Plotting Editor`, representing an 86 cm wide plotter bed) with 7 top toolbar buttons (`EXIT`, `Print`, `24/10`, `12/20`, `8/30`, `grey`, `mcol`) and interactive sub-windows for dragging and positioning the **Illumination**, **Title**, **Depthbar**, and **Custom Logo** widgets prior to printing.
