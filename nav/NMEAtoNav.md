---
layout: default
title: NMEAtoNav
parent: Navigation Tools
nav_order: 9
tool_name: NMEAtoNav
source_path: code/nav/NMEAtoNav.c
category: Navigation & Georeferencing
input_formats: ["ASCII NMEA-0183 logs ($GPGGA, $INGGA, $GNGGA, $PNCTGGA, $GPGGK, $INGGK, $GNGGK, $GPZDA, $INZDA, $GPGLL, $INGLL, $GPVTG, $HEHDT, $SDDPT, $PTNL)"]
output_formats: [".nav (jcu_nav_rec binary)", "ASCII text (-ascii)", ".merged (SingleBeam HDCS v3 with -sbes)"]
related_tools: ["Generic_to_Nav", "QNSYtoNav", "mergeNav", "appendNav", "fixnav"]
---

# NMEAtoNav

## Description
`NMEAtoNav` parses raw NMEA-0183 serial ASCII log files and converts navigation, heading, speed, RTK height, single-beam depth (`$SDDPT`), or Trimble `$PTNL` attitude/baseline telegrams into 48-byte OMG binary navigation files (`.nav`), diagnostic ASCII tables (`-ascii`), or OMG-HDCS v3 SingleBeam `.merged` files (`-sbes`).

By default, `NMEAtoNav` accepts both `GGA` and `GGK` position telegrams with the `$GP` talker prefix and GPS quality indicators between `1` and `6`. Talker prefixes (`-GP`, message types `-IN`, `-GN`, `-PNCT`), specific telegram selectors (`-use_GGA`, `-use_GGK`, `-use_GLL`), quality thresholds (`-minGPS_quality`, `-maxGPS_quality`), and date sources (`-year`/`-jday` vs. `-use_ZDA` or `-YRJD_from_nav`) can all be tailored on the command line.

---

## Usage

```bash
NMEAtoNav [OPTIONS] -comp <output_file> <input_nmea_file(s)>
```

### Common Workflow Examples

**1. Convert standard `$GPGGA` logs using `$GPZDA` for date stamps:**
```bash
NMEAtoNav -GP -use_GGA -use_ZDA -comp vessel.nav nmea_serial_*.log
```

**2. Extract only RTK Fixed (`GPS_quality == 4`) `$INGGA` fixes with ellipsoidal height stored in `azi`:**
```bash
NMEAtoNav -IN -use_GGA -minGPS_quality 4 -maxGPS_quality 4 -ellipsoid \
    -year 2022 -jday 185 -check_for_EOD -comp rtk_ellipsoid.nav posmv_nmea.log
```

**3. Inherit Year and Julian Day from an existing `.nav` file and apply a 0.2s latency delay:**
```bash
NMEAtoNav -YRJD_from_nav merged/JD185/0001.nav -delay 0.2 -comp aux_gps.nav aux_nmea.txt
```

**4. Convert `$GPGLL` + `$SDDPT` single-beam echosounder logs directly into an OMG-HDCS `.merged` file:**
```bash
NMEAtoNav -use_GLL -use_ZDA -sbes -comp sbes_line01.merged echosounder.nmea
```

---

## Arguments

### Talker ID & Telegram Selection

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output filename (`.nav`, ASCII text, or `.merged` if `-sbes`). | None |
| `<mergefile(s)>` | **Required.** One or more input NMEA-0183 log files (up to 300 files). | None |
| `-GP` | Accept `$GP...` talker prefix (`device_type = GP`). | **Default** |
| `-IN` | Accept `$IN...` (Integrated Navigation, e.g., POS MV) talker prefix. | Disabled |
| `-GN` | Accept `$GN...` (Multi-GNSS) talker prefix. | Disabled |
| `-PNCT` | Accept `$PNCT...` talker prefix (added for USNS *Maury* 2016). | Disabled |
| `-use_GGA` | Only extract position fixes from `GGA` telegrams (rejects `GGK` and `GLL`). | `use_GGA = 1`, `use_GGK = 1` |
| `-use_GGK` | Only extract position fixes from `GGK` telegrams (rejects `GGA` and `GLL`). Note: receiving a `GGK` automatically enables `use_ZDA` using the date embedded in the `GGK` telegram. | `use_GGA = 1`, `use_GGK = 1` |
| `-use_GLL` | Only extract position fixes from `GLL` telegrams (`GPGLL` or `INGLL`; rejects `GGA` and `GGK`). Assigns `GPS_quality = 1`. | Disabled (`0`) |
| `-PTNL` | Parse Trimble `$PTNL` attitude/baseline telegrams (accepts baselines within $\pm 5\%$ of `3.04` m). Stores `yaw` in `azi`, `tilt` in `velocity`, and `baseline * 1000` in `depth`. | Disabled |

### Date, Time & Latency Options

