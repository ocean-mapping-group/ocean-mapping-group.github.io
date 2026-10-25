---
layout: default
title: PostScript & Vector Plotting (plot)
parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 7
has_children: true
---

# Scientific & Diagnostic Plotting (`plot`)

The `plot` directory contains vector plotting programs built on top of [`plotlib`](../plotlib/) for generating 2D Cartesian and polar plots (`plot.meta`) of multibeam beam patterns, seafloor angular response curves, grain-size correlations, motion sensor residuals, tide time series, sound velocity profiles, and swath cross-sections.

---

## Backscatter, Beam Pattern & Angular Response Plotting

* [`plotBP`](plotBP.html) — Polar and Cartesian plotter for empirical beam patterns (`getBeamPattern`, `newGetBP`), grazing-angle response curves, and 3 dB beam footprints.
* [`plotBP_before_june15_changes`](plotBP_before_june15_changes.html) — Preserved pre-June 2015 version of `plotBP`.
* [`plotAngular`](plotAngular.html), [`plotAng2`](plotAng2.html), [`plotAngStrip`](plotAngStrip.html) — Plotters for seafloor angular response (`.ar`, `.angstrip`) curves and grazing-angle backscatter variation.
* [`plotAAC`](plotAAC.html) — Plots Area-Angle Curves (AAC) for backscatter normalization and classification.
* [`plotGS`](plotGS.html) — Plots sediment grain-size samples against acoustic backscatter metrics.
* [`makeFoot`](makeFoot.html) & [`plotFoot`](plotFoot.html) — Computes and plots 3 dB multibeam beam footprints across the swath.

---

## Swath, Bathymetry, Attitude & Time-Series Plotting

* [`asciiplot`](asciiplot.html) & [`multiplot`](multiplot.html) — General-purpose XY scatter and line plotters for multi-column ASCII datasets.
* [`plot2D`](plot2D.html) — 2D density/histogram and scatter plotter.
* [`plotSwath`](plotSwath.html) & [`plotProf`](plotProf.html) — Plots across-track multibeam bathymetry profiles and DTM cross-sections.
* [`BDplot`](BDplot.html) — Plots bottom-detection amplitude vs. phase trajectories.
* [`downHill`](downHill.html) — Plots down-slope bathymetric gradients and refraction/roll artifacts.
* [`plotRoll`](plotRoll.html) & [`plotDelayHeave`](plotDelayHeave.html) — Plots roll bias residuals and delayed heave vs. real-time heave time series.
* [`plotTides`](plotTides.html) — Plots tidal elevation time series and gauge comparisons.
* [`plotSvSonar`](plotSvSonar.html) — Plots surface sound speed at the transducer (`td_sound_speed`) against SVP casts.
* [`plotAspectRatio`](plotAspectRatio.html) — Plots target or swath aspect ratio metrics.
* [`plotDump`](plotDump.html), [`plotMultiDump`](plotMultiDump.html), [`plotFFT_BF`](plotFFT_BF.html), [`parseBIST`](parseBIST.html) — Diagnostic plotters for trace dumps, FFT beamformed spectra, and Kongsberg Built-In Self-Test (BIST) logs.
