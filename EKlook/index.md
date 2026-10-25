---
layout: default
title: Simrad EK60/EK80 Echosounder Suite (EKlook)
parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 2
has_children: true
---

# EKlook Broadband Echosounder Suite (`code/EKlook/`)

The `EKlook/` suite provides an interactive X11/Motif multi-window workbench ([`EKlook`](EKlook.html)) and automated batch processing utilities ([`BatchProcEK`](BatchProcEK.html), [`comboCalibEK_ARCs`](comboCalibEK_ARCs.html)) for analyzing **Kongsberg Simrad EK60 and broadband EK80** split-beam echosounder data unpacked and matched-filtered by `readEA600` (`code/knudsen/readEA600.c`).

For an end-to-end guide covering raw `.raw` unpacking, broadband FM pulse compression, interactive inspection, and spectral Angular Response Curve (ARC) calibration, see the **[Simrad EA600 / EK60 / EK80 Broadband Echosounder Workflow](../workflows/ek60-ek80-echosounder-workflow.html)**.

---

## Executables & Interactive Workbench

* **[`EKlook`](EKlook.html)** (`code/EKlook/EKlook.c`): Main 6-window interactive X11/Motif application for inspecting matched-filtered power (`.MF_dB`), raw power (`.Raw_dB`), Fore–Aft / Port–Starboard split-beam phase angles (`.FA_phase`, `.PS_phase`), complex IQ traces (`.MF_IQ`), target strength polar plots, windowed FFT spectra, and seabed Angular Response Curves (ARCs).
* **[`BatchProcEK`](BatchProcEK.html)** (`code/EKlook/BatchProcEK.c`): Command-line batch processor that iterates over multiple `.merged` and matched-filtered trace files using `.BottomTrackGuide` parameters to extract full-bandwidth (`.ARC_fullBW`, `.ARC_3D`) and FFT sub-banded (`.ARC_FFTbins`, `.ARC_FFT3D`) Angular Response Curves.
* **[`comboCalibEK_ARCs`](comboCalibEK_ARCs.html)** (`code/EKlook/comboCalibEK_ARCs.c`): Post-processing utility that merges multiple `.ARC_FFTbins` or `.ARC_3D` files, applies frequency-dependent sphere calibration curves (`-calib`), and extracts 2D frequency or grazing-angle slices (`-Freq2Dslice`, `-Graz2Dslice`).

---

## Interactive GUI Modules & Internal Libraries (within `EKlook`)

* **[`EK_ZoomImage`](EK_ZoomImage.html)** (`code/EKlook/EK_ZoomImage.c`): Manages the **ZOOM EK-Trace Window** for single-ping envelope, complex I/Q, and split-beam phase inspection, plus bottom-track guide editing.
* **[`EK_BottomBS`](EK_BottomBS.html)** (`code/EKlook/EK_BottomBS.c`): Manages the **BOTTOM Detect / ARC Window** for interactive bottom picking (`dBdrop`, `phaseOffZero`), ensonified area modeling, and live ARC stacking.
* **[`EK_Polar`](EK_Polar.html)** (`code/EKlook/EK_Polar.c`): Manages the **POLAR EK-Trace Window** for bullseye target-strength plots, split-beam radial angle roll-off modeling, and calibration sphere verification.
* **[`EK_FFT`](EK_FFT.html)** (`code/EKlook/EK_FFT.c`): Manages the **FFT EK-Trace Window** for windowed complex FFT analysis, matched-filter autocorrelation ripple removal, and sphere TS spectral comparison.
* **[`EK_PosMotion`](EK_PosMotion.html)** (`code/EKlook/EK_PosMotion.c`): Manages the **Position-Motion EK-Trace Window**, displaying the 2D geographic backdrop, 3D OpenGL beam footprint cone, and multi-sensor attitude time series.
* **[`EK_event_loop`](EK_event_loop.html)** (`code/EKlook/EK_event_loop.c`): Central X11 event dispatcher routing mouse and keyboard events across all 6 `EKlook` windows.
* **[`EK_init`](EK_init.html)** (`code/EKlook/EK_init.c`): Initializes environmental defaults, WBT impedance parameters, and display ranges on `EKlook` startup.
* **[`EK_funcs`](EK_funcs.html)** (`code/EKlook/EK_funcs.c`): Core computational routines for loading trace files, ray-tracing bottom strikes, calculating ensonified area, and accumulating ARCs.
* **[`ek_fft_funcs`](ek_fft_funcs.html)** (`code/EKlook/ek_fft_funcs.c`): Complex FFT (`four1`), cosine tapering, frequency wrapping, and ripple detrending library.
