---
layout: default
title: stripSS
parent: XTF Tools
nav_order: 6
tool_name: stripSS
source_path: code/xtf/stripSS.c
category: Backscatter & Image Processing
input_formats: [".xtf"]
output_formats: [".8bit", ".pgm", ".ascii"]
related_tools: ["extractRI", "extractSnippet", "getTVG", "xtfTool"]
---

# stripSS

## Overview
`stripSS` extracts sidescan trace packets (`XTF_HEADER_SONAR`, packet ID 0) from an XTF file and generates an 8-bit waterfall raster image in OMG/JHC (`.8bit`) or Portable Graymap (`.pgm`) format, plus an optional `.ascii` dump. For Reson XTF files that also contain bathymetry packets (`XTF_HEADER_BATHY`, ID 2), `stripSS` can automatically clip water-column noise, overlay bottom-track sounding picks, remove empirical TVG spreading loss, and plot 50-pixel-wide strips of transmit power, receiver gain, and pulse width along the left edge of the image.

## Usage
```bash
stripSS [OPTIONS] -in <inputfile.xtf>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<inputfile.xtf>` | **Required** | Path to the input `.xtf` file. Output files use the stripped basename (`<basename>.8bit`, `<basename>.pgm`, `<basename>.ascii`). |
| `-pgm` | None | Off (`.8bit`) | Write a Portable Graymap (`<basename>.pgm`) instead of an OMG/JHC (`<basename>.8bit`) image. |
| `-slin` | None | Off | Apply a linear min/max contrast stretch from 16-bit input dynamic range to 8-bit (`0..255`). Mutually exclusive with `-slog` and `-clog`. |
| `-slog` | None | Off | Apply a logarithmic (`10 * log10`) min/max contrast stretch to 8-bit (`0..255`). |
| `-clog` | None | Off | Apply logarithmic compression (`20 * log10(value)`) without min/max stretching. |
| `-no_TVG` | None | Off | Remove spherical/cylindrical TVG spreading (`spreading * log10(range)`) using Reson bathymetry header TVG parameters and compress logarithmically (`20 * log10`). |
| `-db_shift` | `<dB>` | `0.0` | Additive decibel shift applied after `-no_TVG` correction. |
| `-wc` | None | Water column suppressed | Do **not** suppress the water column. By default (`waterColumn = 1`), `stripSS` computes the mean digital number inside the water column (using `ping.SensorAuxAltitude`) and clips values below `maxWCMean` to zero during stretching. |
| `-plot` | None | Off | Prepend three 50-pixel-wide grayscale indicator columns on the left side of the image showing scaled Reson Power, Gain, and Pulse Width for each ping. |
| `-bt` | None | Off | Overlay Reson multibeam sounding slant-range picks onto the sidescan waterfall image (plotted with pixel value `14`). |
| `-ascii` | None | Off | Dump raw ping amplitudes (and power/gain/pulseWidth if `-plot` is active) to `<basename>.ascii`. |
| `-v` | None | Off | Print file header, dynamic range statistics, and a 5-bin ASCII histogram of the output 8-bit image. |

## How It Works
1. **Two-Pass Scanning:**
   * **Pass 1:** Scans all `XTF_HEADER_SONAR` packets to verify sample counts (`maxNumSamples`), determine global 16-bit/8-bit `minIn` and `maxIn` values, and (unless `-wc` is specified) estimate the mean water-column noise floor (`maxWCMean`) above the nadir altitude (`SensorAuxAltitude`). If `-plot` is enabled on Reson data, calls `getResonDynamicRanges()` to find the min/max range of power, gain, and pulse width.
   * **Pass 2:** Converts each scanline to 8-bit according to the chosen scaling mode (raw division by 65535, `-slin`, `-slog`, `-clog`, or `-no_TVG`), optionally prepends the 150-pixel parameter strip (`-plot`), overlays sounding ranges (`-bt`), and writes the scanline to `<basename>.8bit` or `<basename>.pgm`.

## Practical Examples

**1. Generate a logarithmically stretched PGM sidescan waterfall with Reson gain/power/pulse strips:**
```bash
stripSS -v -pgm -slog -plot -in reson_line01.xtf
```

**2. Remove TVG spreading and overlay multibeam bottom detections:**
```bash
stripSS -pgm -no_TVG -db_shift 15.0 -bt -in reson_line01.xtf
```
