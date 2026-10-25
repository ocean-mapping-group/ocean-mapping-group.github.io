---
layout: default
title: combineMultiADCP_wshiftoption
parent: Teledyne RDI ADCP Processing (adcp)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 6
tool_name: combineMultiADCP_wshiftoption
source_path: code/adcp/combineMultiADCP_wshiftoption.c
category: adcp
input_formats:
- jcu_nav Depth-Averaged ADCP Vectors (.nav)
- JHC Grid (.r4 / .8bit)
output_formats:
- jcu_nav Phase-Averaged Vectors (.phase###)
related_tools:
- combineMultiADCP
- combineMultiADCP_garret
- calc_ellipse2
---

# combineMultiADCP_wshiftoption

## Description
`combineMultiADCP_wshiftoption` is a specialized version of [`combineMultiADCP`](combineMultiADCP.html). It processes and combines depth-averaged ADCP (Acoustic Doppler Current Profiler) data from multiple tidal cycles, with additional options to apply a time shift (`-tshift`) and set a manual reference epoch (`-reftime`) for precise M2 tidal phase alignment across multi-day or multi-vessel surveys.

## Usage

```bash
combineMultiADCP_wshiftoption [OPTIONS] -grid <coarseDTM> -out <outfilenameprefix> -in <infilename(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-grid <coarseDTM>` | **Required.** Specifies the coarse DTM grid file (in JHC format) for spatial binning. | `-grid my_grid.r4` |
| `-phase_step <degrees>` | The phase step in degrees for processing the tidal cycle. An output file is generated for each step. | `20` |
| `-phase_window <degrees>` | The width of the phase window in degrees for averaging data around each phase step. | `20` |
| `-min_vels_in_bin <number>` | The minimum number of velocity vectors required within a bin to be included in the output. | `50` |
| `-tshift <seconds>` | Applies a time shift (in seconds) to the input data for phase alignment. | `-tshift 3600` |
| `-reftime <timestamp>` | Manually specifies the reference time (as a Unix timestamp in seconds since 1970) for $0^\circ$ tidal phase. | `-reftime 1000000000`|
| `-out <outfilenameprefix>` | **Required.** Specifies the prefix for the output filenames (`<outfilenameprefix>.phase###`). | `-out phase_vectors` |
| `-in <infilename(s)>` | **Required.** One or more input `jcu_nav` `.nav` files containing depth-averaged ADCP data. | `-in adcp_run1.nav adcp_run2.nav` |

## How It Works

The functionality is identical to `combineMultiADCP`, with two enhancements to the tidal phase calculation:

1.  **Grid and Data Loading:** Loads a JHC grid and reads the input `.nav` files.
2.  **Phase Calculation with Time Shift & Reference Epoch:** When calculating the M2 tidal phase ($T_{\text{M2}} = 44{,}712\text{ s}$) for each ADCP vector, it incorporates the user-defined `-tshift` and `-reftime` values rather than defaulting solely to the first record's timestamp.
3.  **Binning and Averaging:** Steps through the tidal cycle, identifies all data points within each phase window, bins them into the appropriate grid cells, and averages the North and East velocity components.
4.  **Output:** Writes the averaged vectors for each phase step to `<outfilenameprefix>.phase###`.
