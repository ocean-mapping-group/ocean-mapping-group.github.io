---
layout: default
title: extractSVTS
parent: Grid Tools
nav_order: 28
---
---
layout: default
title: extractSVTS
parent: Grid Tools
nav_order: 28
---
# extractSVTS

## Description
`extractSVTS` is a specialized data extraction utility designed to pull a single vertical water column profile (Sound Velocity, Temperature, and Salinity) from 3D oceanographic model output for a specific geographic location and time.

The tool takes a target location and time as input. It then searches through a series of model time-slice files to find the one closest in time to the target. Using the model grid geometry, it identifies the model node(s) nearest to the target location and extracts the full vertical profile for S, T, and SV. The resulting profile is saved as a new OMG-HDCS watercolumn (`.jwc`) file. By default, it uses bilinear interpolation between the four nearest model nodes for a more accurate result.

This tool is primarily designed to work with data from the **SalishSeaCast** model.

## Usage
```bash
extractSVTS <location_option> <model_option> <parameter_files> [OPTIONS]
```

### Example
```bash
extractSVTS -jwcin dip.jwc -custom_Salish lat.r4 lon.r4 mask.r4 -param3D model/timeslice1.time model/timeslice2.time
```

## Arguments

### Location and Time Input (Choose one)
| Option | Description |
|---|---|
| `-jwcin <input.jwc>` | Specifies an OMG-HDCS watercolumn file. The tool will use the latitude, longitude, and timestamp from this file as the target for extraction. |
| `-dipin <lat> <lon> <yr> <jday> <hr> <min>` | Manually specifies the target location and time: latitude, longitude, year, Julian day, hour, and minute. |

### Model and Parameter Input (Required)
| Option | Description |
|---|---|
| `-custom_Salish <lat.r4> <lon.r4> <mask.r4>` | **Required.** Specifies the three critical geometry files that define the SalishSeaCast model grid: <br> 1. `lat.r4`: A grid of node latitudes. <br> 2. `lon.r4`: A grid of node longitudes. <br> 3. `mask.r4`: A grid defining valid water cells. |
| `-param3D <model_time_file(s)>` | **Required.** One or more `.time` files from the SalishSeaCast output. The tool searches these to find the time slice closest to the target dip time. It then uses the prefix of the closest file to find the corresponding `.salinity.r4`, `.temperature.r4`, and `.soundSpeed.r4` files for that time step. |

### Other Options
| Option | Description |
|---|---|
| `-nointerp` | Disables the default bilinear interpolation. Instead of interpolating between the four nearest model nodes, the tool will simply extract the profile from the single closest node. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Input Parsing:** Determines the target geographic location and time from either a JWC file (`-jwcin`) or manual input (`-dipin`).
2.  **Model Geometry Loading:** Loads the SalishSeaCast model grid geometry files (`lat.r4`, `lon.r4`, `mask.r4`).
3.  **Time Step Search:** Scans the list of `.time` files specified by `-param3D` to find the model time step closest to the target time.
4.  **Model Node Identification:** Locates the model node(s) closest to the target geographic location within the identified time step.
5.  **Parameter Loading:** Loads the corresponding 3D parameter grids (salinity, temperature, and sound velocity, or calculates sound velocity if not present) for the closest time step.
6.  **Profile Extraction:** Extracts the vertical profile (S, T, SV) for the target location.
    *   If `-nointerp` is not set, it uses bilinear interpolation between the four nearest model nodes to derive more accurate profile values.
    *   If `-nointerp` is set, it takes values directly from the single closest node.
7.  **Output:** Saves the extracted vertical profile as a new OMG-HDCS watercolumn (`.jwc`) file.

## Output Files
*   A new OMG-HDCS watercolumn file with a `.jwc` extension (e.g., `input.salish.jwc` or `closest.salish.jwc`).

## Dependencies
*   `array.h`: For `JHC_header` structure and grid data handling.
*   `support.h`: For general utility functions and error handling.
*   `j_EM_watercol.h`: For OMG-HDCS watercolumn file format.
*   `j_proj.h`: For coordinate projection functions.

## Notes
This tool is critical for extracting point-specific oceanographic data from complex 3D models, enabling direct comparisons with observed SVPs or providing environmental context for other analyses. The interpolation options allow users to balance computational speed with accuracy. If a sound speed grid is not available, the tool can calculate it on-the-fly using the Chen-Millero equation.

## Output File
The tool generates a single OMG-HDCS watercolumn file with a `.jwc` extension (e.g., `input.salish.jwc` or `closest.salish.jwc`). This file contains the extracted vertical profile of Sound Velocity, Temperature, and Salinity. If the sound speed file (`.soundSpeed.r4`) is not found for a given time slice, it will be calculated automatically using the Chen-Millero equation from the temperature and salinity data.
