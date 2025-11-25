---
layout: default
title: calc_ellipse1
parent: adcp
---

# calc_ellipse1

## Description
`calc_ellipse1` is a tool for calculating tidal ellipses from ADCP (Acoustic Doppler Current Profiler) data. It reads depth-averaged velocity vectors from multiple tidal cycles, sorts them by tidal phase and spatial location in area bins, and outputs temporally interpolated velocity vectors at the center of each bin. This is useful for analyzing tidal current patterns and creating tidal ellipse parameters.

## Usage
```bash
calc_ellipse1 (-v) -grid coarseDTM -phase_step 5 -phase_window 10 (-min_vels_in_bin 50) -out outfilenameprefix -ellipse_file ellipse_parameter_file -in infilename(s)
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output |
| `-grid coarseDTM` | Specify the coarse DTM grid file for binning |
| `-phase_step 5` | Phase step in degrees (360 deg = one tidal cycle) |
| `-phase_window 10` | Phase window for averaging |
| `-min_vels_in_bin 50` | Minimum number of velocities required in a bin (optional) |
| `-out outfilenameprefix` | Output filename prefix |
| `-ellipse_file` | Ellipse parameter file |
| `-in infilename(s)` | Input filename(s) |

## How It Works
1. **Data Reading:** Reads jcu_nav format depth-averaged vectors from multiple ADCP tidal cycles
2. **Sorting:** Sorts data by tidal phase and location in spatial bins
3. **Interpolation:** Outputs temporally interpolated velocity vectors at bin centers
4. **Ellipse Calculation:** Computes tidal ellipse parameters for current analysis
