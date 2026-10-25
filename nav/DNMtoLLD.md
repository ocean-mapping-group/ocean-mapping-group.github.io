---
layout: default
title: DNMtoLLD
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 6
tool_name: DNMtoLLD
source_path: code/nav/DNMtoLLD.c
category: Navigation & Georeferencing
input_formats:
- ASCII text (Australian Navy Division of National Mapping format)
output_formats:
- ASCII .lld / .llz (lat lon depth)
related_tools:
- Generic_to_Nav
- dohypackLNW
- dumpnav
---

# DNMtoLLD

## Description
`DNMtoLLD` reads ASCII hydrographic data files produced by the Royal Australian Navy / Division of National Mapping (DNM) and extracts valid 3-column geographic sounding records into a simple space-delimited `lat lon depth` ASCII file.

It skips the initial header line of each input file (`count == 0`), buffers character-by-character up to newline (`\n`, ASCII `10`), and unpacks any line beginning with three valid numeric values (`latitude`, `longitude`, `depth`).

---

## Usage

```bash
DNMtoLLD [OPTIONS] -comp <output_lld_file> <input_dnm_file(s)>
```

### Common Workflow Examples

**1. Convert a single Division of National Mapping file to ASCII `lat lon depth`:**

```bash
DNMtoLLD -comp survey_soundings.lld ran_dnm_sheet01.txt
```

**2. Convert and concatenate multiple DNM files with verbose debugging:**

```bash
DNMtoLLD -v -comp combined_dnm.lld dnm_part1.txt dnm_part2.txt dnm_part3.txt
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output ASCII file path (`lat lon depth` format). | None |
| `<mergefile(s)>` | **Required.** One or more input Division of National Mapping ASCII files (up to 300 files). | None |
| `-skip <N>` | Decimation value parsed on the command line (`skip = strtoint(*argv)`). | `1` |
| `-new` | Increments internal `new_flag` counter. | Disabled |
| `-v` | Enable verbose output: prints each newline character code, line character count, and parsed `lat lon` coordinates. | Disabled |

---

## Input & Output Record Formats

### Input Format
* Line-oriented ASCII text (up to 500 characters per line buffered in `telegram[500]`).
* The first line of each file (`count == 0` after incrementing from `-1`) is treated as a file header and skipped before `unpack()` is called (`if (count > 0) unpack()`).
* Subsequent lines are parsed with `sscanf(telegram, "%lf%lf%f", &lat, &lon, &depth)`. Any line that successfully yields 3 numeric tokens is treated as a valid sounding fix (`got_a_fix++`).

### Output Format
Each valid record is written to the `-comp` output file as a space-delimited ASCII line:

```text
<lat_deg> <lon_deg> <depth_m>
```
Formatted via `fprintf(tidefile, "%lf %lf %f\n", lat, lon, depth)` (6 decimal places for latitude, longitude, and depth).

---

## How It Works

1. Parses command-line options and opens the output file (`-comp`) for writing (`"w"`).
2. Loops through each input file (`name[0 .. no_files-1]`):
   * Initializes `count = -1` and `tot_char = 0`.
   * Reads the file byte-by-byte using `fgetc(file)`.
   * Appends each byte to `telegram[tot_char++]`.
   * When a newline character (`c == 10`) is encountered:
     * Prints progress every 600 records (`got %d records`).
     * Increments `count`.
     * If `count > 0` (skipping the first line of the file), calls `unpack()`, which attempts `sscanf(telegram, "%lf%lf%f", &lat, &lon, &depth)`.
     * Resets `tot_char = 0`.
   * If `got_a_fix` is set, writes `lat lon depth` to the output file and resets `got_a_fix = 0`.
3. Closes all files and exits with status `0`.
