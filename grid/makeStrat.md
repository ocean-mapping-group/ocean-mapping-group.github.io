---
layout: default
title: makeStrat
parent: Grid Tools
tool_name: makeStrat
source_path: code/grid/makeStrat.c
category: gridding
input_formats: ["Multi-column ASCII cross-section profiles (X Y1 Y2 ... Yn)"]
output_formats: [".8bit (JHC 8-bit stratigraphic cross-section image)", "_00000.layer .. _NNNNN.layer (per-horizon step images)"]
related_tools: ["extractProfile", "plotProfile", "findHorizon"]
---

# makeStrat

## Overview

`makeStrat` generates a 2D 8-bit stratigraphic cross-section raster (`JHC_header`, `data_type = 1`) from a time-series of overlapping bathymetric profiles (`-profiles <file> -numlines <N>`). As each successive horizon $j = 0 \dots N-1$ is drawn from oldest to youngest, `makeStrat` erodes (wipes out) any older sediment above the current horizon and paints newly deposited sediment between the current horizon and underlying layers with a progressive greyscale value (`20 + j * grey_step`).

In addition to the final composite stratigraphic section (`-out <file>`), it outputs intermediate snapshot frames (`<out>_00000.layer`, `<out>_00001.layer`, ...) for every time step $j$ to animate bedform migration and stratigraphic preservation.

---

## Syntax & CLI Options

```bash
makeStrat -xlen <nx> -ylen <ny> [-Xmin <xmin> -Xmax <xmax>] (-Ymin <ymin> -Ymax <ymax> | -Yrange <dy>) [-grey_step <step>] -profiles <Xsect.prof> -numlines <N> -out <outfile>
```

| Option | Description | Default |
|---|---|---|
| `-xlen <pixels>` | **Required.** Horizontal width (`dx`) of the output 8-bit image in pixels. | None |
| `-ylen <pixels>` | **Required.** Vertical height (`dy`) of the output 8-bit image in pixels. | None |
| `-profiles <filename>` | **Required.** Input multi-column ASCII file where each row has an $X$ distance followed by `numlines` elevation values ($Y_0, Y_1, \dots, Y_{N-1}$). | None |
| `-numlines <N>` | **Required.** Number of profile horizons per $X$ sample (note: flag is `-numlines`, up to 100 horizons). | `0` |
| `-out <filename>` | **Required.** Output 8-bit `JHC_header` filename for the final stratigraphic section. | None |
| `-Xmin <val>` / `-Xmax <val>` | Horizontal coordinate bounds mapped to `[0, xlen]`. If omitted, automatically scans the input file for min/max $X$. | Auto-detect from file |
| `-Ymin <val>` / `-Ymax <val>` | Vertical depth/elevation bounds mapped to `[0, ylen]`. Required unless `-Yrange` is provided. | None |
| `-Yrange <val>` | If `-Ymin`/`-Ymax` are omitted, automatically centers a vertical window of height `<val>` around the mean non-zero elevation (`Ysum / Ycount +- Yrange/2`). | `0.0` |
| `-grey_step <val>` | Greyscale increment per depositional layer (`colour = 20 + j * grey_step`). | `10` |

---

## How It Works

1. **Profile Ingestion & Coordinate Scaling:**
   - Reads up to `50,000` along-section points (`Xvals[i]` and `Yvals[0..numlines-1][i]`).
   - Automatically determines `[Xmin, Xmax]` and/or `[Ymin, Ymax]` (via `-Yrange`) if not explicitly set on the command line.
   - Scales all $(X, Y)$ coordinates into integer pixel indices `0..xlen-1` and `0..ylen-1`.
2. **Horizon Rasterization & Erosion/Deposition Simulation:**
   - For each horizon $j = 0 \dots \text{numlines}-1$:
     - Draws a continuous 1-pixel-thick horizon trace (`DN = 255`) across `image_1` using linear pixel interpolation between consecutive profile vertices.
     - For each column `i = 0..xlen-1` containing the horizon:
       - **Erosion:** Scans downward from the top of the image (`k = 0`) until hitting the new horizon (`DN == 255`), setting all overlying pixels to `0` (water column / eroded material) and marking the horizon interface as `254`.
       - **Deposition:** Continues scanning downward below the horizon while pixels are `0` (unfilled space above older preserved horizons) and fills them with layer age color `20 + j * grey_step`.
     - Writes intermediate frame `<outname>_<05d>.layer` as an 8-bit `JHC_header` image.
3. **Final Output:** Writes the completed stratigraphic cross-section to `<outname>`.

---

## Examples

**Generate a 12-horizon synthetic stratigraphy animation and composite image from repetitive dune profiles:**
```bash
makeStrat \
    -xlen 1000 -ylen 400 \
    -Yrange 15.0 \
    -grey_step 15 \
    -profiles dune_migration_12lines.prof \
    -numlines 12 \
    -out dune_strat.8bit
```

---

## Workflow Context

- **Upstream:** Multi-epoch profile tables extracted along a repeat survey line using [`extractProfile`](extractProfile.md).
- **Downstream:** View `<out>` and `<out>_*.layer` in `jview` or convert to animations showing dune/bedform foreset preservation and erosion bounding surfaces.
