---
layout: default
title: appendNav_asciiSecs
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 12
tool_name: appendNav_asciiSecs
source_path: code/nav/appendNav_asciiSecs.c
category: Navigation & Georeferencing
input_formats:
- .nav (jcu_nav_rec binary)
- .r4 / OMG1 mapsheet (-area)
output_formats:
- .nav (jcu_nav_rec binary)
- ASCII text (-ascii, -excel, -arc)
related_tools:
- appendNav
- stripNav
- dumpnav
- mergeNav
---

# appendNav_asciiSecs

## Description
`appendNav_asciiSecs` is a streamlined variant of [`appendNav`](appendNav.html) that concatenates, decimates (`-skip`), filters by quality flag (`-goodonly`), clips by geographic bounding box (`-area` or interactive `-region`) or time window (`-start` / `-end`), shifts coordinates (`-latshift` / `-lonshift`), and exports up to 1,000 binary OMG navigation files (`jcu_nav_rec`, `.nav`).

When exporting to ASCII (`-ascii`), `appendNav_asciiSecs` formats the seconds field with hundredths-of-a-second precision (`%05.2f`, combining `tm_sec + centisecs / 100.0`) or, when `-excel` is also passed, outputs the Unix epoch timestamp in seconds (`(double)tide_rec.time`) alongside `lat`, `lon`, `azi`, and `velocity`.

---

## Usage

```bash
appendNav_asciiSecs [OPTIONS] -comp <output_file> <input_nav_file(s)>
```

### Common Workflow Examples

**1. Export binary `.nav` files to ASCII with fractional seconds (`%05.2f`):**

```bash
appendNav_asciiSecs -ascii -goodonly -comp track_secs.txt merged/JD100/*.nav
```

**2. Export binary `.nav` files to Excel-friendly ASCII with Unix epoch seconds (`-ascii -excel`):**

```bash
appendNav_asciiSecs -ascii -excel -goodonly -comp track_epoch.txt merged/JD100/*.nav
```

**3. Export ArcGIS CSV track points with directory and line name attributes (`-ascii -arc`):**

```bash
appendNav_asciiSecs -ascii -arc -skip 10 -comp arc_points.csv merged/JD100/*.nav
```

**4. Clip and concatenate binary `.nav` files within a mapsheet's geographic bounds and a UTC time window:**

```bash
appendNav_asciiSecs -area survey_grid.r4 \
    -start 2022 180 12 00 -end 2022 180 18 30 \
    -comp clipped_afternoon.nav merged/JD180/*.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output filename (binary `.nav` by default, or ASCII/CSV if `-ascii` is set). | None |
| `<mergefile(s)>` | **Required.** One or more binary `.nav` files (up to 1,000 files). | None |
| `-skip <N>` | Read and output every $N$-th record from each input `.nav` file. | `1` (every record) |
| `-goodonly` | Exclude navigation records flagged as bad (`tide_rec.flag[3] != 0`). | Disabled (include all) |
| `-start <yr> <jday> <hr> <min>` | Minimum UTC time filter (requires 4 integers: 4-digit year, Julian day, hour, minute). | Disabled |
| `-end <yr> <jday> <hr> <min>` | Maximum UTC time filter (requires 4 integers: 4-digit year, Julian day, hour, minute). Used together with `-start`. | Disabled |
| `-area <array.file>` | Clip navigation fixes to the geographic bounding box (`xmin`, `xmax`, `ymin`, `ymax`) of an OMG1 `JHC_header` mapsheet file. | Disabled |
| `-region` | Interactively prompt on `stdin` via `get_area()` for minimum/maximum latitude and longitude bounds. | Disabled |
| `-latshift <deg>` | Add a constant latitude offset (decimal degrees) to every output fix. | `0.0` |
| `-lonshift <deg>` | Add a constant longitude offset (decimal degrees) to every output fix. | `0.0` |
| `-ascii` | Write ASCII text instead of binary `jcu_nav_rec`. | Binary `.nav` |
| `-excel` | Used with `-ascii`. Outputs `lat lon unix_time azi velocity` on each line. | Disabled |
| `-arc` | Used with `-ascii`. Outputs comma-separated GIS records including file index, subdirectory name, and stripped filename. | Disabled |
| `-v` | Enable verbose flag (`verbose_flag`). | Disabled |

---

## Output Format Details

### 1. Binary Mode (Default)
Writes 48-byte `jcu_nav_rec` structures sequentially via `nav_write()`.

### 2. Standard ASCII Mode (`-ascii`)
Each line contains 9 space-delimited columns (note `lon` precedes `lat`):

```text
 <lon_deg> <lat_deg> <YYYY> <JDAY> <HH> <MM> <SS.cc> <azi> <velocity>
```
Formatted via:

```c
fprintf(tidefile, " %13.8f %13.8f %4d %03d %02d %02d %05.2f %.2f %.2f\n", ...);
```

### 3. Excel ASCII Mode (`-ascii -excel`)
Each line contains 5 space-delimited columns (`lat` precedes `lon`, followed by Unix epoch time in seconds):

```text
 <lat_deg> <lon_deg> <unix_seconds> <azi> <velocity>
```

### 4. ArcGIS CSV Mode (`-ascii -arc`)
Each line contains 10 comma-separated columns:

```text
<file_idx>,<lon_deg>,<lat_deg>,<YYYY>,<JDAY>,<HH>,<MM>,<SS.cc>,<subdir_name>,<line_basename>
```

---

## How It Works

1. Parses command-line options and, if `-area` or `-region` is active, initializes the bounding box `(blat, tlat, tlon, blon)` from the `JHC_header` of `<array.file>` or interactively via `get_area()`.
2. For each input `.nav` file, computes `numrec = filesize / JCU_BINNAV_RECLEN` (48 bytes) and prints the start-of-line and end-of-line UTC timestamps and degree-decimal-minute coordinates to `stdout`.
3. Iterates through records with step `k += skip`, checking:
   * `!goodonly_flag || !tide_rec.flag[3]`
   * Geographic bounds (`lat` within `(blat, tlat)` and `lon` within `(tlon, blon)`) if `-area` or `-region` is set.
   * Time bounds (`time > mintime && time < maxtime`) if `-start` (and `-end`) is set.
4. Applies optional `-latshift`/`-lonshift` offsets and writes either binary `jcu_nav_rec` or the selected ASCII representation.
