---
layout: default
title: selectcb
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: selectcb
source_path: code/grid/selectcb.c
category: gridding
input_formats:
- URI SeaBeam Binary (sb_urirec)
- ASCII Lat/Lon/Depth
output_formats:
- ASCII Projected XYZ (Mercator)
- ASCII Geographic Lat/Lon/Depth
related_tools:
- weigh_grid
- project
- dump_merged
---

# selectcb

## Overview

`selectcb` extracts, spatially/temporally filters, and optionally Mercator-projects bathymetric soundings from University of Rhode Island (URI) SeaBeam 19-beam binary records (`sb_urirec`) or 3-column ASCII sounding files.

---

## Syntax & CLI Options

```
selectcb [-v] [-just_dump] [-justfilt] [-ascii] [-skip <N>] [-lola] <outfilename> <infilename(s)...>
```

| Flag | Description |
|------|-------------|
| `-v` | Verbose progress logging. |
| `-just_dump` | Bypass interactive area/time prompts and dump all valid SeaBeam soundings (`depth > 0`) as `lon lat depth`. |
| `-justfilt` | Filter soundings by the interactive geographic/time bounds, but output unprojected `lat lon depth` instead of Mercator `x y depth`. |
| `-ascii` | Read 3-column ASCII input (`lat lon depth` by default) instead of binary URI SeaBeam records. |
| `-lola` | When used with `-ascii`, interpret the first two input columns as `lon lat` instead of `lat lon`. |
| `-skip <N>` | Subsample every `N`-th ping/record (default: `1`, process every record). |
| `<outfilename>` | Output ASCII file. |
| `<infilename(s)...>` | One or more input URI SeaBeam binary or ASCII sounding files. |

---

## How It Works

1. **Interactive Area & Time Window Selection (`get_area`)**:
   - Unless `-just_dump` is specified, prompts `stdin` interactively for:
     - Geographic bounding box (`bottom_lat`, `top_lat`, `left_lon`, `right_lon` in decimal degrees) and Mercator reference latitude (`proj_lat`).
     - Whether to filter by time (`y/n`), and if so, start and end times (`year julian_day hour minute`).
2. **URI SeaBeam Decoding (`process_cb_data`)**:
   - Reads 100-byte `sb_urirec` records (containing date/time, heading, center lat/lon, and 19 depth + cross-track distance pairs).
   - For each valid beam (`depth[i] > 0`), resolves the beam's true geographic position from the vessel heading and cross-track offset `xtrack[i]`, tests against the bounding box, and writes either Mercator `x y depth` (`mercat`), geographic `lat lon depth` (`-justfilt`), or `lon lat depth` (`-just_dump`).
3. **ASCII Filtering (`process_ascii_data`)**:
   - With `-ascii`, reads 3-column text lines, swaps columns if `-lola` is set, filters against the bounding box, and writes Mercator `x y depth` or unprojected `lat lon depth` (`-justfilt`).

---

## Examples

### Dump all valid beams from URI SeaBeam files to ASCII `lon lat depth`

```bash
selectcb -just_dump seabeam_all.xyz cruise91_01.cb cruise91_02.cb
```

### Interactively filter and Mercator-project an ASCII `lon lat depth` file

```bash
selectcb -ascii -lola region_merc.xyz raw_soundings.xyz
```

---

## Workflow Context

- **Downstream**: [`weigh_grid`](weigh_grid.html), [`surface`](surface.html).
- **Related Tools**: [`project`](project.html), [`dump_merged`](../omg/dumpFlags.html).
