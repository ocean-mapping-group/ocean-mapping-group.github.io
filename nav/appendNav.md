---
layout: default
title: appendNav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 3
tool_name: appendNav
source_path: code/nav/appendNav.c
category: Navigation & Georeferencing
input_formats:
- .nav
output_formats:
- .nav
- .decnav
- ASCII text
- .kml
- .curr
- .avcr
related_tools:
- read_kmall
- mergeNav
- stripNav
- jview
---

# appendNav

## Description
`appendNav` concatenates, decimates, time-sorts, clips (by geographic bounding box or time window), and exports one or more binary OMG navigation files (`.nav`, `jcu_nav_rec` format). It can handle up to 10,000 input `.nav` files in a single invocation.

In the Kongsberg `.kmall` unraveling workflow (`unravel_KMALL_single` and `unravel_KMALL_2500m_RevHplus_netatt2`), `appendNav` is used to create a 10x decimated navigation file in the `decnav/<subdir>/` directory for fast trackline plotting in `jview`:

```bash
appendNav -skip 10 -comp decnav/$SUBDIR/$LINE_NUMBER.decnav merged/$SUBDIR/$LINE_NUMBER.nav
```

---

## Usage

```bash
appendNav [OPTIONS] -comp <output_file> <input_nav_file(s)>
```

### Common Workflow Examples

**1. Decimate a line's navigation by a factor of 10 (standard Kongsberg unravel pipeline):**

```bash
appendNav -skip 10 -comp decnav/JD100/0001_line.decnav merged/JD100/0001_line.nav
```

**2. Concatenate and chronologically sort all decimated nav files from a survey into a single master trackline:**

```bash
appendNav -presortnav -goodonly -comp master_survey.nav decnav/JD*/*.decnav
```

**3. Export navigation to Google Earth KML or comma-separated ASCII:**

```bash
appendNav -kmlpath -skip 5 -comp survey_track.kml decnav/JD100/*.decnav
appendNav -ascii_comma -with_1970_time -comp survey_track.csv decnav/JD100/*.decnav
```

**4. Clip navigation to the exact time bounds of a `.merged` file or the geographic bounds of a mapsheet:**

```bash
appendNav -timeboundsof merged/JD100/0001_line.merged -comp line1_clipped.nav raw_posmv.nav
appendNav -area region.r4 -comp in_region.nav decnav/JD*/*.decnav
```

---

## Arguments

### Core Input / Output & Decimation

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output filename (binary `.nav` by default, or ASCII/CSV/KML depending on flags). | None |
| `<navfile(s)>` | **Required.** One or more binary `.nav` files (up to 10,000 files). | None |
| `-skip <N>` | Read and output every $N$-th navigation record from each input file. | `1` (every record) |
| `-goodonly` | Skip navigation records flagged as bad (`tide_rec.flag[3] != 0`). | Disabled (include all) |
| `-presortnav` | Before concatenating, read the first timestamp of every input `.nav` file and bubble-sort the file list chronologically so out-of-order filenames are appended in true time order. | Disabled |

### Time Filtering & Shifting

| Option | Description | Default |
|---|---|---|
| `-start <yr> <jday> <hr> <min>` | Only include fixes after the specified UTC Julian Day and minute. | None |
| `-end <yr> <jday> <hr> <min>` | Only include fixes before the specified UTC Julian Day and minute. | None |
| `-start_sec <yr> <jday> <hr> <min> <sec>` | Same as `-start` with 1-second resolution (alias: `-time_start`). | None |
| `-end_sec <yr> <jday> <hr> <min> <sec>` | Same as `-end` with 1-second resolution (alias: `-time_end`). | None |
| `-start_1970 <unix_sec>` | Start time in seconds since Jan 1, 1970. | None |
| `-end_1970 <unix_sec>` | End time in seconds since Jan 1, 1970. | None |
| `-sec_later <sec>` | Used with `-start_1970`; sets `maxtime = mintime + sec_later`. | None |
| `-start_rec <N>` / `-end_rec <M>` | Restrict extraction to record indices $[N, M)$ within the input file. | All records |
| `-timeboundsof <file.merged>` | Automatically read the first and last ping timestamps of `<file.merged>` and filter `.nav` records to that exact time window. | Disabled |
| `-intimeshiftsecs <sec>` | Add a constant time offset (in seconds, e.g., `86400` for +1 day) to every input nav record's timestamp. | `0.0` |
| `-delay <sec>` | Apply a time delay (seconds) to output records. | `0.0` |

### Spatial Filtering & Coordinate Shifts

| Option | Description | Default |
|---|---|---|
| `-area <mapfile>` | Only include navigation fixes that fall within the geographic bounding box of `<mapfile>` (an OMG1 `JHC_header` grid). | Disabled |
| `-region` | Interactively prompt on stdin for minimum/maximum latitude and longitude bounds. | Disabled |
| `-latshift <deg>` / `-lonshift <deg>` | Add a constant latitude or longitude offset to every output record. | `0.0` |

### Export Formats (ASCII, CSV, GIS, KML, Tidal Phase)

| Option | Description | Default |
|---|---|---|
| `-ascii` | Output space-delimited ASCII text instead of binary `jcu_nav_rec`. | Binary `.nav` |
| `-ascii_comma` | Output comma-separated values (CSV). Implies `-ascii`. | Disabled |
| `-with_1970_time` | Include Unix epoch timestamp in ASCII output. | Disabled |
| `-title_line "<string>"` | Write a custom header row at the top of the ASCII output file. | None |
| `-excel` / `-arc` / `-aldeberan` | Specialized ASCII column formatting for Excel, ArcGIS, or Aldebaran import. | Disabled |
| `-kmlpath` | Export the navigation track as an OGC KML 2.2 `<LineString>` (`yellowLineGreenPoly` style) for Google Earth visualization. | Disabled |
| `-tide_phase_sort <period_hrs> <N_steps>` | Bins records into `<N_steps>` tidal phase files (`<comp>_pstep_000.curr` .. `<N-1>.curr`) based on tidal period (e.g., `12.4206` hrs for $M_2$) relative to `-phase_zero <yr> <jday> <hr> <min>`. | Disabled |
| `-tide_sort_centre_area` | Used with `-tide_phase_sort` and `-area`; also computes average North/East currents per phase bin (`<comp>_pstep_NNN.avcr`). | Disabled |
| `-v` | Enable verbose output. | Disabled |

---

## Troubleshooting

| Symptom / Error | Cause | Resolution |
|---|---|---|
| `...puked on appendNav...` in `error.log` during unraveling | `merged/$SUBDIR/$LINE_NUMBER.nav` did not exist or could not be opened because `read_kmall` produced empty `.nav_1` or failed earlier. | Check `ls -la merged/$SUBDIR/$LINE_NUMBER.nav*`. Verify that `#SPO` position datagrams exist in the `.kmall` file and that `.nav_1` (or `.nav_2`/`.nav_3`) was copied to `.nav`. |
| `Yo start_rec and end_rec reversed?` | `-end_rec` is less than or equal to `-start_rec`. | Ensure `-end_rec` is strictly greater than `-start_rec`. |
