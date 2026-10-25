---
layout: default
title: AGCtoNav
parent: Navigation Tools
nav_order: 4
tool_name: AGCtoNav
source_path: code/nav/AGCtoNav.c
category: Navigation & Georeferencing
input_formats: ["ASCII text (AGC, JGSPEC, NRL Joan, DAPSY, OIC UTM nav)"]
output_formats: [".nav (jcu_nav_rec binary)"]
related_tools: ["Generic_to_Nav", "NMEAtoNav", "QNSYtoNav", "mergeNav", "appendNav"]
---

# AGCtoNav

## Description
`AGCtoNav` converts Atlantic Geoscience Centre (AGC) ASCII navigation logs—as well as several other legacy hydrographic and sidescan ASCII navigation formats (`-jgspec`, `-nrl_joan`, `-dapsy`, and `-oicnav` Oceanic Imaging Consultants UTM logs)—into the standard 48-byte OMG binary navigation structure (`jcu_nav_rec`, `.nav`).

It supports concatenating up to 300 input ASCII files into a single output `.nav` file specified with `-comp`, and includes built-in UTM-to-geographic inverse projection (`utmgeo`) using either WGS84 or NAD27 ellipsoids for OIC sidescan navigation logs.

---

## Usage

```bash
AGCtoNav [OPTIONS] -comp <output.nav> <input_ascii_file(s)>
```

### Common Workflow Examples

**1. Convert standard AGC ASCII navigation files for a given survey year:**
```bash
AGCtoNav -year 1995 -comp line01.nav raw_agc_01.txt raw_agc_02.txt
```

**2. Convert Oceanic Imaging Consultants (`-oicnav`) UTM navigation using WGS84 and central meridian -123°:**
```bash
AGCtoNav -oicnav -merid -123.0 -comp oic_track.nav line1.oicnav
```

**3. Convert OIC UTM navigation on NAD27 datum:**
```bash
AGCtoNav -oicnav -nad27 -merid -63.0 -comp oic_nad27.nav line1.oicnav
```

**4. Convert NRL (`-nrl_joan`), DAPSY (`-dapsy`), or JGSPEC (`-jgspec`) ASCII logs:**
```bash
AGCtoNav -nrl_joan -comp nrl_track.nav nrl_nav.txt
AGCtoNav -dapsy -comp dapsy_track.nav dapsy_nav.txt
AGCtoNav -jgspec -comp jgspec_track.nav jgspec_nav.txt
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output binary navigation filename (`jcu_nav_rec` format). | None |
| `<mergefile(s)>` | **Required.** One or more input ASCII navigation files (up to 300 files). | None |
| `-year <YYYY>` | Survey year used when parsing default AGC timestamps (which only contain `DDDHHMMSS` Julian day and time). | Unset |
| `-jday <DDD>` | Julian day override (parsed by CLI parser; overwritten by file records in most modes). | Unset |
| `-oicnav` | Parse Oceanic Imaging Consultants (OIC) 5-column UTM ASCII navigation format (`rtime heading course easting northing`). Requires `-merid`. | Disabled |
| `-merid <deg>` | UTM central meridian in decimal degrees longitude (e.g., `-123.0` or `-63.0`). **Required** when `-oicnav` is enabled; hardwired to Northern Hemisphere (`'n'`). | `0.0` |
| `-nad27` | Used with `-oicnav`. Sets `Ellipsoid = 2` (NAD27) instead of `Ellipsoid = 1` (WGS84) for UTM-to-geographic conversion. | Disabled (WGS84) |
| `-jgspec` | Parse 5-column JGSPEC ASCII navigation format (`id YYMMDD HHMMdm lat lon`) with deduplication on consecutive timestamp strings. | Disabled |
| `-nrl_joan` | Parse 8-column NRL (Joan) ASCII navigation format (`year jday hour min sec millisec lat lon`). | Disabled |
| `-dapsy` | Parse 7-column DAPSY ASCII navigation format (`year jday hour min sec lat lon`). | Disabled |
| `-skip <N>` | Decimation factor parsed on the command line (`skip = strtoint(*argv)`). | `1` |
| `-new` | Increments internal `new_flag` counter. | Disabled |
| `-v` | Enable verbose output (prints parsed Julian Day in `-jgspec` mode). | Disabled |

---

## Input & Output Record Formats

### Input ASCII Formats

1. **Default AGC Format (3 columns):**
   ```text
   <DDDHHMMSS> <lat_deg> <lon_deg>
   ```
   * Column 1 (`string`): 9-character packed string where characters `0..2` are Julian Day (`day`), `3..4` are `hour`, `5..6` are `min`, and `7..8` are `sec`. Requires `-year <YYYY>` on the command line to compute Unix epoch time via `stdtime_from_jul_day(year, day, hour, min, sec)`.

2. **JGSPEC Format (`-jgspec`, 5 columns):**
   ```text
   <id_str> <YYMMDD> <HHMMdd> <lat_deg> <lon_deg>
   ```
   * `<YYMMDD>` (`str2`): 2-digit year (`1900 + year`), 2-digit month, 2-digit day of month (converted to Julian day using a non-leap cumulative month table).
   * `<HHMMdd>` (`str3`): 2-digit hour, 2-digit minute, and 2-digit tenths of a minute (`sec = decmin * 6.0`). Only writes a fix when the first 5 characters of `str3` differ from the previous record (`strncmp(str3, last_str3, 5)`).

3. **NRL Joan Format (`-nrl_joan`, 8 columns):**
   ```text
   <year> <jday> <hour> <min> <sec> <millisec> <lat_deg> <lon_deg>
   ```
   * Converts `millisec` to hundredths of a second: `tide_rec.centisecs = millisec / 10`.

4. **DAPSY Format (`-dapsy`, 7 columns):**
   ```text
   <year> <jday> <hour> <min> <sec> <lat_deg> <lon_deg>
   ```
   * Sets `tide_rec.centisecs = 0`.

5. **OIC UTM Format (`-oicnav`, 5 columns):**
   ```text
   <unix_time_sec> <heading_deg> <course_deg> <easting_m> <northing_m>
   ```
   * Converts `(easting, northing)` to `(lat, lon)` in decimal degrees via `utmgeo(&lat, &lon, merid, easting, northing, 'n')`.
   * Stores heading in radians in `tide_rec.azi` (`heading * M_PI / 180.0`) and splits `rtime` into integer seconds (`tide_rec.time`) and fractional hundredths (`tide_rec.centisecs`).

### Output Binary Format (`jcu_nav_rec`)
Writes 48-byte `jcu_nav_rec` records sequentially via `nav_write()` with `flag[0..3] = 0`, `velocity = 0.0`, and `azi = 0.0` (except in `-oicnav` mode where `azi` holds heading in radians).

---

## How It Works

1. Parses command-line flags and verifies that at least one input file is provided and that `-merid` is non-zero if `-oicnav` is selected.
2. Opens the output file (`-comp`) in write mode (`"w"`).
3. Iterates through each input file in order, scanning whitespace-delimited fields according to the active format flag (`-jgspec`, `-nrl_joan`, `-dapsy`, `-oicnav`, or default AGC).
4. Converts calendar or Julian dates into Unix epoch seconds (`stdtime_from_jul_day`) and writes each populated `jcu_nav_rec` structure to the output `.nav` file.
