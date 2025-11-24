---
layout: default
title: convert3D_TSZ_to_SV
parent: Grid Tools
nav_order: 13
---
---
layout: default
title: convert3D_TSZ_to_SV
parent: Grid Tools
nav_order: 13
---
# convert3D_TSZ_to_SV

## Description
`convert3D_TSZ_to_SV` is a specialized command-line utility for converting 3D gridded Salinity (S), Temperature (T), and Depth (Z) data into Sound Velocity (SV) profiles. It's designed to process output from oceanographic models (specifically mentioned SalishSeaCast NetCDF files, which are converted to JHC `.r4` grids for S, T, and Z at various layers). For each grid cell and depth layer, it reads S and T values, uses the corresponding Z from a `.zvals` file, calculates pressure, and then computes sound velocity using the Chen-Millero equation. The output is a new set of JHC `.r4` grid files for sound velocity for each depth layer, along with copied `.zvals` and `.time` files.

## Usage
```bash
convert3D_TSZ_to_SV -prefix <SectionPath/SectionPrefix> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-prefix <SectionPath/SectionPrefix>` | **Required.** Specifies the base path and prefix for the input S, T, and Z data files. The tool expects files named `<prefix>.salinity.r4`, `<prefix>.temperature.r4`, and `<prefix>.salinity.zvals`. The output sound velocity file will be named `<prefix>.soundSpeed.r4`. | `-prefix SalishSea_Data/Converted/2024-10-26/salishsea.2024_jd299_12-00-00_Oct-26` |
| `-testTSZtoSv` | Enables an interactive test mode where the user can manually input Salinity, Temperature, and Depth values to see the calculated Sound Velocity. | |
| `-v` | Enable verbose output during processing. | |

## How It Works
1.  **File Opening:** Opens the input `.r4` grids for salinity (`.salinity.r4`), temperature (`.temperature.r4`), and the `.zvals` file. Creates a new `.r4` grid for sound velocity (`.soundSpeed.r4`).
2.  **Header Reading:** Reads the `JHC_header` from the input `.r4` files, ensuring dimensions match.
3.  **Data Processing:** Iterates through each grid cell and each depth layer:
    *   Reads `salinity` and `temperature` values from the respective grids.
    *   Reads `depth` from the `.zvals` file.
    *   Calculates `pressure` from `depth`.
    *   Computes `sound_velocity` using the Chen-Millero equation (an empirical formula for calculating sound speed from salinity, temperature, and pressure).
    *   Writes the calculated `sound_velocity` to the output `.soundSpeed.r4` grid.
4.  **Auxiliary File Copying:** Copies the input `.zvals` and `.time` files to new output files with the `<prefix>` and appropriate extensions.

## Output Files
*   `<prefix>.soundSpeed.r4`: A JHC-format 32-bit floating-point grid file containing sound velocity for each grid cell and depth layer.
*   `<prefix>.zvals`: Copied `.zvals` file.
*   `<prefix>.time`: Copied `.time` file.

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions.
*   `support.h`: For general utility functions and error handling.
*   Internal functions for Chen-Millero equation (`vchemilli`).

## Notes
This tool is specifically designed for processing SalishSeaCast model output, but the underlying principle of converting TSZ to SV using empirical equations is broadly applicable in oceanography. The accuracy of the calculated sound velocity depends on the quality of the input S, T, and Z data and the chosen empirical equation. The `-testTSZtoSv` option is useful for quick verification of the sound velocity calculation.
