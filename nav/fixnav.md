---
layout: default
title: fixnav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 19
tool_name: fixnav
source_path: code/nav/fixnav.c
category: Navigation & Georeferencing
input_formats:
- .nav (jcu_nav_rec binary)
output_formats:
- .nav (modified in-place)
related_tools:
- filtnav
- mergeNav
- appendNav
- NMEAtoNav
---

# fixnav

## Description
`fixnav` scans a binary 48-byte OMG navigation file (`jcu_nav_rec`, `.nav`) for timing anomalies—specifically $\pm 24\text{-hour}$ ($\pm 86,400\text{ s}$) day-rollover jumps that occurred in legacy Kongsberg Simrad EM100 navigation telegrams—and repairs them **in-place** by adding or subtracting multiples of $86,400\text{ seconds}$ (`24 * 60 * 60 * back_flag`) to subsequent record timestamps.

It can also be run in read-only diagnostic mode (`-testonly`) to report time gaps $> 30\text{ seconds}$, negative time jumps (`dtime < 0.0`), and $\pm 24\text{-hour}$ day jumps without modifying the `.nav` file, or with `-skip <N>` to manually shift all records after Record `0` by $-N \times 86,400\text{ seconds}$.

---

## Usage

```bash
fixnav [OPTIONS] <filename.nav>
```

### Common Workflow Examples

**1. Inspect a `.nav` file for time gaps ($> 30\text{ s}$), negative time steps, and 24-hour jumps without modifying the file:**

```bash
fixnav -testonly merged/JD100/0001_line.nav
```

**2. Automatically detect and repair $\pm 24\text{-hour}$ day jumps in-place:**

```bash
fixnav merged/JD100/0001_line.nav
```

**3. Manually shift all timestamps (from record 1 onward) by +1 day ($+86,400\text{ s}$) using `-skip -1`:**

```bash
fixnav -skip -1 merged/JD100/0001_line.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<filename>` | **Required.** Binary `.nav` file (`jcu_nav_rec` format) to inspect or repair. Opened in `"r+"` mode and **modified in-place** unless `-testonly` is specified. | None |
| `-testonly` | Diagnostic mode: scan and print all time gaps ($> 30\text{ s}$), negative time jumps (`< 0.0 s`), and $\pm 24\text{-hour}$ jumps without writing any changes to `<filename>`. | Disabled (modifies file in-place) |
| `-skip <N>` | Initializes `back_flag = N`, applying an immediate shift of $-N \times 86,400\text{ seconds}$ (`nav_rec.time -= 24 * 60 * 60 * back_flag`) starting at record `1` (unless modified further by detected 24-hour jumps). | `0` |
| `-v` | Increments internal `verbose_flag` counter. | Disabled |

---

## Anomaly Detection Rules

For every record $i = 1 \dots \text{length}-1$, `fixnav` computes `dtime = nav_rec.time - old_time` (where `old_time` is the un-shifted timestamp `time + centisecs / 100.0` of record $i - 1$):

| Condition | Console Message | Effect on `back_flag` |
|---|---|---|
| `dtime > 30.0` | `more than 30 second gap rec <i> (<dtime>)` | None (informational warning) |
| `dtime < 0.0` | `negative time jump          <i> (<dtime>)` | None (informational warning) |
| `-87000 < dtime < -85800` ($-86400 \pm 600\text{ s}$) | `time jumping backward <dtime>` | `back_flag--` (adds $+86,400\text{ s}$ to subsequent records) |
| `+85800 < dtime < +87000` ($+86400 \pm 600\text{ s}$) | `time jumping forward <dtime>` | `back_flag++` (subtracts $86,400\text{ s}$ from subsequent records) |

---

## How It Works

1. Opens `<filename>` in read-write mode (`"r+"`) and calculates the number of 48-byte records (`length = ftell(glofile) / JCU_BINNAV_RECLEN`).
2. Reads Record `0` and initializes `old_time = nav_rec.time`.
3. Iterates through records $i = 1 \dots \text{length}-1$:
   * Reads Record $i$ and computes `dtime = nav_rec.time - old_time`.
   * Updates `old_time = (double)nav_rec.time + (double)nav_rec.centisecs / 100.0` (using the raw, un-adjusted timestamp of Record $i$ so consecutive raw deltas are compared).
   * Checks `dtime` against the $30\text{ s}$, $0\text{ s}$, and $\pm(86400 \pm 600)\text{ s}$ thresholds, decrementing or incrementing `back_flag` when a backward or forward 24-hour jump is encountered.
   * If `-testonly` is not set and `back_flag != 0`, adjusts `nav_rec.time -= 24 * 60 * 60 * back_flag` and writes Record $i$ back to disk via `nav_write(glofile, i, &nav_rec)`.
