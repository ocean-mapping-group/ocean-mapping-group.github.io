---
layout: default
title: makefile (Singlebeam)
parent: Single-Beam Echosounder Tools (singlebeam)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 2
---

# singlebeam/makefile

## Description
Build configuration (`code/singlebeam/makefile`) for compiling the [`refoCustom`](refoCustom.html) singlebeam converter executable and installing it into `$(LOCALBIN)`.

## Targets & Dependencies
* **`all`**: Builds `refoCustom`.
* **`refoCustom`**: Links `$(LOCALOBJ)/refoCustom.o` and `$(LOCALOBJ)/OMG_HDCS_jversion.o` against `-L$(LOCALLIB) -llocal -lm` and moves the resulting binary to `$(LOCALBIN)`.
* **`clean`**: Removes local object files (`*.o`), backup files (`*~`), and `core` dumps.
