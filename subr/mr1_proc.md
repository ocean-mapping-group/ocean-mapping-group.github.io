---
layout: default
title: mr1_proc
parent: Core Shared Libraries (subr)
module_name: mr1_proc
source_path: code/subr/mr1_proc.c
header_path: code/subr/mr1_proc.h
category: Sonar Format I/O & Interferometric Processing (MR1)
related_tools:
  - MR1toOMG
  - weigh_grid
  - jview
---

# `mr1_proc` — HIG Hawaii MR1 Towed Interferometric Sidescan Processing Library

## Overview & Purpose in the OMG Architecture

`mr1_proc` (`code/subr/mr1_proc.c`, `code/subr/mr1_proc.h`), written by John E. Hughes Clarke in March 1992 aboard R/V *Moana Wave* (cruise MW9204 in the Western Solomon Sea), implements the complete acoustic signal processing, ping stacking, phase-inversion detection, first-break altitude picking, slant-range correction, and interferometric phase-bathymetry reconstruction pipeline for the **Hawaii Institute of Geophysics (HIG / HMRG) MR1** towed bathymetric sidescan sonar (`MR1toOMG`).

The MR1 system logs raw quadrature (`I/Q` real and imaginary) acoustic samples from dual receiver arrays (`A` and `B`) on port and starboard sides (`mr1_raw.h`). `mr1_proc` unpacks the raw 64-sample packets, checks and corrects for $90^\circ$ receiver phase-lag inversions, applies time-varying gain (TVG) and ambient noise subtraction, decimates the 20,000-sample traces down to 512 sidescan pixels per side, picks the seafloor first arrival, performs flat-seafloor slant-range correction, and maps filtered inter-stave phase angles into 120 across-track bathymetric soundings (`OMG_MR1_zx_rec`) and 8-bit sidescan records (`OMG_MR1_ss_rec` in `OMG_mr1.h`).

---

## Key Data Structures, Constants & Globals (`code/subr/mr1_proc.h`, `code/subr/OMG_mr1.h`)

### Processing Mode & Bottom-Pick Constants
- **Operating Modes (`mode`)**: `SINGLE` (`0`), `CONT` (`1`), `EDIT` (`2`).
- **Decimation Factor**: `DEC` (`25` samples per bin).
- **Bottom-Pick Modes (`detect_flag`)**: `PICK_STBD` (`0`), `PICK_PORT` (`1`), `PICK_BOTH` (`2`), `PICK_SHALLOW` (`3`), `PICK_DEEP` (`4`).

### Companion Output Structures (`code/subr/OMG_mr1.h`)
- `OMG_head`: 136-byte header (sized identically to `jcu_all_rec` in `jcu_glo.h`) storing `time`, `centisecs`, `azi`, `ping_rate`, `pixel_size`, `lat`, `lon`, `fishdepth`, `altitude`, 12-sample arrays of `pitch[12]`, `roll[12]`, `heading[12]`, `port_pick`, `stbd_pick`, `port_threshold`, `stbd_threshold`, `min_value`, `max_value`, `byte_offset`, and `status`.
- `OMG_MR1_ss_rec`: 1160-byte sidescan record (`OMG_head header`, `unsigned char stbd_data[512]`, `port_data[512]`), binary-compatible with JCU GLORIA tools.
- `OMG_phase_bathy` & `OMG_MR1_zx_rec`: Interferometric phase-bathymetry record containing `OMG_head header` and `OMG_phase_bathy beam[120]` (`bin_time`, `phase_angle`, `quality`, `bin_echo`, `depth`, `offset`, `status`).

### Key Global Processing Buffers (`code/subr/mr1_proc.h`)
- **Raw & Stacked Quadrature Arrays (20,000 samples/side)**:
  `out_samp port_raw_data[20000]`, `stbd_raw_data[20000]`, `short port_stack[20000]`, `stbd_stack[20000]`, `float port_amplitude[20000]`, `stbd_amplitude[20000]`, `port_phase[20000]`, `stbd_phase[20000]`, `port_phase_real/imag[20000]`, `stbd_phase_real/imag[20000]`.
- **Decimated 512-Bin Sidescan & Phase Arrays**:
  `float port_slr_ampl[512]`, `stbd_slr_ampl[512]`, `port_dec_ampl[512]`, `stbd_dec_ampl[512]`, `port_dec_phas[512]`, `stbd_dec_phas[512]`, `port_dec_stdv[512]`, `stbd_dec_stdv[512]`.
