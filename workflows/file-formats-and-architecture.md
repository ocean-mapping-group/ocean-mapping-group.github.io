---
layout: default
title: OMG File Formats & Directory Architecture
parent: Processing Workflows & Guides
nav_order: 1
category: workflows
related_tools:
- read_kmall
- RTlite
- mergeNav
- mergeAtt
- newMergeAtt
- makess
- make_blank
- weigh_grid
- mos2
- swathed
- jview
---

# OMG File Formats & Directory Architecture

The Ocean Mapping Group (OMG) software suite processes raw multibeam sonar datagrams by **unraveling** (demultiplexing) a single vendor log file (such as Kongsberg `.kmall` or `.all`) into a set of synchronized binary and ASCII companion files sharing a common `<line_prefix>`.

Understanding how these companion files interact—and where they must reside on disk—is essential for both manual processing and automated LLM-assisted workflows.

---

## Standard Survey Directory Structure

An OMG processing workspace is typically organized by Julian Day (`JDxxx`) or survey area, with separate subdirectories for raw vendor files, unravelled swath files, decimated navigation, and sidescan time-series:

```text
survey_project/
├── raw/                         # Raw Kongsberg .kmall / .kmwcd or .all / .wcd files
│   ├── 0001_20240615_120000_Ship.kmall
│   └── 0001_20240615_120000_Ship.kmwcd
├── merged/                      # Unravelled OMG_HDCS swath & companion files
│   ├── 0001_20240615_120000_Ship.merged
│   ├── 0001_20240615_120000_Ship.param
│   ├── 0001_20240615_120000_Ship.nav
│   ├── 0001_20240615_120000_Ship.orientation
│   ├── 0001_20240615_120000_Ship.ss_data
│   ├── 0001_20240615_120000_Ship.16_data
│   ├── 0001_20240615_120000_Ship.sectors
│   ├── 0001_20240615_120000_Ship.sv_filtered
│   ├── 0001_20240615_120000_Ship.watercol
│   └── 0001_20240615_120000_Ship.WC_Phase1
├── decnav/                      # Filtered & decimated navigation (from stripNav)
│   └── 0001_20240615_120000_Ship.nav
├── ss/                          # Processed GLORIA-format sidescan lines (from makess / glfill)
│   └── 0001_20240615_120000_Ship.ss
└── grids/                       # Regional grids and mosaics
    ├── area.blank               # Blank grid header (from make_blank -float)
    ├── area.weight              # Accumulated weight raster (from weigh_grid)
    ├── area.r4                  # 32-bit float depth grid (from weigh_grid -extract)
    ├── area.8bit                # 8-bit greyscale depth raster (from r4to8bit)
    ├── area.sun                 # Sun-illuminated hillshade (from addSUN)
    ├── area_mos.blank           # Blank mosaic header (from make_blank -8bit -prime 255)
    ├── area.mos                 # 8-bit sidescan mosaic (from mos2)
    └── area.ran                 # Pixel-to-track range buffer (from mos2)
```

---

## Companion File Ecosystem (`<prefix>.*`)

When `read_kmall` or `RTlite` unravels a raw file with output prefix `<prefix>`, it creates a suite of files that always travel together. Many OMG tools take `<prefix>.merged` or `<prefix>` on the command line and implicitly open sibling files by replacing or appending extensions.

### 1. Core Bathymetry & Swath Geometry

| Extension | Header / Struct (`code/subr/`) | Format & Contents | Primary Producers & Consumers |
| :--- | :--- | :--- | :--- |
| `.merged` | `OMG_HDCS_summary_header` + `OMG_HDCS_profile_header` + `OMG_HDCS_beam_data` (`OMG_HDCS_jversion.h`) | Binary swath file (typically **Version 4**, `toolType = 25` for KMALL). Stores file bounds, per-ping vessel position/heading/heave/tide/TX-orientation, and per-beam 3D offsets (`along_track`, `across_track`, `depthOffset`), two-way travel time, launch angles, reflectivity, and status flags. | **Produced by:** `read_kmall`, `RTlite`<br>**Modified in-place by:** `mergeNav`, `mergeAtt`, `newMergeAtt`, `mergeTide`, `mergeHeave`, `swathed`, `moveOverWCinfo`<br>**Read by:** `getBounds`, `weigh_grid`, `makess`, `mos2` |
| `.param` | ASCII key-value text (`OMG_HDCS_ship_parameters`) | Vessel lever-arm installation offsets (`Trans1_X`, `Trans1_Y`, `Trans1_Z`, `Ref_Roll`, `Ref_Pitch`, `Ref_Heading`, `Nav_X`, `Nav_Y`, `Nav_Z`, `Motion_X`, `Motion_Y`, `Motion_Z`) and waterlines extracted from `#IIP` or installation datagrams. | **Produced by:** `read_kmall`, `RTlite`<br>**Read by:** `mergeNav`, `mergeAtt`, `newMergeAtt` |
| `.sectors` | Binary sector records | Transmit sector parameters per ping (tilt angles, center frequencies, bandwidths, pulse lengths, waveform IDs, and absorption coefficients). | **Produced by:** `read_kmall`, `RTlite`<br>**Read by:** `newMergeAtt`, `makess`, `deTVG` |

