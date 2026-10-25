---
layout: default
title: sidescan/hist Suite
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 6
---

# Histogram & Gap-Filling Tools (`sidescan/hist`)

The `hist` directory (`code/sidescan/hist/`) contains utilities for radiometric histogram equalization and across/along-track invalid pixel interpolation in JCU GLORIA (`.ss`) and EM-12 look-alike sidescan records.

## Available Tools & Files

* **[`glhist`](glhist.html)** — Performs Chavez-style histogram equalization on JCU GLORIA / EM-12 sidescan files, mapping the cumulative input DN distribution onto a target Gaussian or uniform distribution while excluding invalid/background pixels (`-invalid`).
* **[`glfill`](glfill.html)** — Interpolates across-track gaps of invalid pixels (such as nadir gaps or missing samples Resulting from slant-range stretching or multibeam backscatter rebinning) in GLORIA `.ss` scanlines.
* **[`glfudge`](glfudge.html)** — Performs 2D (across-track and along-track) interpolation of missing or zeroed pixels in JCU GLORIA `.ss` files using surrounding valid scanline neighbors.
* **[`glfill.c_bug`](glfill.c_bug.html)** — Preserved October 1991 revision of `glfill.c` (`-invalid`, `-lower_level`) prior to across-track edge boundary fixes.
* **[`glhist_pre_steve0531.c`](glhist_pre_steve0531.c.html)** — Earlier baseline implementation of `glhist.c` prior to May 31 updates by S. Hughes / J. Hughes Clarke.
* **[`glfudge.o`](glfudge.o.html)** — Compiled object module for [`glfudge`](glfudge.html).
* **[`makefile`](makefile.html)** — Build rules for `glhist`, `glfill`, and `glfudge`.

## Typical Workflow
When processing Simrad EM-12 or multibeam backscatter cast into GLORIA `.ss` format (e.g., via `swathed` / `jview`), invalid sample gaps are first bridged with [`glfill`](glfill.html) or [`glfudge`](glfudge.html), and dynamic range is equalized with [`glhist`](glhist.html) prior to mosaicking with [`mapmos`](../mapmos/mapmos.html).
