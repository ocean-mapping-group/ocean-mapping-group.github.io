---
layout: default
title: glfill.c_bug
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 4
tool_name: glfill (Oct 1991 revision)
source_path: code/sidescan/hist/glfill.c_bug
category: Sidescan Histogram & Gap Filling
input_formats:
- JCU GLORIA / EM-12 look-alike (.ss)
output_formats:
- Gap-filled JCU GLORIA (.ss)
related_tools:
- glfill
- glfudge
- glhist
---

# glfill.c_bug

## Description
`glfill.c_bug` is an October 1991 revision of [`glfill.c`](glfill.html) written by John Hughes Clarke to interpolate invalid across-track pixels in Simrad EM-12 multibeam sidescan records stored in JCU GLORIA look-alike format (`gloria_rec`). It was preserved in `code/sidescan/hist/` prior to fixing an indexing bug when scanning across-track gaps near the outer swath edge.

## CLI Options & Usage

```bash
glfill [-invalid <val>] [-lower_level <val>] <rawfile> <fillfile>
```
* **`-invalid <0..255>`**: Digital Number representing invalid/missing data (default: `255`).
* **`-lower_level <0..255>`**: Threshold level parsed for compatibility (default: `150`).
* **`<rawfile>`**: Input JCU GLORIA `.ss` sidescan file.
* **`<fillfile>`**: Output gap-filled `.ss` file.

## Algorithm
For each scanline (`gloria_rec`), `glfill.c_bug` processes `port_data[0..495]` and `stbd_data[0..495]` independently:
1. Finds the innermost valid pixel (`start`) and outermost valid pixel (`end`) where `data[i] != invalid_value`.
2. Walks from `start` to `end`; whenever an invalid pixel run `[first_bad .. next_good - 1]` is encountered, linearly interpolates intermediate pixel values between `data[first_bad - 1]` and `data[next_good]`.
*(Note: In `glfill.c_bug`, the inner `while` loop increments `i` instead of `j` when searching for `next_good` on the port side, which was fixed in [`glfill.c`](glfill.html)).*
