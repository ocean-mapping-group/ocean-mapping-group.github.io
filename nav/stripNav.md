---
layout: default
title: stripNav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 2
tool_name: stripNav
source_path: code/nav/stripNav.c
category: Navigation & Georeferencing
input_formats:
- .merged
- .ss
output_formats:
- .nav
- .nav.strip
- ASCII text
- .orientation
related_tools:
- mergeNav
- appendNav
- doallWEB_Tide
- read_kmall
- jview
---

# stripNav

## Description
`stripNav` extracts a navigation time series (or attitude, tide, outer-beam positions, or average sidescan backscatter) from one or more OMG-HDCS `.merged` files or GLORIA `.ss` sidescan files and writes the output into a binary `jcu_nav_rec` file (48 bytes per record) or an ASCII table.

In the Kongsberg `.kmall` unraveling pipeline (`unravel_KMALL_single`), `stripNav` is called immediately after `getBounds` and `doallWEB_Tide` to extract the ping-by-ping navigation track and merged tidal height from the `.merged` file into `<line>.nav.strip`:

```bash
stripNav -comp merged/$SUBDIR/$LINE_NUMBER.nav.strip merged/$SUBDIR/$LINE_NUMBER.merged
```
Because `stripNav` stores `profile.tide` in `tide_rec.depth` and vessel heading (or roll/pitch/heave if requested) in `tide_rec.azi`, it is widely used both for trackline plotting in `jview` and for inspecting tidal or attitude records embedded in `.merged` files.

---

## Usage

```bash
stripNav [OPTIONS] -comp <output_nav_or_ascii_file> <input_file(s).merged | .ss>
```

### Common Examples

**1. Extract ping-by-ping binary navigation from a `.merged` file (standard unravel step):**

```bash
stripNav -comp merged/JD100/0001_line.nav.strip merged/JD100/0001_line.merged
```

**2. Extract decimated navigation (every 10th ping) only for pings that have valid unflagged depths:**

```bash
stripNav -skip 10 -with_valid_depths -comp active_survey.nav merged/JD100/*.merged
```

**3. Dump ASCII time series of timestamp, lat/lon, time/distance step, heading, roll, pitch, and heave:**

```bash
stripNav -ascii -plusll -plusdtdm -comp motion_dump.txt merged/JD100/0001_line.merged
```

**4. Extract heading from a GLORIA `.ss` sidescan file into an OMG `.orientation` file (e.g., for EdgeTech systems where heading was only logged in sidescan):**

```bash
stripNav -ss -dumpss_att extracted.orientation -comp temp.nav ss/JD100/0001_line.ss
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output filename (binary `jcu_nav_rec` format by default, or ASCII if `-ascii` / `-proj_re_map` is specified). | None |
| `<mergefile(s)>` | **Required.** One or more input `.merged` files (up to 300 files), or `.ss` files if `-ss` is specified. | None |
| `-skip <N>` | Extract every $N$-th ping profile from the input file(s). | `1` (every ping) |
| `-ss` | Input file(s) are GLORIA `.ss` sidescan files rather than OMG-HDCS `.merged` files. | Disabled (`.merged`) |
| `-unique` | Only write a record if its latitude differs from the previous record (`oldlat != tide_rec.lat`), suppressing duplicate fixes when ping rate exceeds GPS update rate. | Disabled |
| `-with_valid_depths` | Only strip navigation for pings that contain at least one valid, unflagged sounding (`observedDepth != 0 && status == 0`). Useful for plotting coverage after editing in `swathed`. | Disabled |
| `-roll` | Store vessel roll (degrees) in the `.nav` record's `azi` field instead of heading. | Disabled |
| `-pitch` | Store vessel pitch (degrees) in the `.nav` record's `azi` field instead of heading. | Disabled |
| `-heave` | Store vessel heave (meters) in the `.nav` record's `azi` field instead of heading. | Disabled |
| `-heading` | Explicitly store vessel heading (degrees) in the `.nav` record's `azi` field (this is also the default behavior). | Enabled |
| `-ascii` | Write output as an ASCII text file (`JDAY HH MM SS secfrac ping_time [lat lon] [dtime ddist] heading roll pitch heave`) instead of binary `jcu_nav_rec`. | Binary `.nav` |
| `-plusll` | Used with `-ascii`. Includes `lat lon` (8 decimal places) in the ASCII output columns. | Disabled |
| `-plusdtdm` | Used with `-ascii`. Includes inter-ping time step `dtime` (seconds) and distance step `ddist` (meters) in the ASCII output columns. | Disabled |
| `-proj_re_map <mapfile>` | Projects each ping's `(lon, lat)` onto the coordinate grid of `<mapfile>` (an OMG1 `JHC_header` mapsheet) and writes ASCII rows (`mapx mapy heading roll pitch heave surf_sound_speed`) for pings falling inside the map bounds. Automatically enables `-ascii`. | Disabled |
| `-dumpss_att <attfile>` | Used with `-ss`. Extracts the heading from a GLORIA `.ss` sidescan file and writes a valid OMG-HDCS v3 `.orientation` attitude file (`<attfile>`) so heading can be merged back onto bathymetry. | Disabled |
| `-dump_dB_val` | Used with `-ss`. Computes the average starboard sidescan backscatter intensity (in dB) for each ping and stores it in `tide_rec.velocity`. | Disabled |
| `-dB_threshold <dB>` | Used with `-ss -dump_dB_val`. Counts and reports the percentage of pings whose average backscatter falls below `<dB>` (e.g., `-20.0` dB) to detect acoustic dropouts or bubble sweepdown. | `0` |
| `-v` | Verbose output (warns on non-unique navigation fixes). | Disabled |

---

## Output Format Details

### Binary Mode (Default)
Writes 48-byte `jcu_nav_rec` structures to the `-comp` file:
* `lat`, `lon`: Transducer latitude and longitude in decimal degrees (computed via `locate_transducer(&profile, &summary, &lat, &lon)`).
* `time`, `centisecs`: Ping timestamp in seconds since Jan 1, 1970 + hundredths of a second.
* `azi`: Vessel heading in degrees (or roll, pitch, or heave if `-roll`, `-pitch`, or `-heave` is passed).
* `depth`: `profile.tide` (in millimeters) for `.merged` files, or `header.altitude` for `.ss` files.

### ASCII Mode (`-ascii`)
Each line contains:

```text
<jday> <hour> <min> <sec> <secfrac> <unix_time> [lat lon] [dtime ddist] <heading> <roll> <pitch> <heave>
```
If `-proj_re_map <mapfile>` is used, each line contains:

```text
<mapx_px> <mapy_px> <heading_deg> <roll_deg> <pitch_deg> <heave_m> <surf_sound_speed_m_s>
```
