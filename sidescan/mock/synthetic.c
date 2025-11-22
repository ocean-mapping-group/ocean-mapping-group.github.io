---
layout: default
title: synthetic
parent: Mock Tools
grand_parent: sidescan
nav_order: 13
---
# synthetic

## Description
`synthetic` is a utility designed to generate synthetic sidescan images. It creates these images based on an input grazing angle mosaic and a user-specified backscatter model, which can be either Lambertian or linear. Additionally, it has the capability to apply a "real" angular response function (derived empirically) to a grazing angle image to produce a synthetic backscatter image that mimics observed data. This tool is a key component in sidescan modeling and analysis pipelines.

## Usage
```bash
synthetic [-strip] [-real <response_file>] [-lamb <nadir_intercept>] [-linear <nadir_intercept> <slope>] -infile <grazing_mosaic> -outfile <synthetic_mosaic>
```

## Arguments

| Option | Description |
|---|---|
| `-strip` | If specified, the tool will apply a real angular response function (from `-real`) to the input grazing mosaic. |
| `-real <response_file>` | When used with `-strip`, specifies an ASCII file containing a "real" angular response function (e.g., from `build_back`'s `.resp` output). This function is used to convert grazing angles to synthetic backscatter. |
| `-lamb <nadir_intercept>` | Activates the Lambertian backscatter model. Specifies the nadir intercept (in dB) of the Lambertian curve. |
| `-linear <nadir_intercept> <slope>` | Activates the linear backscatter model. Specifies the nadir intercept (in dB) and the slope (dB/degree) of the linear relationship. |
| `-infile <grazing_mosaic>` | **Required.** The input grazing angle mosaic file (JHC image format or GLORIA format). |
| `-outfile <synthetic_mosaic>` | **Required.** The output synthetic backscatter mosaic file. |

## How It Works
The tool operates in two main modes: applying a real angular response (`-strip` with `-real`) or generating synthetic data based on a theoretical model (`-lamb` or `-linear`).

**Mode 1: Applying a Real Angular Response (`-strip` and `-real`)**
1.  **Load Real Response:** The tool reads an ASCII file (`<response_file>`) containing a "real" angular response function into the `realresponse` array. This array likely maps grazing angle digital numbers to corresponding backscatter digital numbers.
2.  **Process GLORIA File:** It reads the input GLORIA file (`grazfile`) record by record.
3.  **Apply Response:** For each pixel in the port and starboard data that is valid (not 15 or 255):
    *   It uses the grazing angle value (`graz_Rec.stbd_data[i]`) as an index into the `realresponse` array to get the synthetic backscatter value.
    *   The `graz_Rec.stbd_data[i] - 15` is used to adjust the index to the 0-239 range.
    *   The resulting synthetic backscatter value is written back into the `graz_Rec.stbd_data[i]` (and `port_data`).
4.  **Write Output:** The modified `graz_Rec` is written to the output file (`synfile`).

**Mode 2: Generating from Theoretical Models (`-lamb` or `-linear`)**
1.  **Input Grazing Mosaic:** The tool reads the input grazing angle mosaic (`grazfile`). This file is expected to be a JHC image format with a `JHC_header`.
2.  **Backscatter Model Selection:**
    *   **Lambertian (`-lamb`):** The backscatter strength `S_b` (in dB) is calculated using the formula: `S_b = lamb_intercept + 10 * log10(pow(sin(graz_ang), 2.0))`, where `graz_ang` is the grazing angle in radians.
    *   **Linear (`-linear`):** The backscatter strength `S_b` (in dB) is calculated using the formula: `S_b = linear_intercept + linear_slope * theta`, where `theta` is the grazing angle in degrees (scaled from DN).
3.  **Pixel-by-Pixel Generation:** For each pixel in the input grazing angle mosaic:
    *   It converts the 8-bit grazing angle value (`graz_rec[i]`) to a grazing angle in degrees (`theta`) and then radians (`graz_ang`).
    *   It applies the chosen backscatter model (`-lamb` or `-linear`) to calculate `S_b`.
    *   `S_b` is then scaled and converted to an 8-bit digital number (`DN_value`) based on the `min_dB` and `max_dB` range.
    *   The resulting `DN_value` is written to the `syn_rec` array.
4.  **Write Output:** The `syn_rec` (synthetic backscatter image data) is written to the output file (`synfile`), preceded by the `JHC_header`.
