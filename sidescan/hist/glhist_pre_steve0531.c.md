---
layout: default
title: glhist_pre_steve0531.c
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 6
tool_name: glhist (pre-May 31 revision)
source_path: code/sidescan/hist/glhist_pre_steve0531.c
category: Sidescan Histogram & Gap Filling
input_formats:
- JCU GLORIA / EM-12 (.ss)
output_formats:
- Histogram-equalized JCU GLORIA (.ss)
related_tools:
- glhist
- glfill
- glfudge
---

# glhist_pre_steve0531.c

## Description
`glhist_pre_steve0531.c` is the baseline October 1991 implementation of [`glhist`](glhist.html) by John Hughes Clarke, preserved before May 31 modifications by Steve Hughes. It performs two-pass Chavez-style Gaussian histogram equalization on JCU GLORIA / Simrad EM-12 look-alike sidescan sonar files.

## CLI Options & Usage

```bash
glhist [-invalid <val>] <rawfile> <eqfile>
```
* **`-invalid <0..255>`**: Pixel value to exclude from histogram accumulation and leave unchanged in the output (default: `255`).
* **`<rawfile>`**: Input JCU GLORIA `.ss` sidescan file.
* **`<eqfile>`**: Output histogram-equalized `.ss` file.

## Algorithm
1. **Target Distribution (`build_target`)**: Computes a 256-bin Gaussian probability density curve centered at `DN = 127` with standard deviation `STD_DEV = 42.0` (`3σ = 127`), scaled to `10,000` total counts, and integrates its cumulative distribution `cum_target[0..255]`.
2. **Input Histogram Pass (`get_raw_distribution`)**: Reads every `gloria_rec` in `<rawfile>`, accumulating valid (`!= invalid_value` and `!= 0`) port and starboard pixels (`0..495`) into `raw[0..255]`, then normalizes to a 10,000-count cumulative distribution `cum_raw[0..255]`.
3. **Lookup Table & Remapping (`build_lut`)**: Maps each input grey level `i` to the output grey level `j` whose `cum_target[j]` best matches `cum_raw[i]`, rewinds `<rawfile>`, and writes the remapped scanlines to `<eqfile>`.
