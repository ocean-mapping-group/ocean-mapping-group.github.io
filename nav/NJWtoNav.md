---
layout: default
title: NJWtoNav
parent: Navigation Tools
nav_order: 8
tool_name: NJWtoNav
source_path: code/nav/NJWtoNav.c
category: Navigation & Georeferencing
input_formats: ["ASCII text (NJW-SSP towfish/ship UTM navigation)"]
output_formats: [".nav (jcu_nav_rec binary)"]
related_tools: ["AGCtoNav", "AuketoNav", "mergeNav", "appendNav"]
---

# NJWtoNav

## Description
`NJWtoNav` converts 9-column NJW-SSP ASCII towfish and ship UTM navigation files into the 48-byte OMG binary navigation format (`jcu_nav_rec`, `.nav`).

During execution, `NJWtoNav` prompts interactively on `stdin` for the reference ellipsoid (`1` for WGS84 or `2` for NAD27) and the UTM central meridian in decimal degrees longitude, then converts the towfish UTM coordinates (`fish_easting`, `fish_northing`) into geographic latitude and longitude (`utmgeo`) and tracks midnight rollovers across consecutive records.

---

## Usage

```bash
NJWtoNav [OPTIONS] -year <YYYY> -jday <DDD> -comp <output.nav> <njw_ssp_infile(s)>
```

### Common Workflow Examples

**1. Convert an NJW-SSP towfish navigation file with year and Julian day specified on the command line:**
```bash
# Prompts on stdin for Ellipsoid (1=WGS84, 2=NAD27) and Meridian (e.g. -63.0)
NJWtoNav -year 1997 -jday 145 -comp towfish.nav line01.njw
```

**2. Non-interactive pipeline execution using a here-string for ellipsoid and meridian:**
```bash
NJWtoNav -year 1997 -jday 145 -comp towfish.nav line01.njw <<< "1 -63.0"
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output binary `.nav` filename (`jcu_nav_rec` format). | None |
| `<njw_ssp_infile(s)>` | **Required.** One or more 9-column NJW-SSP ASCII input files (up to 300 files). | None |
| `-year <YYYY>` | Survey year. If omitted (`-1`), `NJWtoNav` prompts on `stdin` (`give me the year and JD:`). Two-digit years `< 100` have `1900` added automatically. | `-1` (interactive prompt) |
| `-jday <DDD>` | Starting Julian day (`1..366`). If omitted (`-1`), `NJWtoNav` prompts on `stdin`. Automatically increments by `+1` if `adjusted_time` wraps across midnight. | `-1` (interactive prompt) |
| `-skip <N>` | Decimation value parsed on the command line (`skip = strtoint(*argv)`). | `1` |
| `-v` | Enable verbose flag (`verbose_flag`). | Disabled |

### Interactive `stdin` Prompts
Regardless of command-line flags, `NJWtoNav` always prompts for two parameters at startup:
1. `which ellipsoid (1) WGS84 (2) NAD27` -> reads integer `Ellipsoid` (`1` or `2`).
2. `meridian? (decimal longitude please (e.g. -63.0) ** NOTE hardwired to Northern Hemisphere)` -> reads `double merid`.
3. If `-year` or `-jday` was not provided on the command line, it also prompts: `give me the year and JD:` -> reads `short year, day`.

---

## Input & Output Record Formats

### Input ASCII Format (9 columns)
Each line of an NJW-SSP file must contain 9 whitespace-delimited floating-point numbers:
```text
<nmea_time> <time_corr> <adjusted_time> <fish_easting> <fish_northing> <ship_easting> <ship_northing> <averaged_line_azi> <layback>
```
* `nmea_time` (`double`): Raw NMEA time.
* `time_corr` (`double`): Time correction offset.
* `adjusted_time` (`double`): Seconds since midnight (`00:00:00` UTC). Used to compute the fix timestamp (`stdtime_from_jul_day(year, day, 0, 0, 0) + adjusted_time`).
* `fish_easting`, `fish_northing` (`double`): Towfish UTM coordinates in meters (converted to `lat`, `lon` via `utmgeo(&lat, &lon, merid, fish_easting, fish_northing, 'n')`).
* `ship_easting`, `ship_northing` (`double`): Ship UTM coordinates in meters (read but not written to `.nav`).
* `averaged_line_azi`, `layback` (`float`): Line azimuth and towfish layback (read but not written to `.nav`).

### Output Binary Structure (`jcu_nav_rec`)
Writes 48-byte `jcu_nav_rec` records:
* `lat`, `lon`: Towfish geographic coordinates in decimal degrees.
* `time`: Integer Unix epoch seconds.
* `centisecs`: Fractional hundredths of a second (`(adjusted_time - (int)adjusted_time) * 100.0`).
* `azi`: `0.0`.
* `velocity`: `0.0`.
* `flag[0..3]`: `0`.

---

## How It Works

1. Parses CLI flags and prompts on `stdin` for `Ellipsoid` and `merid` (and `year`/`day` if not supplied).
2. Opens the output `.nav` file (`-comp`).
3. For each input file, reads 9-column records in a `while (fscanf(...) == 9)` loop:
   * **End-of-Day Detection:** Compares `adjusted_time` against `last_adjusted_time`. If `adjusted_time < last_adjusted_time`, prints `tripped on end of day!!` and increments `day += 1`.
   * **Time Conversion:** Computes Unix epoch seconds for midnight of `(year, day)` and adds `adjusted_time`.
   * **UTM Inverse Projection:** Calls `utmgeo()` with Northern Hemisphere (`'n'`) and the user-specified central meridian to convert `fish_easting` and `fish_northing` into `lat` and `lon`.
   * Writes the record via `nav_write()`.
