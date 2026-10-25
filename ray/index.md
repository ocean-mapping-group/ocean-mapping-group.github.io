---
layout: default
title: Ray Tools
nav_order: 17
has_children: true
---

# Acoustic Ray Tracing & Sound Velocity Profiles (`ray`)

The `ray` directory contains acoustic ray-tracing engines, sound velocity profile (SVP) comparison utilities, harmonic mean sound speed calculators, and `plotlib`-based oceanographic cast plotters.

---

## Ray Tracing & Refraction Solvers

* [`Ray`](Ray.md) & [`traceRay`](traceRay.md) — Core Snell's Law constant-gradient layered acoustic ray tracers computing two-way travel time, horizontal range, depth, and ray bending across water-column sound velocity profiles.
* [`buildray`](buildray.md) — Pre-computes 2D depth/range ray-tracing lookup tables (`JHC_header` float grids) from an SVP cast for fast swath refraction correction.
* [`calcRayDiff`](calcRayDiff.md) — Quantifies across-track depth and radial positioning errors induced by mismatches between two sound velocity profiles (`compareTwoSVPs`).
* [`Switch`](Switch.md) — Models depth and across-track discontinuities caused by switching active sound velocity profiles during multibeam acquisition.

---

## Sound Velocity Profile Analysis & Plotting

* [`plotSVP`](plotSVP.md) — Comprehensive `plotlib` vector plotter for temperature, salinity, density, and sound speed casts (`plot.meta`).
* [`compareTwoSVPs`](compareTwoSVPs.md) — Compares two sound velocity casts and computes depth-dependent refraction residuals.
* [`svpSonar`](svpSonar.md) — Evaluates surface sound speed (`td_sound_speed`) vs. profile-integrated harmonic sound speed at transducer draft.
* [`new_speedtosalinity`](new_speedtosalinity.md) — Inverting empirical seawater sound speed equations (Chen & Millero / Del Grosso / Mackenzie) to estimate salinity from measured sound speed, temperature, and pressure.
* [`plotOS500`](plotOS500.md) & [`plotSOLN`](plotSOLN.md) — Specialized plotters for Ocean Seven OS500 CTD/SVP probes and ray-tracing solution curves.
