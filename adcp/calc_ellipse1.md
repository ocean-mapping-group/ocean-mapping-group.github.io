---
layout: default
title: calc_ellipse1
parent: Teledyne RDI ADCP Processing (adcp)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 2
tool_name: calc_ellipse1
source_path: code/adcp/calc_ellipse1.c
category: adcp
input_formats:
- jcu_nav Depth-Averaged ADCP Vectors (.nav)
- JHC Grid (.r4 / .8bit)
output_formats:
- jcu_nav Tidal Ellipse Vectors (_ellipse.nav)
- jcu_nav Residual Current Vectors (_residual.nav)
- jcu_nav Phase-Averaged Vectors (.phase###)
related_tools:
- calc_ellipse
- calc_ellipse2
- combineMultiADCP
- readADCP
---

# calc_ellipse1

## Description
`calc_ellipse1` is a command-line utility for calculating M2 tidal current ellipses and mean residual circulation from depth-averaged ADCP (Acoustic Doppler Current Profiler) `.nav` files. Like [`calc_ellipse`](calc_ellipse.html) and [`calc_ellipse2`](calc_ellipse2.html), it reads depth-averaged velocity vectors from multiple tidal cycles, bins them spatially using a coarse JHC grid (`-grid`) and temporally by M2 tidal phase ($12.42\text{ hours} = 360^\circ$), and computes the principal-axis tidal ellipse parameters for each grid cell.

Unlike `calc_ellipse` (which writes only a CSV file), `calc_ellipse1` outputs two binary `jcu_nav` files—`<ellipse_file>_ellipse.nav` and `<ellipse_file>_residual.nav`—so that tidal ellipses and mean residual vectors can be plotted directly on mapsheets in `jview` and `plot_nav`.

## Usage

```bash
calc_ellipse1 [OPTIONS] -grid <coarseDTM> -out <outfilenameprefix> -ellipse_file <ellipse_prefix> -in <infilename(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-grid <coarseDTM>` | **Required.** Coarse DTM grid file (in JHC `.r4` or `.8bit` format) defining the spatial bins. | `-grid bay_200m.r4` |
| `-phase_step <degrees>` | Phase step in degrees for stepping through the $360^\circ$ M2 tidal cycle. | `5` (default `360`) |
| `-phase_window <degrees>` | Phase window width in degrees for averaging observations around each step. | `10` (default `360`) |
| `-min_vels_in_bin <number>` | Minimum number of velocity vectors required in a spatial bin to compute an ellipse. | `50` |
| `-out <outfilenameprefix>` | **Required.** Output filename prefix for phase-stepped vector files (`<prefix>.phase###`). | `-out bay_phase` |
| `-ellipse_file <prefix>` | **Required.** Output prefix for the `<prefix>_ellipse.nav` and `<prefix>_residual.nav` files. | `-ellipse_file bay_m2` |
| `-in <infilename(s)>` | **Required.** One or more input `jcu_nav` `.nav` files containing depth-averaged ADCP velocity vectors. | `-in pass1.nav pass2.nav` |

## How It Works
1. **Grid & Vector Loading:** Reads the JHC header of `-grid` to establish spatial cells and loads all depth-averaged current vectors (`velocity` and `azi`) from the input `.nav` files, computing each observation's M2 tidal phase relative to the initial timestamp.
2. **Spatial & Phase Binning:** Accumulates $\sum N$, $\sum E$, $\sum N^2$, $\sum E^2$, and $\sum (N \cdot E)$ within each grid cell across the tidal cycle.
3. **Harmonic / Variance Ellipse Solution:** For every grid node with at least `-min_vels_in_bin` observations, computes the mean residual current $(\bar{N}, \bar{E})$ and solves the velocity covariance eigenvalue problem to obtain the semi-major axis ($a$), semi-minor axis ($b$), orientation angle ($\theta$ clockwise from North), and ellipticity ($e = 1 - b/a$).
4. **Binary `jcu_nav` Output:** Writes `<ellipse_file>_ellipse.nav` (encoding major axis, minor axis, and orientation in the `jcu_nav_rec` fields) and `<ellipse_file>_residual.nav` (encoding residual speed and direction).

## Output Files
* **`<ellipse_file>_ellipse.nav`**: Binary `jcu_nav` file containing the tidal ellipse parameters at each valid grid node (`azi` = semi-major axis $a$, `velocity` = semi-minor axis $b$, `depth` = orientation $\theta$).
* **`<ellipse_file>_residual.nav`**: Binary `jcu_nav` file containing the tidal-mean residual current magnitude (`velocity`) and azimuth (`azi`) at each grid node.
* **`<outfilenameprefix>.phase###`**: Phase-binned `jcu_nav` vector files for each tidal phase step.
