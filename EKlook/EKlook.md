---
layout: default
title: EKlook
parent: EKlook Tools
nav_order: 9
tool_name: EKlook
source_path: code/EKlook/EKlook.c
category: EKlook
input_formats:
  - JHC Float Trace Arrays (.MF_dB, .Raw_dB, .PS_phase, .FA_phase, .MF_IQ)
  - OMG_HDCS (.merged)
  - OMG Attitude (.orientation)
  - Pulse Replica (.pulse)
  - JHC 8-bit Backdrop (.mos)
  - JHC Float Area Maps (.r4)
  - Sphere TS Reference (.dat)
output_formats:
  - Bottom Track Guide (.BottomTrackGuide)
  - Ping Parameters (.ping_Params)
  - Angular Response Curves (.ARC_fullBW, .ARC_3D, .ARC_FFTbins, .ARC_FFT3D)
related_tools:
  - BatchProcEK
  - comboCalibEK_ARCs
  - EK_ZoomImage
  - EK_BottomBS
  - EK_Polar
  - EK_FFT
  - EK_PosMotion
---

# EKlook

## Description
`EKlook` is an interactive 6-window X11/Motif application designed for visualizing, calibrating, and analyzing Kongsberg Simrad EK60 and broadband EK80 split-beam echosounder data unpacked by `readEA600`. It allows users to examine uncompressed and matched-filtered trace power (`.Raw_dB`, `.MF_dB`), complex IQ waveforms (`.MF_IQ`), Fore–Aft and Port–Starboard split-beam phase angles (`.FA_phase`, `.PS_phase`), bottom detections, windowed FFT spectra, and broadband Angular Response Curves (ARCs).

## Usage
```bash
EKlook [OPTIONS] -prefix <EK_file_prefix>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-mountangle <degrees>` | Forces a specific transducer mount roll angle (in degrees) for beam-pointing and grazing angle calculations. | `45.0` |
| `-guidedepth <meters>` | Forces a specific nadir water depth (in meters) as an initial bottom-detection guide. | `400.0` |
| `-sensitivity <value>` | Sets the split-beam electrical-to-mechanical Angle Sensitivity for along and across angles. | `10.0` |
| `-twowaybeamwidth <degrees>` | Sets the two-way $-3\text{ dB}$ beam width in degrees. | `12.0` |
| `-backdrop <orthomap.mos>` | Specifies an 8-bit JHC image file to use as a geographic backdrop in the Position-Motion view. | `orthomap.mos` |
| `-areas <AreaMapFileName(s)>` | Specifies one or more JHC `.r4` area map files for spatial filtering and slope-corrected grazing angles. | `custom_rot_mapsheet.r4` |
| `-sphereTS <sphereTS_filename>` | Specifies an ASCII reference file containing theoretical tungsten-carbide sphere Target Strength (TS) vs. frequency. | `TSvFreq.dat` |
| `-prefix <EK_file_prefix>` | **Required.** File prefix for the EK companion files produced by `readEA600` (e.g., `<prefix>.MF_dB`, `<prefix>.PS_phase`, `<prefix>.merged`). | `matchedfilted` |
| `-forgot` | Adjusts `mindB`, `maxdB`, and `trimdB` by subtracting 120.0 dB and disables `BulkCalibration`. | |

## Interactive Widgets / Views

`EKlook` orchestrates six interactive windows:
*   **Main Thumbnail & Power Histogram Window:** Overview of the entire file's trace power and dB distribution.
*   **[ZOOM EK-Trace Window](EK_ZoomImage.md):** Zoomed-in viewing of trace segments and single-ping power, I/Q, and split-beam phase profiles (`EK_ZoomImage.c`).
*   **[FFT EK-Trace Window](EK_FFT.md):** Windowed Fast Fourier Transform spectral analysis of complex `.MF_IQ` trace segments (`EK_FFT.c`).
*   **[POLAR EK-Trace Window](EK_Polar.md):** Polar bullseye plots of target strength and split-beam mechanical angles (`EK_Polar.c`).
*   **[BOTTOM Detect / ARC Window](EK_BottomBS.md):** Interactive bottom detection (`dBdrop`, `phaseOffZero`) and Angular Response Curve (ARC) generation (`EK_BottomBS.c`).
*   **[Position-Motion EK-Trace Window](EK_PosMotion.md):** 2D geographic map backdrop, 3D OpenGL beam footprint cone, and attitude time-series view (`EK_PosMotion.c`).

## See Also
* [Simrad EA600 / EK60 / EK80 Broadband Echosounder Workflow](../workflows/ek60-ek80-echosounder-workflow.md)
* [`BatchProcEK`](BatchProcEK.md), [`comboCalibEK_ARCs`](comboCalibEK_ARCs.md)
