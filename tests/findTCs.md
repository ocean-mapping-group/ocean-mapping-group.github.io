---
layout: default
title: findTCs
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 6
tool_name: findTCs
source_path: code/tests/findTCs.c
category: Passive Acoustic & Time-Series Classification (tests)
input_formats:
- spectrafile (2-column ASCII spectral time series)
- filtfile (2-column ASCII high-pass filtered envelope time series)
output_formats:
- classfile (10-line per-minute YES/NOO spike classification table)
- .wav.datetime (2-line start/end Julian day & Unix epoch timestamp sidecar)
related_tools:
- testFIR
- testChirp
---

# findTCs

## Overview
`findTCs` (`code/tests/findTCs.c`, authored by John Hughes Clarke in July 2018) is a time-series transient spike classifier and timestamp sidecar generator created to detect impulsive acoustic events (such as turbidity current / bedload impact transients or hydrophone clicks, "TCs") in 10-minute (`600 s`) passive acoustic `.wav` recordings sampled at $44.1\text{ kHz}$.

It performs two functions:
1. **Timestamp Sidecar Generation (`.wav.datetime`):** Parses compact filename date-time strings from either the 2018 format (`-yrmon 2018-06 -dahrmnse 20143218`) or the 2019 ISO-like format (`-yrmon 2018-06 -yrmondahrmnse 20190621T060810`), converts them to Julian Day (`stdtime_dmy_to_jul_day`) and Unix epoch seconds since 1970 (`stdtime_from_jul_day`), and writes start/end timestamps to `<yrmon>/<stamp>.wav.datetime`.
2. **Per-Minute Transient Spike Classification:** Reads a 2-column ASCII spectral time series (`spectrafile`) and a matching 2-column high-pass filtered time series (`filtfile`), divides the 10-minute record into 10 one-minute windows, counts how many quarter-second samples exceed `|filthigh| > threshold`, and labels each minute with `YES` (if `noabove > aboveOK`) or `NOO`.

---

## Syntax & CLI Options

```bash
findTCs [-v] [-yrmon <YYYY-MM>] [-dahrmnse <DDHHMMSS> | -yrmondahrmnse <YYYYMMDDTHHMMSS>] \
        [-reclen_secs <secs>] [-just_datetime] \
        [-threshold <val>] [-aboveOK <count>] \
        [<spectrafile> <filtfile> <classfile>]
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-yrmon <YYYY-MM>` | Directory/year-month prefix string (e.g., `2018-06`). Used to parse year/month in 2018 mode and to construct the output path `<yrmon>/<stamp>.wav.datetime`. | None |
| `-dahrmnse <DDHHMMSS>` | 8-character day-hour-minute-second string (2018 naming convention, e.g., `20143218` for 20th day, 14:32:18). | None |
| `-yrmondahrmnse <str>` | 15-character timestamp string `YYYYMMDDTHHMMSS` (2019 naming convention, e.g., `20190621T060810`). | None |
| `-reclen_secs <int>` | Recording duration in seconds added to the start time to form the second line of `.wav.datetime`. | `0` (typically `600` for 10-min files) |
| `-just_datetime` | Exit immediately after writing the `.wav.datetime` file without reading `spectrafile` or `filtfile`. | `0` (Disabled) |
| `-threshold <float>` | Absolute amplitude threshold on `filtfile` values (`fabs(filthigh[k]) > threshold`) to count a sample as an impulsive spike. | `2.0` |
| `-aboveOK <int>` | Minimum number of threshold-exceeding samples within a 1-minute window required to trigger a `YES` classification (`noabove > aboveOK`). | `5` |
| `<spectrafile>` | Positional argument 1: Input 2-column ASCII spectral file (up to 10,000 samples). Required unless `-just_datetime` is set. | None |
| `<filtfile>` | Positional argument 2: Input 2-column ASCII high-pass filtered file (must have the same sample count as `spectrafile`). | None |
| `<classfile>` | Positional argument 3: Output per-minute classification log file. | None |
| `-v` | Enable verbose output (`verbose_flag++`). | `0` |

---

## Classification & Timestamp Algorithm

### 1. Julian Day & Epoch Conversion
When `-yrmon` and either `-dahrmnse` or `-yrmondahrmnse` are provided, `findTCs` extracts `year`, `month`, `day`, `hour`, `min`, and `sec`, calls `stdtime_dmy_to_jul_day(day, month, year)` and `stdtime_from_jul_day(year, jday, hour, min, sec)`, and writes two lines (start time and start time + `reclen_secs`) to `<yrmon>/<stamp>.wav.datetime`:

```text
  2019 6 21 6 8 10 -- jday 172 -- 1970time 1561097290.00 
  2019 6 21 6 8 610 -- jday 172 -- 1970time 1561097890.00 
```

### 2. One-Minute Window Spike Counting
Assuming a 10-minute (`600 s`) recording with `count1` total decimated envelope samples (each representing $10,000 / 44,100 \approx 0.2268\text{ s}$), `findTCs` sets `samp_per_min = count1 / 10`. For each minute $m \in [0, 9]$:

$$N_{\text{above}}(m) = \sum_{j=0}^{\text{samp\_per\_min}-1} \mathbb{I}\!\left(\left|\text{filthigh}[m \cdot \text{samp\_per\_min} + j]\right| > \text{threshold}\right)$$

If $N_{\text{above}}(m) > \text{aboveOK}$, the minute is flagged `YES`; otherwise `NOO`:

```text
 2019 172 06 08 10 JD172_21th_06mnth_YES 12
 2019 172 06 09 10 JD172_21th_06mnth_NOO 1
```

---

## Example Usage

```bash
# 1. Generate only the .wav.datetime file for a 10-minute (600 s) recording
findTCs -yrmon 2019-06 -yrmondahrmnse 20190621T060810 -reclen_secs 600 -just_datetime

# 2. Classify a 10-minute hydrophone record using threshold 2.0 and spike count > 2
findTCs -yrmon 2019-06 -yrmondahrmnse 20190621T060810 -reclen_secs 600 \
        -threshold 2.0 -aboveOK 2 rec.spectra rec.filt rec.class
```
