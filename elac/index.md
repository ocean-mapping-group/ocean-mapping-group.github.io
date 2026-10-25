---
layout: default
title: ELAC Tools
has_children: true
nav_order: 5
---

# ELAC Tools

Tools in the `elac/` directory convert and filter multibeam bathymetry acquired by **Honeywell ELAC Nautik BottomChart** (FAU Fast Acquisition Unit format) systems in OMG HDCS `.merged` format. (See also [`elac2omg`](../xtf/elac2omg) in the `xtf/` directory and [`xse2omg`](../xse/xse2omg) in the `xse/` directory for newer XTF and XSE ELAC formats.)

## Tool Summary

| Tool | Source | Description |
| :--- | :--- | :--- |
| [qualityFlag](qualityFlag) | `elac/qualityFlag.c` | Flags or unflags beams in OMG HDCS `.merged` files based on ELAC SNR quality factors or SeaBat 8101 detection bitmasks. |
| [refoELAC](refoELAC) | `elac/refoELAC.c` | Converts raw Honeywell ELAC BottomChart FAU format files into OMG HDCS `.merged` files and generates `.quality` and `.amplitudes` histograms. |
