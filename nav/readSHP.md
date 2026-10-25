---
layout: default
title: readSHP
parent: Navigation Tools
nav_order: 28
tool_name: readSHP
source_path: code/nav/readSHP.c
category: Navigation & Georeferencing
input_formats: [".shp", ".shx", ".dbf"]
output_formats: ["ASCII contour/segment (.asc, .ascii)", ".nav", ".seg"]
related_tools: ["navtoSHP", "iNav2SHP", "makeDBF", "jview", "sortCont"]
---

# readSHP

## Description
`readSHP` reads ESRI Shapefile geometry (`.shp`) and spatial index (`.shx`) files using the internal OMG Shapefile library (`code/subr/j_SHP.c`), prints header and record diagnostics to `stdout`, and optionally exports the vertex coordinates into OMG ASCII contour/polygon format (`lat lon 0.00` separated by `0.0 0.0 0.0` segment delimiters for overlay in `jview`) or binary OMG navigation format (`jcu_nav_rec`, via `-navbin`).

If the input Shapefile coordinates are projected in Universal Transverse Mercator (UTM) meters rather than geographic degrees, `readSHP` can unproject them on the fly to WGS84 latitude and longitude when given the UTM zone's central meridian (`-merid <deg>`) and hemisphere (`-Shemi` for Southern Hemisphere).

---

## Usage

```bash
readSHP [-v] [-navbin] [-merid <deg> [-Shemi]] [-separate] [-debug_index <N>] [-out <outfile_or_prefix>] <filename.shp>
```

### Common Workflow Examples

**1. Inspect the header, spatial bounds, and record structure of a Shapefile:**
```bash
readSHP coastlines/bay_of_fundy.shp
```

**2. Convert a geographic WGS84 Shapefile into a single OMG ASCII line/polygon overlay file for `jview`:**
```bash
readSHP -out bay_coastline.ascii coastlines/bay_of_fundy.shp
```

**3. Unproject a UTM Zone 19N (Central Meridian -69.0°) Shapefile into WGS84 ASCII segments:**
```bash
readSHP -merid -69.0 -out pipeline_route.ascii gis/pipeline_utm19n.shp
```

**4. Export each Shapefile record into its own numbered file (`prefix_0000.asc`, `prefix_0001.asc`, ...):**
```bash
readSHP -separate -outpolygons/lease_block gis/lease_blocks.shp
```

**5. Convert a Shapefile into a binary OMG `.nav` file (`jcu_nav_rec`):**
```bash
readSHP -navbin -out trackline.nav gis/vessel_track.shp
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<filename.shp>` | **Required.** Input Shapefile name (strips extension and opens `<base>.shp`, `<base>.shx`, and optionally checks for `<base>.dbf`). | None |
| `-out <filename>` | Output filename (or filename prefix when `-separate` is also specified). If omitted, `readSHP` only prints Shapefile diagnostics to `stdout`. | None (stdout only) |
| `-navbin` | Write output vertices as 48-byte binary `jcu_nav_rec` records instead of ASCII text. Sets `time = k` (point index within record) and `azi = velocity = flag[0..3] = 0`. | Disabled (ASCII output) |
| `-separate` | Instead of writing all shape records into a single output file, create a separate numbered file for each index record $i$: `<out>_0000.asc`, `<out>_0001.asc`, ... (or `<out>_0000.seg` when combined with `-navbin`). | Disabled (single file) |
| `-merid <deg>` | Input Shapefile coordinates are in UTM meters; convert $(E, N)$ to WGS84 $(\text{lat}, \text{lon})$ using `<deg>` as the UTM central meridian in decimal degrees (e.g., `-69.0` for UTM Zone 19, `133.0` for Zone 53). Hardwired to `Ellipsoid = 1` (WGS84). | Disabled (assumes input is already Lon/Lat) |
| `-Shemi` | Used with `-merid`: specifies that the UTM coordinates are in the **Southern Hemisphere** (`utmgeo(..., 's')`, false northing 10,000,000 m). | Northern Hemisphere (`'n'`) |
| `-debug_index <N>` | Only print detailed `print_shp_index_record` and `print_shp_record` vertex dumps for record index `<N>` (0-based), suppressing full dumps for all other records. | `-1` (print all records) |
| `-skip <sec>` | Parsed on the command line for CLI symmetry with `navtoSHP`. | `0` |
| `-v` | Increment verbose flag. | Disabled |

---

## Output Formats

### 1. ASCII Segment Format (Default)
In default ASCII mode, `readSHP` writes `lat lon 0.00` lines compatible with OMG contour/line plotting utilities (`jview`, `plot_cont`, `iNav2SHP -ascii`). Multi-part shapes and separate records are delimited by `0.0 0.0 0.0` (and `0.000 0.000 <part_index>` at the start of each part $j$):
```text
0.0 0.0 0.0
0.000 0.000 0
45.123456 -66.543210 0.00
45.124000 -66.542000 0.00
0.0 0.0 0.0
```

### 2. Binary `.nav` Format (`-navbin`)
When `-navbin` is specified, each vertex $k$ is written via `nav_write()` as a 48-byte `jcu_nav_rec`:
* `tide_rec.lat = sh_rec_cont.points[k].LE_Y`
* `tide_rec.lon = sh_rec_cont.points[k].LE_X`
* `tide_rec.time = k`, `tide_rec.centisecs = 0`, `azi = velocity = 0.0`, `flag[0..3] = 0`.
*(Note: If `-separate` is combined with `-navbin`, a leading/trailing `0.0 0.0 0.0\n` string is also written before/after the binary records in each `_%04d.seg` file).*
