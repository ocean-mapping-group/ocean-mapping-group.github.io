---
layout: default
title: merged2GMTiles
parent: James Muggah (james) Tools
nav_order: 6
tool_name: merged2GMTiles
source_path: code/james/merged2GMTiles.c
category: Raster Processing & Web Mapping (james)
input_formats: [".merged", ".file_bounds"]
output_formats: [".header (OMG1 256x256 Spherical Mercator tile headers)", "stdout (tile header filenames)"]
related_tools: ["map2GMTiles", "getBounds", "checkBounds", "weigh_grid"]
---

# merged2GMTiles

## Description
`merged2GMTiles` reads the spatial bounding box of an OMG-HDCS `.merged` multibeam file (along with its `<prefix>.file_bounds` sidecar created by [`getBounds`](../omg/getBounds.md)), computes all intersecting $256\times 256$ Spherical Mercator (EPSG:900913 / Google Maps) pyramid tiles at the specified `-zoomlevel` (default `14`), and prints their `<tx>_<ty>_<zoomlevel>.header` names to `stdout`.

When `-output_header` is specified, `merged2GMTiles` also writes each 1024-byte `OMG1` binary `.header` file (`dx = 256`, `dy = 256`, Mercator projection `1`, WGS84 ellipsoid `1`) so that [`weigh_grid`](../gridding/weigh_grid.md) or [`mos2`](../sidescan/mos2.md) can directly grid multibeam bathymetry and backscatter into Google Map web tiles.

---

## Usage

```bash
merged2GMTiles [-v] [-fresh] [-output_header] [-dont_touch] [-zoomlevel <Z>] \
    [-n <north> -s <south> -w <west> -e <east>] \
    -in <filename.merged>
```

### Examples

**1. Ensure `.file_bounds` exists and generate Zoom Level 14 `.header` files for a `.merged` line:**
```bash
getBounds merged/JD200/0005_line.merged
merged2GMTiles -zoomlevel 14 -output_header -dont_touch -in merged/JD200/0005_line.merged
```

**2. Print intersecting tile names at Zoom Level 16 without creating `.header` files:**
```bash
merged2GMTiles -zoomlevel 16 -in merged/JD200/0005_line.merged
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <filename.merged>` | Input OMG-HDCS `.merged` file. Requires `<prefix>.file_bounds` (created by `getBounds`) in the same directory. | Required |
| `-zoomlevel <Z>` | Spherical Mercator (Google Maps) zoom level ($0 \le Z \le 20+$). | `14` |
| `-output_header` | Write 1024-byte `OMG1` `.header` files (`<tx>_<ty>_<zoomlevel>.header`) to the current directory. | Disabled (prints names to `stdout` only) |
| `-dont_touch` | Do not overwrite `<tx>_<ty>_<zoomlevel>.header` files that already exist on disk. | Overwrites existing headers |
| `-n <lat>` `-s <lat>` `-w <lon>` `-e <lon>` | Optional project area cutoff parameters. | `[-90..90, -180..180]` |
| `-fresh` | Flag parsed for CLI compatibility. | Disabled |
| `-v` | Verbose mode: prints summary header bounds, `.file_bounds` coordinates and timespan, total number of tiles, and per-tile bounds. | Disabled |

---

## How It Works

1. **Summary & `.file_bounds` Extraction:**
   Opens `<prefix>.merged` and reads `OMG_HDCS_summary_header`. Then opens `<prefix>.file_bounds` (exiting with an error if missing), reads record `0` via `OMG_HDCS_read_bounds`, and calls `OMG_HDCS_interp_bounds(&bounds, summary)` to obtain `minLat`, `maxLat`, `minLon`, `maxLon`.
2. **Spherical Mercator Tile Range Calculation:**
   Projects `(minLat, minLon)` and `(maxLat, maxLon)` to EPSG:900913 meters (`LatLonToMetres`) and computes the bounding tile indices `pxtoTiles` and `pxtoTilesMAX` at `zoomlevel`.
3. **45,000-Tile Safety Guard:**
   Computes `numTiles = (pxtoTiles.ty + 1 - pxtoTilesMAX.ty) * (pxtoTilesMAX.tx + 1 - pxtoTiles.tx)`. If `numTiles >= 45000` (indicating uncleaned navigation spikes in `.file_bounds`), aborts tile creation and prints:
   ```text
   ---File: <filename.merged> has bad bounds --------------
   ```
4. **Header Emission:**
   For each tile `(l, k)` in the bounding range, computes exact WGS84 tile bounds (`TileLatLonBounds`), mid-latitude Mercator pixel scale `res = initialResolution * cos(projection_latitude * pi/180) / exp2(zoomlevel)`, and writes `<l>_<k>_<zoomlevel>.header` ( converting longitude bounds to OMG's West-positive convention `ymax = -mins[1]`, `ymin = -maxs[1]`, `proj_merid = -projection_latitude`).
