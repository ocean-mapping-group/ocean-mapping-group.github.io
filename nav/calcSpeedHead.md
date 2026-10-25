---
layout: default
title: calcSpeedHead
parent: Navigation Tools
nav_order: 14
tool_name: calcSpeedHead
source_path: code/nav/calcSpeedHead.c
category: Navigation & Georeferencing
input_formats: [".nav (jcu_nav_rec binary)"]
output_formats: [".nav (modified in-place)"]
related_tools: ["mergeNav", "stripNav", "dumpnav", "filtnav", "avNav"]
---

# calcSpeedHead

## Description
`calcSpeedHead` computes fix-to-fix Speed Over Ground (`velocity`, in m/s) and Course Over Ground (`azi`, in degrees $0^\circ..360^\circ$) from consecutive latitude/longitude positions and timestamps in one or more binary OMG navigation files (`jcu_nav_rec`, `.nav`), **updating the input `.nav` files in-place**.

> [!WARNING]
> **In-Place Modification & Field Placement:**
> 1. `calcSpeedHead` opens every input `.nav` file in read-write mode (`"r+"`) and overwrites its records directly. Back up your `.nav` files first if you need to preserve the original values.
> 2. To avoid overwriting data already stored in `tide_rec.azi` (which often holds RTK height, tide, or gyro heading), `calcSpeedHead` writes the computed speed (m/s) into `tide_rec.velocity` and writes the **computed course/azimuth (scaled by 100)** into the integer `tide_rec.depth` field (`tide_rec.depth = azi * 100.0`). Record `0` inherits the speed and course computed for Record `1`.

---

## Usage

```bash
calcSpeedHead [OPTIONS] <navfile(s)>
```

### Common Workflow Examples

**1. Compute speed and course in-place for one or more `.nav` files:**
```bash
calcSpeedHead merged/JD100/0001_line.nav
```

**2. Run with quality-control warnings for time steps outside $[0.05, 0.25]\text{ s}$ and speeds outside $[1.0, 5.0]\text{ m/s}$:**
```bash
calcSpeedHead -check -allowed_mpers 1.0 5.0 -allowed_dtime 0.05 0.25 merged/JD100/*.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<nav(s)>` | **Required.** One or more binary `.nav` files (up to 300 files). **Modified in-place.** | None |
| `-check` | Enable diagnostic warnings when inter-fix time step `dtime` or speed `velocity` falls outside the allowed bounds (or equals `0.0`). | Disabled |
| `-allowed_mpers <min> <max>` | Used with `-check`. Minimum and maximum acceptable vessel speed in m/s. Requires **two** floating-point values. | `0.5` to `7.0` m/s (~1 to 14 knots) |
| `-allowed_dtime <min> <max>` | Used with `-check`. Minimum and maximum acceptable inter-fix time step (`dtime`) in seconds. Requires **two** floating-point values. | `0.02` to `1.0` s (50 Hz to 1 Hz) |
| `-accept <N>` | Integer parameter parsed on the command line (`accept = strtoint(*argv)`). | `9` |
| `-comp <filename>` | Parsed on the command line (`tidename = *argv`), though `fopen(tidename, "w")` is commented out in the source and all writes go in-place to `<nav(s)>`. | Unused |
| `-ascii` | Increments internal `ascii_flag` counter (unused in output loop). | Disabled |
| `-v` | Enable verbose output (prints `lat`, `lon`, original `azi`, `dtime`, computed `azi`, and `velocity` for every fix). | Disabled |

---

## How It Works

1. Opens each input `.nav` file in `"r+"` mode and determines the total number of 48-byte records (`numrec = ftell(file[j]) / JCU_BINNAV_RECLEN`).
2. Reads Record `0` into `last_rec`, then iterates through $k = 1 \dots \text{numrec}-1$:
   * **Distance Calculation:** Computes geodesic distance (meters) between `(tide_rec.lat, tide_rec.lon)` and `(last_rec.lat, last_rec.lon)` using `compute_distance_2()`.
   * **Course Over Ground (`azi`):** Computes the local north/east step (`dlat = (lat2 - lat1) * 60 * 1852`, `dlon = (lon2 - lon1) * 60 * 1852 * cos(lat2)`) and azimuth in degrees $[0, 360)$:
     $$\text{azi} = (\text{atan2}(-\text{dlon}, -\text{dlat}) + \pi) \times \frac{180}{\pi}$$
   * **Time Step & Speed:** Computes exact timestamp difference including hundredths of a second (`dtime = time1 - time2`). If `dtime != 0`, sets `velocity = distance / dtime`; otherwise sets `velocity = 0.0` to prevent division by zero.
   * **Quality Checks (`-check`):** Emits `warning()` messages if `dtime < mindtime`, `dtime > maxdtime`, `dtime == 0.0`, `velocity > maxvel`, `velocity < minvel`, or `velocity == 0.0`.
   * **In-Place Record Update:** Stores `tide_rec.depth = azi * 100.0` and `tide_rec.velocity = velocity`, writes `tide_rec` back to index `k` (and on the first iteration `tide_rec_no == 0`, also copies `velocity` and `depth` back into Record `0`).
3. At the end of each file, prints summary averages across the line:
   ```text
   Averages -- dtime <av_Dtime> Azi <av_Azi> Speed <av_Speed> Velocity <av_Velocity>
   ```
   where `av_Speed` is the scalar mean speed and `av_Velocity` / `av_Azi` are the vector-averaged velocity magnitude and direction.