### 2. Navigation, Attitude & Tide Files

| Extension | Header / Struct (`code/subr/`) | Format & Contents | Primary Producers & Consumers |
| :--- | :--- | :--- | :--- |
| `.nav_1`, `.nav_2`, `.nav_3` | `jcu_nav_rec` (`jcu_nav.h`) | Binary 32-byte records (`year`, `day`, `sec`, `usec`, `lat`, `lon`, `head`, `vel`, `flags`, `qual`, `sol`) written by `read_kmall` for Kongsberg `#SPO` sensor systems `0`, `1`, and `2`. | **Produced by:** `read_kmall`<br>**Copied to:** `.nav` before running `mergeNav` |
| `.nav` | `jcu_nav_rec` (`jcu_nav.h`) | Active binary navigation file used by downstream OMG tools. | **Produced by:** `RTlite`, `stripNav`, `appendNav`, or copied from `.nav_1`<br>**Read by:** `mergeNav`, `makess`, `getBounds` |
| `.orientation_1`, `.net_att_1`, `.net_att_2` | `OMG_HDCS_attitude` (`OMG_HDCS_jversion.h`) | High-rate binary motion records (`roll`, `pitch`, `heave`, `heading` in $10^{-7}$ radians / mm) split by `#SKM` `sensorInputFormat`:<br>• `1` (KM Binary) $\rightarrow$ `.net_att_2`<br>• `2` (EM3000) $\rightarrow$ `.orientation_1`<br>• `7` (POS M/V GRP 102/103) $\rightarrow$ `.net_att_1` | **Produced by:** `read_kmall`<br>**Copied to:** `.orientation` before running `mergeAtt` / `newMergeAtt` |
| `.orientation` | `OMG_HDCS_attitude` (`OMG_HDCS_jversion.h`) | Active binary high-rate attitude file used by `mergeAtt` and `newMergeAtt`. | **Produced by:** `RTlite` or copied from `.net_att_2` / `.net_att_1` / `.orientation_1`<br>**Read by:** `mergeAtt`, `newMergeAtt` |
| `.heave` | Binary delayed heave | POS/MV delayed heave records (`#SKM` delayed heave). | **Produced by:** `read_kmall`, `RTlite`<br>**Read by:** `mergeHeave` |
| `.tide` | ASCII tide table | Chronological tide height records (`YYYY DDD HH MM SS.SS Tide_m`). | **Produced by:** `doallWEB_Tide` or gauge conversion scripts<br>**Read by:** `mergeTide` |

### 3. Sound Velocity Profiles (SVP)

| Extension | Format & Contents | Primary Producers & Consumers |
| :--- | :--- | :--- |
| `.sv`, `.sv_0`, `.sv_1` | Raw ASCII sound velocity casts unpacked from `#SVP` datagrams (`.sv_0` for CTD casts, `.sv_1` for direct sound velocity casts). | **Produced by:** `read_kmall`, `RTlite` |
| `.sv_filtered` | Cleaned and depth-sorted sound velocity profile (`depth_m  sound_speed_m_s`) used for ray-tracing. | **Produced by:** `read_kmall`, `RTlite`<br>**Read by:** `newMergeAtt -redoref`, `mergeAtt -redoref` |
| `.ssv` | Surface sound velocity time-series (`#SCL` / `#MRZ` transducer sound speed). | **Produced by:** `read_kmall`, `RTlite` |

### 4. Backscatter, Snippets & Sidescan Files

| Extension | Header / Struct (`code/subr/`) | Format & Contents | Primary Producers & Consumers |
| :--- | :--- | :--- | :--- |
| `.ss_data` | Raw byte stream | Packed seabed image / snippet amplitude samples (0.5 dB steps). Byte offset and byte length for each ping are stored in the `.merged` profile header (`ss_offset`, `ss_length`). | **Produced by:** `read_kmall`, `RTlite`<br>**Read by:** `deTVG`, `makess` |
| `.16_data` | `E_3K_Extra` / snippet descriptors | Per-beam seabed image descriptors (sorting direction, detection info, sample count, centre sample index). | **Produced by:** `read_kmall`, `RTlite`<br>**Read by:** `deTVG`, `makess` |
| `.ss_data_deTVG` | Raw byte stream | Snippet samples with Kongsberg's empirical real-time TVG flattened by `deTVG`. | **Produced by:** `deTVG`<br>**Read by:** `makess -use_deTVG` |
| `.ss` | `gloria_Header` + `gloria_rec` (`gloria.h`) | Slant-range / across-track binned sidescan trace file (256-byte header per ping followed by port and starboard 8-bit backscatter scanlines). | **Produced by:** `makess`, modified in-place by `glfill` and `stretchacres`<br>**Read by:** `mos2` (via `tomos`) |

