---
layout: default
title: GoogleMapTileCreation
parent: James Muggah (james) Tools
nav_order: 2
tool_name: GoogleMapTileCreation
source_path: code/james/GoogleMapTileCreation.c
category: Raster Processing & Web Mapping (james)
input_formats: [".sun_315 / .r4 / .8bit (basemap)", ".nav / .decnav", ".r4 (mapsheets)", ".txt (ASCII lat/lon)"]
output_formats: [".txt (pixel coordinate index)"]
related_tools: ["map2GMTiles", "merged2GMTiles", "GM_fillGap"]
---

# GoogleMapTileCreation

## Description
`GoogleMapTileCreation` projects geographic coordinates from one of three input sources—binary navigation files (`-nav`), OMG raster mapsheet bounding corners (`-map`), or ASCII latitude/longitude lists (`-ascii`)—into pixel coordinates `(x, y)` on a reference OMG basemap (`-basemap`). Output records are appended (`fopen(outname, "a")`) to the specified output text file (`-out`).

When used in the OMG Google Maps tile generation pipeline with `-nav <file>.decnav`, `GoogleMapTileCreation` decodes decimated navigation fixes at a configurable time interval (`-skip`, default 3600 seconds), projects each fix onto the basemap grid, and automatically rewrites the file path from `/decnav/<line>.decnav` to `/merged/<line>.merged`, appending `<x_px> <y_px> <merged_path>` to the output index file.

---

## Usage

```bash
GoogleMapTileCreation [-v] [-keep_out] -basemap <basemap_file> \
    [-nav <infile.nav> [-skip <sec>]] \
    [-map <map1.r4 ...> [-repeat_ul] [-name]] \
    [-ascii <infile.txt>] \
    -out <output.txt>
```

### Examples

**1. Index which basemap pixels are crossed by a `.decnav` file and map back to `.merged` path:**
```bash
GoogleMapTileCreation -basemap arctic_overview.sun_315 \
    -nav /survey/decnav/2010/line001.decnav -skip 600 \
    -out pixel_merged_index.txt
```

**2. Output the 4 (or 5 closed-polygon) pixel corners of `.r4` mapsheets on a basemap:**
```bash
GoogleMapTileCreation -basemap arctic_overview.sun_315 \
    -map sheet1.r4 sheet2.r4 -repeat_ul -name \
    -out sheet_outlines_px.txt
```

**3. Project an ASCII list of `<lat> <lon>` points onto basemap pixel coordinates:**
```bash
GoogleMapTileCreation -basemap bay.sun_315 -ascii waypoints.txt -out waypoints_px.txt
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-basemap <file>` | Reference OMG mapsheet (`.sun_315`, `.r4`, `.8bit`) whose `JHC_header` defines the target projection, ellipsoid, and pixel dimensions (`dx`, `dy`). | Required |
| `-out <output.txt>` | Output ASCII file (opened in **append** mode `"a"`). | Required |
| `-nav <infile.nav>` | Input binary navigation file (`jcu_nav_rec`, 48 bytes/record). Automatically substitutes `.decnav` (or any extension) with `.merged` and replaces `/decnav/` with `/merged/` in the third output column. | None |
| `-skip <sec>` | Minimum time interval in seconds between consecutive navigation records processed in `-nav` mode (`nav_record.time - old_time >= skip`). | `3600` |
| `-map <file1 ...>` | One or more OMG mapsheet files (up to 1,000 files). Projects the 4 corners `(0,0)`, `(0,dy)`, `(dx,dy)`, `(dx,0)` of each map onto `-basemap` pixel coordinates. | None |
| `-repeat_ul` | Used with `-map`: repeats the upper-left corner `(0,0)` as a 5th vertex to close the polygon box on each output line. | Disabled |
| `-name` | Used with `-map`: prefixes each output line with the mapsheet filename. | Disabled |
| `-ascii <infile.txt>` | Input whitespace-delimited ASCII file with `<latitude> <longitude>` (decimal degrees) per line. | None |
| `-keep_out` | Keep points whose projected pixel coordinates fall outside `[0..dx, 0..dy]` of the basemap (`reject_out_of_bounds = 0`). | Rejects out-of-bounds |
| `-v` | Verbose output: prints `<lat> <lon> --> <x> <y>` for every projected coordinate. | Disabled |

---

## Output Formats

* **`-nav` mode:** Appends one line per accepted nav fix:
  ```text
  <x_pixel> <y_pixel> <path_with_/merged/_and_.merged>
  ```
* **`-map` mode:** Appends one line per mapsheet containing the 4 (or 5 with `-repeat_ul`) projected corner pixel coordinate pairs:
  ```text
  [<map_filename>] <x_ul> <y_ul> <x_ll> <y_ll> <x_lr> <y_lr> <x_ur> <y_ur> [<x_ul> <y_ul>]
  ```
* **`-ascii` mode:** Appends one line per input coordinate pair:
  ```text
  <x_pixel> <y_pixel>
  ```
