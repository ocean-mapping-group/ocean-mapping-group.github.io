---
layout: default
title: Sbat2OMG
parent: Reson SeaBat 9001/8101 Legacy (Sbat)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 4
tool_name: Sbat2OMG
source_path: Sbat/Sbat2OMG.c
category: format_conversion
input_formats:
- HUFF_SEABAT_ASCII
output_formats:
- OMG_HDCS
related_tools:
- RESON2OMG
- 8101toOMG
- GSF9002toOMG
---

# Sbat2OMG

## Overview

`Sbat2OMG` converts 60-beam Reson SeaBat 9001 multibeam bathymetry stored in Lloyd Huff's ASCII format (with UTM Easting/Northing coordinates referenced to central meridian -69.0°W) into OMG HDCS v1 `.depth` files (`toolType = Seabat9001`, `numDepths = 60`).

## Usage

```
Sbat2OMG (-v) (-allowed 3) (-centre 30) -old linename -new linename
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-old` | `<linename>` | *required* | Input Huff-format ASCII SeaBat 9001 file. |
| `-new` | `<linename>` | *required* | Output file prefix; creates `<linename>.depth`. |
| `-allowed` | `<min_quality>` | `3` | Minimum acceptable beam quality (`quality[j] >= allowed`); beams below this value are flagged with `status = 22`. |
| `-centre` | `<beam_index>` | `30` | Center beam index. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **ASCII Ping Header & UTM Conversion**: For each ping, reads a 10-field ASCII header (`year`, `jday`, `secs`, `heave`, `roll`, `pitch`, `heading`, `tide`, `ship_east`, `ship_north`) and converts UTM Easting/Northing to WGS84 latitude and longitude via `utmgeo(&ship_lat, &ship_lon, -69.0, ship_east, ship_north, 'n')`.
2. **60-Beam Loop**: Reads 60 lines per ping (`beamno`, `depth`, `across`, `along`, `c_east`, `c_north`, `quality`, `bs`), converts each beam's UTM coordinates to latitude/longitude via `utmgeo()`, negates `depth`, `across`, and `along` into millimeters (`-(int)(val * 1000.0)`), flags beams where `quality < allowed` as `status = 22`, and writes the OMG HDCS v1 profile and beams to `<linename>.depth`.
3. **Summary Header Finalization**: Rewinds `<linename>.depth` at EOF to update `summary.numProfiles` with the total ping count and prints the time and geographic bounding box.

## Practical Examples

### Convert a Huff ASCII SeaBat 9001 file to OMG `.depth` format

```bash
Sbat2OMG -v -allowed 3 -old huff_line01.asc -new huff_line01
```
This creates `huff_line01.depth`.
