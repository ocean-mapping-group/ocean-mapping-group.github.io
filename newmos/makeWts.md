---
layout: default
title: makeWts
parent: Mosaicking Tools
nav_order: 4
tool_name: makeWts
source_path: code/newmos/makeWts.c
category: Backscatter & Sidescan Mosaicking
output_formats: ["MOS_weights (ASCII weight table)"]
related_tools: ["mos2", "weigh_grid"]
---

# makeWts

## Description
`makeWts` (`code/newmos/makeWts.c`) is an interactive command-line utility for generating **custom across-track priority weight tables** (`MOS_weights` by default) made of piecewise-linear ramps. It supports two output modes:
1. **Mosaicking Weight Mode (Default, for [`mos2 -custom_weight`](mos2.md))**:
   Initializes an array of `num` integers (typically `1024` for GLORIA `.ss` files, max `2048`) to `255` (the **lowest** priority weight in `mos2` / `comboMOS`), prompts the user for one or more index ranges `[start_no, end_no]` and integer weight ramps `[start_wt, end_wt]` in `0..255` (where **`0` is highest priority** and **`255` is lowest priority / do-not-mosaic**), and writes a header line (`<num>`) followed by `<index> <weight>` pairs.
2. **Gridding Weight Mode (`-grid`, for [`weigh_grid`](../grid/weigh_grid.md))**:
   Initializes an array of `num` floats to `1.0` (the **highest** weight in `weigh_grid`), prompts for floating-point weight ramps `[start_wt, end_wt]` in `0.0..1.0` (where **`0.0` is lowest weight** and **`1.0` is highest weight**), and writes `<index> 1 <weight>` lines.

---

## Usage

```bash
makeWts [-v] [-grid] [-num <N>] [-out <wtfilename>]
```

### Interactive Example (Building a 1024-Sample Custom Weight Curve for `mos2`)

Suppose you want to suppress the nadir stripe (samples `480..543` set to `255`) and favor mid-swath samples (`256` on port and `768` on starboard set to weight `10`) for a 1024-sample `.ss` sidescan swath:

```bash
$ makeWts -num 1024 -out custom_1024.wts
 priming 1024 weights with 255 (lowest weight) 

 input start no end no start_weight end_weight, (0 0 0 0 == stop)
 (e.g. 0 512 0 255 <CR> 
 (remember 0 == highest 255 == lowest weight)

makes a ramp over the first 512 weights from 0 to 255)
0 256 200 10
256 480 10 250
544 768 250 10
768 1023 10 200
0 0 0 0
```

You can then pass `custom_1024.wts` to `mos2`:
```bash
mos2 -custom_weight custom_1024.wts -swap_dirs ss/ merged/ bay_mos ss/*.ss
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-num <N>` | Number of across-track samples/beams in the weight table (maximum `2048`). If omitted on the command line, `makeWts` interactively prompts `input no. weights` on `stdin`. | Prompted (`1024` typical for `.ss`) |
| `-out <wtfilename>` | Output ASCII filename for the generated weight curve. | `MOS_weights` |
| `-grid` | Switch from `mos2` integer weight conventions (`0` = highest, `255` = lowest, output format `<idx> <wt>`) to `weigh_grid` floating-point weight conventions (`1.0` = highest, `0.0` = lowest, output format `<idx> 1 <wt>`). | Disabled (`mos2` mode) |
| `-v` | Enable verbose mode. | Disabled |

---

## Interactive Input Format & Output File Structure

At the interactive prompt, enter four whitespace-separated numbers per ramp segment:
```text
<start_no> <end_no> <start_weight> <end_weight>
```
- Constraints enforced by `makeWts`:
  - `0 <= start_no < end_no <= num - 1`
  - In default (`mos2`) mode: `0 <= start_weight, end_weight <= 255` (integer).
  - In `-grid` (`weigh_grid`) mode: `0.0 <= start_weight, end_weight <= 1.0` (float).
- Enter `0 0 0 0` to finish and write the output file.

| Mode | Output File Header | Output Row Format (`i = 0 .. num-1`) |
|---|---|---|
| Default (`mos2 -cw`) | `<num>\n` | `<i_index> <int_weight>\n` |
| `-grid` (`weigh_grid`) | *(None)* | `<i_index> 1 <float_weight_3dec>\n` |
