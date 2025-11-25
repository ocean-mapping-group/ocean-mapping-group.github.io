---
layout: default
title: calc_ellipse
parent: ADCP Tools
nav_order: 2
---

# calc_ellipse

## Description
`calc_ellipse` is a command-line utility designed to analyze ADCP (Acoustic Doppler Current Profiler) data to determine tidal ellipse parameters. It processes depth-averaged current vectors from one or more tidal cycles, sorts them by tidal phase and spatial location using a grid, and then calculates the properties of the tidal ellipse (major/minor axes, orientation, etc.) for each grid cell.

This tool is an earlier version or variant of `calc_ellipse1` and `calc_ellipse2`.

## Usage
```bash
calc_ellipse [OPTIONS] -grid <coarseDTM> -out <outfilenameprefix> -ellipse_file <ellipse_parameter_file> -in <infilename(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-grid <coarseDTM>` | **Required.** Specifies the coarse DTM grid file (in JHC format) for binning the ADCP data. | `-grid my_grid.jhc` |
| `-phase_step <degrees>` | The phase step in degrees for processing the tidal cycle (default is 360, which processes the whole cycle at once). | `5` |
| `-phase_window <degrees>` | The phase window in degrees for averaging data around each phase step (default is 360). | `10` |
| `-min_vels_in_bin <number>` | Minimum number of valid velocity vectors required in a bin to perform calculations. | `50` |
| `-out <outfilenameprefix>` | **Required.** Specifies the prefix for the output phase-specific `.nav` files. | `-out phase_vectors` |
| `-ellipse_file <ellipse_parameter_file>`| **Required.** Specifies the name of the output file for the calculated ellipse parameters (in CSV format). | `-ellipse_file ellipse_data.csv` |
| `-in <infilename(s)>` | **Required.** One or more input OMG-HDCS `.nav` files containing depth-averaged ADCP data. | `-in adcp_run1.nav adcp_run2.nav` |

## How It Works

1.  **Grid and Data Loading:** The tool loads a JHC grid file to define spatial bins and reads one or more `.nav` files containing the ADCP current data. It calculates the tidal phase for each data point relative to the time of the first measurement.
2.  **Binning and Stacking:** For each phase step defined by `-phase_step`, the tool processes all input data points. If a data point falls within the current phase window and is located within a grid cell, its velocity components (and their products and squares) are added to the running sums for that cell.
3.  **Ellipse Calculation:** For each grid cell that accumulates more than `min_vels_in_bin` data points, the tool calculates the residual current (time-averaged flow) and the tidal ellipse parameters. The ellipse calculation uses the variance of the north and east velocity components to determine the major and minor axes (`a` and `b`), orientation (`theta`), and ellipticity (`e`).
4.  **Output:**
    *   It writes the averaged velocity vector for each phase step to a corresponding file named `<outfilenameprefix>.phase###`.
    *   The primary output is the CSV file specified by `-ellipse_file`, which contains the columns: `lat,lon,theta,e,a,b,N_av,E_av` for each grid cell that met the minimum data threshold.

## Output File

*   **`<ellipse_parameter_file>`**: A CSV file containing the calculated tidal ellipse parameters for each valid grid cell. The columns are:
    *   `lat`: Latitude of the cell center.
    *   `lon`: Longitude of the cell center.
    *   `theta`: Orientation of the major axis in degrees clockwise from North.
    *   `e`: Ellipticity.
    *   `a`: Magnitude of the semi-major axis.
    *   `b`: Magnitude of the semi-minor axis.
    *   `N_av`: North component of the residual (mean) current.
    *   `E_av`: East component of the residual (mean) current.
*   **`<outfilenameprefix>.phase###`**: A set of `.nav` files, one for each phase step, containing the averaged current vectors for that phase.