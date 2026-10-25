---
layout: default
title: sidescan/seabed Suite
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 10
---

# Seabed Profiling Tools (`sidescan/seabed`)

The `seabed` directory (`code/sidescan/seabed/`) contains utilities for extracting and analyzing nadir seabed depth profiles and near-nadir acoustic return envelopes from JCU GLORIA (`.ss`) sidescan sonar records.

## Available Tools

* **[`profile`](profile.html)** — Extracts along-track water depth, towfish altitude, and nadir acoustic backscatter profiles from GLORIA sidescan scanlines for comparison with independent echo-sounder bathymetry and verification of bottom-pick accuracy.
* **[`makefile`](makefile.html)** — Build rules for compiling `profile`.

## Workflow Context
`profile` works alongside [`slant/bpick`](../slant/bpick.html), [`azibat/editbat`](../azibat/editbat.html), and [`azibat/mergebat`](../azibat/mergebat.html) to verify that the nadir seabed depth stored in each `gloria_rec` header accurately tracks the true seafloor before running [`slant/glslant`](../slant/glslant.html).
