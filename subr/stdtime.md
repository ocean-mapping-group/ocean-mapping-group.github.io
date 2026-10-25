---
layout: default
title: stdtime
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/stdtime.c
category: Core System, I/O & Time Utilities
related_tools:
- support
- OMG_HDCS_jversion
- sonar_geometry
- xtf_utils
module_name: stdtime
header_path: code/subr/stdtime.h
---

# stdtime

## Overview
`stdtime` (`stdtime.c` / `stdtime.h`), originally written by Guy Carpenter (Jan 1990) and extended by Jonathan Beaudoin (2007) and John Hughes Clarke (2024), is the standard **Unix epoch and Julian day time conversion library** used across almost every Ocean Mapping Group program.

In hydrographic data processing, sonar datagrams variably report timestamps as Year/Month/Day (`YYYY-MM-DD`), Year and Day-of-Year (`YYYY/DOY`, referred to throughout the OMG codebase as `jul_day` $1..366$), or Unix epoch seconds since `00:00:00 UTC, January 1, 1970`. `stdtime` converts seamlessly between calendar dates, Julian days (day-of-year), Unix epoch timestamps, and human-readable formatted strings.

---

## Global Variables & Constants

- `extern int stdtime_days_in_month[12]` — Lookup array `{31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}` giving the number of days in each month (1–12) for a non-leap year.
- `IS_LEAP_YEAR(int year)` — Returns `1` if `year` is a leap year (`year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)`), `0` otherwise.

---

## Public Functions

| Function | Signature | Description |
|---|---|---|
| `stdtime_dmy_to_jul_day` | `short stdtime_dmy_to_jul_day(short day, short month, short year)` | Converts a calendar date (`day` $1..31$, `month` $1..12$, full 4-digit `year` e.g. `2025`) into a 1-based Day of Year (`1..365`, or `1..366` in leap years). |
| `stdtime_from_dmy` | `int stdtime_from_dmy(short day, short month, short year)` | Returns the Unix timestamp (seconds since `00:00:00 1-Jan-1970`) for `00:00:00` on the given `day`, `month`, and 4-digit `year`. |
| `stdtime_from_jul_day` | `int stdtime_from_jul_day(short year, short day, short hour, short min, short sec)` | Converts a 4-digit `year`, 1-based Day of Year (`day` $1..366$), `hour` ($0..23$), `min` ($0..59$), and `sec` ($0..59$) into Unix epoch seconds since `1-Jan-1970`. Used heavily by CLI flags like `-time_start <yr> <jd> <hr> <min> <sec>` in `mos2` and `weigh_grid`. |
| `stdtime_nicetime` | `int stdtime_nicetime(char *result, char *format, int time)` | Formats a Unix timestamp (`time` in seconds since 1970, evaluated via `gmtime()`) into `result` according to `format`. |
| `stdtime_now` | `int stdtime_now(void)` | Queries `gettimeofday()` and returns the current local time in seconds since `1-Jan-1970`. |
| `stdtime_now_double` | `int stdtime_now_double(double *dtime)` | Queries `gettimeofday()` and writes high-precision seconds (including microsecond fraction `tv_usec / 1e6`) into `*dtime`. |

---

## `stdtime_nicetime` Format Specifiers

`stdtime_nicetime(result, format, time)` supports custom `%` format tokens (with optional width/precision digits such as `%02h` or `%.2m`):

| Token | Output | Example |
|---|---|---|
| `%Y` | 4-digit year string | `2025` |
| `%j` | Day of year (`tm_yday + 1`, $1..366$) | `185` |
| `%M` | 3-letter month abbreviation | `Jul` |
| `%n` | Numeric month ($1..12$) | `7` |
| `%D` | Day of month ($1..31$) | `4` |
| `%W` | 3-letter weekday abbreviation | `Fri` |
| `%T` | Full `HH:MM:SS` time string | `14:05:09` |
| `%h` | Zero-padded hour (`%02d`, $00..23$) | `14` |
| `%m` | Zero-padded minute (`%02d`, $00..59$) | `05` |
| `%s` | Zero-padded second (`%02d`, $00..59$) | `09` |

---

## Architectural Role
`stdtime` is linked into virtually every executable in the repository. Because OMG-HDCS `.merged` and `.orientation` files store `refTime` (in hundreds of seconds since 1970) plus scaled `timeOffset` integers, `stdtime` provides the universal bridge between binary HDCS timestamps, raw sonar datagram headers (Simrad, Reson, XTF, JSF, GSF), and user-facing Julian-day command-line arguments.
