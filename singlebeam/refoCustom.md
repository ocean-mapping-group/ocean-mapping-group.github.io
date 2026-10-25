---
layout: default
title: refoCustom
parent: Single-Beam Echosounder Tools (singlebeam)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 1
tool_name: refoCustom
source_path: code/singlebeam/refoCustom.c
category: singlebeam
input_formats:
- BCHYDRO ASCII Singlebeam
- SDG 48-Byte Binary Singlebeam
output_formats:
- OMG_HDCS Singlebeam (.merged)
related_tools:
- readEA600
- knud2glo
- mergeTide
- weigh_grid
---

# refoCustom

## Description
`refoCustom` (`code/singlebeam/refoCustom.c`) reformats custom hydrographic singlebeam echosounder logs into the `OMG_HDCS` (`.merged`) binary format (`summary.toolType = SingleBeam`, `summary.sensorNumber = 1`). It supports two agency-specific input formats:
1. **BCHYDRO (`-BCHydro`)**: Space-delimited ASCII records containing UTM Northing, UTM Easting, Depth (m), and Timestamp.
2. **SDG (`-SDG`)**: 48-byte (`LENGTH_SDG = 48`) big-endian binary records containing timestamp, raw and processed Easting/Northing, raw and processed depths, tidal correction, sound-velocity correction, draft/heave correction, and a 16-bit bitwise quality status flag.

## Usage

```bash
refoCustom [-v] [-BCHydro [-local_datum <m>]] [-SDG [-showbits]] <infile> <outfile.merged>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-v` | Enable verbose output. | Off |
| `-BCHydro` | Parse the input file as BC Hydro space-delimited ASCII (`Northing Easting Depth Time`). | — |
| `-local_datum <value>` | Apply a vertical datum offset (in meters) to observed depths when using `-BCHydro`. | `0.0` |
| `-SDG` | Parse the input file as 48-byte binary SDG singlebeam records. | — |
| `-showbits` | (With `-SDG`) Print a human-readable breakdown of the 16-bit `status_flag` bits for every record. | Off |
| `<infile>` | **Required.** Input custom singlebeam file (BCHYDRO ASCII or SDG binary). | — |
| `<outfile>` | **Required.** Output `OMG_HDCS` `.merged` file. | — |

## How It Works

### 1. Processing BC Hydro ASCII Data (`-BCHydro`)
* Reads each ASCII line (`Northing Easting Depth Time`).
* Converts UTM coordinates (`merid = -125.0`, Northern Hemisphere) to WGS84 Latitude and Longitude using `utmgeo`.
* Subtracts `local_datum` (if specified via `-local_datum`) from the observed depth and writes a 1-beam `OMG_HDCS_profile_header` and `OMG_HDCS_beam` record to `<outfile>`.

### 2. Processing SDG Binary Data (`-SDG`)
* Reads 48-byte big-endian binary records via `read_SDG()`, byte-swapping integer and short fields (`get_swapped_int`, `get_swapped_short`):
  * `time` (seconds), `raw_y_pos`, `raw_x_pos`, `proc_y_pos`, `proc_x_pos`
  * `raw_depth`, `proc_depth`, `tidal_corr`, `velo_corr`, `draft_heave_corr`
  * `status_flag` (16-bit bitmask indicating position/depth rejection states; inspectable via `-showbits`)
* Converts `proc_y_pos` and `proc_x_pos` to geographic coordinates, populates `profile.tide` from `sdgr.tidal_corr`, sets `beams[0].observedDepth` from `sdgr.raw_depth`, maps rejected status bits to `beams[0].status`, and writes each profile to `<outfile>`.

## Example

```bash
# Convert a BC Hydro ASCII survey with a 2.45 m local datum offset:
refoCustom -v -BCHydro -local_datum 2.45 reservoir_sb.txt reservoir_sb.merged

# Convert an SDG binary singlebeam file while inspecting status flag bits:
refoCustom -v -SDG -showbits sdg_line04.bin sdg_line04.merged
```
