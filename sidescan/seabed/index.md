---
layout: default
title: Seabed Tools
parent: Sidescan Tools
nav_order: 10
has_children: true
---

# Seabed Profiling Tools (`sidescan/seabed`)

The `seabed` directory (`code/sidescan/seabed/`) contains utilities for extracting and analyzing nadir seabed depth profiles and near-nadir acoustic return envelopes from JCU GLORIA (`.ss`) sidescan sonar records.

## Available Tools

* **[`profile`](profile.md)** — Extracts along-track water depth, towfish altitude, and nadir acoustic backscatter profiles from GLORIA sidescan scanlines for comparison with independent echo-sounder bathymetry and verification of bottom-pick accuracy.
* **[`makefile`](makefile.md)** — Build rules for compiling `profile`.

## Workflow Context
`profile` works alongside [`slant/bpick`](../slant/bpick.md), [`azibat/editbat`](../azibat/editbat.md), and [`azibat/mergebat`](../azibat/mergebat.md) to verify that the nadir seabed depth stored in each `gloria_rec` header accurately tracks the true seafloor before running [`slant/glslant`](../slant/glslant.md).
