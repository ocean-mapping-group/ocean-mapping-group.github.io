---
layout: default
title: map2GMTiles
parent: James Muggah — Global Mapper Tiles & Utils (james)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 5
tool_name: map2GMTiles
source_path: code/james/map2GMTiles.c
category: Raster Processing & Web Mapping (james)
input_formats:
- .r4
- .8bit
- .sun_*
output_formats:
- .header (OMG1 256x256 Spherical Mercator tile headers)
- stdout (tile header filenames)
related_tools:
- merged2GMTiles
- GoogleMapTileCreation
- GM_fillGap
- header
- remap
---

# map2GMTiles

## Description
`map2GMTiles` computes the Spherical Mercator (EPSG:900913 / EPSG:3857, Google Maps / OpenStreetMap standard $256\times 256$ pixel pyramid) tile indices `(tx, ty, zoomlevel)` that cover an input OMG raster mapsheet (`.r4`, `.8bit`, or `.sun_*`) or a user-specified geographic bounding box (`-n`, `-s`, `-e`, `-w`).

For every intersecting Google Map tile at the target `-zoomlevel` (default `14`), `map2GMTiles` prints `<tx>_<ty>_<zoomlevel>.header` to `stdout`. When `-output_header` is specified, it also creates the 1024-byte `OMG1` binary `.header` file on disk (`256 x 256` pixels, Mercator projection `projection = 1`, WGS84 `ellipsoid = 1`, with local latitude-scaled pixel size `res`) so OMG tools such as `weigh_grid`, `mos2`, or `remap` can grid or resample data directly into Google Map tiles.

---

## Usage

```bash
map2GMTiles [-v] [-fresh] [-output_header] [-dont_touch] [-zoomlevel <Z>] \
    [-n <north_lat> -s <south_lat> -w <west_lon> -e <east_lon>] \
    -in <filename.{r4,8bit}>
```

### Examples

**1. List all Zoom Level 14 Google Map tiles covering an `.r4` bathymetry mapsheet:**

```bash
map2GMTiles -zoomlevel 14 -in bay_bathy.r4
```

**2. Generate `256x256` OMG `.header` files for Zoom Level 12 without overwriting existing tile headers:**

```bash
map2GMTiles -zoomlevel 12 -output_header -dont_touch -in arctic_grid.r4
```

**3. Generate tile headers for an explicit geographic bounding box:**

```bash
map2GMTiles -zoomlevel 10 -output_header -n 75.0 -s 73.0 -w -110.0 -e -102.0 -in reference.r4
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | Input OMG raster file (`.r4`, `.8bit`, `.sun_*`) with a 1024-byte `JHC_header`. Supports Mercator (`projection = 1`), UTM (`projection = 2`), and Polar Stereographic (`projection = 10`). Rotated mapsheets (`4`, `5`, `11`) are rejected. | Required |
| `-zoomlevel <Z>` | Google Maps Spherical Mercator pyramid zoom level ($0 \le Z \le 20+$). | `14` |
| `-output_header` | Write `<tx>_<ty>_<zoomlevel>.header` files (`JHC_header`, `256x256` Mercator) in the current working directory. Without this flag, only prints the header filenames to `stdout`. | Disabled (report names only) |
| `-dont_touch` | When `-output_header` is enabled, skip creating `<tx>_<ty>_<zoomlevel>.header` if the file already exists on disk. | Overwrites existing headers |
| `-n <lat>` `-s <lat>` `-w <lon>` `-e <lon>` | Override the input file's geographic bounds with explicit North, South, West, and East limits (all 4 must be provided together; note internal West-positive OMG sign convention). | Derived from `-in` header |
| `-fresh` | Flag parsed for CLI compatibility with `merged2GMTiles`. | Disabled |
| `-v` | Verbose mode: prints geographic bounds, total number of tiles, and per-tile coordinate mappings. | Disabled |

---

## Spherical Mercator Tile Equations

`map2GMTiles` implements the standard Web Mercator (EPSG:900913 / EPSG:3857) spherical projection ($R = 6,378,137\text{ m}$, $\text{originShift} = \pi R = 20,037,508.342789244\text{ m}$, $\text{tileSize} = 256\text{ px}$):
1. **WGS84 $(\text{lat}, \text{lon}) \to \text{Meters }(m_x, m_y)$ (`LatLonToMetres`):**
   $$m_x = \frac{\text{lon}\cdot\text{originShift}}{180}, \qquad m_y = \ln\left(\tan\left(\frac{(90 + \text{lat})\pi}{360}\right)\right)\cdot\frac{\text{originShift}}{\pi}$$
2. **Resolution at Zoom Level $Z$ (`Resolution`):**
   $$\text{res}(Z) = \frac{2\pi R}{256 \cdot 2^Z}, \qquad \text{res}_{\text{lat}}(\phi, Z) = \frac{2\pi R \cos\phi}{256 \cdot 2^Z}$$
3. **Tile Indices $(t_x, t_y)$ (`MetresToTile` / `PixelsToTile`):**
   Converts $(m_x, m_y)$ to global pyramid pixel coordinates $(p_x, p_y)$ and flips $t_y$ from TMS (bottom-up) to Google Maps (top-down):
   $$t_y^{\text{GM}} = (2^Z - 1) - t_y^{\text{TMS}}$$
4. **Sanity Limit:**
   To guard against corrupted mapsheet headers, `map2GMTiles` only generates headers if the total tile count `numTiles = numTilesX * numTilesY < 45000`; otherwise it prints `---File: <inname> has bad bounds --------------`.
