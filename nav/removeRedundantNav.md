---
layout: default
title: removeRedundantNav
parent: Navigation Tools
nav_order: 29
tool_name: removeRedundantNav
source_path: code/nav/removeRedundantNav.c
category: Navigation & Georeferencing
input_formats: [".nav"]
output_formats: [".nav"]
related_tools: ["thin_nav", "appendNav", "fixnav", "navedit", "mergeNav"]
---

# removeRedundantNav

## Description
`removeRedundantNav` concatenates and filters one or more binary OMG navigation files (`.nav`, `jcu_nav_rec`, up to 200 files) into a composite output `.nav` file (`-comp`), removing either:
1. **Consecutive Duplicate Positions (Default Mode):** Drops fixes where both latitude and longitude are identical to the previously written fix (`tide_rec.lat == oldlat && tide_rec.lon == oldlon`). This is commonly used when a low-rate positioning system (e.g., 1 Hz GPS) was logged at a higher datagram rate, producing repeated identical coordinates.
2. **Anomalous Time Jumps (`-reject_timejump_over <sec>`):** Drops fixes whose timestamp step $\Delta t = t_k - t_{k-1}$ exceeds a specified positive or negative threshold in seconds.

---

## Usage

```bash
removeRedundantNav [-v] [-skip <N>] [-reject_timejump_over <sec>] -comp <out_navfile> <input_navfile(s)>
```

### Common Workflow Examples

**1. Remove consecutive duplicate lat/lon fixes from a navigation file:**
```bash
removeRedundantNav -comp merged/JD100/0001_line_unique.nav merged/JD100/0001_line.nav
```

**2. Concatenate multiple `.nav` files while rejecting any forward or backward time jumps larger than 5 seconds:**
```bash
removeRedundantNav -reject_timejump_over 5.0 -comp clean_track.nav raw_nav/*.nav
```

**3. Reject only backward (negative) time jumps larger than 0.5 seconds:**
```bash
removeRedundantNav -reject_timejump_over -0.5 -comp monotonic_track.nav raw_nav/line1.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output binary `.nav` filename (`tidename`). | None |
| `<input_navfile(s)>` | **Required.** One or more input binary `.nav` files (up to 200 files). *(Note: input files are opened with `"r+"`, so they must be writable by the current user even though they are only read).* | None |
| `-skip <N>` | Step through each input file by $N$ records (`for (k = 0; k < numrec; k += skip)`). | `1` (every record) |
| `-reject_timejump_over <sec>` | Switches filter mode from position deduplication to time-jump rejection:<br>• **If `<sec> > 0`:** Rejects any fix where $\|\Delta t\| = \|t_k - t_{k-1}\| \ge \text{sec}$ (both forward and backward jumps).<br>• **If `<sec> < 0`:** Rejects only **backward** time jumps where $-\Delta t \ge -\text{sec}$ (i.e. $\Delta t \le \text{sec}$). | `0.0` (position deduplication mode) |
| `-v` | Increment verbose flag. | Disabled |

---

## Comparison: `removeRedundantNav` vs. `thin_nav`

Both [`removeRedundantNav`](removeRedundantNav.md) and [`thin_nav`](thin_nav.md) clean redundant navigation records, but they differ in multi-file support, output naming, and time filtering:

| Feature | `removeRedundantNav` | [`thin_nav`](thin_nav.md) |
|---|---|---|
| **Number of Input Files** | Up to 200 `.nav` files (concatenates into `-comp`) | Single `.nav` file |
| **Output Filename** | User-specified via `-comp <outfile>` | Automatically appends `_thin` (`<filename>_thin`) |
| **Decimation (`-skip`)** | Supported (`-skip <N>`) | Not supported |
| **Position Deduplication** | Default mode (`lat != oldlat \|\| lon != oldlon`) | Default mode (`lat != oldlat \|\| lon != oldlon`) |
| **Time Filtering** | `-reject_timejump_over <sec>` (rejects large forward/backward $\Delta t$ spikes; updates `last_time = this_time` on every record) | `-by_time` (strictly monotonic filter: keeps only fixes where `new_time > old_time`, updating `old_time` only when a record is kept) |

---

## How It Works

1. **File Iteration:**
   Opens the output file `<tidename>` for writing (`"w"`) and loops over each input `.nav` file `name[j]`, determining its record count via `ftell(file[j]) / JCU_BINNAV_RECLEN` (`48` bytes).
2. **Filtering Loop (`k = 0; k < numrec; k += skip`):**
   * **When `-reject_timejump_over` is non-zero:**
     Computes `this_time = tide_rec.time + tide_rec.centisecs / 100.0` and `time_diff = this_time - last_time` (with `last_time = this_time` on `k == 0`).
     * If `reject_timejump_over > 0`: writes the fix if `fabs(time_diff) < reject_timejump_over`; otherwise prints `rejected <k> (<time_diff>) of <numrec> ++`.
     * If `reject_timejump_over < 0`: writes the fix if `-time_diff < -reject_timejump_over` (i.e., `time_diff > reject_timejump_over`); otherwise rejects it.
   * **When `-reject_timejump_over` is `0` (Default):**
     Writes the fix to the output file if `tide_rec.lat != oldlat || tide_rec.lon != oldlon` and updates `oldlat` and `oldlon`.
3. **Summary Report:**
   Upon completion, prints `of <tide_rec_no> recs <useful> unique`.
