---
layout: default
title: convertWOA01
parent: Jonathan Beaudoin (jonnyb) Tools
nav_order: 6
tool_name: convertWOA01
source_path: code/jonnyb/woa/convertWOA01.c
category: Oceanographic Climatology & Databases (jonnyb)
input_formats: ["NOAA WOA01 quarter-degree (1440x720) or 1-degree (360x180) ASCII grids"]
output_formats: [".r4 (32-bit float OMG mapsheets)", ".8bit (8-bit OMG mapsheets)", "woa01_depth.r4"]
related_tools: ["svp_woa01", "soundscape", "wod2db3"]
---

# convertWOA01 & convertWOA01_mask

## Description
`convertWOA01` (`code/jonnyb/woa/convertWOA01.c`) and `convertWOA01_mask` (`code/jonnyb/woa/convertWOA01_mask.c`) convert NOAA World Ocean Atlas 2001 (`WOA01`) global ASCII climatology grids across all 33 standard oceanographic depth levels ($0, 10, 20, 30, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1750, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500\text{ m}$) into binary OMG mapsheets (`JHC_header`, geographic projection `projection = 3`, WGS84):
* `convertWOA01` converts quarter-degree ($0.25^\circ \times 0.25^\circ$, $1440\times 720$ cells) temperature (`-t`) and salinity (`-s`) grids into `.r4` floating-point volumes or per-depth `.r4` slices (`-split`), and optionally generates `woa01_depth.r4` (`-depths`) recording the maximum valid depth at each grid cell.
* `convertWOA01_mask` converts one-degree ($1.0^\circ \times 1.0^\circ$, $360\times 180$ cells) temperature (`-t`), salinity (`-s`), or gridpoint mask (`-gp`, `-8bit`) files into `.r4` or `.8bit` OMG grids.

---

## Usage

```bash
# Quarter-degree (1440x720) WOA01 temperature/salinity conversion:
convertWOA01 [-v] [-split] [-depths] (-s | -t) -in <woa01_ascii_file>

# One-degree (360x180) WOA01 conversion:
convertWOA01_mask [-v] [-8bit] [-split] (-s | -t | -gp) -in <woa01_1deg_ascii_file>
```

### Examples

**1. Convert a quarter-degree WOA01 temperature file into a 33-layer `.r4` volume and extract `woa01_depth.r4`:**
```bash
convertWOA01 -t -depths -in t0101an1.woa
```

**2. Split a WOA01 salinity file into 33 individual depth-level `.r4` mapsheets (`*.0000.r4` .. `*.5500.r4`):**
```bash
convertWOA01 -s -split -in s0101an1.woa
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <input_file>` | Input NOAA WOA01 ASCII grid file. | Required |
| `-s` | Input contains Salinity data (`SALINITY`, `min_value = 0.0`, `max_value = 40.0`). | Required (`-s`, `-t`, or `-gp`) |
| `-t` | Input contains Temperature data (`TEMPERATURE`, `min_value = -3.0`, `max_value = 35.0`). | Required (`-s`, `-t`, or `-gp`) |
| `-gp` | Input contains 8-bit Gridpoint count/mask data (`GRIDPOINT`, supported in `convertWOA01_mask`). | Disabled |
| `-split` | Write 33 separate OMG mapsheet files named `<inname>.<DDDD>.r4` (e.g., `.0000.r4`, `.0010.r4`, ..., `.5500.r4`) instead of a single concatenated 33-layer volume. | Single multi-layer `.r4` |
| `-depths` | (`convertWOA01` only) Write `woa01_depth.r4` containing the deepest standard depth level (meters) with valid data at each of the $1440\times 720$ cells. | Disabled |
| `-8bit` | (`convertWOA01_mask` only) Output 8-bit unsigned char (`.8bit`) instead of 32-bit float (`.r4`). | Disabled (unless `-gp`) |
| `-v` | Enable verbose output. | Disabled |
