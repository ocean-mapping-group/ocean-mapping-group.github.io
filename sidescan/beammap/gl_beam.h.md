---
layout: default
title: gl_beam.h
parent: Beammap Tools
grand_parent: Sidescan Tools
nav_order: 4
tool_name: gl_beam.h
source_path: code/sidescan/beammap/gl_beam.h
category: Sidescan Beam Pattern Processing
input_formats: ["C Header File"]
output_formats: ["Included by mapbeam.c, debeam.c, joinbeam.c"]
related_tools: ["mapbeam", "debeam", "joinbeam"]
---

# gl_beam.h

## Description
`gl_beam.h` is the shared C header file (written by Guy Carpenter, April 1990) defining grid dimensions, depth bounds, and array-indexing macros for the 2D empirical beam-pattern mapping and removal tools ([`mapbeam`](mapbeam.md), [`debeam`](debeam.md), and [`joinbeam`](joinbeam.md)).

## Constants & Macros

| Symbol | Definition | Description |
| :--- | :--- | :--- |
| `SWATH_WIDTH` | `(GLORIA_SIDESIZE * 2)` | Total across-track pixels per scanline (`496 × 2 = 992` pixels). |
| `PIX_SIZE` | `30` | Ground-range pixel spacing in meters (`30 m` for GLORIA). |
| `MIN_DEPTH` | `0` | Minimum water depth (`0 m`) mapped in the 2D beam table. |
| `MAX_DEPTH` | `3000` | Maximum water depth (`3000 m`) mapped in the 2D beam table. |
| `DEPTH_RES` | `512` | Number of vertical water-depth rows in the 2D beam lookup array. |
| `ALEN` | `(SWATH_WIDTH * DEPTH_RES)` | Total elements (`992 × 512 = 507,904`) in the 2D beam map array. |
| `AINDEX(ROW, COL)` | `(ROW * SWATH_WIDTH + COL)` | Row-major 1D offset macro into the `DEPTH_RES × SWATH_WIDTH` beam array. |
| `DTOR(D)` | `((D) * M_PI / 180.0)` | Degrees-to-radians conversion macro. |
| `DEPTHTOROW(D)` | `(((D) - MIN_DEPTH) * DEPTH_RES / (MAX_DEPTH - MIN_DEPTH))` | Maps nadir water depth `D` (in meters) to row index `0..511`. |
