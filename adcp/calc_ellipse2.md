---
layout: default
title: calc_ellipse2
parent: ADCP Tools
nav_order: 3
---

# calc_ellipse2

## Description
`calc_ellipse2` is a command-line utility for calculating tidal ellipse parameters from ADCP (Acoustic Doppler Current Profiler) data. It processes depth-averaged velocity vectors from multiple tidal cycles, sorting them by tidal phase and spatial location into bins defined by a coarse DTM grid. The tool then computes tidal ellipse parameters (major axis, minor axis, orientation, and ellipticity) for each bin and outputs the results to nav-format files. It can also output residual currents.

This tool is a modification of `calc_ellipse1` with a focus on direct ellipse parameter calculation.

## Usage
```bash
calc_ellipse2 [OPTIONS] -grid <coarseDTM> -out <outfilenameprefix> -ellipse_file <ellipse_parameter_file> -in <infilename(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-ascii` | Output an additional ASCII file with ellipse parameters. | |
| `-grid <coarseDTM>` | **Required.** Specifies the coarse DTM grid file for binning the ADCP data. | `-grid my_grid.jhc` |
| `-phase_step <degrees>` | The phase step in degrees for processing the tidal cycle. | `5` |
| `-phase_window <degrees>` | The phase window in degrees for averaging data around each phase step. | `10` |
| `-min_vels_in_bin <number>` | Minimum number of valid velocity vectors required in a bin to perform calculations. | `50` |
| `-out <outfilenameprefix>` | **Required.** Specifies the prefix for the output filenames. This will be used to generate phase-specific files. | `-out phase_vectors` |
| `-ellipse_file <ellipse_parameter_file>`| **Required.** Specifies the prefix for the output ellipse and residual current `.nav` files. | `-ellipse_file ellipse_data` |
| `-in <infilename(s)>` | **Required.** One or more input OMG-HDCS `.nav` files containing depth-averaged ADCP data. | `-in adcp_run1.nav adcp_run2.nav` |

## How It Works

1.  **Grid Loading:** The tool loads a JHC format grid file specified by the `-grid` option to define the spatial bins.
2.  **Data Loading:** It reads one or more `.nav` files containing depth-averaged ADCP vector data. The phase of each vector is calculated relative to the start time of the first record.
3.  **Binning & Averaging:** For each phase step, the tool iterates through all the ADCP data. Vectors falling within the current phase window and within the spatial extent of the grid are binned. The north and east velocity components (and their products and squares) are summed for each bin.
4.  **Ellipse Calculation:** After binning, it calculates the average (residual) current and the tidal ellipse parameters (major/minor axes, orientation, ellipticity) for each bin that meets the `-min_vels_in_bin` threshold. The calculation is based on the method described in USGS OFR 02-217.
5.  **Output:** The results are written to two separate `.nav` files:
    *   `_ellipse.nav`: Contains the major axis, minor axis, and orientation of the tidal ellipse.
    *   `_residual.nav`: Contains the residual current magnitude and direction.
    An optional ASCII file can also be generated.

## Output Files

*   **`<outfilenameprefix>.phase###`**: A series of files (one for each phase step) containing the averaged velocity vectors. (Note: The code appears to open this file but may not write to it if ellipse calculation is the primary goal).
*   **`<ellipse_parameter_file>_ellipse.nav`**: A `.nav` file where `azi` is the major axis, `velocity` is the minor axis, and `depth` is the orientation (theta).
*   **`<ellipse_parameter_file>_residual.nav`**: A `.nav` file containing the magnitude and direction of the residual current.
*   **`asciifile`**: If `-ascii` is used, this file is created with comma-separated values for lat, lon, theta, ellipticity, major axis, minor axis, and residual north/east velocity components.