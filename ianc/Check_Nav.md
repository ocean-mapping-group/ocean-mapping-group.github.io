---
layout: default
title: Check_Nav
parent: Ian Church (ianc) Tools
nav_order: 1
tool_name: Check_Nav
source_path: code/ianc/Check_Nav.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats: ["OMG Binary Navigation (.nav)"]
output_formats: ["ASCII Standard Output / Grace Tabular Text"]
related_tools: ["POStoNav", "areaNavEdit", "HycomSSP", "modelAnalysis"]
---

# Check_Nav

## Description

`Check_Nav` is a diagnostic and quality-control command-line utility for inspecting binary OMG/JHC navigation files (`jcu_nav_rec`). Originally adapted by Ian Church in December 2007 from John Hughes Clarke's `NJWtoNav.c`, the program reads fixed-length binary navigation records and reports position, timing, azimuth/elevation, course-made-good (CMG) or depth, vessel velocity, and GPS quality/status flags.

In addition to human-readable record-by-record inspection, `Check_Nav` supports summary bounding-box and elevation/azimuth range extraction (`-minmax`), mean and standard deviation calculation over a user-defined value window (`-stdev`), hour-of-day filtering (`-time`), single-record lookup (`-record`), interactive paging (`-pause`), and machine-readable columnar output formatted for plotting in Grace/xmgrace (`-grace`).

## Usage

```bash
Check_Nav [-v] [-record <rec_no>] [-pause] [-minmax] [-stdev <min> <max>] [-grace] [-time <min_hour> <max_hour>] <navfile>
```

### Example Commands

Inspect all records in a binary navigation file with interactive pausing after each record:

```bash
Check_Nav -pause survey_line01.nav
```

Print the start/end timestamps, geographic bounding box, and minimum/maximum azimuth/elevation values:

```bash
Check_Nav -minmax survey_line01.nav
```

Compute the mean and standard deviation of the azimuth/elevation field (`azi`) for values between `-5` and `5`, while also reporting bounding coordinates:

```bash
Check_Nav -minmax -stdev -5 5 survey_line01.nav
```

Export space-delimited columns for plotting in Grace:

```bash
Check_Nav -grace survey_line01.nav > survey_line01.dat
```

## CLI Arguments and Options

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-v` | None | Increments the verbosity flag (`verbose_flag`). |
| `-record` | `<int>` | Displays only the single 1-based record number specified by `<int>` and exits immediately. |
| `-pause` | None | Pauses execution after printing each navigation record and waits for the user to press `Enter` (`getchar()`). |
| `-minmax` | None | Suppresses full record dumps and computes minimum/maximum values for `azi` (azimuth/elevation), `lat`, and `lon`, along with the Julian day and UTC timestamp of the first and last records. |
| `-stdev` | `<min> <max>` | Computes the sample mean and standard deviation of the `azi` field across records whose `azi` falls within `[min, max]` (integer bounds). When combined with `-minmax`, restricts min/max tracking to records within `[min, max]`. |
| `-grace` | None | Outputs space-delimited numeric rows (`time lat lon azi velocity depth flag[0] flag[1] flag[2] flag[3]`) without headers or trailers for direct ingestion into Grace (`xmgrace`). |
| `-time` | `<min_hour> <max_hour>` | Filters normal record output to records whose UTC hour (`tm_hour` from `gmtime()`, `0`–`23`) falls inclusively between `min_hour` and `max_hour`. |
| `<navfile>` | `<path>` | Path to the input binary OMG/JHC navigation file (`jcu_nav_rec`). |

## File Formats

### Input Format
* **OMG Binary Navigation (`.nav`)**: Fixed-record binary navigation stream read via `nav_read(FILE *, unsigned int rec_no, jcu_nav_rec *)` defined in `jcu_nav.h`. Each `jcu_nav_rec` contains:
  * `time` (`int`): Unix epoch timestamp in seconds.
  * `centisecs` (`int`): Sub-second time component in hundredths of a second.
  * `lat`, `lon` (`double`): Geographic latitude and longitude in decimal degrees.
  * `azi` (`float`): Vessel heading/azimuth or GPS antenna height/elevation (e.g., when populated by `POStoNav`).
  * `depth` (`int`): Course Made Good (in centi-degrees) or bathymetric depth.
  * `velocity` (`float`): Speed over ground.
  * `flag[0..3]` (`unsigned char` / `int`): Status and quality indicators, where `flag[1]` encodes GPS quality (`1` = Single Point, `2` = Differential, `4,5` = RTK/PPK, `6` = Dead Reckoning), `flag[2]` stores the number of satellites, and `flag[3]` is commonly used for manual/spatial edit flagging (such as by `areaNavEdit`).

### Output Format
* **Standard Diagnostic Output**: Multi-line labeled blocks per record showing record index, `Latitude`, `Longitude`, `Epoch`, UTC `asctime` string, `Azimuth / Elevation`, `CMG (centi-degrees) / Depth`, `Velocity`, and `Flag 0` through `Flag 3`.
* **Grace Tabular Output (`-grace`)**: One line per record formatted as:
  ```text
  <time> <lat> <lon> <azi> <velocity> <depth> <flag0> <flag1> <flag2> <flag3>
  ```

## How It Works

1. **First Pass (Record Counting & Mean Accumulation)**: `Check_Nav` opens `<navfile>` and iterates sequentially with `nav_read()` until `feof()` is reached, counting the total number of records (`total_rec`). If `-stdev` is enabled, it accumulates `tide_rec.azi` across all records and divides by `total_rec` to establish the mean before rewinding the file pointer.
2. **Second Pass (Filtering, Statistics, and Display)**: After calling `rewind(tidefile)`, the program reads each record again:
   * If `-record <N>` was passed, a skip counter suppresses all records except record `N`, prints that record, and returns `0`.
   * Convert `tide_rec.time` to UTC broken-down time (`struct tm`) via `gmtime()`.
   * When `-minmax` is active, it prints the start time on record `0` and end time on record `total_rec - 1`, while updating `min`, `max`, `minLat`, `maxLat`, `minLon`, and `maxLon` (optionally gated by the `-stdev min max` window).
   * When `-stdev` is active, squared deviations `pow(tide_rec.azi - mean, 2)` are summed for records within `[stdev_min, stdev_max]` and finalized after the loop as `sqrt(stdev / (total_rec - 1))`.
   * Otherwise, each unskipped record passing the `-time` hour filter is printed in either verbose human-readable format or compact `-grace` tabular format.
