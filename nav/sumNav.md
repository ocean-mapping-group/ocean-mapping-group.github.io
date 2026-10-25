---
layout: default
title: sumNav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 31
tool_name: sumNav
source_path: code/nav/sumNav.c
category: Navigation & Georeferencing
input_formats:
- .nav
- ASCII XYZ/LLZ trackline
output_formats:
- ASCII summary statistics (stdout)
related_tools:
- appendNav
- stripNav
- navedit
- calcSpeedHead
---

# sumNav

## Description
`sumNav` calculates the total survey trackline distance (in kilometers) and elapsed survey duration (in minutes, hours, and days) across one or more binary OMG navigation files (`.nav`, `jcu_nav_rec`, up to 1,000 files) or 3-column ASCII `lat lon val` route files (`-ascii`).

It is commonly used for end-of-cruise and Canadian Hydrographic Service (CHS) production reporting ("line kilometers run") as well as for estimating transit and survey durations from planned ASCII waypoint files given a target vessel speed (`-speed_knots`).

---

## Usage

```bash
# Summarize total distance and time for binary .nav files
sumNav [-v] [-skip <N>] [-maxjump <km>] <navfile(s)>

# Estimate distance and survey time for ASCII planned lines (lat lon val)
sumNav -ascii [-speed_knots <kts>] [-maxjump <km>] <ascii_file(s)>
```

### Common Workflow Examples

**1. Compute line kilometers and hours for all survey lines in a Julian Day directory:**

```bash
sumNav -skip 10 merged/JD100/*.nav
```
Example output:

```text
 3 file(s) being read
 merged/JD100/0001_line.nav : 4500 
 file merged/JD100/0001_line.nav has 12.450120 km 48.200000 minutes
 ...
 All file  add up to 38.912045 km 2.514000 hours 0.104750 days
```

**2. Estimate survey duration at 7.5 knots for a set of planned ASCII waypoint lines:**

```bash
sumNav -ascii -speed_knots 7.5 -maxjump 50.0 planned_lines/*.llz
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<navfile(s)>` | **Required.** One or more binary `.nav` files (or 3-column ASCII `lat lon value` files when `-ascii` is set; up to 1,000 files). *(Note: files are opened with `"r+"`, so they must have write permission even though `sumNav` does not modify them).* | None |
| `-skip <N>` | Step through binary `.nav` files every $N$-th record (`k += skip`) to speed up computation and smooth high-frequency jitter. | `1` (every record) |
| `-maxjump <km>` | Maximum allowable inter-fix distance jump in kilometers. Any step where $\text{distance} > \text{maxjump}$ prints `"ridiculous distance jump, <d> ignoring"` and is excluded from the cumulative distance total. *(For planned ASCII waypoints with long legs, increase `-maxjump`, e.g., `-maxjump 100.0`).* | `0.5` km (500 m) |
| `-ascii` | Read 3-column whitespace-delimited ASCII files (`lat lon value`) instead of binary `.nav` files. Prints leg-by-leg distance and duration at `-speed_knots`. | Disabled (binary `.nav` mode) |
| `-speed_knots <kts>` | Vessel speed in knots used in `-ascii` mode to compute leg duration: $\Delta t = \frac{3600 \times \text{distance}}{\text{speed\_knots} \times 1.853}$ seconds. | `8.0` knots |
| `-comp <filename>` | Parsed on the command line (`tidename`), legacy option from `appendNav` (unused). | None |
| `-v` | Increment verbose flag. | Disabled |

---

## How It Works

1. **Inter-Fix Distance Calculation:**
   For each consecutive pair of records (at step `-skip` in binary mode, or consecutive lines in `-ascii` mode), `sumNav` converts latitude and longitude differences to kilometers using the standard nautical mile approximation ($1' = 1.853\text{ km}$):
   $$\Delta y_{\text{km}} = (\text{lat}_k - \text{lat}_{k-1}) \times 60.0 \times 1.853$$
   $$\Delta x_{\text{km}} = (\text{lon}_k - \text{lon}_{k-1}) \times 60.0 \times 1.853 \times \cos\left(\text{lat}_{k-1} \frac{\pi}{180}\right)$$
   $$\text{distance} = \sqrt{\Delta x_{\text{km}}^2 + \Delta y_{\text{km}}^2}$$
2. **Jump Rejection Thresholds:**
   * **Distance Jump Guard:** If $\text{distance} > \text{maxjump}$ (default `0.5` km), the segment is ignored and a warning is printed.
   * **Time Jump Guard (Binary Mode):** Computes $\Delta t = t_k - t_{k-1}$. If $\Delta t > 600.0$ seconds (10 minutes, hardcoded `timejump = 600.0`), prints `"ridiculous time jump, 600.000000 ignoring"` and excludes that time step from `this_time`.
3. **Per-File and Grand Totals:**
   Prints each file's total kilometers and minutes, followed by a grand total across all input files in kilometers, hours (`total_time / 3600.0`), and 24-hour days (`total_time / 86400.0`).
