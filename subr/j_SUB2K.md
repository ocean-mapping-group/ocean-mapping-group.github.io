---
layout: default
title: j_SUB2K
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_SUB2K.c
category: Sonar Format I/O & Interferometric Processing
related_tools:
- SUB2KtoOMG
- SwathPlus converters
- weigh_grid
- jview
module_name: j_SUB2K
header_path: code/subr/j_SUB2K.h
---

# `j_SUB2K` — Submetrix 2000 & SEA SWATHplus Interferometric Sonar Processing Library

## Overview & Purpose in the OMG Architecture

`j_SUB2K` (`code/subr/j_SUB2K.c`, `code/subr/j_SUB2K.h`), authored by John E. Hughes Clarke (May 1999, with subsequent updates by Bill Danforth and Jonathan Beaudoin through 2008), implements the complete binary packet parser, multi-row phase-differencing interferometric processor, lookup-table (LUT) angle resolver, spatial bin filter, and OMG_HDCS converter for **Submetrix Series 2000** and **SEA SWATHplus** (`.sxr`, `.sxp`, `.sxi`) bathymetric sidescan systems.

Because Submetrix / SWATHplus sonars measure raw phase differences across multiple receiver staves (`AB`, `AC`, `AD`) at high sample rates rather than forming discrete beams in hardware, `j_SUB2K` provides both raw packet I/O and the full signal-processing chain required to resolve phase wraps, convert stave phase differences into physical depression angles (`prangs`), filter outliers via cross-track/depth spatial binning and tracking gates, and output standard `OMG_HDCS` bathymetry, attitude, navigation, and sidescan trace files.

---

## Key Data Structures, Constants & Macros

### Navigation & MRU Configuration Macros
- `NFOR_UTM` (`0`), `NFOR_GGA` (`1`), `NFOR_RMC` (`2`): Selects how embedded GPS strings inside `0x0a` blocks are parsed (projected UTM vs. NMEA `$GPGGA` / `$GPRMC` telegrams via `jNMEA`).
- `TSS_MRU` (`1`), `F180_MRU` (`2`), `F180_MCOM` (`3`): Specifies the motion reference unit packet format (TSS, Coda Octopus F180, or TSS/Simrad MCOM).
- `SUBX_PORT` (`0`), `SUBX_STBD` (`1`), `SUBX_UNASSIGNED` (`99`): Transducer side identifiers.
- `MAX_SAMS` (`8192`): Maximum time-series samples per ping trace.
- `MAX_BINS_PER_SIDE` (`512`): Maximum cross-track spatial bins per side for gridded phase-bathymetry reduction.
- `DESIGN_NOMINAL_SOUND_SPEED` (`1490.0`), `DESIGN_SSV` (`1460.0`): Baseline design sound speeds (m/s) for stave wavelength spacing calculations.

### Core Structs (`code/subr/j_SUB2K.h`)
- `BathyIO` & `BathyIO2`: Raw sonar ping headers for legacy Submetrix 2000 (`0x00`) and SWATHplus v3 (`0x16`) SXR blocks, storing ping number, transducer channel, FPGA ID, operating frequency, hardware gain, phase clock scale, transmit power, pulse length, sample count, sample interval, and timestamps (`sec`/`usec`).
- `TxBoardInfo`: Per-channel hardware configuration (`tdcrtype`, `ctrlreg`, `txcycles`, `rxsamps`, `rxrate`, `analch`).
- `BathySample`: Individual raw interferometric sample containing stave phase differences (`ab`, `ac`, `ad`), transducer number (`txno`), amplitude bytes (`samp0`, `samp1`, `anal0`, `anal1`), sample index (`sampNumber`), and 16-bit `rawAmplitude`.
- `cXYZAPing`, `cXYZATxer`, `cXYZAPoint`, `CPosn`, `CPosnOffset`: Data structures for pre-processed SXP/SXI (`0x28`, `0x29`) XYZA point clouds, transducer mounting offsets, and ping-level attitude/tide/sound speed metadata.
- `GPSdata` & `MRUdata`: Parsed navigation (`sec`, `usec`, `northing`, `easting`, `lat`, `lon`, `merid`, `elevation`) and motion sensor (`raw_depth`, `compass`, `roll`, `pitch`, `heading`, `rolldot`, `pitchdot`, `height`, `heightdot`, `lateral_disp`, `axial_disp`) records.

---

## Public Functions & Signatures

### File Management & Block Synchronization
- `void open_SUBX_files(char *inname, char *omgname)` / `void close_SUBX_files()`
  Opens the input Submetrix/SWATHplus file and initializes output OMG HDCS swath (`omgfile`), navigation (`navfile`, `anvfile`), attitude (`mrufile`), and sidescan (`sssfile`, `sstfile`, `rawAfile`, `rawPfile`) streams.
- `void search_for_ping_start(FILE *file, int *block_type, int *block_size, int *ateof)`
  Scans the binary stream byte-by-byte to synchronize on valid packet identifiers (`0x00` raw sonar, `0x16` v3 raw sonar, `0x09` MRU, `0x0a` GPS, `0x0b` XYZA, `0x0d` PhaseCal, `0x28` proc data, `0x29`–`0x31` SXI blocks) and validates block sizes.
