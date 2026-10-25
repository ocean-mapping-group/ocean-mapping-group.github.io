---
layout: default
title: Generic_to_Nav
parent: Navigation Tools
nav_order: 7
tool_name: Generic_to_Nav
source_path: code/nav/Generic_to_Nav.c
category: Navigation & Georeferencing
input_formats: ["ASCII CSV / text (Marine Institute Env, Starmon TD, MarineTraffic AIS, BGS Shapefile Extract, AutoWeather1, GrafNav)"]
output_formats: [".nav (jcu_nav_rec binary)", ".nav.llz (MarineTraffic mode)"]
related_tools: ["AGCtoNav", "NMEAtoNav", "PNAVtoNav", "QNSYtoNav", "dumpnav"]
---

# Generic_to_Nav

## Description
`Generic_to_Nav` is a multi-format ASCII-to-binary navigation converter that strips punctuation delimiters (colons, slashes, commas, dashes, degree symbols, quotes, and ISO `T` separators) from heterogeneous ASCII log files and packs the resulting timestamps, geographic coordinates, and environmental/kinematic attributes into 48-byte OMG `jcu_nav_rec` (`.nav`) files.

It includes pre-configured parser profiles for six specialized ASCII datasets:
1. **`-MI_env_data`** (default): Marine Institute environmental sensor logs (`DD-Mon-YYYY HH:MM:SS.fff`, lon, lat, and up to 10 environmental channels).
2. **`-Starmon_TD_data`**: Star-Oddi Starmon temperature-depth logger files (with European comma/decimal-point swapping).
3. **`-MarineTraffic`**: AIS vessel track exports (`MMSI`, status, speed, lon, lat, course, heading, timestamp), simultaneously writing a segmented `<outfilename>.llz` file split by MMSI and maximum distance jumps (`-maxdist`).
4. **`-AutoWeather1`**: Automated weather station logs (NMEA-style `DDMM.mmmm` coordinates + true/relative wind speed and direction).
5. **`-BGS_shape_extract`**: British Geological Survey shapefile coordinate extracts (`DDD° MM' SS.ss" E/W/N/S`).
6. **`-GrafNav`**: Waypoint GrafNav post-processed GNSS trajectories (16-line header, DMS coordinates, ellipsoidal height, standard deviations, and quality flag).

---

## Usage

```bash
Generic_to_Nav [DATA_TYPE_FLAG] [OPTIONS] -comp <output.nav> <input_ascii_file(s)>
```

### Common Workflow Examples

**1. Convert Marine Institute environmental data, storing channel 4 in `azi` and rejecting `-999.0`:**
```bash
Generic_to_Nav -MI_env_data -val_to_use 4 -invalid -999.0 -comp env_ch4.nav mi_sensor_log.csv
```

**2. Convert Waypoint GrafNav post-processed GNSS export (automatically skips 16 header lines):**
```bash
Generic_to_Nav -GrafNav -comp grafnav_rtk.nav GrafNav_Export.txt
```

**3. Convert MarineTraffic AIS CSV logs into `.nav` and segmented `.nav.llz` tracks:**
```bash
Generic_to_Nav -MarineTraffic -maxdist 1000 -comp ais_tracks.nav marinetraffic_export.csv
```

**4. Convert shipboard automated weather station logs (wind direction in `azi`, wind speed in `velocity`):**
```bash
Generic_to_Nav -AutoWeather1 -comp wind_track.nav weather_station.csv
```

---

## Arguments

### Data Type Profiles

