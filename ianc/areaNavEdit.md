---
layout: default
title: areaNavEdit
parent: Ian Church — Hydrodynamic & 3D Ray-Trace Suite (ianc)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 4
tool_name: areaNavEdit
source_path: code/ianc/areaNavEdit.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats:
- OMG Binary Navigation (.nav)
output_formats:
- OMG Binary Navigation (.nav)
related_tools:
- Check_Nav
- POStoNav
---

# areaNavEdit

## Description

`areaNavEdit` is a spatial filtering utility for OMG/JHC binary navigation files (`.nav`). Written by Ian Church in May 2010, the tool reads an input binary navigation file, tests every navigation record's geographic coordinates `(lat, lon)` against a user-specified rectangular bounding box (`-lat1`, `-lat2`, `-lon1`, `-lon2`), flags records falling outside the box by setting `flag[3] = 1` (and `flag[3] = 0` inside the box), and writes the resulting records to a new binary navigation file.

This allows automated spatial clipping or de-weighting of navigation fixes outside a survey sheet or region of interest without deleting records or altering record indices in the binary `.nav` stream.

## Usage

```bash
areaNavEdit [-v] -lat1 <deg> -lat2 <deg> -lon1 <deg> -lon2 <deg> -out <nav_outfile> -in <nav_infile>
```

### Example Commands

Flag all navigation points outside the bounding box (`45°N` to `85°N`, `-114°W` to `-66°W`):

```bash
areaNavEdit -v -lat1 45 -lat2 85 -lon1 -66 -lon2 -114 -out clipped.nav -in raw_survey.nav
```

Verify the resulting flags using `Check_Nav`:

```bash
Check_Nav clipped.nav
```

## CLI Arguments and Options

All bounding box and file arguments are required (`argc >= 12`).

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-v` | None | Enables verbose output (`verbose_flag`), printing the total record count and `Flagged Bad Nav......................` whenever a record falls outside the bounding box. |
| `-lat1` | `<float>` | First latitude boundary in decimal degrees (automatically ordered with `-lat2` so `lat1` becomes the northern/upper bound). |
| `-lat2` | `<float>` | Second latitude boundary in decimal degrees (automatically ordered with `-lat1` so `lat2` becomes the southern/lower bound). |
| `-lon1` | `<float>` | First longitude boundary in decimal degrees (automatically ordered with `-lon2` so `lon1` becomes the western/lower bound). |
| `-lon2` | `<float>` | Second longitude boundary in decimal degrees (automatically ordered with `-lon1` so `lon2` becomes the eastern/upper bound). |
| `-in` | `<nav_infile>` | Path to the input binary OMG navigation file. |
| `-out` | `<nav_outfile>` | Path to the output binary OMG navigation file with updated `flag[3]` values. |

## File Formats

### Input and Output Format: OMG Binary Navigation (`.nav`)
* Both input and output files consist of fixed-length `jcu_nav_rec` records of size `JCU_BINNAV_RECLEN` bytes (defined in `jcu_nav.h`).
* Every field of `in_nav_rec` (`time`, `centisecs`, `lat`, `lon`, `azi`, `depth`, `velocity`, `flag[0..2]`) is preserved identically in `out_nav_rec`.
* Only `out_nav_rec.flag[3]` is modified:
  * `0`: Record lies strictly inside the bounding box (`lat2 < lat < lat1` and `lon1 < lon < lon2`).
  * `1`: Record lies on or outside the bounding box.

## How It Works

1. **Argument Validation & Bound Normalization**: `areaNavEdit` checks that at least 12 command-line tokens were supplied (`ARGC >= 12`; otherwise it exits with return code `4`). After parsing `-lat1`, `-lat2`, `-lon1`, and `-lon2`, it normalizes the bounds so that `lat1 >= lat2` (Upper/North vs. Lower/South) and `lon1 <= lon2` (West/Lower vs. East/Upper), printing the resulting `Upper West` (`lat1, lon1`) and `Lower East` (`lat2, lon2`) corners.
2. **Record Count Determination**: The input file is seeked to `SEEK_END` (`fseek(inNavFile, 0, 2)`), and the total number of binary records `numrec` is computed as `ftell(inNavFile) / JCU_BINNAV_RECLEN` before seeking back to the beginning of the file.
3. **Bounding Box Evaluation & Flagging**: For each record `k` from `0` to `numrec - 1`:
   * `nav_read(inNavFile, k, &in_nav_rec)` reads the record.
   * If `in_nav_rec.lat > lat2 && in_nav_rec.lat < lat1 && in_nav_rec.lon > lon1 && in_nav_rec.lon < lon2`, `out_nav_rec.flag[3]` is set to `0`.
   * Otherwise, `out_nav_rec.flag[3]` is set to `1` and `numFlag` is incremented.
   * `nav_write(outNavFile, k, &out_nav_rec)` writes the updated record to the output file.
4. **Summary Reporting**: Upon completion, the program prints `Flagged <numFlag>/<numrec> Records in <inName>` and closes both file handles.
