---
layout: default
title: jNMEA
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/jNMEA.c
category: Navigation, Attitude & Sensor Telegram Parsers
related_tools:
- NMEAtoNav
- RT
- RTLite
- read_kmall
- readEA600
- humm2omg
- oceanReader
- plotSVP
- upAGCDIG
module_name: jNMEA
header_path: code/subr/jNMEA.h
---

# `jNMEA` — NMEA-0183 Navigation, Timing, and Attitude Telegram Parser

## Overview & Purpose
The `jNMEA` module (`code/subr/jNMEA.c` and `code/subr/jNMEA.h`) parses standard NMEA-0183 ASCII comma-delimited navigation, timing, velocity, and attitude sentences into strongly typed C structures. Originally written by John Hughes Clarke in September 1997 and extended by Brian Danforth (2005) and JHC (2008–2010), it handles talker prefixes from standalone GPS (`$GP`), multi-constellation GNSS (`$GN`), integrated navigation systems (`$IN`), and Trimble proprietary attitude strings (`$PTNL`), automatically converting `DDMM.MMMM` latitude/longitude strings into signed double-precision decimal degrees and extracting millisecond-precision UTC timestamps.

---

## Key Data Structures (`jNMEA.h`)

### 1. Position Fix Telegrams (`GGA`, `GGK`, `RMC`, `GLL`)
- **`NMEA_GPGGA_telegram` (`$GPGGA`, `$INGGA`, `$GNGGA`):**
  - **Time:** `short hour, min, secs, millisecs;`
  - **Position:** `int lat_deg; double lat_min; short lat_sign; int lon_deg; double lon_min; short lon_sign;` and precomputed signed decimal degrees `double lat, lon;`.
  - **Quality & Geodesy:** `int GPS_quality` (`0` invalid, `1` SPS, `2` DGPS, `3` PPS, `4` RTK Fixed, `5` RTK Float), `int num_sats`, `float HDOP`, `float antenna_altitude`, `char antenna_units`, `float geoid_height`, `char geoid_units`, `float correction_age`, `char Terminator[10]`.
- **`NMEA_GPGGK_telegram` (`$GPGGK`, `$INGGK`):**
  - Adds calendar date (`short day, month, year`) and RTK/PPK quality flags alongside `lat`, `lon`, and ellipsoidal `antenna_altitude`.
- **`NMEA_GPRMC_telegram` (`$GPRMC`, `$INRMC`):**
  - Recommended Minimum Navigation Information: UTC time (`hour, min, secs, millisecs`), `char status` (`'A'` valid, `'V'` warning), `lat`, `lon`, speed over ground `float speed` (knots), course over ground `float course` (degrees), date (`day, month, year`), and `float magneticVariation` (`magVarSign`).
- **`NMEA_GPGLL_telegram` (`$GPGLL`, `$INGLL`):**
  - Geographic Latitude/Longitude and UTC fix time (`hour, min, secs, millisecs`, `lat`, `lon`).

### 2. Timing, Velocity & Attitude Telegrams (`ZDA`, `VTG`, `VHW`, `PTNL`)
- **`NMEA_GPZDA_telegram` (`$GPZDA`, `$INZDA`, `$GNZDA`):**
  - UTC timestamp (`hour, min, secs, millisecs`) and full calendar date (`day, month, year`).
- **`NMEA_GPVTG_telegram` (`$GPVTG`, `$INVTG`, `$GNVTG`):**
  - Track made good and ground speed: `float true_heading`, `float magnetic_heading`, `float SOG_1` (knots), `float SOG_2` (km/h).
- **`NMEA_LGVHW_telegram`:**
  - Water speed and heading (`ships_gyro`, `magnetic_compass`, `speed_knots`).
- **`TRIM_PTNL_telegram` (`$PTNL,AVR,...`):**
  - Trimble dual-antenna GNSS attitude telegram containing UTC time (`hour, min, secs, millisecs`), `float yaw` (degrees), `float tilt` (pitch/roll in degrees), and `float baseline` separation (meters).

---

## Public Functions & Signatures

```c
void jnmea_read_INGGA(char *telegram, int tot_char, int verbose_flag, NMEA_GPGGA_telegram *gpgga_str);
void jnmea_read_INGGK(char *telegram, int tot_char, int verbose_flag, NMEA_GPGGK_telegram *gpggk_str);
void jnmea_read_INRMC(char *telegram, int tot_char, int verbose_flag, NMEA_GPRMC_telegram *gprmc_str);
void jnmea_read_GPGLL(char *telegram, int tot_char, int verbose_flag, NMEA_GPGLL_telegram *gpgll_str);
void jnmea_read_INZDA(char *telegram, int tot_char, int verbose_flag, NMEA_GPZDA_telegram *gpzda_str);
void jnmea_read_GPVTG(char *telegram, int tot_char, int verbose_flag, NMEA_GPVTG_telegram *gpvtg_str);
void jnmea_read_PTNL (char *telegram, int tot_char, int verbose_flag, TRIM_PTNL_telegram  *ptnl_str);
```

- **Parsing Mechanics:**
  - Each parser scans `telegram` up to `tot_char` bytes for the matching 5-character NMEA mnemonic (e.g., `GPGGA`, `INGGA`, or `GNGGA`), replaces commas `,` with spaces in a local scratch buffer while carefully preserving empty comma-delimited fields (`,,`), and extracts fields sequentially via `sscanf()`.
  - Latitude (`DDMM.MMMM`) and Longitude (`DDDMM.MMMM`) are split into integer degrees and floating-point minutes, signed according to the hemisphere character (`'N'`/`'S'`, `'E'`/`'W'`), and stored in `lat` and `lon` as `(deg + min / 60.0) * sign`.

---

## How It Fits Into the OMG Architecture
`jNMEA` is the standard ASCII navigation decoder across all OMG ingestion and real-time tools:
- **Standalone Navigation Converters (`NMEAtoNav`):** Converts raw logged NMEA serial streams directly into binary OMG `.nav` files.
- **Sonar Format Converters (`read_kmall`, `readEA600`, `humm2omg`, `oceanReader`, `upAGCDIG`, `plotSVP`):** Decodes embedded NMEA strings encapsulated inside Kongsberg `.kmall`, Simrad EA400/EA600 `.raw`, and Humminbird sonar packets.
- **Real-Time Acquisition (`RT`, `RTLite`):** Parses live UDP/serial NMEA broadcasts (`RT_unravel.c`, `RTlite_unravel.c`) to geolocate incoming multibeam pings.
