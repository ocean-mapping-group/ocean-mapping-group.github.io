---
layout: default
title: combineMultiADCP_garret
parent: ADCP Tools
nav_order: 5
---

# combineMultiADCP_garret

## Description
`combineMultiADCP_garret` is a command-line utility used to process and combine depth-averaged ADCP (Acoustic Doppler Current Profiler) data from multiple tidal cycles. The tool reads data in JCU navigation format, sorts the vectors by tidal phase and spatial location, and bins them using a provided grid. It then calculates a temporally averaged vector for each bin at discrete phase steps through the tidal cycle.

This version of the tool is identical in functionality to `combineMultiADCP`. The "_garret" suffix may denote a version developed or modified by a specific user.

## Usage
```bash
combineMultiADCP_garret [OPTIONS] -grid <coarseDTM> -out <outfilenameprefix> -in <infilename(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-grid <coarseDTM>` | **Required.** Specifies the coarse DTM grid file (in JHC format) used for spatial binning of the ADCP data. | `-grid my_grid.jhc` |
| `-phase_step <degrees>` | The phase step in degrees for processing the tidal cycle. The tool will generate an output file for each step. | `20` |
| `-phase_window <degrees>` | The width of the phase window in degrees for averaging data around each phase step. | `20` |
| `-min_vels_in_bin <number>` | The minimum number of velocity vectors required within a bin for it to be processed and included in the output. | `50` |
| `-out <outfilenameprefix>` | **Required.** Specifies the prefix for the output filenames. The output files will be named `<outfilenameprefix>.phase###`. | `-out phase_vectors` |
| `-in <infilename(s)>` | **Required.** One or more input OMG-HDCS `.nav` files containing depth-averaged ADCP data from different tidal cycles. | `-in adcp_run1.nav adcp_run2.nav` |

## How It Works

1.  **Grid and Data Loading:** The tool first loads a JHC-format grid to define the spatial bins. It then reads all specified input `.nav` files, which contain the depth-averaged ADCP current vectors. For each vector, it calculates the tidal phase (0-360 degrees) based on a 12.42-hour tidal cycle, relative to the timestamp of the very first data point.
2.  **Phase Stepping and Binning:** The tool iterates through the tidal cycle in steps defined by `-phase_step`. For each phase step:
    *   It initializes all grid cells (nodes) to zero.
    *   It goes through all the loaded ADCP data and identifies vectors that fall within the current phase window (`phase` to `phase + phase_window`).
    *   For these vectors, it determines the corresponding grid cell and adds their North and East velocity components to that cell's running sum.
3.  **Averaging and Output:** After processing all data for a given phase step, it iterates through the grid cells.
    *   If a cell's count of vectors is greater than `min_vels_in_bin`, it calculates the average North and East velocity components.
    *   It converts this average vector back to magnitude and azimuth.
    *   This final averaged vector is written as a record in a new `.nav` file named `<outfilenameprefix>.phase###`, where `###` is the phase angle.
4.  **Looping:** The process repeats for the next phase step until the entire 360-degree cycle is covered.

## Output Files

The tool generates a series of `.nav` files, one for each phase step. For example, with a `-phase_step` of 20, the output files would be:
*   `<outfilenameprefix>.phase000`
*   `<outfilenameprefix>.phase020`
*   `<outfilenameprefix>.phase040`
*   ...and so on, up to the final phase step before 360.

Each file contains a list of averaged current vectors, with one record for each grid cell that had sufficient data for that phase window.