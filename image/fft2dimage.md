---
layout: default
title: fft2dimage
parent: Image Tools
nav_order: 22
tool_name: fft2dimage
source_path: code/image/fft2dimage.c
category: Spectral & Backscatter Analysis
input_formats: ["OMG1 32-bit float bathymetry DTM (.r4)"]
output_formats: ["2D FFT power spectrum (.fft)", "Dominant wavelength (.wav.r4), azimuth (.azi.r4), and amplitude (.mag.r4) grids", "Vector track (.nav) and ASCII summary (.txt)"]
related_tools: ["subimage", "pastemos", "r4to8bit", "jview"]
---

# fft2dimage

## Description
`fft2dimage` performs 2D Fast Fourier Transform (FFT) spectral analysis on a 32-bit floating-point (`.r4`) `OMG1` bathymetric DTM to quantify bedform/sandwave crest orientation, dominant wavelength, and wave height amplitude. It operates either on a single $2^n \times 2^n$ sub-window (`-xstart`, `-ystart`) or in a sliding-window loop (`-loopstep`) across the entire mapsheet to produce regional bedform maps (`.wav.r4`, `.azi.r4`, `.mag.r4`, and `.nav`).

## CLI Options & Usage
```bash
fft2dimage -in <bathy.r4> -out <prefix> -power <n> \
  [-xstart <col> -ystart <row> | -loopstep <step_pixels>] \
  [-remove_average] [-detrend] [-taper] [-wavelength]
```
* **`-in <bathy.r4>`**: Input 32-bit float `OMG1` bathymetric DTM.
* **`-out <prefix>`**: Output filename prefix.
* **`-power <n>`**: Base-2 exponent setting the FFT window dimension ($2^n \times 2^n$, where $n \le 10$, e.g., `-power 6` = $64 \times 64$ cells).
* **`-xstart <col> -ystart <row>`**: Upper-left pixel coordinates for a single-window 2D FFT (writes `<prefix>` and `<prefix>.fft`).
* **`-loopstep <step>`**: Steps the $2^n \times 2^n$ FFT window across the entire DTM every `<step>` pixels (accepting windows with $\ge 90\%$ valid soundings), outputting `<prefix>.wav.r4`, `<prefix>.azi.r4`, `<prefix>.mag.r4`, `<prefix>.nav`, and `<prefix>.txt`.
* **`-remove_average`**: Subtracts the mean depth of the window before the FFT.
* **`-detrend`**: Fits and subtracts a least-squares 3D plane ($z = ax + by + c$) to remove regional seabed slope.
* **`-taper`**: Applies a radial cosine edge taper across the outer 25% of the window to suppress spectral leakage.
* **`-wavelength`**: Outputs spatial wavelength in meters rather than spatial frequency ($1/\lambda$).

## Algorithm
For each valid $2^n \times 2^n$ sub-grid, `fft2dimage` removes the mean/planar trend, applies the radial cosine taper, executes a 2D complex-to-complex radix-2 FFT (`fft2d()`), locates the peak spectral power bin `(max_i, max_j)`, and converts the wavenumber vector `(kx, ky)` into dominant bedform wavelength $\lambda$, crest-normal azimuth (`0°–180°`), and RMS amplitude. The resulting `.mag.r4` and `.azi.r4` grids can be combined into a directional color-wheel map using [`pastemos`](pastemos.md).
