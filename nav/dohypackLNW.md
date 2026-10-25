---
layout: default
title: dohypackLNW
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 15
tool_name: dohypackLNW
source_path: code/nav/dohypackLNW.c
category: Navigation & Georeferencing
input_formats:
- ASCII .llz (OMG segmented lat lon label)
- Hypack .LNW (planned survey line file)
output_formats:
- Hypack .LNW (planned survey line file)
- ASCII .llz (OMG segmented lat lon label)
related_tools:
- Generic_to_Nav
- DNMtoLLD
- embedNav
- jview
---

# dohypackLNW

## Description
`dohypackLNW` performs bidirectional conversion between OMG segmented ASCII `lat lon label` (`.llz`) planned survey line files and **HYPACK `.LNW`** (Line File) UTM planned line files:
* **`-jhc2hy` (default):** Converts an OMG `.llz` file (where individual survey lines are separated by `0.0 0.0 <label>` sentinel rows) into a HYPACK `.LNW` file (`LNS`, `LIN`, `PTS easting northing`, `LNN`, `EOL`) using forward UTM projection (`geoutm`).
* **`-hy2jhc`:** Converts a HYPACK `.LNW` file into an OMG `.llz` file (inserting `0.0 0.0 0.0` before `LIN` and `0.00 0.00 0.00` at `LNN`) using inverse UTM projection (`utmgeo`).

Both conversions use the WGS84 ellipsoid (`Ellipsoid = 1`) and Northern Hemisphere (`'n'`), with the UTM central meridian specified via `-merid <deg>` (or prompted interactively on `stdin` if omitted).

---

## Usage

```bash
dohypackLNW [-jhc2hy | -hy2jhc] [-merid <deg>] [-skipline <N>] -in <infile> -out <outfile>
```

### Common Workflow Examples

**1. Convert OMG planned lines (`.llz`) to a HYPACK `.LNW` file (UTM Zone 20N, central meridian -63.0°):**

```bash
dohypackLNW -jhc2hy -merid -63.0 -in planned_lines.llz -out survey_plan.LNW
```

**2. Convert a HYPACK `.LNW` file to an OMG `.llz` file for display in `jview`:**

```bash
dohypackLNW -hy2jhc -merid -63.0 -in survey_plan.LNW -out planned_lines.llz
```

**3. Skip a 1-line header in the input `.llz` file before converting to `.LNW`:**

```bash
dohypackLNW -jhc2hy -skipline 1 -merid -123.0 -in header_lines.llz -out lines.LNW
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | **Required.** Input filename (OMG `.llz` when `-jhc2hy`, or HYPACK `.LNW` when `-hy2jhc`). | None |
| `-out <filename>` | **Required.** Output filename (HYPACK `.LNW` when `-jhc2hy`, or OMG `.llz` when `-hy2jhc`). | None |
| `-jhc2hy` | Convert OMG `.llz` (`lat lon label`) to HYPACK `.LNW` (`whichway = 1`). | **Default** (`1`) |
| `-hy2jhc` | Convert HYPACK `.LNW` to OMG `.llz` (`whichway = -1`). | Disabled |
| `-merid <deg>` | UTM central meridian in decimal degrees longitude (e.g., `-63.0`). If omitted (`0`), prompts interactively on `stdin`: `meridian? (decimal longitude please (e.g. -63.0) ** NOTE hardwired to Northern Hemisphere - -WGS84)`. | `0.0` (prompts if `0`) |
| `-skipline <N>` | Number of initial lines to skip at the top of the input file before parsing. | `0` |
| `-debug` | In `-jhc2hy` mode, writes intermediate debug lines (`lineno point_lineno pointinline lat lon east north`) to the output file before the `LNS` block. | Disabled |
| `-v` | Enable verbose flag (`verbose_flag`). | Disabled |

> [!NOTE]
> Any unrecognized positional argument on the command line triggers `usage(" weird command line arg?.. %s .", *argv)`. Always prefix the input and output files with `-in` and `-out`.

---

## Input & Output Format Details

### OMG `.llz` Format
Whitespace-delimited ASCII lines containing `lat lon label` (up to 1,000 points across up to 100 lines):

```text
0.0 0.0 0.0
45.123456 -63.123456 0.0
45.234567 -63.234567 0.0
0.0 0.0 0.0
```
Rows where `lat == 0 && lon == 0` act as polyline segment separators.

### HYPACK `.LNW` Format

```text
LNS <total_number_of_lines>
LIN <num_points_in_line>
PTS <easting_m> <northing_m>
PTS <easting_m> <northing_m>
LNN <line_index>
EOL
```

---

## How It Works

1. Validates that both `-in` and `-out` were supplied, sets `Ellipsoid = 1` (WGS84), and prompts for `merid` on `stdin` if `-merid` was not passed.
2. Opens the input and output files and skips `-skipline` initial lines.
3. **In `-jhc2hy` mode (`whichway == 1`):**
   * Reads all `(lat, lon, label)` tuples into `Points[]`.
   * Iterates over all points: when `(lat == 0 && lon == 0)` is encountered after a non-zero point, increments `nolines` and `lineno`. Otherwise, projects `(lat, lon)` to UTM `(east, north)` via `geoutm()` and appends the point index to `Lines[lineno]`.
   * Writes the `LNS <nolines>` header, followed by `LIN`, `PTS`, `LNN`, and `EOL` blocks for each line.
4. **In `-hy2jhc` mode (`whichway == -1`):**
   * Scans the `.LNW` file line-by-line: writes `0.0 0.0 0.0` on `LIN`, converts `PTS <east> <north>` to `lat lon 0.0` via `utmgeo(..., 'n')`, and writes `0.00 0.00 0.00` on `LNN`.
