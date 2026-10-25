---
layout: default
title: his.nov30
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 15
tool_name: his.nov30
source_path: code/sidescan/destripe/his.nov30
category: Workflow Log
input_formats:
- OMG Swath (.merged)
- JCU GLORIA (.ss)
output_formats:
- Gap-filled GLORIA (.ss_fill)
related_tools:
- DelayEditor
- swathed
- jview
- glfill
- glgain
---

# his.nov30 (`sidescan/destripe`)

## Description
`his.nov30` is a preserved C-shell command history log (dated November 30, 1995, 09:49–11:19) recorded during an interactive multibeam/sidescan processing session on the `river_174_1010` dataset. It documents the practical workflow connecting attitude delay calibration, swath editing, GLORIA `.ss` backscatter extraction, gap interpolation (`glfill`), and gain/destripe tool development.

## Recorded Workflow Steps

1. **Roll/Pitch Latency Calibration (`DelayEditor`)**:

   ```csh
   DelayEditor -fix -scale 1.03 -lag -0.61 temp.merged
   ```
   Iteratively tests roll scale factors (`1.03`) and time lags (`-0.75` to `-0.61 s`) on `temp.merged` and inspects the updated swath in `swathed`.
2. **Sidescan Extraction & Viewing (`jview`)**:

   ```csh
   jview -gl river_174_1010.ss
   ```
   Inspects the extracted JCU GLORIA format sidescan file `river_174_1010.ss`.
3. **Across-Track Gap Interpolation (`glfill`)**:

   ```csh
   glfill river_174_1010.ss river_174_1010.ss_fill
   jview -gl river_174_1010.ss_fill
   ```
   Runs [`glfill`](../hist/glfill.html) to interpolate missing across-track samples and verifies the filled scanlines in `jview`.
4. **Radiometric Filter Development (`gain/`, `destripe/`)**:
   Navigates to `/usr/local/src/jcu/sidescan/gain` and `destripe` to adapt [`glgain`](../gain/glgain.html) and [`destripe`](destripe.html) for shallow-water river swath backscatter.
