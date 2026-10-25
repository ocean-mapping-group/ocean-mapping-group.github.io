---
layout: default
title: sidescan/slant Suite
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 11
---

# Slant-Range Correction & Bottom Picking Tools (`sidescan/slant`)

The `slant` directory (`code/sidescan/slant/`) provides the core geometric rectification tools that detect the first seafloor acoustic return (water-column/seabed interface) and project raw time-sampled (slant-range) sidescan scanlines into true horizontal across-track ground range.

## Available Tools

* **[`bpick`](bpick.html)** — Automated and threshold-assisted bottom picker that scans raw GLORIA `.ss` records across nadir to detect the first high-amplitude seabed arrival on port and starboard channels, updating the header water depth / altitude fields.
* **[`glslant`](glslant.html)** — Performs slant-range-to-ground-range geometric correction on JCU GLORIA `.ss` files (producing `.slr` files), removing the water column and mapping each sample from slant range $R$ to horizontal ground range $x = \sqrt{R^2 - z^2}$ assuming either a flat seafloor or local cross-track slope.
* **[`downGrade`](downGrade.html)** — Downsamples/decimates high-resolution sidescan records along-track and/or across-track into standard GLORIA record dimensions for regional overview processing.
* **[`makefile`](makefile.html)** — Build configuration for `glslant`, `bpick`, and `downGrade`.

## Typical Workflow
1. Run [`bpick`](bpick.html) on raw `.ss` files to determine towfish altitude above the seabed.
2. Smooth noisy bottom picks along-track using [`azibat/smthbpick`](../azibat/smthbpick.html) or edit outliers with [`azibat/editbat`](../azibat/editbat.html).
3. Run [`glslant`](glslant.html) to remove the water column and map slant range into ground range (`.slr`), ready for empirical beam pattern correction ([`beammap/debeam`](../beammap/debeam.html)).
