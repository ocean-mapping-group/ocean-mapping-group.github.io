---
layout: default
title: readISS_ASCII
parent: Navigation Tools
nav_order: 27
tool_name: readISS_ASCII
source_path: code/nav/readISS_ASCII.c
category: Navigation & Georeferencing
input_formats: ["ISS-60 ASCII Weather / SST (.d01)"]
output_formats: [".Wind (.nav)", ".Pressure", ".airTemp", ".Humidity", ".SST (ASCII)", ".SSV1 (ASCII)", ".SSV2 (ASCII)"]
related_tools: ["Generic_to_Nav", "NMEAtoNav", "appendNav", "mergeNav"]
---

# readISS_ASCII

## Description
`readISS_ASCII` (authored by John Hughes Clarke, May 2022) parses ASCII environmental and oceanographic data files logged by the **ISS-60** integrated survey system (`6Xxxxxxx.d01` files, such as shipboard meteorological weather station logs or sea-surface temperature / surface sound velocity logs) and converts them into OMG binary `.nav` (`jcu_nav_rec`) or ASCII `lat lon value` files.

It supports two distinct ISS-60 ASCII formats:
1. **`-iss_wea` (ISS-60 Weather Format):** Extracts timestamp, position, and true wind speed/direction, converting wind direction from the meteorological convention (*direction wind blows FROM*) to the oceanographic vector convention (*direction wind blows TO*, by adding `180.0°` modulo `360.0°`) and writing a binary `jcu_nav_rec` file `<comp>.Wind` suitable for current/vector plotting and tidal-phase binning in [`appendNav`](appendNav.md).
2. **`-iss_sst` (ISS-60 Sea-Surface Temperature & Sound Velocity Format):** Extracts latitude, longitude, sea-surface temperature (`SST`), and dual surface sound velocity channels (`SV1`, `SV2`), writing three space-delimited ASCII XYZ files: `<comp>.SST`, `<comp>.SSV1`, and `<comp>.SSV2`.

---

## Usage

```bash
# Parse ISS-60 Weather files into binary <out>.Wind
readISS_ASCII [-v] -iss_wea -comp <out_prefix> <raw_d01_files...>

# Parse ISS-60 SST/SSSV files into ASCII <out>.SST, <out>.SSV1, <out>.SSV2
readISS_ASCII [-v] -iss_sst -comp <out_prefix> <raw_d01_files...>
```

### Common Workflow Examples

**1. Convert a directory of ISS-60 weather logs into a binary `.Wind` vector track:**
```bash
readISS_ASCII -iss_wea -comp env/survey_met raw/met/6W*.d01
# Produces: env/survey_met.Wind (in 48-byte binary jcu_nav_rec format)
```

**2. Extract Sea-Surface Temperature and Surface Sound Velocity tracks:**
```bash
readISS_ASCII -iss_sst -comp env/surface_ocean raw/sst/6S*.d01
# Produces ASCII files: env/surface_ocean.SST, env/surface_ocean.SSV1, env/surface_ocean.SSV2
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-iss_wea` | Parse ISS-60 meteorological/weather ASCII records. Creates `<comp>.Wind` (populated with binary `jcu_nav_rec` records) and opens empty placeholder files `<comp>.Pressure`, `<comp>.airTemp`, and `<comp>.Humidity`. | Disabled (one of `-iss_wea` or `-iss_sst` is **required**) |
| `-iss_sst` | Parse ISS-60 Sea-Surface Temperature and Surface Sound Velocity ASCII records. Writes 3-column ASCII `lat lon value` records to `<comp>.SST`, `<comp>.SSV1`, and `<comp>.SSV2`. | Disabled |
| `-comp <prefix>` | **Required.** Output filename prefix (`tidename`) to which `.Wind`, `.SST`, `.SSV1`, `.SSV2`, etc. are appended. | None |
| `<input_files...>` | **Required.** One or more ISS-60 ASCII `.d01` files (up to 300 files in a single run). | None |
| `-delay <sec>` | Parsed on the command line (`timedelay`), reserved for timestamp latency adjustment. | `0.0` |
| `-v` | Enable verbose line-reading and timestamp diagnostics. | Disabled |

---

## Input & Output Record Formats

### 1. Weather Mode (`-iss_wea`)
* **Input ASCII Line Format:**
  Lines beginning with `H` or `#` are treated as header/comment lines and echoed to `stdout`. Data lines have `/` and `:` separators in the first 19 characters replaced by spaces and are parsed as 20 fields:
  ```text
  YYYY/DDD HH:MM:SS.ss latdeg latmin N/S londeg lonmin E/W SensorID:SensorNo app_azi app_spd_ms act_azi act_spd_ms air_temp pressure humidity
  ```
* **Output Binary `<comp>.Wind` (`jcu_nav_rec`):**
  * `lat`, `lon`: Decimal degrees (`S` and `W` negated).
  * `time`, `centisecs`: UTC epoch seconds computed via `stdtime_from_jul_day(year, day, hour, min, 0) + dsec`.
  * `azi`: `(actual_wind_azimuth + 180.0)` wrapped to $[0, 360)^\circ$ (direction wind is blowing **TO**).
  * `velocity`: `actual_wind_speed_ms` (m/s).

### 2. SST / Surface Sound Velocity Mode (`-iss_sst`)
* **Input ASCII Line Format:**
  Data lines have all `/` and `:` characters replaced with spaces and are parsed as 16 fields:
  ```text
  YYYY/DDD HH:MM:SS.ss latdeg latmin N/S londeg lonmin E/W SensorID:SensorNo SST SV1 SV2
  ```
* **Output ASCII Files (`<comp>.SST`, `<comp>.SSV1`, `<comp>.SSV2`):**
  Each file receives one line per observation formatted as:
  ```text
  <latitude> <longitude> <value>
  ```