### 5. Water Column Files

| Extension | Format & Contents | Primary Producers & Consumers |
| :--- | :--- | :--- |
| `.watercol` | Binary water column amplitude arrays (0.5 dB integer steps) unpacked from `#MWC` (`.kmwcd` or `.wcd`). Byte pointers are stored in `.merged`. | **Produced by:** `read_kmall`, `RTlite`<br>**Read by:** `newMergeAtt -wc`, `jview` water column viewer |
| `.WC_Phase1` | Binary split-beam phase difference arrays unpacked from `#MWC` when phase data are logged. | **Produced by:** `read_kmall`<br>**Read by:** `newMergeAtt -wc` |

### 6. Gridded Rasters (`OMG1` / `JHC_header`)

All OMG 2D raster files (`.blank`, `.r4`, `.weight`, `.8bit`, `.sun`, `.mos`, `.ran`) share the same **1024-byte `JHC_header`** (`code/subr/array.h`) identified by the magic string `"OMG1"` in the first 4 bytes.

| Extension | `data_type` | Pixel Size | Description |
| :--- | :---: | :---: | :--- |
| `.blank` | `1` (8-bit) or `3` (float) | 1 or 4 bytes | Initialized raster template defining projection (`projection`, `central_meridian`), bounds (`xmin`, `xmax`, `ymin`, `ymax`), grid spacing (`dx`, `dy`), and dimensions (`xdim`, `ydim`). |
| `.r4` | `3` | 4 bytes (`float`) | 32-bit IEEE floating-point bathymetric depth or backscatter grid. Background/no-data value is `9999.0f`. |
| `.weight` | `3` | 4 bytes (`float`) | Cumulative beam weight array maintained by `weigh_grid` during incremental swath gridding. |
| `.8bit` | `1` | 1 byte (`u_char`) | 8-bit unsigned integer greyscale image (`0..254` data, `255` background). |
| `.sun` | `1` | 1 byte (`u_char`) | 8-bit sun-illuminated relief image generated by `addSUN`. |
| `.mos` | `1` | 1 byte (`u_char`) | 8-bit sidescan / backscatter mosaic generated by `mos2`. |
| `.ran` | `1` | 1 byte (`u_char`) | Auxiliary distance-from-nadir range buffer maintained by `mos2` to resolve overlapping swaths in favor of near-range traces. |

---

## Coordinate, Angle & Depth Sign Conventions

> [!IMPORTANT]
> Different parts of the OMG codebase evolved across different decades and sensor conventions. Paying close attention to sign conventions avoids inverted grids, mirrored swaths, and doubled lever-arm offsets.

1. **Bathymetric Depth Sign Convention:**
   - Inside `.merged` files (`depthOffset`) and `.r4` grids, water depths below the sea surface are **positive** (e.g., `+2500.0` m is 2500 m water depth), while Drying Heights / Topography above sea level are **negative**.
   - Conversely, tide files merged with `mergeTide` add `tide` directly unless `-flip` is passed (`depth = raw_depth - tide` when using `mergeTide -flip`).
2. **Longitude Sign Convention:**
   - Geographic longitudes are positive East (`0` to `+180`) and negative West (`-180` to `0`).
   - Inside `OMG_HDCS` binary structs, latitudes and longitudes are stored as signed 32-bit integers in units of **$10^{-7}$ radians** (converted via `R2D` and `1.0e7` scale factors).
3. **Vessel Reference Frame & Lever Arms (`.param` vs `mergeNav`):**
   - In `.param` files written by `read_kmall`, Kongsberg `#IIP` coordinates use:
     - `+X` = Forward (bow)
     - `+Y` = Starboard
     - `+Z` = Downward
   - When `mergeNav -param <file.param>` reads `Nav_X` and `Nav_Y`, it automatically negates them (`nav_offset_x = -Nav_X`, `nav_offset_y = -Nav_Y`) so they represent the vector from the GPS antenna to the Reference Point (`RP - GPS`).
   - If you instead supply manual CLI flags (`mergeNav -dx <X> -dy <Y>`), `+dx` is **Starboard** and `+dy` is **Forward**. Always prefer `-param <line>.param` for Kongsberg datasets to avoid sign mistakes.
