---
layout: default
title: testutm
parent: Grid Tools
tool_name: testutm
source_path: code/grid/testutm.c
category: gridding
input_formats: ["Interactive stdin Coordinates"]
output_formats: ["stdout Projected / Geographic Coordinates"]
related_tools: ["convertutm", "project", "locate_fix"]
---

# testutm

## Overview

`testutm` is an interactive command-line calculator for testing forward (geographic to grid) and inverse (grid to geographic) coordinate transformations across the three standard OMG projections—**UTM**, **New Brunswick Double Stereographic (`nbstereo`)**, and **Mercator**—and six reference ellipsoids (`WGS84`, `NAD27`, `CLK66`, `AGD84`, `Sphere`, `ATS77`).

---

## Syntax & CLI Options

```
testutm
```

All projection parameters and coordinate pairs are prompted interactively from `stdin`.

---

## How It Works

1. **Interactive Configuration**:
   - Prompts for the map projection:
     - `1`: **UTM** (`geoutm` / `utmgeo`, requires central meridian `merid`).
     - `2`: **New Brunswick Stereographic** (`nbstereo_init`, `nbstereo` / `nbstereo_inv`).
     - `3`: **Mercator** (`merc_init`, `mercator` / `inv_merc`; prompts for `scale`, `proj_lat`, `origin_lat`, and `origin_lon`).
   - Prompts for input angle format: `0` for `degrees minutes` or `1` for `decimal degrees`.
   - Prompts for the reference ellipsoid:
     - `(1) WGS84`, `(2) NAD27`, `(3) CLK66`, `(4) AGD84`, `(5) Sphere`, `(6) ATS77`.
2. **Continuous Conversion Loop**:
   - Repeatedly prompts whether to convert **Geo to Grid (`1`)** or **Grid to Geo (`2`)**, reads the input coordinates from `stdin`, executes the selected forward or inverse projection routine, and prints the resulting coordinates to `stdout`.

---

## Examples

### Run the interactive coordinate transformation calculator
```bash
testutm
```
Example interactive session (WGS84 UTM forward conversion at central meridian -69°):
```text
 UTM (1) or NB stereo (2) or Merc (3)?
1
  degrees and minutes (0) or decimal degrees (1) ?
1
 which ellipsoid (1) WGS84 (2) NAD27 (3) CLK66 (4) AGD84 (5) Sphere (6) ATS77 
1
 Geo to UTM (1) or UTM to Geo (2) ?
1
 input lat (decdeg)  lon  (decdeg) merid 
45.25 -66.05 -69.0
```

---

## Workflow Context

- **Batch Counterparts**: [`convertutm`](convertutm.html) (batch file conversion between Lat/Lon, UTM, and NB Stereographic) and [`project`](project.html) (batch Mercator projection).
