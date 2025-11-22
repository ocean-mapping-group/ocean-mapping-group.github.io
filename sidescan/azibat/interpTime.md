---
layout: default
title: interpTime
parent: Sidescan Tools
grand_parent: azibat
nav_order: 5
---
# interpTime

## Description
`interpTime` is a utility used to interpolate fractional seconds in a JCU format sidescan file. This is particularly useful for data from sources like AGCDIG SEGY format, which may only have integer second time stamps, especially when dealing with high-ping-rate sonars like the Simrad MS992.

## Usage
```bash
interpTime [-v] [-f<filter_length>] <jcuglofile>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-f<filter_length>` | If specified, the tool will apply a moving average filter to the timestamps instead of interpolating. The filter length is the number of pings to average over (e.g., `-f10` for a 10-ping moving average). |
| `<jcuglofile>` | **Required.** The input JCU format sidescan file. This file is modified in place. |

## How It Works
The tool operates in two modes:

1.  **Interpolation Mode (default):**
    *   It first reads all the timestamps from the input file and calculates the average ping interval (`avdiff`).
    *   It then iterates through the timestamps. If it finds consecutive records with the same integer timestamp, it assumes they are from a high-ping-rate sonar and interpolates fractional seconds for them by adding multiples of the `avdiff`.
    *   The `centisecs` field in the record header is updated with the interpolated fractional second.

2.  **Filtering Mode (`-f`):**
    *   If the `-f` option is used, the tool applies a moving average filter to the timestamps.
    *   It calculates a new timestamp for each record by averaging the timestamps of the surrounding `filter_length` records.
    *   Both the `time` (integer part) and `centisecs` (fractional part) fields in the record header are updated with the new smoothed timestamp.

In both modes, the input file is modified in place.
