---
layout: default
title: dumpnav
parent: Navigation Tools
nav_order: 16
tool_name: dumpnav
source_path: code/nav/dumpnav.c
category: Navigation & Georeferencing
input_formats: [".nav (jcu_nav_rec binary)"]
output_formats: [".txt (ASCII text)"]
related_tools: ["appendNav", "appendNav_asciiSecs", "stripNav", "mergeNav"]
---

# dumpnav

## Description
`dumpnav` is a lightweight utility that reads a binary 48-byte OMG navigation file (`jcu_nav_rec`, `.nav`) and dumps its timestamps, latitude, longitude, and optional speed (`-speed`), azimuth/height/tide (`-azi`), and integer depth (`-depth`) fields to an ASCII text file.

If `-out <output_filename>` is not specified on the command line, `dumpnav` automatically strips the extension from the input filename and writes to `<basename>.txt`.

---

## Usage

```bash
dumpnav [OPTIONS] <filename.nav>
```

### Common Workflow Examples

**1. Dump a `.nav` file to `<basename>.txt` with default human-readable calendar dates (`YYYY Mon DD HH:MM:SS`):**
```bash
dumpnav merged/JD100/0001_line.nav
# Writes merged/JD100/0001_line.txt
```

**2. Dump Unix epoch timestamps (with hundredths of a second), lat, lon, speed, azimuth, and depth to a custom file:**
```bash
dumpnav -1970 -speed -azi -depth -out full_nav_dump.txt merged/JD100/0001_line.nav
```

**3. Dump Julian Day timestamps (`YYYY JDAY HH:MM:SS`) decimated to every 10 seconds:**
```bash
dumpnav -jday -skip 10 -out decimated_10s.txt merged/JD100/0001_line.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<filename>` | **Required.** Input binary `.nav` file (`jcu_nav_rec` format). Only a single input file is accepted (`unknown appendage` error if multiple positional args are passed). | None |
| `-out <output_filename>` | Explicit path for the output ASCII file. | `<input_basename>.txt` |
| `-1970` | Format the timestamp column as fractional seconds since Jan 1, 1970 (`%.2lf`, combining `nav_rec.time + nav_rec.centisecs / 100.0`). | Disabled (`%Y %n %D %T`) |
| `-jday` | Format the timestamp column as `YYYY JDAY HH:MM:SS` (`stdtime_nicetime` format `"%Y %j %T"`). Overridden if `-1970` is also set. | Disabled (`%Y %n %D %T`) |
| `-speed` | Append `nav_rec.velocity` (`%.3f`) to each output line. | Disabled |
| `-azi` | Append `nav_rec.azi` (`%.3f`) to each output line. | Disabled |
| `-depth` | Append `nav_rec.depth` (`%d`) to each output line. | Disabled |
| `-skip <seconds>` | Only output records whose integer Unix timestamp is an exact multiple of `<seconds>` (`((int)nav_rec.time) % skip < 1`). | `0` (dump every record) |
| `-v` | Increment internal `verbose` counter. | Disabled |

---

## Output Format Details

Each line written to the output file has the structure:
```text
<timestamp_string> <lat_deg> <lon_deg> [velocity] [azi] [depth]
```
Where `<timestamp_string>` depends on the time-format flag:
* **Default (neither `-1970` nor `-jday`):** `stdtime_nicetime(string, "%Y %n %D %T", (int)nav_rec.time)` -> e.g., `2022 Apr 10 14:23:05` (1-second resolution).
* **`-jday`:** `stdtime_nicetime(string, "%Y %j %T", (int)nav_rec.time)` -> e.g., `2022 100 14:23:05` (1-second resolution).
* **`-1970`:** `sprintf(string, "%.2lf", (double)nav_rec.time + (double)nav_rec.centisecs / 100)` -> e.g., `1649597785.24` (0.01-second resolution).

Optional trailing columns are appended in the fixed order `[velocity] [azi] [depth]` whenever `-speed`, `-azi`, and/or `-depth` are specified.

---

## How It Works

1. Parses command-line flags and verifies that a single input `<filename>` was provided.
2. Opens `<filename>` for reading and opens either the `-out` file or `mem_strappend(mem_stripext(filename), ".txt")` for writing.
3. Seeks to the end of the `.nav` file to compute `length = ftell(nav_file) / JCU_BINNAV_RECLEN` (48 bytes per record).
4. Loops over $i = 0 \dots \text{length}-1$:
   * Reads record $i$ via `nav_read(nav_file, i, &nav_rec)`.
   * Checks the time modulo condition `if (!skip || ((int)nav_rec.time) % skip < 1)`.
   * Formats the timestamp string (`-1970`, `-jday`, or default calendar date) and prints `lat`, `lon`, and any requested optional fields (`-speed`, `-azi`, `-depth`) to `outfile`.
