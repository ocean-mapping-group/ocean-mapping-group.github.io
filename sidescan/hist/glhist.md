---
layout: default
title: glhist
parent: Histogram Tools
grand_parent: sidescan
nav_order: 3
---
# glhist

## Description
`glhist` is a utility designed for "Chavez-like histogram equalization" on JCU GLORIA format files, particularly suited for EM-12 type data. This tool corrects for across-track variations in intensity, essentially destriping the imagery by normalizing pixel values based on statistical properties. It supports both a static equalization derived from the entire dataset and a more dynamic rolling average normalization for more localized corrections.

## Usage
```bash
glhist [-invalid <value>] [-roll <size>] [-show_sections] [-v] [-normalize <value>] [-first <ping>] [-last <ping>] [-start <pixel>] [-finish <pixel>] <rawfile> <eqfile>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-invalid <value>` | Specifies the pixel value that represents invalid data. These pixels are ignored in calculations. | `255` |
| `-roll <size>` | Activates rolling average normalization. Specifies the number of pings to use for calculating the rolling average. | `0` (static equalization) |
| `-show_sections` | Used with `-roll`, for debugging the sectioning and interpolation process. | (None) |
| `-v` | Enable verbose output. | (None) |
| `-normalize <value>` | Specifies a value to normalize the overall average intensity to. | `0.0` (calculated average) |
| `-first <ping>` | Specifies the first ping (record) number to include in the statistical analysis. | `0` |
| `-last <ping>` | Specifies the last ping (record) number to include in the statistical analysis. | `no_recs` (end of file) |
| `-start <pixel>` | Specifies the starting across-track pixel index to include in calculations. | `0` |
| `-finish <pixel>` | Specifies the ending across-track pixel index to include in calculations. | `1024` |
| `<rawfile>` | **Required.** The input JCU GLORIA file. |
| `<eqfile>` | **Required.** The output JCU GLORIA file with histogram equalization applied. |

## How It Works
The tool operates in two primary modes: static equalization or rolling average normalization.

**Static Equalization (Default, if `-roll` is not used):**
1.  **Calculate Average Profile:**
    *   It iterates through the specified ping range (`-first` to `-last`) and pixel range (`-start` to `-finish`).
    *   For each across-track pixel position `j`, it calculates `sum_data[j]` (sum of pixel values) and `count[j]` (number of valid pixels).
    *   `sum_data[j]` is then divided by `count[j]` to get the average intensity profile across the swath.
    *   An overall `average` intensity across the entire swath is also computed. This can be overridden by `-normalize`.
2.  **Apply Equalization:**
    *   It then re-reads the input file record by record.
    *   For each valid pixel `in_rec.stbd_data[j]`:
        *   `newvalue = (float)in_rec.stbd_data[j] - sum_data[j];` (removes the average profile)
        *   `newvalue = average + newvalue * Scale;` (adds back the overall average, scaled).
    *   The `newvalue` is clamped between 1.0 and 255.0.
    *   The modified pixel is written to the output record.

**Rolling Average Normalization (if `-roll` is used):**
1.  **Sectioning and Rolling Averages:**
    *   The input file is divided into sections of `roll_size` pings.
    *   For each section, it calculates `roll_sum_data[section][j]` (sum of pixels at position `j` within the section) and `roll_avg[section]` (overall average intensity for the section).
2.  **Interpolated Averages:**
    *   When processing each ping `i` for output, it interpolates the `interp_avg` and `interp_sum_data` from the `roll_avg` and `roll_sum_data` of the surrounding sections. This creates a dynamically changing reference profile.
3.  **Apply Normalization:**
    *   For each valid pixel `in_rec.stbd_data[j]`:
        *   `newvalue = (float)in_rec.stbd_data[j] - interp_sum_data;` (removes the local average profile)
        *   `newvalue = interp_avg + newvalue * Scale;` (adds back the interpolated overall average, scaled).
    *   The `newvalue` is clamped between 1.0 and 255.0.
    *   The modified pixel is written to the output record.
