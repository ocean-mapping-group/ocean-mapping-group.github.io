---
layout: default
title: navedit
parent: Navigation Tools
nav_order: 25
tool_name: navedit
source_path: code/nav/navedit.c
category: Navigation & Georeferencing
input_formats: [".nav"]
output_formats: [".nav (modified in-place)", "ASCII diagnostics (stdout)"]
related_tools: ["fixnav", "flagNav", "removeRedundantNav", "thin_nav", "mergeNav", "appendNav"]
---

# navedit

## Description
`navedit` is an interactive binary navigation record browser, in-place editor, and non-interactive diagnostic/repair utility for OMG `.nav` files (`jcu_nav_rec`, 48 bytes per fix).

It supports four operating modes:
1. **Non-Interactive Time-Step & Continuity Check (`-check`):** Scans the entire `.nav` file and reports minimum/maximum $\Delta t$, typical sampling frequency (Hz), and any backward (negative) time jumps.
2. **Centre-Fix Quick Dump (`-show_centre_fix`):** Prints the single navigation record at `length / 2` (the midpoint of the file) to `stdout` via `nav_show()` and exits immediately.
3. **Midnight Rollover Repair (`-fix_midnight`):** Detects backward time jumps of $\approx 86,400$ seconds (`dtime < 0 && fabs(dtime) > 86000`) caused by UTC midnight rollovers where the date was not incremented, adds `86400` seconds to `glo_rec.time`, and writes the corrected record in-place.
4. **Interactive Record Editor (Default):** Steps forward/backward or jumps to arbitrary record numbers and allows in-place modification of time offsets (`t`), velocity (`v`), validity status flag `flag[3]` (`s`), or latitude/longitude (`l`).

---

## Usage

```bash
# Non-interactive quality check
navedit -check [-verbose] <filename.nav>

# Print the middle record of a .nav file
navedit -show_centre_fix <filename.nav>

# Repair un-incremented UTC midnight rollovers in-place
navedit -fix_midnight <filename.nav>

# Interactive record browser and in-place editor
navedit <filename.nav>
```

### Common Workflow Examples

**1. Check a navigation file for backward time jumps, gaps, and sampling rate:**
```bash
navedit -check merged/JD100/0001_line.nav
```
Example output:
```text
 merged/JD100/0001_line.nav 
  4520 records in file
Checked Nav, mindt 0.1999 (rec 14), maxdt 1.0001 (rec 892) typical freq 5.00 Hz, # -ve 0 of 4520
```

**2. Inspect the midpoint position and timestamp of a survey line:**
```bash
navedit -show_centre_fix merged/JD100/0001_line.nav
```

**3. Repair a 24-hour (-86400 s) midnight rollover jump in-place:**
```bash
navedit -fix_midnight raw_nmea.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<filename>` | **Required.** Binary `.nav` file to inspect or edit (opened in `"r+"` read-write mode). | None |
| `-check` | Non-interactive continuity check: computes `mindt`, `maxdt`, average frequency (`1.0 / avdt`), and prints every record where `dtime < 0.0` with its formatted UTC date/time. | Disabled |
| `-verbose` | Used with `-check`: prints `Record <i >, time <t>...dt = <dtime>` for every record in the file. *(Note: the flag is `-verbose`, not `-v`).* | Disabled |
| `-show_centre_fix` | Reads and prints only the midpoint record (`rec_num = length / 2`) using `nav_show()` and exits cleanly. Suppresses header banners so output can be piped into scripts. | Disabled |
| `-fix_midnight` | Scans consecutive records; whenever `dtime < 0 && fabs(dtime) > 86000`, adds `86400` seconds to `glo_rec.time` and writes it in-place. *(Note: repairs single-step rollovers; run [`fixnav`](fixnav.md) if all subsequent records in the file also need shifting).* | Disabled |

---

## Interactive Editor Commands

When invoked without `-check`, `-show_centre_fix`, or `-fix_midnight`, `navedit` enters an interactive command loop on `stdin`:

| Command | Action |
|---|---|
| `r` | Prompt for a target record number (`0` to `length - 1`) and display it. |
| `+` or `+<N>` | Advance forward 1 record (`+`) or `<N>` records (e.g., `+100`) and display it. |
| `-` or `-<N>` | Step backward 1 record (`-`) or `<N>` records (e.g., `-50`) and display it. |
| `c` | Modify the current record in-place. Prompts for the field to change:<br>• `t` — **Time:** prompts for an integer second offset (positive or negative) to add to `glo_rec.time`.<br>• `v` — **Velocity:** prompts for a new speed value (`glo_rec.velocity`).<br>• `s` — **Status:** toggles `glo_rec.flag[3]` between `0` (valid) and `1` (flagged/rejected).<br>• `l` — **Lat/Lon:** prompts for new decimal degrees `lat lon` (`%lf %lf`). |
| `e` | Exit `navedit`. |

---

## `nav_show` Output Format

Each displayed record is formatted by `nav_show()` (`code/subr/jcu_nav.c`) as a single line:
```text
  lat           lon           depth vel    azi     year jday (mm dd) hh mm ss.cc f0 f1 f2 f3
  45.12345678  -66.98765432     0  4.120 182.400 2023 145 ( 5 25) 14 32 10.20  8  3 12  0
```
