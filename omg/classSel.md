---
layout: default
title: classSel
parent: OMG Tools
nav_order: 81
---
# classSel

## Description
`classSel` is a utility designed to extract and analyze backscatter characteristics from angular look-up tables (LUTs) of multibeam data. It calculates various statistical parameters, such as mean backscatter, slope of the angular response, and specific values at nadir, center, and tail angles, within user-defined spatial windows.

The tool operates on pre-generated LUT files (`.lut` and `.num`), which store backscatter values and associated metadata (profile, beam, grazing angle, intensity) for individual soundings. It effectively performs a moving window analysis over these LUTs to classify or characterize the seafloor.

## Usage
```bash
classSel -lut <LUThandle> [-step <pixels>] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-lut <LUThandle>` | **Required.** The handle (base name) for the Look-Up Table files. The tool expects `<LUThandle>.lut` and `<LUThandle>.num` files. |
| `-step <pixels>` | Specifies the size of the square analysis window (in pixels) for both X and Y dimensions. | `10` |
| `-v` | Enable verbose output. |

## How It Works
1.  **Load Information (`load_up_info`):**
    *   Opens the `.lut` (Look-Up Table) and `.num` (number of samples) files using the provided `LUThandle`.
    *   Reads the JHC headers from both files to get dimensions (`dx`, `dy`) and `data_type`.
    *   Reads the `num` array (containing the count of valid samples per pixel) into memory.
    *   **Note:** The `.lut` file (containing `Sb_value` structures) is *not* fully loaded into memory but accessed via `fseek` for individual pixels due to its potentially large size.
2.  **Windowed Analysis:**
    *   The tool iterates through the `num_header.dy` and `num_header.dx` dimensions, effectively moving a square analysis window of size `step` by `step` pixels.
    *   For each window:
        *   **Calculate Angular Dependence (`calc_ang_dep`):**
            *   Resets `Sbmean` (sum of linear backscatter) and `Sb_count` for 90-degree bins (0-89 degrees).
            *   Iterates through all pixels (`k`, `i`) within the current window.
            *   For each pixel, it `fseek`s to the corresponding location in the `.lut` file and reads `tot` (`num` of samples) `Sb_value` structures.
            *   For each `Sb_value`, it extracts the `Sb` (backscatter intensity, converted to linear scale) and `angle` (grazing angle).
            *   Accumulates `Sb` in `Sbmean[(int)angle + 0.5]` and `Sb_count[(int)angle + 0.5]++`.
            *   After processing all samples in the window, it calculates `Sbmean[i] /= Sb_count[i]` for each bin where data exists.
            *   It then calculates `Nadir`, `Centre`, and `Tail` backscatter values (in linear units, then converted to dB) by averaging `Sbmean` within specific angle ranges (80-90 deg for Nadir, 40-50 deg for Centre, 15-25 deg for Tail).
            *   **Least-Squares Fit (Commented Out):** There's commented-out code for performing a linear least-squares fit on the `10.0*log10(Sbmean[i])` vs. angle to determine `Slope` and `Average`. This is not currently active.
3.  **Output Grids:**
    *   After analyzing all windows, it creates four output `.r4` (unsigned char) files:
        *   `<LUThandle>.mea`: Mean backscatter (Centre value).
        *   `<LUThandle>.slp`: Slope of the angular response (currently `Slope` is not actively calculated in `calc_ang_dep`).
        *   `<LUThandle>.nad`: Nadir backscatter.
        *   `<LUThandle>.tai`: Tail backscatter.
    *   These output grids are created with the same header as the `num` file, and each pixel represents the calculated parameter for the corresponding analysis window. The values are scaled to `0-255` based on `dB_min` and `dB_max`.
4.  **Memory Management:** Allocates and frees memory for the output grids.
