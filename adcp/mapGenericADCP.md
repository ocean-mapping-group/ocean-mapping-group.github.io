---
layout: default
title: mapGenericADCP
parent: ADCP Tools
nav_order: 9
---

# mapGenericADCP

## Description
`mapGenericADCP` is a command-line utility that georeferences and maps generic, binned ADCP (Acoustic Doppler Current Profiler) data onto a 2D cross-sectional grid. The tool is designed to work with a specific set of input files representing the North, East, and Downward (NED) velocity components, along with a corresponding navigation file.

It projects the time-series of vertical profiles onto a spatial map, averaging the data from multiple pings/ensembles that fall into the same output grid cell. The result is a set of 2D JHC-formatted arrays representing different aspects of the current field along the specified section (e.g., North component, Magnitude, Along-track component, etc.).

## Usage
```bash
mapGenericADCP -map <map.blank> -Xpixel <x_size> -Zpixel <z_size> -in <infile(s)> -out <outfileprefix> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-in <infile(s)>` | **Required.** One or more input navigation files (`.nav`). The tool automatically infers the names of the required North (`.N.r4`), East (`.E.r4`), and Downward (`.D.r4`) velocity component files based on the input nav file's prefix. | `-in survey1.dec3.nav` |
| `-out <outfileprefix>`| **Required.** Specifies the prefix for the output JHC files. | `-out adcp_section` |
| `-map <map.blank>` | **Required.** A blank JHC file that defines the geographic area and orientation (rotation) of the output map section. | `-map section_line.blank` |
| `-Xpixel <size>` | **Required.** The horizontal size (width) of each pixel in the output section, in the map's native units (e.g., meters). | `10.0` |
| `-Zpixel <size>` | **Required.** The vertical size (height) of each pixel in the output section, in meters. | `1.0` |
| `-mindepth <meters>` | The minimum depth to include in the output section. | `50.0` |
| `-maxdepth <meters>` | The maximum depth to include in the output section. | `150.0` |
| `-time_start <Y J H M S>`| Defines the start time for processing data (Year, Julian Day, Hour, Minute, Second). | `-time_start 2023 145 16 22 00` |
| `-time_end <Y J H M S>` | Defines the end time for processing data. | `-time_end 2023 145 18 30 00` |
| `-reducedY <top> <bottom>` | Restricts processing to a specific Y-coordinate range within the input map, useful for isolating a portion of a larger map. | `-reducedY 4000 4500` |
| `-orthomap` | Orients the output section orthogonal to the map's primary axis. The default is `-alongmap`. | |
| `-alongmap` | Orients the output section along the map's primary axis (default). | |
| `-lr_flip` | Flips the output section left-to-right. | |
| `-no_flip` | Disables left-to-right flipping (default). | |
| `-dump_NED_averages` | If specified, writes a text file (`<outfileprefix>.NED_av.txt`) containing the averaged NED profile across the entire section. | |
| `-v` | Enable verbose output. | |
| `-testrot` | Enters a diagnostic mode to test vector rotation calculations without processing files. | |

## How It Works

1.  **Setup Output Grid:** The tool first defines the output grid based on the `-map` file and the `-Xpixel` and `-Zpixel` arguments. This creates an empty 2D section (horizontal distance vs. depth).
2.  **Process Input Files:** It iterates through each specified input `.nav` file. For each navigation record (representing one ADCP ping/ensemble):
    *   It checks if the record is within the specified time bounds.
    *   It projects the ping's geographic coordinates (lat/lon) onto the input map to find its position.
    *   If the ping falls within the map's boundaries (and the optional `-reducedY` range), the tool reads the corresponding vertical profiles of North, East, and Downward velocities from the associated `.r4` files.
3.  **Binning and Stacking:** For each depth bin in the velocity profiles:
    *   It calculates the corresponding pixel location (horizontal and vertical) in the output section grid.
    *   The N, E, and D velocity values for that depth bin are added to the running sum for that output pixel. A counter for the number of contributions is also incremented.
4.  **Averaging and Calculation:** After processing all input files, the tool iterates through every pixel in the output grid. If a pixel has received contributions (i.e., its counter is greater than zero), it calculates the average N, E, and D velocities.
5.  **Component Calculation:** From the averaged NED velocities, it calculates additional components:
    *   **Magnitude:** `sqrt(N^2 + E^2)`
    *   **Azimuth:** `atan2(E, N)`
    *   **Radial (Along-track):** Velocity component parallel to the section's orientation.
    *   **Tangential (Across-track):** Velocity component perpendicular to the section's orientation.
6.  **Write Output Files:** The tool writes each calculated component into a separate JHC-formatted (`.r4`) file, using the specified output prefix.

## Input File Requirements

This tool requires a specific set of input files:
*   A JHC navigation file (e.g., `survey1.dec3.nav`).
*   Three corresponding JHC float-array files (`.r4`) with identical dimensions, containing the binned velocity data:
    *   `survey1.dec3.N.r4` (North velocity)
    *   `survey1.dec3.E.r4` (East velocity)
    *   `survey1.dec3.D.r4` (Downward velocity)

## Output Files

*   **`<outfileprefix>.N.r4`**: 2D map of the North velocity component.
*   **`<outfileprefix>.E.r4`**: 2D map of the East velocity component.
*   **`<outfileprefix>.D.r4`**: 2D map of the Downward velocity component.
*   **`<outfileprefix>.Mag.r4`**: 2D map of the total horizontal velocity magnitude.
*   **`<outfileprefix>.Azi.r4`**: 2D map of the velocity direction (azimuth).
*   **`<outfileprefix>.Rad.r4`**: 2D map of the along-track (radial) velocity component.
*   **`<outfileprefix>.Tan.r4`**: 2D map of the across-track (tangential) velocity component.
*   **`<outfileprefix>.history`**: A text file logging the input files processed.
*   **`<outfileprefix>.NED_av.txt`**: (Optional) An ASCII file with the average NED profile if `-dump_NED_averages` is used.