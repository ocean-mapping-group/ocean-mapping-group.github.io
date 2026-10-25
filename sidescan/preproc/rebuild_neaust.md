---
layout: default
title: rebuild_neaust
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 2
tool_name: rebuild_neaust
source_path: code/sidescan/preproc/rebuild_neaust
category: Sidescan Preprocessing
input_formats:
- Raw IOS GLORIA (.ios)
- Navigation / Bathymetry files
output_formats:
- Slant-range corrected (.slr)
- Beam-corrected (.beam)
- 2D beam maps (.map, .cnt)
related_tools:
- neaust_fixazi
- mapbeam
- debeam
- joinbeam
- glslant
---

# rebuild_neaust

## Description
`rebuild_neaust` is the master C-shell batch pipeline script (written by Guy Carpenter, November 7, 1990) that automates end-to-end preprocessing of all 62 GLORIA sidescan passes (`ps89_001` through `ps89_062`) from the 1989 Northeast Australia survey.

## Six-Stage Processing Pipeline

1. **Median Gain Normalization (`gainmed_neaust`)**:
   Computes pass-level median gain statistics across `/home/daintree/data/neaust/gloria/raw/*.ios` into `gain.ave` and `gain.pass`.
2. **Slant-Range & Navigation Preprocessing (`preprocI_plus`)**:
   Converts each `.ios` pass (`001..062`) into a slant-range corrected `.slr` file (`/u/guy/data/neaust/gloria/slr/ps89_<num>.slr`).
3. **Empirical Beam Pattern Mapping & Removal ([`mapbeam`](../beammap/mapbeam.html) & `debeam2`)**:
   Accumulates a cumulative 2D depth-vs-grazing-angle beam lookup table (`neaust.map` and `neaust.cnt`) across passes `001..062` using `mapbeam`, then removes the empirical beam pattern from each `.slr` file to produce `/u/guy/data/neaust/gloria/beam/ps89_<num>.beam`.
4. **Azimuth Repair ([`neaust_fixazi`](neaust_fixazi.html))**:
   Recomputes and smooths corrupted azimuths on passes `001–003` using `azimerge -layback 150` and `smthazi -t 6 -f 3`.
5. **Time-Mark Repair (`fixmark`)**:
   Repairs corrupted ping timestamps on passes `001`, `010`, `025`, `041`, and `050`.
6. **Multi-Survey Beam Map Joining ([`joinbeam`](../beammap/joinbeam.html))**:
   Combines the Northeast Australia beam map (`neaust.map`) with the SOPAC beam map (`sopac.map`) into a unified lookup table (`neso.map`).
