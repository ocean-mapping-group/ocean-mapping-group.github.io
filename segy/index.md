---
layout: default
title: SEGY Tools
has_children: true
nav_order: 22
---

# SEGY Tools

Tools in the `segy/` directory unpack, inspect, and convert seismic, sub-bottom profiler, and multi-channel sidescan datasets stored in **SEG-Y** (and vendor-extended SEG-Y variants such as SeaBeam 2112 4 kHz sub-bottom, Kongsberg SBP 120, ORE SE880, EG&G Chirp, Atlantic Geoscience Centre 4-channel digitizer, and Klein System 5000) into OMG HDCS, GLORIA, and binary image formats.

## Tool Summary

| Tool | Source | Description |
| :--- | :--- | :--- |
| [klein](klein) | `segy/klein.c` | Converts raw Klein System 5000 10-beam sidescan data into ORE SE880-compatible SEG-Y format with optional decimation. |
| [mergePick](mergePick) | `segy/mergePick.c` | Interpolates digitized sub-bottom reflector picks onto an ASCII seismic pick/trace table produced by `upsegy`. |
| [readSB_SEGY](readSB_SEGY) | `segy/readSB_SEGY.c` | Unpacks single- or multi-channel SEG-Y sub-bottom profiler data (SeaBeam 2112 4 kHz, SBP 120, SonarWiz) into `.chan1`, `.nav`, and OMG HDCS `.merged` / `.merged.ss_data` / `.merged.fl_data` files. |
| [readore](readore) | `segy/readore.c` | Interactive reader and 4-channel splitter (`channel1`–`channel4`) for ORE SE880 SEG-Y sidescan/sub-bottom files. |
| [upAGCDIG](upAGCDIG) | `segy/upAGCDIG.c` | Unpacks 4-channel (120 kHz & 300 kHz port/starboard + NMEA trace) AGC digitizer SEG-Y sidescan files into GLORIA (`.120_rawss`, `.300_rawss`), `.nmea`, and slant-range-corrected files. |
| [upsegy](upsegy) | `segy/upsegy.c` | Unpacks EG&G Chirp complex (in-phase/quadrature) SEG-Y traces into `.envelope`, `.inphase`, `.aligned`, `.nav`, and `.picks` files. |
