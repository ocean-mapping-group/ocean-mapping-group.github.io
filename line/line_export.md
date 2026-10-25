---
layout: default
title: line_export
parent: Survey Line Export (line)
tool_name: line_export
source_path: code/line/line_export.c
category: Survey Planning & Navigation Export
input_formats: [".lines (OMG_Line_List)", ".r4 / .blank (JHC_header)"]
output_formats: [".lnw (Hypack Planned Lines)", ".asciiplan (Kongsberg SIS Planned Lines)"]
related_tools: ["jview", "omg_line", "hypack2omg"]
---

# line_export

## Overview
`line_export` (`code/line/line_export.c`) converts interactive survey line plans saved from [`jview`](../JV/jview.md) (`.lines` files, parsed via [`omg_line`](../subr/omg_line.md)) into third-party hydrographic acquisition line-planning formats:
1. **HYPACK Planned Lines (`.lnw`)** — Projected into UTM Easting/Northing coordinates (`geoutm`) either as discrete 2-point survey lines (`LIN 2` / `PTS` / `LNN` / `EOL`) or as a single continuous multi-waypoint route (`-do_route`).
2. **Kongsberg Seafloor Information System (`.asciiplan`)** — Exported in geographic WGS84 decimal degrees (`DEG` header followed by `_LINE` records with timestamps).

---

## Usage

```bash
# Export OMG survey lines to HYPACK .lnw format (requires central UTM meridian)
line_export -hypack -merid -63.0 [-do_route] -in patch_test.lines -map area.r4 [-out patch_test.lnw]

# Export OMG survey lines to Kongsberg SIS .asciiplan format
line_export -sis -in patch_test.lines -map area.r4 [-out patch_test.asciiplan]
```

---

## Command-Line Arguments

| Option | Description | Default |
|---|---|---|
| `-in <lines_file>` | **Required.** Input OMG survey line list file (`.lines`) created in `jview`. | None |
| `-map <map_file>` | **Required.** Reference OMG map/grid file (`JHC_header`, e.g., `.r4` or `.blank`) used to determine the geodetic ellipsoid and project pixel/map coordinates to geographic `(lat, lon)` via `read_OMG_Line_List()`. | None |
| `-hypack` | Export in HYPACK `.lnw` (Planned Line) format. Requires `-merid <deg>`. | **Default** (`HYPACK`) |
| `-merid <lon_deg>` | Central meridian (in decimal degrees, negative West, e.g., `-63.0` for UTM Zone 20N) required when `-hypack` is active to convert `(lat, lon)` to UTM `(Easting, Northing)` via `geoutm()`. | Required for `-hypack` |
| `-do_route` | Used with `-hypack`: combine all line endpoints sequentially into a single continuous HYPACK route (`LNS 1`, `LIN <2*N>`, followed by all `PTS <E> <N>` pairs) instead of separate 2-point lines. | Separate lines |
| `-sis` | Export in Kongsberg SIS `.asciiplan` format using WGS84 decimal degrees (`_LINE <id> 0 <YYYYMMDDHHMMSS> 0 <lat1> <lon1> <lat2> <lon2> "`). | Disabled |
| `-out <outfile>` | Explicit output filename. If omitted, `line_export` strips the extension from `-in` and appends `.lnw` (for `-hypack`) or `.asciiplan` (for `-sis`). | `<prefix>.lnw` or `<prefix>.asciiplan` |

---

## Output Format Details

### 1. HYPACK `.lnw` Format (`-hypack`)
* **Standard mode (default):**
  ```text
  LNS <num_lines>
  LIN 2
  PTS <easting_1> <northing_1>
  PTS <easting_2> <northing_2>
  LNN 1
  EOL
  ...
  ```
* **Route mode (`-do_route`):**
  ```text
  LNS 1
  LIN <2 * num_lines>
  PTS <easting_1> <northing_1>
  PTS <easting_2> <northing_2>
  ...
  LNN 1
  EOL
  ```

### 2. Kongsberg SIS `.asciiplan` Format (`-sis`)
```text
DEG
Exported from UNB/OMG line file
0 0 0 0
_LINE 1 0 20261025101500 0  45.12345678 -66.12345678 45.23456789 -66.23456789 "
```
