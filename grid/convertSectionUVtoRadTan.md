---
layout: default
title: convertSectionUVtoRadTan
parent: Grid Tools
nav_order: 14
---
---
layout: default
title: convertSectionUVtoRadTan
parent: Grid Tools
nav_order: 14
---
# convertSectionUVtoRadTan

## Description
`convertSectionUVtoRadTan` is a command-line utility designed to transform gridded U (eastward) and V (northward) velocity components, typically from an ocean model or ADCP data, into along-section and across-section velocity components. It specifically works with data representing a 2D cross-section extracted from a 3D model (e.g., using `extractVertSection`). It requires the U and V velocity grids and a separate ASCII file containing the azimuth of the profile at each point along the section. The output is three new JHC-format 32-bit floating-point (`.r4`) grids: one for along-section velocity, one for across-section velocity, and one for the current magnitude.

## Usage
```bash
convertSectionUVtoRadTan -prefix <SectionPath/SectionPrefix> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-prefix <SectionPath/SectionPrefix>` | **Required.** Specifies the base path and prefix for the input velocity and azimuth files. The tool expects: <br> - `<prefix>.uVelocity.r4` (U-velocity) <br> - `<prefix>.vVelocity.r4` (V-velocity) <br> - `<prefix>.uVelocity.llazi` (profile azimuths). <br> Output files will be named: <br> - `<prefix>.AlongVel.r4` <br> - `<prefix>.AcrossVel.r4` <br> - `<prefix>.cMagnitude.r4` | `-prefix SalishSea_Data/Converted/Section_A/section_profile` |
| `-testrot` | Enables an interactive test mode where the user can manually input U, V, and azimuth values to see the calculated along-section and across-section components. | |
| `-v` | Enable verbose output during processing. | |

## How It Works
1.  **File Opening:** Opens the input `.r4` grids for U-velocity and V-velocity, and the ASCII file for profile azimuths. Creates three new `.r4` grids for along-section velocity, across-section velocity, and current magnitude.
2.  **Header Reading:** Reads the `JHC_header` from the input `.r4` files, ensuring dimensions match.
3.  **Data Processing:** Iterates through each grid cell:
    *   Reads `u_velocity` and `v_velocity` from the respective grids.
    *   Reads `profile_azimuth` from the azimuth file.
    *   Calculates `current_magnitude` from `u_velocity` and `v_velocity`.
    *   Calculates `along_section_velocity` and `across_section_velocity` by rotating the U and V components into the coordinate system defined by `profile_azimuth`.
    *   Writes these three calculated values to their respective output `.r4` grids.
4.  **`testrot` Mode:** If `-testrot` is enabled, it provides an interactive prompt to input U, V, and azimuth values and displays the calculated radial and tangential components.

## Output Files
*   `<prefix>.AlongVel.r4`: JHC-format `.r4` grid for along-section velocity.
*   `<prefix>.AcrossVel.r4`: JHC-format `.r4` grid for across-section velocity.
*   `<prefix>.cMagnitude.r4`: JHC-format `.r4` grid for current magnitude.

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions.
*   `support.h`: For general utility functions and error handling.
*   `math.h`: For trigonometric functions.

## Notes
This tool is crucial for analyzing current patterns in ocean models or ADCP data along specific transects. By transforming the velocities into along-section and across-section components, it simplifies the interpretation of flow dynamics relative to the section orientation.
