---
layout: default
title: xtf2nav
parent: XTF Tools
nav_order: 8
tool_name: xtf2nav
source_path: code/xtf/xtf2nav.c
category: Navigation Extraction
input_formats: [".xtf", ".idx"]
output_formats: [".nav_0", ".nav_2", ".nav_100", ".nav_107"]
related_tools: ["xtf2orientation", "xtf2param", "xtfTool", "mergeNav", "stripNav"]
---

# xtf2nav

## Overview
`xtf2nav` extracts navigation fixes and vessel/sensor heading from an XTF file and writes binary OMG `jcu_nav_rec` navigation files. Depending on which packet types exist in the XTF file, `xtf2nav` writes up to three separate navigation streams:
* `<prefix>.nav_2` (or `<prefix>.nav_0` if no bathymetry packets exist): Navigation embedded in bathymetry (ID 2 or user-specified `-bathy_source`) or sidescan (ID 0) ping headers, automatically thinned to remove redundant duplicate fixes across high-rate pings.
* `<prefix>.nav_100`: Raw Reson navigation packets (`XTF_HEADER_RESON_NAVIGATION`, ID 100), if present.
* `<prefix>.nav_107`: Raw Applanix POS/MV navigation packets (`XTF_HEADER_POS_RAW_NAVIGATION`, ID 107), if present.

> [!IMPORTANT]
> Downstream OMG tools (`mergeNav`, `jview`, etc.) always read `<prefix>.nav`. After running `xtf2nav`, copy your preferred navigation file (`.nav_2`, `.nav_0`, `.nav_100`, or `.nav_107`) to `<prefix>.nav`!

## Usage
```bash
xtf2nav [OPTIONS] -nav <ship|sensor> -hdg <ship|sensor> -xtf <input.xtf> -omg <output_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-xtf` | `<input.xtf>` | **Required** | Path to the input `.xtf` file (uses `<basename>.idx` if available). |
| `-omg` | `<output_prefix>` | **Required** | Prefix for output navigation files (`.nav_0`, `.nav_2`, `.nav_100`, `.nav_107`). |
| `-nav` | `ship` \| `sensor` | **Required** | Coordinate fields to extract from ping headers (`ShipX/Ycoordinate` vs. `SensorX/Ycoordinate`). |
| `-hdg` | `ship` \| `sensor` | **Required** | Heading field to extract from ping headers (`ShipGyro` vs. `SensorHeading`). |
| `-bathy_source` | `<packet_id>` | `2` (`XTF_HEADER_BATHY`) | Override the bathymetry packet ID used to extract ping-header navigation (e.g., `65` for R2Sonic or `28` for QINSy QMBE). |
| `-zone` | `<zone> <n\|s>` | Geographic (Lat/Lon) | If ping-header coordinates are stored in UTM (detected automatically when lat/lon exceed $\pm 90^\circ / 360^\circ$), convert UTM to WGS84 geographic coordinates using the specified UTM zone and hemisphere (`n` or `s`). |
| `-time_shift` | `<seconds>` | `0.0` | Apply an additive time shift (in seconds) to `baseTime`. |
| `-force_sync` | `<method_id>` | Auto-detect | Force a specific XTF time synchronization method (`get_xtf_synchro`) when automatic detection fails. |
| `-make_west` | None | Off | Negate longitude values (`-resonNavigation.longitude`) in packet ID 100 (`XTF_HEADER_RESON_NAVIGATION`). |
| `-make_south` | None | Off | Negate latitude values (`-resonNavigation.latitude`) in packet ID 100 (`XTF_HEADER_RESON_NAVIGATION`). |
| `-unwrap_day` | None | Off | Apply modulo `86400000` ms (`MILLIS_PER_DAY`) to `time_ms` in packet ID 100 when the millisecond counter fails to reset at midnight. |
| `-millis_from_midnight` | None | Off | Set flag for milliseconds-from-midnight timestamping. |
| `-v` | None | Off | Enable verbose progress output. |
| `-debug` | None | Off | Enable debug diagnostics. |

## How It Works
1. **Index & Time Synchronization:** Loads `<basename>.idx` or builds an XTF index, determines the time synchronization scheme via `get_xtf_synchro()` (or `-force_sync`), and computes `baseTime` (plus any `-time_shift`).
2. **Ping Header Navigation (`.nav_2` or `.nav_0`):** Iterates through all bathymetry packets (`-bathy_source`, default ID 2) or falls back to sidescan packets (ID 0). Deduplicates consecutive fixes with identical `(lat, lon)`, converts UTM to WGS84 if `-zone` is provided, and writes `jcu_nav_rec` records using `baseTime + NavFixMilliseconds / 1000.0`.
3. **Raw Reson Navigation (`.nav_100`) & POS/MV Navigation (`.nav_107`):** If packet ID 100 or ID 107 records exist in the XTF index, extracts them into `<prefix>.nav_100` and `<prefix>.nav_107` respectively.

## Practical Examples

**1. Extract sensor navigation from a Reson XTF file and copy `.nav_2` to `.nav`:**
```bash
xtf2nav -nav sensor -hdg sensor -xtf line01.xtf -omg line01
cp line01.nav_2 line01.nav
```

**2. Extract navigation from an R2Sonic XTF file (packet ID 65) logged in UTM Zone 20N:**
```bash
xtf2nav -bathy_source 65 -zone 20 n -nav ship -hdg ship -xtf r2s_line.xtf -omg r2s_line
cp r2s_line.nav_2 r2s_line.nav
```
