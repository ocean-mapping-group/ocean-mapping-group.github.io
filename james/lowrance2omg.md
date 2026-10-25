---
layout: default
title: lowrance2omg
parent: James Muggah — Global Mapper Tiles & Utils (james)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 4
tool_name: lowrance2omg
source_path: code/james/lowrance2omg.c
category: Sonar Format Unravelers (james)
input_formats:
- .sl2 (Lowrance Sonar Log v2)
output_formats:
- .merged
- .merged.ss_data
- .nav
- .trc
- .llz
related_tools:
- jview
- swathed
- mergeNav
- getBounds
---

# lowrance2omg

## Description
`lowrance2omg` (written by John Hughes Clarke and James Muggah, October 2013) unpacks Lowrance `.sl2` consumer/recreational singlebeam and downscan sonar log files into standard Ocean Mapping Group (OMG) formats:
* `<outname>.merged` — OMG-HDCS v3 bathymetry file (`toolType = Knudsen_320`, 2 beams per ping) storing nadir depth in `beams[0].observedDepth` (mm) and pointers (`beams[0].offset`, `beams[0].no_samples`) to the full acoustic envelope trace.
* `<outname>.merged.ss_data` — Sub-bottom / singlebeam acoustic trace data sidecar for `<outname>.merged` (viewable in `swathed`'s `SE_SUBBOTwin` sub-bottom profiler window).
* `<outname>.nav` — Binary `jcu_nav_rec` navigation file containing unique GPS fixes converted from Lowrance Spherical Mercator meters (`positionX`, `positionY`) to WGS84 latitude/longitude.
* `<outname>.trc` — Raw 1600-sample 8-bit acoustic envelope traces (2-sample decimated from the 3216-byte `.sl2` chunk).
* `<outname>.llz` — ASCII `<lat> <lon> <depth_m>` soundings (converting Lowrance depth from feet to meters via $\times 0.304$).

---

## Usage

```bash
lowrance2omg -start_time <year> <jday> <hour> <min> <sec> [-shift <bytes>] [-v] -in <infile.sl2> -out <outprefix>
```

### Example

```bash
lowrance2omg -start_time 2013 287 16 21 31 -in Sonar0001.sl2 -out lowrance_line01
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <infile.sl2>` | Input Lowrance `.sl2` binary sonar log file. | Required |
| `-out <outprefix>` | Base output prefix; creates `<outprefix>`, `<outprefix>.nav`, `<outprefix>.trc`, `<outprefix>.llz`, `<outprefix>.merged`, and `<outprefix>.merged.ss_data`. | Required |
| `-start_time <yr> <jd> <hr> <mn> <sc>` | Survey start timestamp (5 integers: Year, Julian Day, Hour, Minute, Second), converted to Unix epoch seconds via `stdtime_from_jul_day` to anchor `summary.refTime`. | Required |
| `-shift <bytes>` | Byte offset adjustment applied via `fseek(infile, shift, SEEK_CUR)` after reading the 10-byte `.sl2` file header (`format`, `bytesPerChunk`, `terminal`). | `-2` |
| `-v` | Verbose mode: dumps all 35 integer/float header slots of each 140-byte `.sl2` ping header and prints decoded `timeOffset`, `positionX`, `positionY`, `lowerLimit`, `waterTemp`, `speed`, `track`, `altitude`, and `depth`. | Disabled |

---

## How It Works

1. **`.sl2` File Header & Chunk Layout:**
   Reads the 10-byte file header (`int format`, `int bytesPerChunk`, `short terminal`), seeks by `shift` (default `-2` bytes), and computes `numChunks = (filesize - 10) / bytesPerChunk`.
2. **Ping Header & Trace Extraction:**
   For each chunk, reads `3216` bytes (`trace`), averages adjacent acoustic samples starting at offset `143` (`2+16+125`) into a 1,600-byte array (`ktrace[1600]`), and writes `ktrace` to `<outprefix>.trc` and `<outprefix>.merged.ss_data`.
3. **Coordinate & Depth Conversion:**
   Extracts 32-bit fields from the 140-byte ping header:
   * `timeOffset` (ms) at byte `0` (`0*4`)
   * `lowerLimit` (ft) at byte `44` (`11*4`)
   * `depth` (ft) at byte `64` (`16*4`)
   * `speed` at byte `100` (`25*4`), `waterTemp` at byte `104` (`26*4`)
   * `positionX` (Mercator Easting m) at byte `108` (`27*4`), `positionY` (Mercator Northing m) at byte `112` (`28*4`)
   * `track` at byte `120` (`30*4`), `altitude` at byte `124` (`31*4`)
   Converts `(positionX, positionY)` to WGS84 `(lat, lon)` using radius `OTHER_WGS = 6356752.3142`:
   $$\text{lat} = \left(2\arctan\left(e^{\text{positionY} / R}\right) - \frac{\pi}{2}\right)\frac{180}{\pi}, \qquad \text{lon} = \frac{\text{positionX}}{R}\frac{180}{\pi}$$
   Whenever `(positionX, positionY)` changes from the previous ping, writes a new `jcu_nav_rec` to `<outprefix>.nav`.
4. **OMG-HDCS `.merged` & `.merged.ss_data` Generation:**
   For every ping with non-zero `depth`, writes `<lat> <lon> <depth * 0.304>` to `<outprefix>.llz` and appends a profile + 2-beam record (`toolType = Knudsen_320`) to `<outprefix>.merged`, encoding sample interval scaling into `profile.samp_rate` and `profile.edflag` and linking `beams[0].offset` to the byte offset in `<outprefix>.merged.ss_data`.
