---
layout: default
title: hypack2nav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 21
tool_name: hypack2nav
source_path: code/nav/hypack2nav.c
category: Navigation & Georeferencing
input_formats:
- HYPACK RAW ASCII (.RAW)
output_formats:
- .nav
related_tools:
- dohypackLNW
- NMEAtoNav
- Generic_to_Nav
- mergeNav
- appendNav
---

# hypack2nav

## Description
`hypack2nav` converts ASCII HYPACK singlebeam/multibeam raw survey logs (`.RAW`) into the standard 48-byte binary OMG navigation format (`.nav`, `jcu_nav_rec`).

It parses HYPACK `TND` (Time and Date) header lines to establish the survey day's UTC epoch (`stdtime_from_dmy`) and extracts time-of-day and geographic coordinates from `RAW` (Raw Position) sentences, converting packed NMEA-style `DDDMM.MMMM` coordinates into decimal degrees via `GGA2NAV()`.

---

## Usage

```bash
hypack2nav [-v] <infile> <navfile>
```

### Common Workflow Examples

**1. Convert a HYPACK `.RAW` log file to an OMG binary `.nav` file:**

```bash
hypack2nav 001_1430.RAW 001_1430.nav
```

**2. Convert and inspect the resulting binary navigation file:**

```bash
hypack2nav -v survey_line1.RAW survey_line1.nav
navedit -check survey_line1.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<infile>` | **Required.** Input ASCII HYPACK `.RAW` log file containing `TND` and `RAW` records. | None |
| `<navfile>` | **Required.** Output binary `.nav` filename (`jcu_nav_rec` format, opened as `"wb+"`). Must immediately follow `<infile>`. | None |
| `-v` | Increment verbose flag (`verbose_flag++`). | Disabled |

> [!NOTE]
> Positional arguments `<infile>` and `<navfile>` are parsed as a pair in a single loop iteration: the first non-flag argument is assigned to `inname` and the immediately following argument is assigned to `navname`. Place `-v` before `<infile> <navfile>`.

---

## Input & Output Formats

### Input HYPACK `.RAW` ASCII Records
`hypack2nav` scans each line (up to 255 characters) for two HYPACK record identifiers:

1. **`TND` (Time and Date Header):**

   ```text
   TND HH:MM:SS MM/DD/YYYY
   ```
   * Characters at fixed offsets `&date[13]` (month), `&date[16]` (day), and `&date[19]` (year) are converted via `atoi()` and passed to `stdtime_from_dmy(day, month, year)` to compute the base Unix timestamp (`seconds`) at `00:00:00 UTC` of the survey date.

2. **`RAW` (Raw Device Position Record):**

   ```text
   RAW <dev_id> <sec_of_day> <num_vals> <lat_DDDMM_MMMM> <lon_DDDMM_MMMM> ...
   ```
   * Tokenized by spaces (`strtok(string, " ")`):
     * Token `i == 1` (3rd field overall): `sec_of_day` (integer seconds since midnight).
     * Token `i == 3` (5th field overall): packed latitude (`DDDMMSS` / `100 * DDMM.MMMM` convention).
     * Token `i == 4` (6th field overall): packed longitude (`DDDMMSS` / `100 * DDDMM.MMMM` convention).

### Output Binary `.nav` (`jcu_nav_rec`)
For each unique 1-second timestamp (`sec_of_day != time_test || sec_of_day == 0`), a 48-byte `jcu_nav_rec` is written:
* `lat`, `lon`: Decimal degrees converted by `GGA2NAV()`.
* `time`: `seconds + sec_of_day` (Unix epoch seconds since Jan 1, 1970).
* `centisecs`, `azi`, `depth`, `velocity`, `flag[0..3]`: Initialized to `0`.

---

## How It Works

1. **Date Initialization (`TND`):**
   Reads the input file line by line with `fgets()`. Whenever a `TND` substring is encountered, updates `seconds = stdtime_from_dmy(day, month, year)`.
2. **Coordinate Unpacking (`GGA2NAV`):**
   When a `RAW` substring is encountered, extracts the packed latitude and longitude values and converts them to decimal degrees:
   * Degrees are extracted as `a = (int)(value / 10000)`.
   * Whole minutes are extracted as `b = (int)(((value / 10000) - deg) * 100)`.
   * Fractional minutes are extracted as `(value / 100) - (int)(value / 100)` and combined with `b`, divided by `60.0`, and added to (or subtracted from, for negative longitudes where `sign == 1`) `deg`.
3. **1-Hz Deduplication Filter:**
   Compares `sec_of_day` against the previous record's `time_test`. Only writes a new `jcu_nav_rec` via `nav_write()` when `sec_of_day != time_test` (or `sec_of_day == 0`), filtering sub-second duplicate timestamps to 1-Hz intervals.
