---
layout: default
title: Sidescan Radiometric & Geometric Suite (sidescan)
parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 1
has_children: true
---

# Sidescan Processing Suite (`sidescan`)

The `sidescan` subsystem (`code/sidescan/`) contains the Ocean Mapping Group's comprehensive toolkit for ingesting, editing, radiometrically correcting, geometrically rectifying, and mosaicking sidescan sonar and multibeam backscatter data. Most tools operate on the JCU GLORIA 1024-byte scanline record format (`gloria_rec`, defined in `jcu_glo.h`), which stores per-ping navigation, heading, water depth, slant-range corrections, and 496/512 port and starboard 8-bit acoustic intensity samples.

## Subsystems & Categories

### 1. Format Conversion & Ingestion
* **[Convert Tools (`convert/`)](convert/)** — Format converters into the standard JCU GLORIA `.ss` scanline format from IOS (`ios2glo`), USGS (`usgs2glo`), XSonar (`xsonar2glo`), SSI (`ssi2glo`), JWN (`jwn2glo`), and Q-MIPS ([`Q-Mips/qmips2glo`](convert/Q-Mips/qmips2glo.html)), plus record restructuring (`restructure_glo`).
* **[XTF Tools (`xtf/`)](xtf/)** — Ingestion and header manipulation utilities for Triton eXtended Triton Format (`.xtf`) files (`xtf2glo`, `chxtfhdr`, `xtf_funcs`, `bytes2func`).

### 2. Navigation, Azimuth & Bathymetry Editing
* **[Azibat Tools (`azibat/`)](azibat/)** — Utilities for editing, interpolating, smoothing, and merging towfish azimuth, ship position, time stamps, and nadir bathymetry (`editazi`, `editbat`, `editfix`, `editpos`, `interpTime`, `makeazi`, `mergebat`, `smthazi`, `smthbpick`).
* **[Edit Tools (`edit/`)](edit/)** — Interactive and batch scanline editors for JCU GLORIA and IOS sidescan files (`gledit`, `gltimefix`, `iosedit`).
* **[Merge Tools (`merge/`)](merge/)** — Scanline merging, header injection, layback azimuth calculation, and file concatenation (`addheader`, `appendSS`, `azimerge`, `glmerge`).
* **[Preprocessing Scripts (`preproc/`)](preproc/)** — C-shell batch pipelines automating end-to-end GLORIA pass preprocessing (`rebuild_neaust`, `neaust_fixazi`).

### 3. Slant-Range Correction & Seabed Picking
* **[Slant Tools (`slant/`)](slant/)** — First-return bottom tracking (`bpick`), slant-range-to-ground-range geometric rectification (`glslant`), and scanline decimation (`downGrade`).
* **[Seabed Tools (`seabed/`)](seabed/)** — Extraction and profiling of seafloor depth and acoustic return envelopes (`profile`).

### 4. Radiometric Correction, Destriping & Beam Patterns
* **[Beammap Tools (`beammap/`)](beammap/)** — 2D depth-vs-grazing-angle empirical beam pattern mapping and removal (`mapbeam`, `debeam`, `joinbeam`).
* **[Beam Tools (`beam/`)](beam/)** — Legacy GLORIA empirical beam pattern estimation, depth-binning, spline fitting, and plotting ([`oldstuff/`](beam/oldstuff/)).
* **[Gain Tools (`gain/`)](gain/)** — Time-Varying Gain (TVG) normalization and cosmetic gain balancing (`glcosmetic`, `glgain`).
* **[Destripe Tools (`destripe/`)](destripe/)** — Along-track and across-track destriping, boxcar filtering, nadir damping, and dropout replacement (`destripe`, `destripe_hack`, `gladd`, `glboxfilt`, `gldiff`, `gldropStripes`, `glreplace`, `glsmudge`, `nadirdamp`).
* **[Histogram Tools (`hist/`)](hist/)** — Chavez histogram equalization (`glhist`) and across/along-track invalid pixel interpolation (`glfill`, `glfudge`).

### 5. Mosaicking, Printing & Acoustic Simulation
* **[Mapmos Tools (`mapmos/`)](mapmos/)** — Geographic and Mercator projection scanline mosaicking (`mapmos`).
* **[Print Tools (`print/`)](print/)** — Halftone and greyscale mosaic printing (`printmos`).
* **[Mock & Backscatter Modeling Tools (`mock/`)](mock/)** — Forward modeling of synthetic sidescan imagery over 3D bathymetric DTMs, ray-traced grazing-angle lookup tables, and angular backscatter response analysis (`synthetic`, `build_back`, `build_back_mos`, `back_char`, `back_stack`, `selective_back`, `view_sel`, `beams`, `modarray`, `modbeam`, `offtrack`, `showgains`, `fullmock.f`, `rrmos.f`, `ssmock.f`).
* **[JCU GLORIA Suite Overview (`_.md`)](_.html)** — Architecture and record layout (`gloria_rec`) shared across all `sidescan` programs.
