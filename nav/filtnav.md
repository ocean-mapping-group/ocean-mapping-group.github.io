---
layout: default
title: filtnav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 18
tool_name: filtnav
source_path: code/nav/filtnav.c
category: Navigation & Georeferencing
input_formats:
- .nav (jcu_nav_rec binary)
output_formats:
- .nav.filtered (jcu_nav_rec binary)
related_tools:
- fixnav
- avNav
- calcSpeedHead
- appendNav
- mergeNav
---

# filtnav

## Description
`filtnav` filters a binary 48-byte OMG navigation file (`jcu_nav_rec`, `.nav`) and writes the cleaned output to `<filename>.filtered`.

It operates in one of two modes:
1. **Outlier Rejection & Packing Mode (default):** Iteratively removes flagged records (`packem`), then scans consecutive fixes (`checkem`) to flag and reject duplicate positions, large time jumps ($|\Delta t| > 15\text{ s}$), negative time jumps, and excessive vessel speeds ($> 10\text{ m/s}$, ~19.4 knots). By default it runs `1` pass, or `N` passes if `-times <N>` is specified.
2. **Moving-Window Smoothing Mode (`-smooth`):** Applies a $\pm 5$-record moving average (`flen = 5`, including neighbors within 10 seconds of the center fix) to `lat` and `lon`, and recomputes vessel `velocity` (m/s) and `azi` (degrees $0^\circ..360^\circ$) from the smoothed track.

---

## Usage

```bash
filtnav [OPTIONS] <filename.nav>
```

### Common Workflow Examples

**1. Filter out duplicate fixes, time jumps, and speed spikes (3 iterative passes):**

```bash
filtnav -times 3 raw_line01.nav
# Writes raw_line01.nav.filtered
```

**2. Smooth positions over a $\pm 5$-fix window and recompute course and speed:**

```bash
filtnav -smooth raw_line01.nav
# Writes raw_line01.nav.filtered
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<filename>` | **Required.** Input binary `.nav` file (`jcu_nav_rec` format). Output is automatically written to `<filename>.filtered`. | None |
| `-times <N>` | Number of iterative pack-and-check rejection passes to execute in default outlier-rejection mode. Note: because `checkem()` flags bad fixes *after* `packem()` compacts unflagged fixes, running `-times 2` (or higher) is necessary to physically remove records newly flagged during pass 1. | `1` |
| `-smooth` | Run `smoothnav()` instead of `packem()`/`checkem()`: smooths `lat` and `lon` over a $\pm 5$-record window (for neighbors with $|\Delta t| < 10\text{ s}$) and updates `azi` (degrees) and `velocity` (m/s). | Disabled (outlier rejection mode) |
| `-v` | Enable verbose output (prints pre-smoothed velocity and heading in `-smooth` mode). | Disabled |

---

## Rejection Criteria (Default Mode)

In each pass `j` of `0 .. times - 1`, `filtnav` first compacts the array by discarding any record with `flag[3] != 0` (`packem`), and then evaluates every adjacent pair `(Record[i], Record[i+1])` in `checkem()`:

| Condition | Threshold | Action Taken |
|---|---|---|
| **Duplicate Position** | `Record[i+1].lat == Record[i].lat && Record[i+1].lon == Record[i].lon` | Prints `identical fix` and sets `Record[i+1].flag[3] = 1`. |
| **Large Time Gap** | `fabs(dtime) > 15` seconds | Sets `Record[i+1].flag[3] = 1`. |
| **Speed Spike** | `speed > 10` m/s (where `dy = dlat * 60 * 1853`, `dx = dlon * 60 * 1853 * cos(lat)`) | Prints `<i > speed flag <speed>` and sets **both** `Record[i].flag[3] = 1` and `Record[i+1].flag[3] = 1`. |

Whenever a fix pair is rejected, `checkem()` prints the inter-fix time step, distance, speed, and full record dumps (`nav_show`) for `Record[i]` and `Record[i+1]`.

> [!TIP]
> Because `packem()` is called *before* `checkem()` inside the `for (j = 0; j < times; j++)` loop, a single pass (`-times 1`) flags bad records (`flag[3] = 1`) in the output `.filtered` file without removing them from the record array. Pass `-times 2` (or more) if you want the flagged records physically stripped from `<filename>.filtered`, or use `-goodonly` in [`appendNav`](appendNav.html).

---

## How It Works

1. Opens `<filename>` for reading and `<filename>.filtered` for writing.
2. Computes `length = ftell(glofile) / JCU_BINNAV_RECLEN` (48 bytes), allocates `Record[]` in memory, and reads all records via `nav_read()`.
3. **If `-smooth` is NOT set:** Runs `times` iterations of `upto = packem(length)` followed by `checkem(upto, 1)`.
4. **If `-smooth` IS set:** Loops from index `i = 5` to `length - 5`, averages `lat` and `lon` across neighbors $j \in [-5, 4]$ whose timestamp is within $10\text{ s}$ of `Record[i].time`, computes smoothed azimuth (`getazi`) and speed (`dist / dtime`), and stores them in `Record[i].azi` and `Record[i].velocity`.
5. Writes the resulting `length` records to `<filename>.filtered` via `nav_write()`.
