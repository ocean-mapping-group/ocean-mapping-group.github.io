---
layout: default
title: neaust_fixazi
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 1
tool_name: neaust_fixazi
source_path: code/sidescan/preproc/neaust_fixazi
category: Sidescan Preprocessing
input_formats:
- JCU GLORIA (.beam)
- Navigation time series (neaust.nav)
output_formats:
- Azimuth-corrected JCU GLORIA (.beam)
related_tools:
- azimerge
- smthazi
- rebuild_neaust
---

# neaust_fixazi

## Description
`neaust_fixazi` is a C-shell preprocessing script (written by Guy Carpenter, November 19, 1990) that repairs corrupted towfish compass azimuths in Northeast Australia 1989 GLORIA passes (`ps89_001.beam` through `ps89_003.beam`). For passes where the internal GLORIA compass failed, it computes ship course-made-good with a 150 m towfish layback from the master navigation file (`neaust.nav`) and applies a temporal smoothing filter.

## Script Pipeline
For each affected pass (`ps89_001.beam`, `ps89_002.beam`, `ps89_003.beam`):
1. **Layback Azimuth Merging ([`azimerge`](../merge/azimerge.html))**:

   ```csh
   azimerge -layback 150 ~/data/neaust/nav/neaust.nav $file ${file}.merge
   ```
   Computes the effective towfish track and azimuth assuming a 150-meter cable layback behind the ship navigation fixes in `neaust.nav`.
2. **Temporal Azimuth Smoothing ([`smthazi`](../azibat/smthazi.html))**:

   ```csh
   smthazi -t 6 -f 3 ${file}.merge $file
   ```
   Applies a running smoothing filter (`-t 6 -f 3`) to remove abrupt course changes at navigation fix boundaries and overwrites the repaired `.beam` file.
