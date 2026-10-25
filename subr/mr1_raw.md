---
layout: default
title: mr1_raw
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/mr1_raw.c
category: Sonar Format I/O & Interferometric Processing (MR1)
related_tools:
- MR1toOMG
- mr1_proc
module_name: mr1_raw
header_path: code/subr/mr1_raw.h
---

# `mr1_raw` — HIG Hawaii MR1 Raw Packet Structures, Quadrature Phase & TVG Math Library

## Overview & Purpose in the OMG Architecture

`mr1_raw` (`code/subr/mr1_raw.c`, `code/subr/mr1_raw.h`), written by John E. Hughes Clarke in March 1992 aboard R/V *Moana Wave* (adapted with permission from Hawaii Mapping Research Group / Sandy Shor's `xvgr` code), defines the low-level binary packet and ping header structures (`HDR`, `PING_VALS`, `TOP_VALS`, `packet`, `raw_samp`, `out_samp`) for raw **Hawaii MR1** towed interferometric sidescan data, along with complex quadrature (`I/Q`) amplitude/phase mathematics and Time-Varying Gain (TVG) spreading/absorption lookup tables.

---

## Key Data Structures & Globals (`code/subr/mr1_raw.h`)

### Quadrature Sample & Packet Structs
- `fcomplex`: Floating-point complex number `{ float r, i; }` (in-phase real `r` and quadrature imaginary `i`).
- `out_samp`: Dual-stave unpacked complex sample `{ fcomplex A, B; }` representing upper (`A`) and lower (`B`) receiver stave pairs.
- `raw_samp`: Raw 16-bit integer quadrature sample `{ short ar, br, ai, bi; }` as logged by the MR1 hardware.
- `packet`: Raw 64-sample acoustic telemetry packet:

  ```c
  typedef struct {
      short seq_no;        /* Odd = Port, Even = Starboard           */
      short expon;         /* Binary exponent scale factor (2^expon) */
      raw_samp raw[64];    /* 64 quadrature A/B samples              */
  } packet;
  ```

### Ping Header Structs (`PING_VALS`, `TOP_VALS`, `HDR`)
- `PING_VALS`: Per-side hardware acquisition settings (`filter_samps_to_next_go`, `filter_loop_length`, `start_pkt_seq_no`, `cap_chg_pwr_setting`, `diag_pwr_nsamps`, `ping_ncycles`).
- `TOP_VALS`: Topside trigger and transceiver flags (`ext_trigger_flag`, `ping_interval_secs`, `rcvrs_on_flag`, `xmtrs_on_flag`).
- `HDR`: Master ping header combining `PING_VALS pv[2]` (port/stbd), `TOP_VALS t`, Unix timestamp (`time_secs`, `time_musec`), byte offsets (`port_pwr_offset`, `stbd_pwr_offset`, `acoustic_data_offset`, `attitude_off`, `ping_buf_size`), and physical sampling metadata (`ping_delay`, `port_stbd_separation`, `port_sample_rate`, `stbd_sample_rate`, `fish_depth`, `port_pulse_len`, `stbd_pulse_len`, `port_sample_interval`, `stbd_sample_interval`).

### Global Lookup Tables
- `float expons[256]`: Precomputed powers of two ($2^0, 2^1, \dots, 2^{255}$) used to scale `raw_samp` integers by `packet.expon`.
- `float volt_gain_boost[500]`: Per-packet TVG voltage gain multiplier table up to 15,000 m slant range.

---

## Public Functions & Signatures

### Quadrature Amplitude, Phase & Cross-Correlation Math
- `double get_amplitude(short real, short imag)` & `double Rfl_get_amplitude(float real, float imag)`
  Computes the complex envelope magnitude $\sqrt{\text{real}^2 + \text{imag}^2}$ from 16-bit integer or floating-point `I/Q` components.
- `double get_phase(short real, short imag)` & `double Rfl_get_phase(float real, float imag)`
  Computes the 4-quadrant phase angle in degrees $[0^\circ, 360^\circ)$ from `real` and `imag`.
- `double get_phase_lag(raw_samp raw)` & `double Rfl_get_phase_lag(out_samp raw)`
  Computes the differential interferometric phase angle $\Delta\phi = \phi_A - \phi_B$ wrapped into $(-180^\circ, +180^\circ]$ between stave `A` and stave `B`.
- `void get_cmplxXcorr(out_samp raw, float *magnitude, float *phase_lag)`
  Computes the complex conjugate cross-product $A \cdot B^* = (A_r B_r + A_i B_i) + i(A_i B_r - A_r B_i)$ and extracts the fourth-root cross-correlation `magnitude` and differential `phase_lag` in degrees $(-180^\circ, +180^\circ]$.

### Acoustic Attenuation, TVG Tables & Diagnostics
- `double range_decay(double slant_range)`
  Computes the theoretical two-way spherical spreading and absorption voltage decay factor:
  $$\sqrt{\frac{\exp(-2 \alpha R)}{4\pi R^4}}$$
  using `absorp_coeff = 0.00015` nepers/m.
- `void exp_fill()`
  Populates `expons[0..255]` with $2^i$ (`expons[0] = 1.0`, `expons[i] = 2.0 * expons[i-1]`).
- `void spread_table(int data_period)`
  Populates `volt_gain_boost[]` as a function of packet number (`tdel = data_period * 64` $\mu\text{s}$) out to a 15 km breakpoint using a $30\log_{10}(R/R_0)$ spreading law and $1.5\text{ dB/km}$ two-way absorption coefficient.
- `void printf_header_data(HDR *head)`
  Prints a formatted diagnostic report of all port/starboard `PING_VALS`, `TOP_VALS`, and `HDR` fields to `stdout`.

---

## How It Fits Into the OMG Architecture

`mr1_raw` is the low-level companion to `mr1_proc`, providing the raw packet definitions, `expons[]` scaling table, `volt_gain_boost[]` TVG curve, and complex `I/Q` phase-difference math required by `MR1toOMG`.