| Option | Description | Default |
|---|---|---|
| `-year <YYYY>` | 4-digit survey year. | Unset |
| `-jday <DDD>` | Julian day (`1..366`), or day-of-month if `-month <MM>` is also specified. | Unset |
| `-month <MM>` | If provided (`month != -1`), converts `-jday <day>` and `-month <MM>` to Julian day via `stdtime_dmy_to_jul_day(day, month, year)`. | `-1` |
| `-use_ZDA` | Extract calendar date (`day`, `month`, `year`) dynamically from `$GPZDA` / `$INZDA` (or `GGK`) telegrams. Skips `GGA` fixes prior to the first `ZDA` and handles midnight rollover when `GGA` precedes `ZDA`. | Disabled |
| `-YRJD_from_nav <navfile>` | Read record `0` of `<navfile>` (`jcu_nav_rec`) and extract its UTC `year` and `jday`. | Disabled |
| `-check_for_EOD` | When not using `-use_ZDA`, detect hour reversals (`gpgga.hour < hour`) across midnight and increment `day++`. | Disabled |
| `-delay <secs>` | Time offset (in seconds) added to every fix timestamp (`dtime += timedelay`). | `0.0` |

### Quality Filtering & Attribute Mapping

| Option | Description | Default |
|---|---|---|
| `-minGPS_quality <Q>` | Minimum acceptable `GGA`/`GGK` GPS quality indicator. | `1` |
| `-maxGPS_quality <Q>` | Maximum acceptable `GGA`/`GGK` GPS quality indicator. | `6` |
| `-want_terminator <4chars>` | Only accept `GGA` telegrams whose 4-character checksum/terminator string matches `<4chars>` (e.g., `0327`). | Disabled |
| `-hdt` | Store true heading from `$HEHDT` (or `$GPVTG`) in `tide_rec.azi` instead of antenna altitude. (Note: `unpackHDT` specifically checks for `HEHDT` when triggered by `GPHDT`). | Disabled (`gpgga.antenna_altitude`) |
| `-ellipsoid` | Store ellipsoidal height (`gpgga.antenna_altitude + gpgga.geoid_height`) in `tide_rec.azi`. | Disabled |
| `-separation` | Store geoidal separation (`gpgga.geoid_height`) in `tide_rec.azi`. | Disabled |
| `-sbes` | Write an OMG-HDCS v3 `SingleBeam` `.merged` file when `$SDDPT` depth telegrams or `$PTNL` telegrams are encountered. | Disabled |
| `-ascii` | Output ASCII text instead of binary `jcu_nav_rec`. Default columns: `dtime year day hour min sec fracsec quality num_sats HDOP altitude corr_age`. | Binary `.nav` |
| `-hdop` / `-nosats` / `-corrage` | Used with `-ascii`. Outputs 3-column ASCII (`lat lon <metric>`) with `HDOP`, `num_sats`, or `correction_age`. | Default 12-column ASCII |
| `-skip <N>` | Decimation value parsed on the command line. | `1` |
| `-new` | Increments internal `new_flag` counter. | Disabled |
| `-v` | Enable verbose diagnostic output for every NMEA sentence unpacked. | Disabled |

---

## Output Format Details

### Binary `.nav` Mapping (`jcu_nav_rec`)
* `lat`, `lon`: Decimal degrees from `GGA`, `GGK`, or `GLL`.
* `time`, `centisecs`: Unix epoch seconds + `gpgga.millisecs / 10`.
* `azi`: By default, `gpgga.antenna_altitude` (meters). Overridden by `-hdt` (`true_heading`), `-ellipsoid` (`antenna_altitude + geoid_height`), or `-separation` (`geoid_height`).
* `velocity`: Speed over ground `gpvtg.SOG_1` if `$GPVTG` is present, otherwise `0.0`.
* `depth`: `gpgga.antenna_altitude * 100.0` (centimeters as integer).
* `flag[1]`: `gpgga.GPS_quality`.
* `flag[2]`: `gpgga.num_sats`.
* `flag[0]`, `flag[3]`: `0`.

---

## How It Works

1. Initializes date/time from `-year`/`-jday`/`-month` or reads record `0` of `-YRJD_from_nav`.
2. Scans each input file character-by-character, splitting telegrams on `$` (`0x24`) or `\n`.
3. Dispatches each telegram to the `jNMEA` library parsers (`jnmea_read_INGGA`, `jnmea_read_INGGK`, `jnmea_read_INZDA`, `jnmea_read_GPGLL`, `jnmea_read_GPVTG`, `jnmea_read_PTNL`, `unpackHDT`, `unpackDPT`). Note that `GGA` sentences shorter than 51 chars, longer than 89 chars, or containing $\ge 4$ non-ASCII bytes are rejected to guard against serial line noise.
4. Filters fixes by `minGPS_quality .. maxGPS_quality` and optional `-want_terminator`, computes UTC Unix epoch time (handling `ZDA` updates or `-check_for_EOD` midnight rollovers), and writes binary `.nav`, ASCII, or HDCS `.merged` records.
