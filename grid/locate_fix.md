---
layout: default
title: locate_fix
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: locate_fix
source_path: code/grid/locate_fix.c
category: gridding
input_formats:
- JHC_header mapsheet (.r4 / .8bit / .blank)
- ASCII lat lon depth (or pixX pixY depth)
output_formats:
- .gridvals (ASCII pixX pixY depth or lat lon depth)
- stdout interactive coordinates
related_tools:
- convertutm
- utm
- testutm
- make_blank
- edhead
---

# locate_fix

## Overview

`locate_fix` converts coordinates between geographic coordinates (`lat`, `lon`) and pixel coordinates (`pixX`, `pixY`) on an existing OMG `JHC_header` mapsheet (`-map <file>`). It can run **interactively** (prompting for coordinates on `stdin`) or in **batch file mode** (`-in <datafile>`, writing converted 3-column records to `<datafile>.gridvals`).

---

## Syntax & CLI Options

```bash
locate_fix [OPTIONS] -map <area.base> [-in <datafile>]
```

| Option | Description | Default |
|---|---|---|
| `-map <filename>` | **Required.** Existing OMG `JHC_header` file (`.r4`, `.8bit`, `.blank`, `.mos`) defining the projection, ellipsoid, bounds, and resolution (`xstep`, `ystep`). | None |
| `-geo2pix` | Convert geographic coordinates (`lat`, `lon`) to grid pixel coordinates (`pixX`, `pixY`) using `Project()`. | Default (`geo2pix = 1`) |
| `-pix2geo` | Convert grid pixel coordinates (`pixX`, `pixY`) to geographic coordinates (`lat`, `lon`) and projected `northing`/`easting` using `inv_proj()`. | Disabled |
| `-decdeg` | In interactive `-geo2pix` mode, prompt for decimal degrees (`lat lon`) instead of degrees and decimal minutes (`latdeg min londeg min`). (Note: batch `-in` mode always reads decimal degrees). | Disabled (`deg min` in interactive mode) |
| `-in <filename>` | Batch mode: read 3-column ASCII records (`lat lon depth` for `-geo2pix`, or `pixX pixY depth` for `-pix2geo`) from `<filename>` and write converted records to `<filename>.gridvals`. | Interactive `stdin` mode |
| `-skip <N>` | In batch `-in` mode, decimate output by writing only every `N`-th valid point (`in % skip == 0`). | `1` (write all) |
| `-flip_depth` | Negate the 3rd column (`-rdepth`) when writing `<filename>.gridvals`. | Disabled |
| `-v` | Enable verbose output of every coordinate transformation. | Disabled |

---

## How It Works

1. **Header Inspection:** Opens `-map` and reads its 1024-byte `JHC_header` (`get_print_JHC_header`), supporting all OMG projections (Mercator, UTM, Unprojected Geographic, Rotated UTM, Rotated Mercator, Lambert).
2. **Interactive Mode (when `-in` is omitted):**
   - Prompts the user for `latdeg min, londeg min` (or `lat lon` if `-decdeg` is set, or `pixX pixY` if `-pix2geo` is set).
   - Calls `Project(lon, lat, &x, &y, &header)` or `inv_proj(x, y, &lon, &lat, &easting, &northing, &header)` and prints the result alongside the grid resolution (`mpp`). Repeats while the user answers `y`.
3. **Batch File Mode (`-in <filename>`):**
   - Reads triples (`%lf %lf %f`) from `<filename>`.
   - In `-geo2pix` mode, projects `(lon, lat)` to `(x, y)` and filters out points falling outside the mapsheet (`0 <= x < dx` and `0 <= y < dy`).
   - Writes `x y depth` (or `lat lon depth` in `-pix2geo` mode) to `<filename>.gridvals`.

---

## Examples

**1. Interactive decimal-degree to pixel lookup on a mapsheet:**

```bash
locate_fix -map survey_area.r4 -decdeg
```

**2. Batch-convert an ASCII `lat lon depth` file into pixel coordinates within `survey_area.r4`:**

```bash
locate_fix -map survey_area.r4 -geo2pix -in cores.llz
# Writes cores.llz.gridvals
```

**3. Batch-convert pixel picks (`pixX pixY z`) back into geographic `lat lon z`:**

```bash
locate_fix -map survey_area.r4 -pix2geo -in picked_features.xy
# Writes picked_features.xy.gridvals
```

---

## Workflow Context

- Useful for locating core stations, acoustic targets, or profile endpoints in pixel space on an OMG `.r4` or `.8bit` grid, or converting pixel coordinates picked in an image viewer back to `lat`/`lon`.