- **Phase-to-Angle Lookup Tables & Bathymetry Bins (60 beams/side)**:
  `float port_LUT[90]`, `stbd_LUT[90]`, `port2_depth[60]`, `port2_offset[60]`, `port2_sample[60]`, `port2_phase[60]`, `stbd2_depth[60]`, `stbd2_offset[60]`.
- **X11 Display Buffers**: `XImage *slr_image`, `*raw_image`, `*dep_image`.

---

## Public Functions & Signatures

### Pre-existing Data & LUT Initialization
- `void load_up_preexisting_data()`, `void load_up_slr()`, `void load_up_topo()`
  Loads previously processed `OMG_MR1_ss_rec` (`rawfile`, `slrfile`) and `OMG_MR1_zx_rec` (`depfile`) records into the X11 image buffers (`raw_image`, `slr_image`, `dep_image`) for interactive viewing and re-editing.
- `void pickup_LUT()`
  Initializes the 90-degree phase-to-depression-angle lookup tables (`port_LUT[90]`, `stbd_LUT[90]`).

### Raw Quadrature Unpacking, Stacking & Gain Conditioning
- `void clear_out_acoustic_data()`
  Zeroes the 20,000-sample stack counters, amplitude, and real/imaginary phase accumulators.
- `int load_up_acoustic_data(int no_packets)` / `int read_in_acoustic_data(int no_packets)`
  Reads `no_packets` raw 64-sample `packet` blocks (`mr1_raw.h`) from `infile`, separates odd sequence numbers (port) from even sequence numbers (starboard), and scales the 16-bit integer `ar`, `ai`, `br`, `bi` components by `expons[a_packet.expon]` ($2^{\text{expon}}$).
- `void check_raw_for_invert()`
  Inspects the tail (last 640 samples) of each trace to detect anomalous $+90^\circ$ quadrature phase lags (`mean_phase_lag > 45.0`) and sets `port_invert` / `stbd_invert`.
- `void proc_up_acoustic_data()`, `void normalise_stacked_data()`, `void gain_up_acoustic_data()`, `void subtract_noise()`
  Computes complex cross-correlation magnitudes and phase angles from the `A` and `B` stave channels, normalizes multi-ping stacks, applies empirical TVG (`volt_gain_boost`), and subtracts background noise profiles.

### Decimation, Bottom Picking, Slant-Range Correction & Bathymetry
- `void decimate_amplitude_phase_phaseSD()`
  Averages the 20,000 full-rate samples into 512 bins per side (`port_dec_ampl`, `port_dec_phas`, `port_dec_stdv`), weighting phase vectors by amplitude and computing circular phase standard deviation.
- `void pick_first_break()`
  Scans outward from sample 500 to detect the seafloor first-arrival break (`port_break`, `stbd_break`) using sliding-window amplitude thresholds (`port_threshold`, `stbd_threshold`).
- `void do_flat_seafloor_slant_range_corr()`
  Uses the picked towfish altitude to project slant-range bins onto horizontal ground-range pixels (`port_slr_ampl`, `stbd_slr_ampl`).
- `void compress_to_8bit()`
  Quantizes `port_dec_ampl`/`stbd_dec_ampl` and `port_slr_ampl`/`stbd_slr_ampl` into 8-bit unsigned chars in `raw_rec` and `slr_rec`.
- `void first_method_for_topo()`, `void choose_phase_values()`, `void check_for_inversions()`, `void generate_depth_offsets()`, `void put_depths_in_structure()`, `void paint_in_the_depths()`
  Extracts filtered travel times and phase angles between the first bottom arrival and the first surface multiple, converts phase to depression angle via `port_LUT`/`stbd_LUT`, computes `(depth, offset)` soundings, and populates `dep_rec` (`OMG_MR1_zx_rec`).

---

## How It Fits Into the OMG Architecture

`mr1_proc` (together with `mr1_raw` and `OMG_mr1.h`) powers the `MR1toOMG` interactive processing suite, enabling raw Hawaii MR1 interferometric data to be gridded by `weigh_grid` (`OMG_MR1` format in `j_dtm.h`) and mosaicked by OMG sidescan tools.
