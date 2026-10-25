---
layout: default
title: embedNav
parent: Navigation Tools
nav_order: 17
tool_name: embedNav
source_path: code/nav/embedNav.c
category: Navigation & Georeferencing
input_formats: [".nav (jcu_nav_rec binary)", "ASCII text (lat lon label with -ascii)", "8-bit OMG1 mapsheet (.byte / JHC_header data_type == 1)"]
output_formats: ["8-bit OMG1 mapsheet (modified in-place)"]
related_tools: ["appendNav", "stripNav", "dohypackLNW", "jview"]
---

# embedNav

## Description
`embedNav` rasterizes ("burns") navigation tracklines or fix symbols from up to 50,000 binary OMG `.nav` files (or 3-column `lat lon string` ASCII files when `-ascii` is specified) directly into the pixel array of an existing **8-bit OMG1 mapsheet file** (`header.data_type == 1`), modifying the mapsheet in-place.

It supports plotting every fix along a trackline with configurable pixel thickness (`-linethick 0|1|2`), or plotting a single symbol (crosshair, dot, or box) at the center fix (`numvec / 2`) of each binary `.nav` file (`-cenfix`, `-cendot`, `-cenbox`)—or at every point of an `-ascii` file.

---

## Usage

```bash
embedNav [OPTIONS] -into <8bit_mapsheet_file> <nav_or_ascii_file(s)>
```

### Common Workflow Examples

**1. Burn binary `.nav` tracklines (3 pixels wide, white = 255) into an 8-bit sun-illuminated mapsheet:**
```bash
embedNav -col 255 -linethick 1 -into shade.byte decnav/JD100/*.decnav
```

**2. Plot a center-of-line crosshair symbol (with automatic contrasting box outline) for each `.nav` file:**
```bash
embedNav -cenfix -col 255 -into coverage.byte decnav/JD100/*.decnav
```

**3. Plot box symbols at geographic coordinates listed in an ASCII `lat lon label` file:**
```bash
embedNav -ascii -cenbox -col 0 -linelength 2 -into shade.byte stations.txt
```

**4. Plot symbols at direct pixel `(x, y)` coordinates from an ASCII file:**
```bash
embedNav -ascii -pixel_coords -cendot -col 255 -into shade.byte pixel_picks.txt
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-into <8bitmapsheetfile>` | **Required.** Target 8-bit OMG1 mapsheet file (`JHC_header` with `data_type == 1`). **Modified in-place.** | None |
| `<binnavfile(s)>` | **Required.** One or more binary `.nav` files (or 3-column ASCII files if `-ascii` is set; up to 50,000 files). | None |
| `-col <0..255>` | 8-bit grayscale/palette color value used to draw tracks or symbols. When `col` is `255` or `0` in crosshair mode (`-cenfix` or default `-ascii`), a contrasting border box is automatically drawn in `0` or `255`. | `255` |
| `-linethick <0\|1\|2>` | Pixel thickness (`raster_line_width`): `0` = 1 pixel wide, `1` = 5-pixel plus-sign neighborhood (3 px wide), `2` = 13-pixel diamond/circle neighborhood (5 px wide). Also controls `do_raster_line` thickness. | `0` (1 px) |
| `-linelength <px>` | Extra pixel radius added to box (`-cenbox`) and crosshair (`-cenfix`) symbols (`raster_line_length`). | `0` |
| `-cenfix` | For binary `.nav` files, draw a crosshair symbol (plus a contrasting outline box if `col == 0` or `255`) at the midpoint record (`numvec / 2`) of each file. | Disabled |
| `-cendot` | Draw a single 1-pixel dot (`col`) at the midpoint of each binary `.nav` file (and suppress full trackline drawing), or at each point in `-ascii` mode. Implies `-cenfix`. | Disabled |
| `-cenbox` | Draw a square box symbol (`col`) around the midpoint of each binary `.nav` file (and suppress full trackline drawing), or around each point in `-ascii` mode. Implies `-cenfix`. | Disabled |
| `-ascii` | Read 3-column ASCII files (`lat lon label_string`) instead of binary `jcu_nav_rec` files, drawing a symbol (crosshair by default, or `-cendot` / `-cenbox`) at every point. | Disabled (binary `.nav`) |
| `-pixel_coords` | Used with `-ascii`. Treat the first two columns of the ASCII file directly as mapsheet pixel coordinates `(x, y)` instead of projecting `(lon, lat)` via `Project()`. | Disabled |
| `-jraster` | Increments internal `jraster` flag. | Disabled |
| `-low <val>` / `-high <val>` | Parsed on the command line (`low_limit`, `high_limit`). | Unused |
| `-v` | Enable verbose output (prints projected pixel coordinates for every embedded binary `.nav` fix). | Disabled |

---

## How It Works

1. **Mapsheet Validation & Loading:**
   Opens the target `-into` mapsheet in `"r+"` mode, reads its `JHC_header`, and verifies `header.data_type == 1` (exits with `mapfile isnt an 8bit file !!` otherwise). Allocates `dx * dy` bytes (`cbuf`) and reads the entire 8-bit raster into memory.
2. **Coordinate Projection (`Project`):**
   Uses the mapsheet's projection and ellipsoid (`Ellipsoid = header.ellipsoid`) to convert each fix's `(lon, lat)` into pixel coordinates `(x1, y1)`.
3. **Symbol & Track Rendering:**
   * **ASCII Mode (`-ascii`):** Reads `%lf %lf %s` tuples and draws a dot (`-cendot`), box (`-cenbox`), or crosshair (`do_raster_line`) at every in-bounds coordinate.
   * **Binary `.nav` Mode:**
     * If `-cenfix` (or `-cendot` / `-cenbox`) is enabled, seeks to the middle record (`numvec / 2`) and renders the requested symbol if it lies within `[5, dx-5]` and `[5, dy-5]`.
     * Unless `-cendot` or `-cenbox` is set, loops over all `novects` records in the `.nav` file and stamps the pixel (and its 4 or 12 neighbors for `-linethick 1` or `2`) into `cbuf`.
4. **In-Place Writeback:**
   Seeks to `JHC_OMG_RECLEN` (immediately after the mapsheet header) and writes the updated `dx * dy` byte buffer back to the file.
