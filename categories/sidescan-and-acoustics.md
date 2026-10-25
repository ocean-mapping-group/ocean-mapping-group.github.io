---
layout: default
title: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 8
has_children: true
---

# 3. Sidescan, Echosounders, ADCP & Sub-Bottom

Radiometric/geometric sidescan processing, Simrad EK60/EK80 scientific echosounders, Teledyne RDI ADCP currents, seabed angular response classification, and SEG-Y / Knudsen / EdgeTech JSF sub-bottom profilers.

---

## Directory Modules in This Category

| Module | Directory | Purpose & Key Tools |
| :--- | :--- | :--- |
| **[Sidescan Radiometric & Geometric Suite (sidescan)](../sidescan/)** | `sidescan/` | Comprehensive 16-module sidescan processing suite: slant-range correction, beam pattern removal (`debeam`), TVG, destriping, gain normalization, and azimuthal backscatter. |
| **[Simrad EK60/EK80 Echosounder Suite (EKlook)](../EKlook/)** | `EKlook/` | Interactive and batch processors (`EKlook`, `BatchProcEK`) for Simrad EK60/EK80 `.raw` split-beam scientific echosounders, calibration spheres, and target strength. |
| **[Acoustic WAV Waveform Tools (Wave)](../Wave/)** | `Wave/` | Raw acoustic `.wav` hydrophone/transducer waveform windowing and spectral extraction (`readWave`, `extractWaveWindow`). |
| **[Teledyne RDI ADCP Processing (adcp)](../adcp/)** | `adcp/` | Workhorse & Ocean Surveyor ADCP binary PD0 readers (`readADCP`, `readWinADCP`), tidal current ellipse fitting (`calc_ellipse`), and vector mapping (`makeVectorPlot`). |
| **[Angular Response & Classification (class)](../class/)** | `class/` | Multibeam/sidescan incidence-angle backscatter response curves (`classAngStrip`, `build_back`) and acoustic seabed classification. |
| **[SEG-Y Sub-Bottom & Seismic (segy)](../segy/)** | `segy/` | SEG-Y seismic and chirp sub-bottom profiler readers, envelope detectors, bottom trackers, and curtain exporters. |
| **[Knudsen Chirp Sub-Bottom (knudsen)](../knudsen/)** | `knudsen/` | Knudsen 320B/3260 `.keb` and `.sgy` chirp sub-bottom profiler converters and processors. |
| **[EdgeTech JSF Sidescan & Sub-Bottom (jsf)](../jsf/)** | `jsf/` | EdgeTech `.jsf` dual-frequency sidescan and chirp sub-bottom parser (`jsf2omg`, `jsf2ss`). |
| **[eXtended Triton Format — XTF (xtf)](../xtf/)** | `xtf/` | Triton `.xtf` sidescan and multibeam packet readers (`xtf2omg`, `xtf2ss`). |
| **[Klein Sonar Data Format — SDF (sdf)](../sdf/)** | `sdf/` | Klein System 3000/5000 `.sdf` sidescan unpackers and slant-range converters. |
| **[HAWAII MR1 Towed Sidescan (mr1)](../mr1/)** | `mr1/` | HIGP MR1 long-range towed sidescan phase/amplitude processors (`mr1_raw`, `mr1_proc`). |
| **[Single-Beam Echosounder Tools (singlebeam)](../singlebeam/)** | `singlebeam/` | Single-beam echo sounder digitisers, navigation mergers, and `.merged` pseudo-swath wrappers. |
