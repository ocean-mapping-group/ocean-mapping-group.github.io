---
layout: default
title: mapGenericADCP
parent: ADCP Tools
nav_order: 9
tool_name: mapGenericADCP
source_path: code/adcp/mapGenericADCP.c
category: adcp
input_formats:
  - jcu_nav Navigation (.nav / .decXX.nav)
  - JHC 32-bit Float Velocity Arrays (.N.r4, .E.r4, .D.r4)
  - OMG Map Sheet (.map / .blank)
output_formats:
  - JHC 32-bit Float Section Grids (.N.r4, .E.r4, .D.r4, .Mag.r4, .Azi.r4, .Rad.r4, .Tan.r4)
  - Hit Count History (.history)
  - ASCII NED Profile Summary (.NED_av.txt)
related_tools:
  - readGenericADCP
  - readADCP
  - makeVectorPlot
---

# mapGenericADCP

## Description
`mapGenericADCP` is a command-line utility that georeferences and projects generic or Kongsberg EC150 binned ADCP (Acoustic Doppler Current Profiler) 3D velocity datasets onto a 2D cross-sectional mapsheet grid. It reads a `jcu_nav` navigation file (`<prefix>.nav` or `<prefix>.decXX.nav`) alongside its companion North (`<prefix>.N.r4`), East (`<prefix>.E.r4`), and Downward (`<prefix>.D.r4`) floating-point velocity rasters, bins all ensembles falling within the target `.map` bounds, and outputs 7 co-registered `.r4` velocity component sections.

## Usage
```bash
mapGenericADCP -map <map.blank> -Xpixel <x_size> -Zpixel <z_size> -in <infile(s)> -out <outfileprefix> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-in <infile(s)>` | **Required.** One or more input navigation files (`.nav`). The tool automatically opens the companion `.N.r4`, `.E.r4`, and `.D.r4` velocity component files. | `-in survey1.dec3.nav` |
| `-out <outfileprefix>`| **Required.** Prefix for the output JHC `.r4` section files. | `-out adcp_section` |
| `-map <map.blank>` | **Required.** Blank JHC/OMG `.map` file defining the geographic bounds and rotation of the output section. | `-map section_line.map` |
| `-Xpixel <size>` | **Required.** Horizontal pixel size (width) in the output section, in meters. | `10.0` |
| `-Zpixel <size>` | **Required.** Vertical pixel size (depth bin height) in the output section, in meters. | `1.0` |
| `-mindepth <meters>` | Minimum depth to include in the output section. | `50.0` |
| `-maxdepth <meters>` | Maximum depth to include in the output section. | `150.0` |
| `-time_start <Y J H M S>`| Start time filter (Year, Julian Day, Hour, Minute, Second). | `-time_start 2023 145 16 22 00` |
| `-time_end <Y J H M S>` | End time filter. | `-time_end 2023 145 18 30 00` |
| `-reducedY <top> <bottom>` | Restricts processing to a specific Y-coordinate corridor within the input map. | `-reducedY 4000 4500` |
| `-alongmap` / `-orthomap` | Orient the output section along the map's primary X-axis (`-alongmap`, default) or orthogonal to it (`-orthomap`). | `-alongmap` |
| `-lr_flip` / `-no_flip` | Flip the output section left-to-right (`-lr_flip`) or keep standard orientation (`-no_flip`, default). | `-no_flip` |
| `-dump_NED_averages` | Write an ASCII summary file (`<outfileprefix>.NED_av.txt`) of the section-averaged N, E, D profile. | |
| `-v` | Enable verbose output. | |
| `-testrot` | Diagnostic mode to test vector rotation calculations without processing files. | |

## Output Files

*   **`<outfileprefix>.N.r4`**, **`<outfileprefix>.E.r4`**, **`<outfileprefix>.D.r4`**: 2D sections of North, East, and Downward velocity components (m/s).
*   **`<outfileprefix>.Mag.r4`**, **`<outfileprefix>.Azi.r4`**: 2D sections of horizontal current speed (m/s) and geographic direction (degrees true).
*   **`<outfileprefix>.Rad.r4`**, **`<outfileprefix>.Tan.r4`**: 2D sections of radial (along-section) and tangential (cross-section) velocity components relative to the mapsheet rotation.
*   **`<outfileprefix>.history`**: Log of processed input files and pixel hit counts.
*   **`<outfileprefix>.NED_av.txt`**: (With `-dump_NED_averages`) ASCII table of section-averaged N, E, D velocities vs. depth.
