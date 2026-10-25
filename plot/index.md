---
layout: default
title: Plot Tools
nav_order: 13
has_children: true
---

# Scientific & Diagnostic Plotting (`plot`)

The `plot` directory contains vector plotting programs built on top of [`plotlib`](../plotlib/index.md) for generating 2D Cartesian and polar plots (`plot.meta`) of multibeam beam patterns, seafloor angular response curves, grain-size correlations, motion sensor residuals, tide time series, sound velocity profiles, and swath cross-sections.

---

## Backscatter, Beam Pattern & Angular Response Plotting

* [`plotBP`](plotBP.md) — Polar and Cartesian plotter for empirical beam patterns (`getBeamPattern`, `newGetBP`), grazing-angle response curves, and 3 dB beam footprints.
* [`plotBP_before_june15_changes`](plotBP_before_june15_changes.md) — Preserved pre-June 2015 version of `plotBP`.
* [`plotAngular`](plotAngular.md), [`plotAng2`](plotAng2.md), [`plotAngStrip`](plotAngStrip.md) — Plotters for seafloor angular response (`.ar`, `.angstrip`) curves and grazing-angle backscatter variation.
* [`plotAAC`](plotAAC.md) — Plots Area-Angle Curves (AAC) for backscatter normalization and classification.
* [`plotGS`](plotGS.md) — Plots sediment grain-size samples against acoustic backscatter metrics.
* [`makeFoot`](makeFoot.md) & [`plotFoot`](plotFoot.md) — Computes and plots 3 dB multibeam beam footprints across the swath.

---

## Swath, Bathymetry, Attitude & Time-Series Plotting

* [`asciiplot`](asciiplot.md) & [`multiplot`](multiplot.md) — General-purpose XY scatter and line plotters for multi-column ASCII datasets.
* [`plot2D`](plot2D.md) — 2D density/histogram and scatter plotter.
* [`plotSwath`](plotSwath.md) & [`plotProf`](plotProf.md) — Plots across-track multibeam bathymetry profiles and DTM cross-sections.
* [`BDplot`](BDplot.md) — Plots bottom-detection amplitude vs. phase trajectories.
* [`downHill`](downHill.md) — Plots down-slope bathymetric gradients and refraction/roll artifacts.
* [`plotRoll`](plotRoll.md) & [`plotDelayHeave`](plotDelayHeave.md) — Plots roll bias residuals and delayed heave vs. real-time heave time series.
* [`plotTides`](plotTides.md) — Plots tidal elevation time series and gauge comparisons.
* [`plotSvSonar`](plotSvSonar.md) — Plots surface sound speed at the transducer (`td_sound_speed`) against SVP casts.
* [`plotAspectRatio`](plotAspectRatio.md) — Plots target or swath aspect ratio metrics.
* [`plotDump`](plotDump.md), [`plotMultiDump`](plotMultiDump.md), [`plotFFT_BF`](plotFFT_BF.md), [`parseBIST`](parseBIST.md) — Diagnostic plotters for trace dumps, FFT beamformed spectra, and Kongsberg Built-In Self-Test (BIST) logs.
