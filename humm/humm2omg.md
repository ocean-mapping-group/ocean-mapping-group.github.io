---
layout: default
title: humm2omg
parent: Humminbird Side-Imaging Sonar (humm)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
tool_name: humm2omg
source_path: code/humm/humm2omg.c
category: Raw Sonar Format Conversion
input_formats:
- ASCII serial log ($GPGGA, Trimcube P-telegrams, 6-beam Humminbird depths)
output_formats:
- .merged (OMG_HDCS v3, toolType=Humminbird)
- .nav (jcu_nav_rec)
related_tools:
- jNMEA
- jcu_nav
- OMG_HDCS_jversion
- mergeAtt
---

# humm2omg

## Overview
`humm2omg` (`code/humm/humm2omg.c`, written by John E. Hughes Clarke, October 1999) converts interleaved ASCII serial data logs recorded from a **Humminbird 6-beam wide-swath recreational/coastal echosounder**, a **Trimcube pitch/roll tilt sensor**, and an **NMEA `$GPGGA` GPS receiver** into standard binary OMG-HDCS `.merged` swath bathymetry (`toolType = Humminbird`, 6 beams per ping) and `.nav` (`jcu_nav_rec`) navigation files.

---

## Usage

```bash
humm2omg [-v] [-new] [-skip <n>] -year <YYYY> -jday <DDD> -comp <out_prefix> <ascii_logfile(s) ...>
```

---

## Command-Line Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <prefix>` | **Required.** Output filename prefix; creates `<prefix>.merged` and `<prefix>.nav`. | None |
| `-year <YYYY>` | **Required.** 4-digit survey year used with `-jday` and `$GPGGA` UTC `hhmmss` to compute Unix epoch timestamps (`stdtime_from_jul_day`). | Uninitialized |
| `-jday <DDD>` | **Required.** Julian day of year (`1..366`). | Uninitialized |
| `-skip <n>` | Subsample factor (`skip`). | `1` |
| `-new` | Enable new format flag (`new_flag`). | `0` |
| `-v` | Verbose mode: prints parsed latitude/longitude, pitch/roll, and 6-beam depth/across-track values for every telegram. | Disabled |
| `<file(s)>` | **Required.** Up to 300 input ASCII serial capture files. | None |

---

## Telegram Parsing & Geometric Conversion

As `humm2omg` reads each line from the input ASCII log via `getc_line()`, it dispatches on the leading character(s):

1. **`$GPGGA` NMEA GPS Telegrams (`telegram[0] == '$' && strncmp(telegram+1, "GPGGA", 5) == 0`):**
   * Parsed via `jnmea_read_INGGA()` ([`jNMEA`](../subr/jNMEA.html)).
   * Converted to a `jcu_nav_rec` (`fill_in_nav`) with `time = stdtime_from_jul_day(year, jday, hour, min, sec)` and written sequentially to `<prefix>.nav` via `nav_write()`.
   * Prints `N` to `stdout`.

2. **Trimcube Pitch/Roll Telegrams (`telegram[0] == 'P'`):**
   * Parses two 5-character fixed-width numeric fields (`telegram+1` and `telegram+7`) representing pitch and roll in hundredths of a degree:
     $$\text{pitch} = \frac{\text{val}_1}{100.0}, \quad \text{roll} = \frac{\text{val}_2}{100.0}$$
   * Prints `T` to `stdout`.

3. **Humminbird 6-Beam Depth Telegrams (all other lines):**
   * Parses 6 whitespace-separated raw depth values (`read_humm_telegram`), converts each from 3-inch units into meters:
     $$Z_i = \text{raw}_i \times \frac{2.5 \times 3.0}{100.0} = \text{raw}_i \times 0.075\text{ m}$$
   * Assigns fixed nominal beam depression angles across the 6 beams:
     $$\theta = \{-25^\circ, -15^\circ, -5^\circ, +5^\circ, +15^\circ, +25^\circ\}$$
   * Computes across-track distance assuming flat-bottom geometry:
     $$Y_i = -\tan(\theta_i) \cdot Z_i$$
   * Once at least one `$GPGGA` timestamp has been received (`tide_rec_no > 0`), writes an `OMG_HDCS_profile_header` and 6 `OMG_HDCS_beam` records (in millimeter units, `depth * 1000.0`, `across * 1000.0`) to `<prefix>.merged`.
   * Prints `H` to `stdout`.
