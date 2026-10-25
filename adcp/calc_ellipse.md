---
layout: default
title: calc_ellipse
parent: ADCP Tools
nav_order: 2
tool_name: calc_ellipse
source_path: code/adcp/calc_ellipse.c
category: adcp
input_formats:
  - jcu_nav Depth-Averaged ADCP Vectors (.nav)
  - JHC Grid (.r4 / .8bit)
output_formats:
  - CSV Tidal Ellipse Table
  - jcu_nav Phase-Averaged Vectors (.phase###)
related_tools:
  - calc_ellipse1
  - calc_ellipse2
  - combineMultiADCP
  - readADCP
---

# calc_ellipse

## Description
`calc_ellipse` is a command-line utility designed to analyze ADCP (Acoustic Doppler Current Profiler) data to determine M2 tidal ellipse parameters ($12.42\text{ hours} = 360^\circ$). It processes depth-averaged current vectors from one or more tidal cycles, sorts them by tidal phase and spatial location using a coarse DTM grid, and calculates the properties of the tidal ellipse (semi-major/minor axes, orientation, ellipticity, and residual current) for each grid cell.

This tool is the foundational version of [`calc_ellipse1`](calc_ellipse1.md) and [`calc_ellipse2`](calc_ellipse2.md), writing its ellipse parameters directly to a CSV table.

## Usage
```bash
calc_ellipse [OPTIONS] -grid <coarseDTM> -out <outfilenameprefix> -ellipse_file <ellipse_parameter_file> -in <infilename(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-grid <coarseDTM>` | **Required.** Specifies the coarse DTM grid file (in JHC format) for spatially binning the ADCP data. | `-grid my_grid.r4` |
| `-phase_step <degrees>` | The phase step in degrees for processing the tidal cycle (default is `360`, which processes the whole cycle at once). | `20` |
| `-phase_window <degrees>` | The phase window in degrees for averaging data around each phase step (default is `360`). | `30` |
| `-min_vels_in_bin <number>` | Minimum number of valid velocity vectors required in a grid cell to perform calculations. | `50` |
| `-out <outfilenameprefix>` | **Required.** Specifies the prefix for the output phase-specific `.nav` files (`<prefix>.phase###`). | `-out phase_vectors` |
| `-ellipse_file <ellipse_parameter_file>`| **Required.** Specifies the name of the output CSV file for the calculated ellipse parameters. | `-ellipse_file ellipse_data.csv` |
| `-in <infilename(s)>` | **Required.** One or more input `jcu_nav` `.nav` files containing depth-averaged ADCP velocity vectors. | `-in adcp_run1.nav adcp_run2.nav` |

## How It Works

1.  **Grid and Data Loading:** The tool loads a JHC grid file to define spatial bins and reads one or more `.nav` files containing the ADCP current data. It calculates the M2 tidal phase for each data point relative to the time of the first measurement ($T_{\text{M2}} = 44{,}712\text{ s}$).
2.  **Binning and Stacking:** For each phase step defined by `-phase_step`, the tool processes all input data points. If a data point falls within the current phase window and is located within a grid cell, its North and East velocity components (and their products and squares) are added to the running sums for that cell.
3.  **Ellipse Calculation:** For each grid cell that accumulates more than `min_vels_in_bin` data points, the tool calculates the residual current (time-averaged flow) and the tidal ellipse parameters using the variance/covariance of the North and East velocity components to determine the semi-major and semi-minor axes (`a` and `b`), orientation (`theta`), and ellipticity (`e = 1 - b/a`).
4.  **Output:**
    *   Writes the averaged velocity vector for each phase step to `<outfilenameprefix>.phase###`.
    *   Writes the CSV file specified by `-ellipse_file`, containing `lat,lon,theta,e,a,b,N_av,E_av` for each valid grid cell.

## Output Files

*   **`<ellipse_parameter_file>`**: A CSV file containing the calculated tidal ellipse parameters for each valid grid cell:
    *   `lat`, `lon`: Geographic coordinates of the grid cell center.
    *   `theta`: Orientation of the major axis in degrees clockwise from North.
    *   `e`: Ellipticity ($1 - b/a$).
    *   `a`, `b`: Magnitude of the semi-major and semi-minor axes (m/s).
    *   `N_av`, `E_av`: North and East components of the residual (mean) current (m/s).
*   **`<outfilenameprefix>.phase###`**: A set of `jcu_nav` files, one for each phase step, containing the averaged current vectors for that phase.
