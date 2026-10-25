---
layout: default
title: shputils
parent: Shapelib GIS Library & Tools (shapelib-1.3.0a2)
nav_order: 14
tool_name: shputils
source_path: code/shapelib-1.3.0a2/shputils.c
category: GIS & ESRI Shapefile Library / Tools
input_formats: [".shp", ".shx", ".dbf (ESRI Shapefile + xBase table)"]
output_formats: [".shp", ".shx", ".dbf (Merged, filtered, clipped, or transformed Shapefile)"]
related_tools: ["shpdump", "dbfdump", "shpopen", "dbfopen", "shprewind"]
---

# shputils

## Overview

`shputils` (`code/shapelib-1.3.0a2/shputils.c`, 1,226 lines) is a multi-purpose command-line GIS processing tool authored by Bill Miller (North Carolina Department of Transportation, 1997–2000) and integrated into Shapelib by Frank Warmerdam.

Unlike the single-purpose utilities (`shpdump`, `dbfdump`, `shpadd`, `dbfadd`), `shputils` operates simultaneously on both the geometry (`.shp`/`.shx`) and attribute (`.dbf`) files in a single pass. It can:
1. **Describe** the schema, coordinate bounds, and unique/min/max attribute values of a shapefile (`shputils <in.shp> [LIST|ALL]`).
2. **Append / Merge** an input shapefile into a new or existing output shapefile, automatically matching and merging `.dbf` attribute columns (`mergefields()`).
3. **Select / Unselect** subset features matching a comma-separated list of integer attribute values (`SELECT` / `UNSEL`).
4. **Clip / Erase** features against a rectangular coordinate box or another shapefile's bounding box (`CLIP` / `ERASE` with `TOUCH`, `INSIDE`, or `CUT` predicates).
5. **Rescale Units (`FACTOR`)** between `CM`, `METERS`, `KM`, `INCHES`, `FEET`, `YARDS`, `MILES`, or a custom numeric multiplier.
6. **Translate Coordinates (`SHIFT`)** by an additive $(\Delta X, \Delta Y)$ offset.

---

## Usage

```bash
# Mode 1: Describe shapefile bounds, DBF schema, and item value summaries
shputils <DescribeShape.shp> [LIST | ALL]

# Mode 2: Copy, append, filter, clip/erase, rescale, or shift a shapefile
shputils <InputShape.shp> <OutShape|AppendShape.shp> \
    [FACTOR <in_unit> <out_unit|numeric_factor>] \
    [SHIFT <xshift> <yshift>] \
    [SELECT|UNSEL <field_name> <val1,val2,...>] \
    [CLIP|ERASE <xmin> <ymin> <xmax> <ymax> <TOUCH|INSIDE|CUT>] \
    [CLIP|ERASE <clip_theme.shp> BOUNDARY <TOUCH|INSIDE|CUT>]
```

---

## Command-Line Operations & Modifiers

All operation keywords are matched case-insensitively via `strncasecmp2()`:

| Operation Keyword | Arguments | Description |
| :--- | :--- | :--- |
| *(Describe Mode)* | `<in.shp> [LIST\|ALL]` | Prints `Input Bounds`, entity count, and a table of all `.dbf` fields (`Name`, `Type`, `Len`, `Dec`). If `LIST` or `ALL` is passed, scans the records (up to 5,000 records by default, or unlimited with `ALL`) and prints `Min`/`Max` range or unique value lists (`showitems()`). |
| `SELECT` / `UNSEL` | `<Item> <valuelist>` | Filters features by integer values of `.dbf` column `<Item>` (e.g., `SELECT countycode 3,5,9,13`). `SELECT` writes only matching records; `UNSEL` writes all records **except** matching records (up to 150 comma-separated values in `selectvalues[150]`). |
| `CLIP` / `ERASE` (Box) | `<xmin> <ymin> <xmax> <ymax> <TOUCH\|INSIDE\|CUT>` | Clips (`CLIP`, retains inside) or erases (`ERASE`, retains outside) features against `[xmin, ymin, xmax, ymax]`. |
| `CLIP` / `ERASE` (Theme) | `<theme.shp> BOUNDARY <TOUCH\|INSIDE\|CUT>` | Extracts the bounding box of `<theme.shp>` (`SHPGetInfo`) and uses it as the clip/erase envelope (`ibound = TRUE`). |
| `FACTOR` | `<in_unit> <out_unit\|factor>` | Multiplies all $(X, Y)$ vertex coordinates by a conversion factor (`ifactor`). Supported unit names (`findunit()`): `CM`/`CENTIMETERS` (`39.37`), `METER`/`METERS` (`3937`), `KM`/`KILOMETERS` (`3937000`), `INCH`/`INCHES` (`100`), `FEET`/`FOOT` (`1200`), `YARD`/`YARDS` (`3600`), `MILE`/`MILES` (`6336000`), or a direct numeric factor for `<out_unit>`. |
| `SHIFT` | `<xshift> <yshift>` | Adds `<xshift>` to every $X$ coordinate and `<yshift>` to every $Y$ coordinate **after** any `CLIP`/`ERASE` and **after** any `FACTOR` unit scaling. |

### Spatial Predicates for `CLIP` and `ERASE` (`clip_boundary()`)

- **`INSIDE`**: A feature is considered inside only if **all** of its vertices fall within `[cxmin..cxmax, cymin..cymax]`.
- **`TOUCH`**: A feature is considered touching if **at least one** vertex falls within the clip boundary.
- **`CUT`**: Removes individual vertices outside the clip box in-place (`psCShape->nVertices = i2`), skipping the record if fewer than 2 vertices remain (note in source: line-box intersection insertion is unimplemented).

---

## Example Workflows

```bash
# 1. Inspect schema and value ranges of a shapefile
shputils survey_lines.shp ALL

# 2. Extract survey lines for Julian Day 100 and 101, convert Meters to Feet, and shift X/Y
shputils survey_lines.shp jd100_101_ft.shp \
    SELECT JULIAN_DAY 100,101 \
    FACTOR METERS FEET \
    SHIFT 500000.0 0.0

# 3. Clip a regional shapefile to the bounding box of a local survey shapefile
shputils regional_coast.shp local_coast.shp \
    CLIP survey_bounds.shp BOUNDARY TOUCH
```
