---
layout: default
title: iNav2SHP
parent: Navigation Tools
nav_order: 22
tool_name: iNav2SHP
source_path: code/nav/iNav2SHP.c
category: Navigation & Georeferencing
input_formats: [".nav", "ASCII contour/XYZ", "OMG1 mapsheet (.blank, .r4)"]
output_formats: [".shp", ".shx", ".dbf", ".prj"]
related_tools: ["navtoSHP", "readSHP", "makeDBF", "appendNav", "sortCont"]
---

# iNav2SHP

## Description
`iNav2SHP` (authored by Ian Church, Sept 2009) converts binary OMG navigation files (`.nav`), ASCII contour/XYZ files (such as output from `sortCont`), or OMG1 mapsheet headers (`.blank`, `.r4`) into complete ESRI Shapefile datasets (`.shp`, `.shx`, `.dbf`, and WGS84 `.prj`) using Shapelib (`shapefil.h`).

Unlike the lightweight [`navtoSHP`](navtoSHP.md) utility (which only writes 2D polyline `.shp` and `.shx` files), `iNav2SHP` generates 3D `SHPT_*Z` geometries (`point`, `line`/`arc`, `polygon`, or `multipoint`), populates a matching dBASE `.dbf` attribute table (`PointName`, `Time`, `TimeZone`, `ContourLvl`, or `MapName`/`Resolution`), and writes a standard `GCS_WGS_1984` `.prj` projection file.

---

## Usage

```bash
# Convert a binary .nav file to a Shapefile
iNav2SHP [-v] [-skip <N>] -type <point|line|arc|polygon|multipoint> -out <shp_prefix> -in <navfile>

# Convert ASCII contour segments (from sortCont) to a Shapefile
iNav2SHP -ascii -type line -out <shp_prefix> -in <ascii_contour_file>

# Export OMG1 mapsheet bounding polygons to a Shapefile
iNav2SHP -out <shp_prefix> -map <map1.blank> [<map2.blank> ...]
```

### Common Workflow Examples

**1. Export a vessel trackline `.nav` file as a 3D polyline Shapefile (decimated by 10):**
```bash
iNav2SHP -skip 10 -type line -out tracks/JD100_line1 -in merged/JD100/0001_line.nav
```

**2. Export every 50th navigation fix as individual point features with UTC timestamps:**
```bash
iNav2SHP -skip 50 -type point -out tracks/JD100_fixes -in merged/JD100/0001_line.nav
```

**3. Convert `sortCont` ASCII bathy contours (`lat lon depth` separated by `0.0 0.0 0.0`) to a line Shapefile:**
```bash
iNav2SHP -ascii -type line -out contours/bathy_10m -in contours/bathy_10m.cont
```

**4. Create a polygon index Shapefile of all project mapsheet boundaries:**
```bash
iNav2SHP -out gis/project_mapsheets -map maps/*.blank
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | Input binary `.nav` file (default mode) or ASCII XYZ/contour file (when `-ascii` is set). Not required when `-map` is used. | None |
| `-out <prefix>` | **Required.** Output filename prefix for `<prefix>.shp`, `<prefix>.shx`, `<prefix>.dbf`, and `<prefix>.prj`. | None |
| `-type <geom>` | **Required** (unless `-map` is used, which forces `polygon`). Geometry type:<br>• `point` (`SHPT_POINTZ`)<br>• `line` or `arc` (`SHPT_ARCZ`)<br>• `polygon` (`SHPT_POLYGONZ`)<br>• `multipoint` (`SHPT_MULTIPOINTZ`) | None |
| `-skip <N>` | Read and export only every $N$-th record from the binary `.nav` file. | `0` (all records) |
| `-ascii` | Read an ASCII space-delimited file (`lat lon contourLevel`) where individual contour segments are separated by `0.0 0.0 0.0` lines (standard `sortCont` output). | Disabled (`.nav` mode) |
| `-map <files...>` | Read one or more OMG1 `JHC_header` mapsheet files (up to 10,000 files, e.g., `*.blank` or `*.r4`), unproject their four corners via `inv_proj()`, and write closed 5-vertex `SHPT_POLYGONZ` outlines. | Disabled |
| `-v` | Enable verbose status messages. | Disabled |

---

## Output Shapefile & DBF Schema

Every invocation generates four files (`<out>.shp`, `<out>.shx`, `<out>.dbf`, and `<out>.prj` with `GCS_WGS_1984`). The `.dbf` attribute schema depends on the operating mode:

### 1. Standard Binary `.nav` Mode
* **Coordinates:** $X = \text{lon}$, $Y = \text{lat}$, $Z = \text{azi}$.
* **DBF Fields:**
  * `PointName` (`FTString`, width 20): Vertex index `"0"`, `"1"`, ... for `point` mode, or `"One"` for single-object `line`/`arc`/`polygon`/`multipoint` modes.
  * `Time` (`FTString`, width 20): UTC timestamp string from `asctime(gmtime(&rawtime))` (per-point timestamp in `point` mode; start-of-line timestamp in `line`/`polygon`/`multipoint` modes).
  * `TimeZone` (`FTString`, width 20): `"UTC"`.

### 2. ASCII Contour / XYZ Mode (`-ascii`)
* **Coordinates:** Parses each line as `lat lon Z` (`sscanf(my_string, "%lf %lf %lf", &padfY[m], &padfX[m], &padfZ[m])`). Whenever `lat == 0.0` (`0.0 0.0 0.0` delimiter), flushes the accumulated vertices as a separate shape object; if no `0.0` delimiter is encountered in the entire file, writes a single shape object at EOF.
* **DBF Fields:**
  * `PointName` (`FTString`, width 20): Sequential segment number (`"1"`, `"2"`, ...).
  * `ContourLvl` (`FTString`, width 20): Elevation/depth string (`contour2`) from the 3rd column.

### 3. Mapsheet Boundary Mode (`-map`)
* **Coordinates:** Reads `JHC_header` from each file, calls `inv_proj()` at pixel corners `(0, 0)`, `(dx, 0)`, `(0, dy)`, and `(dx, dy)` to obtain `(UL, UR, LR, LL, UL)` closed polygon rings with $Z = 0$.
* **DBF Fields:**
  * `MapName` (`FTString`, width 20): Mapsheet filename with its extension stripped.
  * `Resolution` (`FTString`, width 20): Grid cell size `JHChead.xstep`.
