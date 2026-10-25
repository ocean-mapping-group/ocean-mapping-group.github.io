---
layout: default
title: thin_nav
parent: Navigation Tools
nav_order: 32
tool_name: thin_nav
source_path: code/nav/thin_nav.c
category: Navigation & Georeferencing
input_formats: [".nav"]
output_formats: [".nav_thin (<filename>_thin)"]
related_tools: ["removeRedundantNav", "appendNav", "fixnav", "navedit", "mergeNav"]
---

# thin_nav

## Description
`thin_nav` filters a binary OMG navigation file (`.nav`, `jcu_nav_rec`) to remove redundant or non-monotonic records and writes the cleaned output to a new binary file named `<filename>_thin`.

It supports two filtering modes:
1. **Thin by Position (Default):** Retains the first record and writes subsequent records only when either latitude or longitude changes (`nav_rec.lat != old_lat || nav_rec.lon != old_lon`).
2. **Thin by Time (`-by_time`):** Enforces strictly increasing timestamps (`new_time > old_time`), dropping any duplicate-timestamp fixes or backward time jumps.

---

## Usage

```bash
thin_nav [-v] [-by_time] <filename>
```

### Common Workflow Examples

**1. Remove duplicate consecutive positions from a `.nav` file:**
```bash
thin_nav merged/JD100/0001_line.nav
# Produces: merged/JD100/0001_line.nav_thin
```

**2. Enforce strictly increasing timestamps (`new_time > old_time`) with verbose logging:**
```bash
thin_nav -v -by_time merged/JD100/0001_line.nav
# Produces: merged/JD100/0001_line.nav_thin
mv merged/JD100/0001_line.nav_thin merged/JD100/0001_line.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<filename>` | **Required.** Input binary `.nav` filename. The output file is automatically named `<filename>_thin` via `mem_strappend(filename, "_thin")`. | None |
| `-by_time` | Switch from position deduplication (`thin_by_position = 1`) to strictly monotonic timestamp filtering (`thin_by_time = 1`). Keeps a record only if its timestamp `time + centisecs / 100.0` is strictly greater than the last **kept** record's timestamp (`new_time > old_time`). | Disabled (thins by position) |
| `-v` | Verbose mode: prints every retained record index and (in `-by_time` mode) warns whenever duplicate or backward timestamps are skipped (`"Got same time on recs i i-1 ... skipping it"`). | Disabled |

---

## How It Works

1. **Initialization & First Record:**
   Opens `<filename>` for reading and `<filename>_thin` for writing. Computes the total number of 48-byte records as `length = ftell(nav_file) / JCU_BINNAV_RECLEN`. Reads record `0`, initializes `old_lat`, `old_lon`, and `old_time = nav_rec.time + nav_rec.centisecs / 100.0`, and writes record `0` directly to `<filename>_thin` (`new_nav_counter = 1`).
2. **Sequential Filtering (`i = 1 .. length - 1`):**
   * **Position Mode (Default):**
     Checks `if (nav_rec.lat != old_lat || nav_rec.lon != old_lon)`. When true, writes `nav_rec` to `<filename>_thin` at index `new_nav_counter`, increments `new_nav_counter`, and updates `old_lat` and `old_lon`.
   * **Time Mode (`-by_time`):**
     Computes `new_time = (double)nav_rec.time + (double)nav_rec.centisecs / 100.0`. Checks `if (new_time > old_time)`. When true, writes `nav_rec` to `<filename>_thin`, increments `new_nav_counter`, and updates `old_time = new_time`. Because `old_time` is only updated when a record is accepted, any backward time glitch is completely skipped until timestamps once again exceed the pre-glitch `old_time`.
3. **Completion Summary:**
   Prints `Thinned <length - new_nav_counter> of <length> nav recs...` and closes both files.
