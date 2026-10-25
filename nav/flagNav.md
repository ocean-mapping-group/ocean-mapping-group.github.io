---
layout: default
title: flagNav
parent: Navigation Tools
nav_order: 20
tool_name: flagNav
source_path: code/nav/flagNav.c
category: Navigation & Georeferencing
input_formats: [".nav"]
output_formats: [".nav (modified in-place)"]
related_tools: ["toNav", "NMEAtoNav", "PNAVtoNav", "mergeNav", "appendNav", "navedit"]
---

# flagNav

## Description
`flagNav` is an in-place quality-control utility for binary OMG navigation files (`jcu_nav_rec`, 48 bytes per record). It inspects the positioning quality indicator stored in `flag[1]` of each navigation record (such as GPS fix quality, differential mode, or PNAV solution flag) and sets the master validity flag `flag[3]` based on a user-specified acceptance threshold (`-accept`).

In the OMG navigation architecture:
* `flag[3] == 0` indicates an **accepted (valid)** navigation fix that will be used by [`mergeNav`](mergeNav.md) and [`appendNav -goodonly`](appendNav.md).
* `flag[3] == 1` indicates a **rejected (flagged)** navigation fix that `mergeNav` and `appendNav -goodonly` will skip during interpolation or export (unless `mergeNav -allnavok` is explicitly specified).

> [!CAUTION]
> **In-Place Modification:**
> `flagNav` opens each input `.nav` file in read/write mode (`"r+"`) and overwrites `flag[3]` directly in the original file. Back up raw `.nav` files before running `flagNav` if you need to preserve pre-existing manual flag edits made in [`navedit`](navedit.md).

---

## Usage

```bash
flagNav [-v] [-accept <min_flag1_val>] <navfile(s)>
```

### Common Workflow Examples

**1. Accept only differential/RTK or higher-grade fixes (`flag[1] >= 3`):**
```bash
flagNav -accept 3 merged/JD100/0001_line.nav
```

**2. Batch-flag multiple navigation files with verbose record-by-record reporting:**
```bash
flagNav -v -accept 2 proc_nav/day100_*.nav
```

**3. Reset all fixes with `flag[1] >= 1` to valid (`flag[3] = 0`):**
```bash
flagNav -accept 1 merged/JD100/*.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<navfile(s)>` | **Required.** One or more binary `.nav` files (up to 300 files in a single invocation) to modify in-place. | None |
| `-accept <int>` | Minimum acceptable integer value in `tide_rec.flag[1]`. Fixes with `flag[1] >= accept` receive `flag[3] = 0` (valid); fixes with `flag[1] < accept` receive `flag[3] = 1` (rejected). | `9` |
| `-v` | Verbose mode: prints `rec_index flag[0] flag[1] accept` for every record inspected. | Disabled |
| `-ascii` | Parsed on the command line (`ascii_flag++`), though binary `nav_read` / `nav_write` is always used in the processing loop. | Disabled |
| `-comp <filename>` | Parsed on the command line (`tidename`), legacy option from `appendNav` template (unused because `flagNav` writes back in-place). | None |

---

## Binary Record Format (`jcu_nav_rec`)

`flagNav` operates on the standard 48-byte `jcu_nav_rec` binary record structure defined in `code/subr/jcu_nav.h`:

| Byte Offset | C Type | Field | Role in `flagNav` |
|---|---|---|---|
| `0..7` | `double` | `lat` | Latitude in decimal degrees (unchanged) |
| `8..15` | `double` | `lon` | Longitude in decimal degrees (unchanged) |
| `16..19` | `int` | `time` | UTC seconds since Jan 1, 1970 (unchanged) |
| `20..21` | `short` | `centisecs` | Hundredths of a second (unchanged) |
| `22..23` | `short` | *padding* | 2-byte alignment padding in 48-byte on-disk record |
| `24..27` | `float` | `azi` | Heading/azimuth or ellipsoid height (unchanged) |
| `28..31` | `float` | `velocity` | Speed over ground (unchanged) |
| `32..33` | `short` | `depth` | Sensor depth or altitude code (unchanged) |
| `34..35` | `short` | `flag[0]` | Satellite count (`SVs`) or primary status (printed with `-v`) |
| `36..37` | `short` | `flag[1]` | **Evaluated quality metric** (compared against `-accept`) |
| `38..39` | `short` | `flag[2]` | PDOP/HDOP scaled integer (unchanged) |
| `40..41` | `short` | `flag[3]` | **Master validity flag** (`0` = valid/accepted, `1` = rejected) |

---

## How It Works

1. **File Discovery & Record Count:**
   Iterates over each input file `name[j]` (up to 300 files), opens it with `fopen(name[j], "r+")`, seeks to the end of the file, and computes the total record count as `numrec = ftell(file[j]) / JCU_BINNAV_RECLEN` (`48` bytes).
2. **Quality Threshold Evaluation:**
   Loops through every record `k` from `0` to `numrec - 1`:
   * Reads record `k` via `nav_read(file[j], k, &tide_rec)`.
   * Evaluates `if (tide_rec.flag[1] >= accept)`:
     * **Pass:** Sets `tide_rec.flag[3] = 0`.
     * **Reject:** Sets `tide_rec.flag[3] = 1`, increments the `rejected` counter, and prints the running count and percentage of rejected fixes.
3. **In-Place Writeback:**
   Writes the updated `jcu_nav_rec` back to index `k` via `nav_write(file[j], k, &tide_rec)` and closes the file upon completion.
