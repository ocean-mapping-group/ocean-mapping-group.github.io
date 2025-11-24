---
layout: default
title: plotFFT_BF
parent: Plot Tools
nav_order: 139
---
# plotFFT_BF

## Description
`plotFFT_BF` is a specialized plotting utility designed to visualize the concepts of FFT (Fast Fourier Transform) beamforming. It simulates a linear array of hydrophones, calculates the amplitude time series for each element based on an incoming plane wave at a specified angle, and then performs an FFT to show the resulting beam pattern (power).

The tool allows for interactive visualization of how the phase differences across the array create a focused beam in a particular direction. It can plot the array configuration, incoming wavelets, amplitude time series, and the final power distribution.

## Usage
```bash
plotFFT_BF [-fft_only] [-size <dx> <dy>] [-sigrange <min> <max>] [-angle <val>] [-v] [-outfile <filenm>]
```

## Arguments

| Option | Description |
|---|---|
| `-fft_only` | Only plots the FFT results (power distribution) and not the incoming wavelets. |
| `-size <dx> <dy>` | Specifies the plot size in centimeters. | `16.0 20.0` |
| `-sigrange <min> <max>` | Sets the signal range for plotting (likely intensity in dB, but context implies power). | |
| `-angle <val>` | Specifies the angle of the incoming plane wave (in degrees). Can be used multiple times for multiple angles. | |
| `-v` | Enable verbose output. | |
| `-outfile <filenm>` | Specifies the output PostScript metafile name. | `plot.meta` |

## How It Works
1.  **Initialization:** Parses command-line arguments to set plotting options, plot size, signal range, and the incoming wave `angle`.
2.  **Plot Setup:** Initializes the `plotlib` PostScript output (`plot.meta`). Sets up the overall plot dimensions (`xlength`, `ylength`, `xoff`, `yoff`). Draws the main plot border.
3.  **Array Visualization:**
    *   Calculates the `locx`, `locy` (screen coordinates) for each of the `NO_ELEMENTS` (128) hydrophone elements in a linear array.
    *   Draws the outline of the hydrophone array.
    *   Draws individual hydrophone elements (boxes).
4.  **Incoming Wavelet Simulation:**
    *   If `fft_only_flag` is *not* set:
        *   For each incoming wave `angle` (specified by `-angle`):
            *   Calculates the phase shift across the array for the incoming wave.
            *   Plots incoming wavelets (cosinusoidal waves) across the array, illustrating the phase differences.
5.  **Amplitude Time Series Calculation:**
    *   Calculates the amplitude time series for each element by summing the contributions of all incoming waves at different time fractions of a wavelength.
6.  **FFT Processing:**
    *   Performs an FFT (using `four1` function) on the calculated amplitude time series for each element.
    *   Calculates the `Power` (magnitude squared) for each element from the FFT results.
7.  **Beam Pattern Plotting:**
    *   Plots the amplitude time series for each element.
    *   Plots the `Power` distribution (beam pattern) in a separate subplot, showing the combined response of the array. This effectively visualizes the spatial filtering characteristic of the array.
8.  **Cleanup:** Calls `plot_close` to finalize the PostScript output.

## Output Files
*   `<outfile_name>`: A PostScript metafile (`.meta`) visualizing the linear array, incoming wavelets (optional), amplitude time series, and the FFT-derived beam pattern.

## Dependencies
*   `plotlib.h`: For `plotlib` functions.
*   `support.h`: For general utility functions.
*   `math.h`: For mathematical functions.
*   `nr.h`: For Numerical Recipes functions (e.g., `four1`).

## Notes
`plotFFT_BF` is a valuable educational and analytical tool for understanding the fundamental principles of array signal processing and beamforming. It clearly demonstrates how phase coherence across an array leads to directional sensitivity. The interactive options for simulating multiple incoming angles allow users to explore the spatial filtering capabilities of a linear array.