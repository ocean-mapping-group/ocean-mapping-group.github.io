---
layout: default
title: Knudsen Chirp Sub-Bottom (knudsen)
parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 7
has_children: true
---

# Knudsen Tools

Tools in the `knudsen/` directory convert, process, bottom-track, radiometrically calibrate, and plot dual-frequency single-beam echosounder, chirp sub-bottom profiler, and sidescan data from **Knudsen Engineering** (320M/320B/3260 KEL `.keb`/`.kea` binary, `B9`/`VX`/`D3`/`E0` USB formats, and SEG-Y), **Furuno FCV-30** (`.hac`), **Simrad/Kongsberg EA600 / EK60 / EK80** (`.raw`), and **iXblue Echoes 3000/3500** (`.xtf`) systems.

## Tool Summary

| Tool | Source | Description |
| :--- | :--- | :--- |
| [calcLineSegments](calcLineSegments) | `knudsen/calcLineSegments.c` | Analyzes vessel gyro heading, course-made-good (CMG), and turn rate across OMG HDCS pings to identify survey line segments. |
| [collapseSeisStack](collapseSeisStack) | `knudsen/collapseSeisStack.c` | Composites multiple map-projected 3D perspective sub-bottom images (`makeSeisPlot -map`) using `.perspect` proximity weights. |
| [fcv30-2glo](fcv30-2glo) | `knudsen/fcv30-2glo.c` | Converts Furuno FCV-30 `.hac` hydroacoustic tuple files into OMG HDCS `.merged`/`.merged.ss_data` or `.chan1`–`.chan5` and `.nav` files. |
| [k16to8](k16to8) | `knudsen/k16to8.c` | Re-quantizes 16-bit Knudsen `.merged.16_data` traces into 8-bit `.merged.ss_data` with TVG, attenuation, ensonified area, bandpass filtering, and cross-talk removal. |
| [kflto8](kflto8) | `knudsen/kflto8.c` | Converts 32-bit floating-point sub-bottom trace files (`.merged.fl_data`) into 8-bit `.merged.ss_data` trace files. |
| [knud2glo](knud2glo) | `knudsen/knud2glo.c` | Converts Knudsen KEL binary envelope files (legacy, `-VX`/`-B9`, `-D3`, `-E0`) into OMG HDCS `.merged` (`.ss_data`, `.16_data`) or GLORIA format plus `.nav`. |
| [makeSeisPlot](makeSeisPlot) | `knudsen/makeSeisPlot.c` | Generates depth-phased, heave-compensated, or 3D perspective-mapped seismic/echosounder scroll images (`JHC_header`) from OMG HDCS sub-bottom files. |
| [makeSeisPlot_Op](makeSeisPlot_Op) | `knudsen/makeSeisPlot_Op.c` | Multi-beam/swath-capable variant of `makeSeisPlot` for projecting sub-bottom and water-column traces onto a 3D perspective map sheet. |
| [make_knudsen_ss](make_knudsen_ss) | `knudsen/make_knudsen_ss.c` | Converts OMG HDCS Knudsen dual-channel trace data into GLORIA sidescan files with optional bottom re-picking and beam-pattern correction. |
| [mergeOtherSonarData](mergeOtherSonarData) | `knudsen/mergeOtherSonarData.c` | Transfers aiding depth, attitude, or clock-drift delay from time-synchronous OMG HDCS multibeam files onto Knudsen or deep multibeam files. |
| [pickSS](pickSS) | `knudsen/pickSS.c` | Re-picks seabed nadir arrival times on HF, LF, or blended 8-bit `.ss_data` traces and optionally updates `.merged` depths in-place. |
| [plotBorder](plotBorder) | `knudsen/plotBorder.c` | Generates a `plotlib` vector border with depth gridlines and time/position tick marks for hardcopy sub-bottom scroll plots. |
| [readEA600](readEA600) | `knudsen/readEA600.c` | Unpacks Kongsberg/Simrad EA600, EK60, and EK80 (CW and broadband FM matched-filtered) `.raw` files into OMG HDCS `.merged` and trace files. |
| [readixBlueXTF](readixBlueXTF) | `knudsen/readixBlueXTF.c` | Unpacks iXblue Echoes 3000/3500 sub-bottom traces (XTF packet type `202`) into `.chan1`, `.nav`, `.orientation`, and OMG HDCS `.merged` files. |
| [upKnudSEGY](upKnudSEGY) | `knudsen/upKnudSEGY.c` | Unpacks Knudsen 320 3.5 kHz SEG-Y sub-bottom files into 8-bit `.120_rawss` trace files. |