- `void handle_SUBX_block()`
  Dispatches the current block buffer to the appropriate packet parser based on `block_type`.

### Packet Parsers (SXR, SXP, SXI)
- `void parse_sonar_block(char *data)` / `void parse_sonar_block2(char *data)`
  Unpacks raw v1/v2 (`BathyIO`) and v3 (`BathyIO2`) SXR sonar records, demultiplexes stave phase arrays (`abphase`, `acphase`, `adphase`) and 16-bit amplitudes, and invokes `handle_raw_sonar_data()`.
- `void parse_proc_block(char *data)`
  Parses processed SXP (`0x28`) blocks containing `cXYZAPing`, `cXYZATxer`, and `cXYZAPoint` soundings.
- `int parse_GPS_block(char *data, int blocksize)` / `void parse_MRU_block(char *data, int blocksize)`
  Extracts timestamps, decodes UTM or NMEA GGA/RMC coordinates, and unpacks TSS, F180, or Simrad EM attitude packets.
- `void parse_parsed_ping_data_block(char *data)`, `void parse_parsed_attitude_block(char *data)`, `void parse_parsed_position_ll(char *data)`
  Decodes SXI (`0x29`, `0x2b`, `0x2c`) processed format records.

### Interferometric Phase-to-Angle & Bathymetric Binning
- `void calc_row_spacings()`, `void prime_IQ()`, `void prime_Alignments()`, `void prime_LUTs()`
  Initializes stave spacing ratios (`PORT_AB`, `PORT_AC`, `PORT_AD`, `STBD_AB`, etc.) and precomputes 3D phase-to-angle lookup tables (`AB_prang_LUT`, `AC_prang_LUT`, `AD_prang_LUT`) across all viable phase wraps.
- `void build_LUT(float separation, float prang_LUT[256][20], int *viable_wraps, int nowraps[20])`
  Populates a 256-phase by 20-wrap lookup table of physical arrival angles for a given stave separation.
- `void likely_angle(int AB, int AC, int AD, float *angle, float *maxdiff)` & `void guess_likely_angles(int rxsamps, unsigned char *ab, unsigned char *ac, unsigned char *ad, float *angles, float *angdiff)`
  Vernier phase unwrapping resolver: compares candidate angles across the `AB`, `AC`, and `AD` stave pairs (or invokes `OMGmod_SEA_phasetoangle`) to select the wrap combination with minimal angular discrepancy (`maxdiff`).
- `void filt_phase(int nosams, int runav, unsigned char *ampl, unsigned char *pin, unsigned char *pout)`
  Applies an amplitude-weighted circular running-average filter to raw 8-bit stave phases before angle resolution.
- `int constrained_bpick(int firstsam, int lastsam, int athresh, int nobelow, int oftotal, unsigned char *ampl)`
  Detects the first bottom return (nadir altitude pick) from the amplitude trace using a sliding window threshold.
- `void make_depths(int rxsamps, float *prangs, float *depths, float *across)`
  Converts slant ranges (sample times) and resolved angles (`prangs`), adjusted for roll and surface sound speed refraction, into `(depths, across)` coordinates.
- `void build_bins(int rxsamps, float *depths, float *across)`, `void search_bins()`, `void calc_gates()`, `void get_depths_in_gates(int rxsamps, float *depths, float *across)`
  Accumulates `(depth, across)` samples into a 2D spatial histogram (`dep_across_bins`), locates peak density bins per cross-track column, establishes shallow/deep tracking gates (`gate_shal`, `gate_deep`), and computes mean depth, across-track distance, and variance within each gate.
- `void filt_pr_depths(int halfwidth, int start, int stop, float median_fraction_of_depth)`
  Applies a cross-track median filter to reject outlier binned soundings.
- `void get_ll_values()`
  Applies full 3D lever-arm and DCM attitude rotation (`jDCM_unrotatef`) to convert sonar-relative binned soundings into local-level (`ll_depth`, `ll_across`, `ll_along`) coordinates.
- `void write_out_swath()`, `void write_out_ss(int mode)`, `void write_out_nav()`, `void write_out_mru()`, `void write_out_sss()`
  Writes the processed `OMG_HDCS` profile headers, beams, sidescan time series, navigation fixes, and attitude records to disk.

---

## How It Fits Into the OMG Architecture

`j_SUB2K` is the core engine behind the Submetrix/SWATHplus ingestion utilities in `code/submetrix/` (such as `SUB2KtoOMG` and interactive phase/bin diagnostic viewers). By translating raw interferometric stave phases and auxiliary sensor blocks directly into `OMG_HDCS` summary/profile files (`.merged`), `.nav`, `.mru`, and `.ss_data` files, it enables downstream OMG tools (`mergeAtt`, `weigh_grid`, `makess`, `jview`, `swathEd`) to grid and mosaic interferometric sidescan data identically to conventional multibeam echosounders.
