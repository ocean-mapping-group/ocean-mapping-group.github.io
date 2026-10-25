---
layout: default
title: dischargeTide
parent: Tide Tools
tool_name: dischargeTide
source_path: code/tide/dischargeTide.c
category: tide
input_formats: ["Environment Canada Daily Discharge CSV"]
output_formats: ["JHC V2 ASCII tide (year jday hour min value)"]
related_tools: ["binTide", "mergeTide"]
---

# dischargeTide

## Overview

`dischargeTide` parses Environment Canada Water Survey daily hydrometric discharge/water-level CSV files (where each row represents day `1..31` across 12 monthly columns `Jan..Dec`) and outputs a chronological 5-column JHC V2 ASCII time series (`year jday 0 0 value`).

---

## Syntax & CLI Options

```bash
dischargeTide [OPTIONS] -tide <in_csv_file> <out_ascii_file>
```

| Option | Description | Default |
|---|---|---|
| `-tide <filename>` | **Required.** Input Environment Canada daily CSV file (with 3 header lines). | None |
| `<out_ascii_file>` | **Required.** Output 5-column JHC V2 ASCII file (`year jday hour min value`). | None |
| `-v` | Enable verbose output showing line parsing and monthly values. | Disabled |

---

## How It Works

1. **Header Skipping:** Reads and skips the first 3 lines of the Environment Canada CSV file.
2. **Comma-Delimited Parsing (`read_line`):**
   - Filters for station IDs matching `08GA022` (Squamish River near Brackendale) or `08GD004` (Homathko River).
   - Extracts `param`, `type`, `year`, `day` (`1..31`), and the 12 monthly floating-point values (`Jan` through `Dec`, skipping the interspersed `SYM` quality symbol columns).
3. **Annual Matrix Transpose:**
   - Buffers rows `day = 1..31` in memory (`thelines[1..31]`).
   - When `day == 31` is reached for a given year, loops over all 12 months (`j = 0..11`) and days (`i = 1..31`), computes the Julian day via `stdtime_dmy_to_jul_day`, and writes non-zero daily values as `year jday 0 0 value`.

---

## Examples

**Convert an Environment Canada daily discharge CSV to binary OMG format:**
```bash
dischargeTide -tide squamish_daily.csv squamish_discharge.asc
binTide -V2 squamish_discharge.asc squamish_discharge.bin
```

---

## Workflow Context

- Used in riverine and fjord hydrographic surveys (such as Squamish River / Howe Sound) to correlate river discharge time series with multibeam surveys and bedform migration.
