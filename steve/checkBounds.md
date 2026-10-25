---
layout: default
title: checkBounds
parent: Steve Brucker (steve) Tools
nav_order: 1
tool_name: checkBounds
source_path: code/steve/checkBounds.c
category: Spatial Indexing & Quality Control (steve)
input_formats: [".merged", ".100ping_bounds", ".file_bounds", "xyzlist (ASCII file list)"]
output_formats: ["Binary bounds array (6 doubles per file)", "ASCII bounds table"]
related_tools: ["getBounds", "weigh_grid", "swathed", "checkEmpty"]
---

# checkBounds

## Description
`checkBounds` inspects the spatial and temporal bounding boxes of one or more OMG-HDCS `.merged` multibeam files (up to 5,000 files via `-xyzlist`) by cross-checking three sources of extent metadata:
1. The `OMG_HDCS_summary_header` embedded at the start of the `.merged` file (`minLat`, `maxLat`, `minLong`, `maxLong`, `refLat`, `refLong`, `refTime`).
2. The 100-ping spatial index file (`<prefix>.100ping_bounds`), which stores 32-byte `OMG_HDCS_bounds` records for every 100-ping block.
3. The global file bounds sidecar (`<prefix>.file_bounds`), which stores a single 32-byte `OMG_HDCS_bounds` record summarizing the entire file.

In addition to exporting global `[mintime, maxtime, minlat, maxlat, minlon, maxlon]` extents in binary (`-out`) or ASCII (`-ascii_out`) format, `checkBounds` performs an automated outlier sanity check: if either the Top-Left (`maxlat, minlon`) or Bottom-Right (`minlat, maxlon`) corner of the bounding box lies more than **50.0 nautical miles** from the file's reference coordinate (`summary.refLat`, `summary.refLong`), `checkBounds` flags the file on `stdout` (`LOOKS LIKE THERES A PROBLEM IN: <file>`).

---

## Usage

```bash
checkBounds [-v] [-in <file.merged> | -xyzlist <listfile>] [-out <binary_bounds>] [-ascii_out <ascii_bounds>]
```

### Examples

**1. Inspect a single `.merged` file and its `.100ping_bounds` / `.file_bounds` in verbose mode:**
```bash
checkBounds -v -in merged/JD200/0012_line.merged
```

**2. Audit an entire survey's `-xyzlist` for corrupted bounding boxes and write an ASCII catalog:**
```bash
checkBounds -xyzlist all_merged.list -ascii_out survey_bounds.txt
```

**3. Export both binary (48 bytes per file) and ASCII global bounds:**
```bash
checkBounds -xyzlist all_merged.list -out global_bounds.bin -ascii_out global_bounds.txt
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <infile.merged>` | Path to a single input `.merged` file to inspect (mutually exclusive with `-xyzlist`). | None |
| `-xyzlist <listfile>` | Path to an ASCII list of `.merged` file paths (loaded via `load_inputfiles_from_list`, supporting up to 5,000 files across one or more list files). | None |
| `-out <outfile>` | Output binary file to which a 6-element `double` array (`maxmins[6]` = `{mintime, maxtime, minlat, maxlat, minlon, maxlon}`, 48 bytes per file) is written for each file that has a `.100ping_bounds` or `.file_bounds` sidecar. | Disabled |
| `-ascii_out <ascii_outfile>` | Output ASCII file (opened in `"wa"` mode) where one line per file is written: `<merged_path> <mintime> <maxtime> <minlat> <maxlat> <minlon> <maxlon>`. | Disabled |
| `-v` | Enable verbose output: prints summary header extents, X/Y distances in km, reference date string, every 100-ping bounding box record, `.file_bounds` info, and re-reads `-out` at completion to verify the binary records. | Disabled |

---

## Output Formats

### 1. ASCII Output (`-ascii_out`)
Each line contains 7 space-separated fields:
```text
<merged_filename> <mintime_s> <maxtime_s> <minlat_deg> <maxlat_deg> <minlon_deg> <maxlon_deg>
```
* `mintime_s`, `maxtime_s`: Unix epoch time in seconds (`%.1f`).
* `minlat_deg`, `maxlat_deg`, `minlon_deg`, `maxlon_deg`: Geographic bounding box in decimal degrees (`%.6f`, WGS84).

### 2. Binary Output (`-out`)
For each processed file with valid bounds, `checkBounds` writes a contiguous 48-byte block (`double maxmins[6]`):
* `maxmins[0]`: `mintime` (seconds since 1970-01-01 00:00:00 UTC)
* `maxmins[1]`: `maxtime` (seconds since 1970-01-01 00:00:00 UTC)
* `maxmins[2]`: `minlat` (decimal degrees)
* `maxmins[3]`: `maxlat` (decimal degrees)
* `maxmins[4]`: `minlon` (decimal degrees)
* `maxmins[5]`: `maxlon` (decimal degrees)

---

## How It Works

1. **Summary Header Decode:**
   Opens `<file>.merged` and calls `OMG_HDCS_read_summary`. Converts integer offsets to decimal degrees:
   $$\text{lat} = \frac{180}{\pi}\left(\text{refLat}\times 10^{-7} + \text{LatOffset}\times 10^{-9}\times\text{positionScale}\right)$$
   and computes approximate North-South (`latdist`) and East-West (`londist`) spans in kilometers.
2. **100-Ping Bounds Scan (`<prefix>.100ping_bounds`):**
   Determines the number of 100-ping records as `filesize / 32` (since each disk record is 32 bytes) and iterates through all records using `OMG_HDCS_read_bounds` and `OMG_HDCS_interp_bounds`, accumulating the overall minimum/maximum latitude, longitude, and time.
3. **Global File Bounds Read (`<prefix>.file_bounds`):**
   Opens `<prefix>.file_bounds` (if present) and reads record `0` via `OMG_HDCS_read_bounds` and `OMG_HDCS_interp_bounds(&bounds, summary)`.
4. **50-Nautical-Mile Sanity Check:**
   Computes the Euclidean distance in nautical miles from the summary header reference point $(\text{ref\_lat}, \text{ref\_lon})$ to both the Top-Left $(\text{maxlat}, \text{minlon})$ and Bottom-Right $(\text{minlat}, \text{maxlon})$ corners:
   $$\Delta d_{\text{TL}} = \sqrt{\left((\text{ref\_lat} - \text{maxlat})\times 60\right)^2 + \left((\text{ref\_lon} - \text{minlon})\times 60\cos(\text{ref\_lat})\right)^2}$$
   If $\Delta d_{\text{TL}} > 50\text{ NM}$ or $\Delta d_{\text{BR}} > 50\text{ NM}$, prints:
   ```text
   LOOKS LIKE THERES A PROBLEM IN: <filename>
   TLy: ... TLx: ... BRy: ... BRx: ... Start Time: ... End Time: ... Timespan(s): ...
   delta_dist_TL: ... delta_dist_BR: ... (miles from reference coords)
   ```
   which immediately identifies lines with unflagged navigation spikes that need cleaning with [`navedit`](../nav/navedit.md) or [`areaNavEdit`](../ianc/areaNavEdit.md) followed by re-running [`getBounds`](../omg/getBounds.md).
