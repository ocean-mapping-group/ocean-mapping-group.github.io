---
layout: default
title: Finite-Element Tide Modeling (Tidecor)
parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 9
has_children: true
---

# Finite-Element Tidal Prediction (`Tidecor`)

The `Tidecor` directory contains **`tidecor2.42`**, the Ocean Mapping Group's 2D triangular finite-element harmonic tidal prediction and datum reduction engine.

---

## Tools in `Tidecor/`

* [`tidecor2.42`](tidecor2.42.html) — Evaluates astronomical tidal elevations and harmonic constituents (`M2`, `S2`, `N2`, `K1`, `O1`, `ISLW`, plus shallow-water satellites) from triangular finite-element meshes (`$TIDECOR_PATH`) directly onto `.merged` swath files, `.nav` navigation files, `.r4` grids, or fixed station CSV time series.