| Option | Description | Implied Header Skip & Delimiter Stripping |
|---|---|---|
| `-MI_env_data` | **Default.** Marine Institute environmental data (`DD Mon YYYY HH:MM:SS.mmm lon lat val[0..9]`). Supports `Sep` and `Oct` month strings. | `skip_first_lines = 0`; strips `:`, `;`, `,`, `'`, `°`, `/` |
| `-GrafNav` | Waypoint GrafNav GNSS export (`MM/DD/YYYY HH:MM:SS.ss gpsweek gpstime latDMS lonDMS H_Ell SDHori SDHeig Qual`). Stores `H_Ell` in `azi`. | `skip_first_lines = 16`; strips `:`, `/` |
| `-MarineTraffic` | MarineTraffic AIS export (`MMSI Status Speed_tenths_kts lon lat Course Heading YYYY-MM-DD HH:MM:SS`). Negates `lon` (since `-` is stripped), stores `Course` in `azi` and `Speed_Knots` in `velocity`, and writes `<out>.llz`. | `skip_first_lines = 1`; strips `:`, `,`, `-` |
| `-AutoWeather1` | Automated weather station (`YYYY-MM-DDTHH:MM:SS heading lat_DDMM lon_DDMM wind_dir rel_wind_dir wind_speed rel_wind_speed`). Stores `wind_dir` in `azi` and `wind_speed` in `velocity`. | `skip_first_lines = 1`; strips `-`, `:`, `T` |
| `-BGS_shape_extract` | BGS shapefile point extract (`id lon_deg lon_min lon_sec EW lat_deg lat_min lat_sec NS`). Negates `lon` and writes timeless positions (`year = -1`). | `skip_first_lines = 1`; strips `,`, `°`, `'`, `"` |
| `-Starmon_TD_data` | Star-Oddi Starmon TD logger (`count DD.MM.YYYY HH:MM:SS,ff val0 val1`). Replaces `.` with space and `,` with `.`. | `skip_first_lines = 0`; `strip_decimal_point = 1`, `switch_comma_point = 1`, `strip_colon = 1` |

### General & Filtering Options

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output binary `.nav` filename. In `-MarineTraffic` mode, also creates `<filename>.llz`. | None |
| `<Generic_ASCII_file(s)>` | **Required.** One or more input ASCII files (up to 300 files). | None |
| `-skip_first_lines <N>` | Override the number of header lines skipped at the start of the first file. | Set by data type (`0`, `1`, or `16`) |
| `-val_to_use <idx>` | Index (`0..9`) of the value array `val[]` to store in `tide_rec.azi` (used primarily with `-MI_env_data`). | `0` |
| `-invalid <val>` | In `-MI_env_data` mode, skip writing records where `val[val_to_use] == invalid`. | `-999.0` |
| `-maxdist <meters>` | In `-MarineTraffic` mode, insert a line-break separator (`0.0 0.0 -1`) in `<comp>.llz` whenever the distance between consecutive fixes exceeds `<meters>`. Also inserts `0.0 0.0 0` when `MMSI` changes. | `1000.0` |
| `-year <YYYY>` | Explicit year override. | `-1` (parsed from file) |
| `-strip_slash` | Replace `/` with space before scanning each line. | Set by profile |
| `-strip_colon` | Replace `:` with space before scanning each line. | Set by profile |
| `-v` | Enable verbose output (prints character-stripped lines and each parsed timestamp/value). | Disabled |

---

## How It Works

1. **Line Reading & Comment Filtering:**
   Reads each input file line-by-line via `getc_line()`. Skips the first `skip_first_lines` lines, and automatically treats any line starting with `'H'` or `'#'` as a comment.
2. **In-Place Character Sanitization:**
   Scans the line buffer and replaces active delimiter characters (`'T'`, `'-'`, `'/'`, `'.'`, `','`, `':'`, `';'`, degree symbol `-80`, single quote `39`, double quote `34`) with spaces (or swaps `,` to `.` for European decimals in `-Starmon_TD_data`).
3. **Profile-Specific Parsing & Coordinate Conversion:**
   Extracts date/time components, converts DMS or NMEA `DDMM.mmmm` coordinates to decimal degrees, and computes Unix epoch time (`stdtime_dmy_to_jul_day` + `stdtime_from_jul_day`).
4. **Binary `.nav` Output:**
   Populates `tide_rec` (`lat`, `lon`, `azi = val[val_to_use]`, `velocity`, `time`, `centisecs`) and writes it via `nav_write()`.
