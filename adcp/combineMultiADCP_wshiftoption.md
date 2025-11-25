---
layout: default
title: combineMultiADCP_wshiftoption
parent: ADCP Tools
nav_order: 6
---

# combineMultiADCP_wshiftoption

## Description
`combineMultiADCP_wshiftoption` is a specialized version of `combineMultiADCP`. It processes and combines depth-averaged ADCP (Acoustic Doppler Current Profiler) data from multiple tidal cycles, but with additional options to apply a time shift and set a manual reference time for more precise tidal phase alignment.

The tool reads JCU navigation format data, sorts the vectors by tidal phase and location, bins them using a grid, and calculates a temporally averaged vector for each bin at discrete phase steps. The time-shifting capabilities make it particularly useful for aligning datasets from different surveys or instruments that may have timing discrepancies.

## Usage
```bash
combineMultiADCP_wshiftoption [OPTIONS] -grid <coarseDTM> -out <outfilenameprefix> -in <infilename(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-grid <coarseDTM>` | **Required.** Specifies the coarse DTM grid file (in JHC format) for spatial binning. | `-grid my_grid.jhc` |
| `-phase_step <degrees>` | The phase step in degrees for processing the tidal cycle. An output file is generated for each step. | `20` |
| `-phase_window <degrees>` | The width of the phase window in degrees for averaging data around each phase step. | `20` |
| `-min_vels_in_bin <number>` | The minimum number of velocity vectors required within a bin to be included in the output. | `50` |
| `-tshift <seconds>` | Applies a time shift (in seconds) to the input data for more accurate phase calculation. This is useful for synchronizing datasets. | `-tshift 3600` |
| `-reftime <timestamp>` | Manually specifies the reference time (as a Unix timestamp) for the start of the tidal cycle, allowing for consistent phasing across different runs. | `-reftime 1000000000`|
| `-out <outfilenameprefix>` | **Required.** Specifies the prefix for the output filenames. The files will be named `<outfilenameprefix>.phase###`. | `-out phase_vectors` |
| `-in <infilename(s)>` | **Required.** One or more input OMG-HDCS `.nav` files containing depth-averaged ADCP data. | `-in adcp_run1.nav adcp_run2.nav` |

## How It Works

The functionality is nearly identical to `combineMultiADCP`, with key differences in the phase calculation:

1.  **Grid and Data Loading:** It loads a JHC grid and reads the input `.nav` files.
2.  **Phase Calculation with Time Shift:** When calculating the tidal phase for each ADCP vector, it incorporates the user-defined `-tshift` and `-reftime` values. This allows for precise alignment of the tidal cycle across multiple input files that might not be perfectly synchronized.
3.  **Binning and Averaging:** It steps through the tidal cycle, and for each phase step, it identifies all data points within the phase window, bins them into the appropriate grid cells, and sums the velocity components.
4.  **Output:** For each phase step, it calculates the average vector for each bin that meets the `min_vels_in_bin` threshold and writes the results to a corresponding `.nav` file named `<outfilenameprefix>.phase###`.

## Output Files

The tool generates a series of `.nav` files, one for each phase step. For example, with a `-phase_step` of 20, the output files would be:
*   `<outfilenameprefix>.phase000`
*   `<outfilenameprefix>.phase020`
*   `<outfilenameprefix>.phase040`
*   ...and so on, up to the final phase step before 360.

Each file contains a list of averaged current vectors, with one record for each grid cell that had sufficient data for that phase window.