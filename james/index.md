---
layout: default
title: James Muggah (james) Tools
nav_order: 24
has_children: true
---

# James Muggah (`james`) Tools

Utilities developed by James Muggah and John Hughes Clarke (`code/james/`) for web-mapping tile generation (Spherical Mercator EPSG:900913 / Google Maps pyramid tiles), raster gap interpolation, Lowrance recreational sonar (`.sl2`) conversion to OMG-HDCS, CARIS HIPS compatibility export, and batch survey line heading extraction.

---

## Tool Categories

### 1. Google Maps / Spherical Mercator Tile Pyramid Generation
* [`map2GMTiles`](map2GMTiles.md) — Computes Spherical Mercator (EPSG:900913 / EPSG:3857) $256\times 256$ pixel tile coordinates (`<tx>_<ty>_<zoom>.header`) covering an input `.r4` or `.8bit` mapsheet (Mercator, UTM, or Polar Stereographic) at a specified zoom level (`-zoomlevel`, default 14) and optionally writes OMG1 `.header` files.
* [`merged2GMTiles`](merged2GMTiles.md) — Computes Spherical Mercator (EPSG:900913) $256\times 256$ tile coordinates (`<tx>_<ty>_<zoom>.header`) covering the `.file_bounds` extent of an OMG-HDCS `.merged` swath file and optionally writes OMG1 `.header` files.
* [`GoogleMapTileCreation`](GoogleMapTileCreation.md) — Projects `.nav` tracklines (mapping `/decnav/*.decnav` to `/merged/*.merged`), `.r4` mapsheet corner polygons, or ASCII `(lat, lon)` coordinate lists onto a reference basemap grid (`-basemap`) to index which basemap pixels/tiles intersect survey data.
* [`GM_fillGap`](GM_fillGap.md) — Fills 1- to 3-pixel internal seams/gaps and left/right boundary edge gaps (`-edgeit`) in `.r4` floating-point grids or `.8bit` raster mapsheets created when adjacent Google Map tile or patch arrays abut.

### 2. Format Conversion & Hydrographic Utilities
* [`lowrance2omg`](lowrance2omg.md) — Converts Lowrance `.sl2` consumer/recreational singlebeam/downscan sonar logs into OMG-HDCS `.merged` + `.merged.ss_data` water-column traces, binary `.nav`, raw 1600-sample `.trc`, and ASCII `.llz` soundings.
* [`omg2hips`](omg2hips.md) — Converts a modern OMG-HDCS `.merged` file into a legacy HDCS summary header layout (`OMG_HDCS_dump_summary_hips`) compatible with CARIS HIPS import, setting zero-depth beams to status `22`.
* [`getHeading`](getHeading.md) — Computes the vector-averaged vessel heading ($\text{atan2}(\sum\sin\theta, \sum\cos\theta)$ in degrees $[0^\circ, 360^\circ)$) for one or more `.merged` files (or an `-xyzlist`) and writes a two-column `<filename> <heading>` table.
