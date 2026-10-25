---
layout: default
title: sm2000toOMG
parent: Grid Tools
tool_name: sm2000toOMG
source_path: code/grid/sm2000toOMG.c
category: gridding
input_formats: ["Kongsberg Mesotech SM2000 Raw IQ Telemetry"]
output_formats: ["OMG HDCS (.merged)", "8-bit Beamformed Magnitude/Phase Rasters", "ASCII Beam Diagnostics (dump_MP, dump_IQ)"]
related_tools: ["weigh_grid", "mosaic"]
---

# sm2000toOMG

## Overview

`sm2000toOMG` performs digital beamforming and bottom detection on raw Quadrature (I/Q) stave recordings from a Kongsberg Mesotech **SM2000** multibeam sonar, producing an OMG HDCS multibeam file along with 8-bit beamformed magnitude, phase, bathymetry, and backscatter diagnostic rasters.

---

## Syntax & CLI Options

```
sm2000toOMG [OPTIONS] <sm2000_fileprefix> <OMGfileprefix>
```

| Flag | Description |
|------|-------------|
| `-plusphase` | Use split-aperture interferometric phase + amplitude bottom detection (`PHASE_PLUS`) instead of amplitude-only (`AMPLITUDE_ONLY`). |
| `-raw` | Process raw element traces (`RAW_TRACES`). |
| `-old` | Use 1997 SM2000 header/format conventions (`VERS_1997`, default: `VERS_1998`). |
| `-split_sep <N>` | Split-aperture sub-array separation (default: `50`). |
| `-swath_sector <deg>` | Desired swath angular sector in degrees (default: `90.0`). |
| `-arc_length <val>` | Transducer array arc length parameter (default: `30.0`). |
| `-depthRange <min> <max>` | Minimum and maximum depth range in meters (default: `20.0 250.0`). |
| `-dBRange <min> <max>` | Minimum and maximum backscatter dynamic range in dB for 8-bit scaling (default: `20.0 100.0`). |
| `-threshold <val>` | Signal detection threshold for first-arrival and bottom picking (default: `1000.0`). |
| `-cosine` | Apply cosine array shading weights during beamforming (default). |
| `-cos_squared` | Apply cosine-squared array shading weights. |
| `-binomial` | Apply binomial array shading weights. |
| `-unshaded` | Use uniform (unshaded) element weights. |
| `-phasing` | Enable phase calibration adjustments (`sm2k_phasing = 1`). |
| `-dumpbeam <beam_no>` | Dump full range-sample magnitude/phase (`dump_MP`) and split-beam I/Q (`dump_IQ`) for beam `<beam_no>` on the first ping and exit. |
| `-v` | Verbose output. |
| `<sm2000_fileprefix>` | Input raw SM2000 I/Q file. |
| `<OMGfileprefix>` | Output prefix for the OMG HDCS file and auxiliary `.mag`, `.phs`, and `.bot` rasters. |

---

## How It Works

1. **Element Geometry & Raw I/Q Ingestion**:
   - Computes stave mount angles (`jSM2K_calc_mount_angles`) and iterates through pings in `<sm2000_fileprefix>`, reading each raw ping header (`jSM2K_read_raw_header`) and per-stave I/Q time series (`jSM2K_read_IQs`).
2. **First Arrival & Beamforming**:
   - Detects the minimum slant range of the first seabed return (`jSM2K_find_first_arrival`) and initializes equiangular beamforming tables (`jSM2K_setup_beamforming`) with the selected aperture shading (`COSINE`, `COS_SQUARED`, `BINOMIAL`, or `UNSHADED`).
   - For each of the `NO_FORMED_BEAMS` beams:
     - Forms the full and split-aperture beam time series (`jSM2K_form_beam_ts`).
     - Executes amplitude or split-phase bottom detection (`jSM2K_do_bd`) and converts sample range and beam angle into depth and across-track distance (`jSM2K_calc_depths`).
3. **Output Generation**:
   - Writes the OMG HDCS multibeam record (`jM2k_write_omg_rec`) and appends 8-bit diagnostic scanlines to the magnitude (`magfile`), phase (`phsfile`), and bottom/imagery (`botfile`) files.

---

## Examples

### Process raw SM2000 stave data using cosine-squared shading and split-phase bottom detection
```bash
sm2000toOMG -plusphase -cos_squared -swath_sector 120 -dBRange 15 85 raw_sm2k_01 omg_sm2k_01
```

---

## Workflow Context

- **Downstream**: [`weigh_grid`](weigh_grid.html), `swathEd`, `jview`.
