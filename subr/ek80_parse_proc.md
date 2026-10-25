---
layout: default
title: ek80_parse_proc
parent: Core Shared Libraries (subr)
module_name: ek80_parse_proc
source_path: code/subr/ek80_parse_proc.c
header_path: code/subr/ek80_parse_proc.h
category: Broadband Echosounder & Split-Beam Signal Processing
related_tools:
  - readEA600
  - EKlook
---

# ek80_parse_proc: Simrad EK80 / EK60 / EA600 Broadband Chirp & Split-Beam Processing Engine

## Overview & Purpose
`ek80_parse_proc` (`ek80_parse_proc.c` / `ek80_parse_proc.h`, ~1,676 lines combined) is a comprehensive parsing and broadband digital signal processing (DSP) library for Kongsberg Simrad EK80 (as well as legacy EK60 and EA600) scientific split-beam echosounders and ADCPs (e.g., EC150, EC300). Stripped out of `readEA600.c` into a standalone `subr/` library by John Hughes Clarke in November 2023 (with updates through 2025/2026), it handles:

1. **XML0 Datagram Parsing (`libxml2`):** Parses `Configuration`, `Environment`, `Parameter`, `PingSequence`, `InitialParameter`, and `Sensor` XML datagrams (`unpack_EK80_xml_param`).
2. **Stage 1 (FPGA) & Stage 2 (PC) Filter Chains:** Stores complex FIR filter coefficients and decimation factors (`ek80_fil`) from `FIL1` datagrams for up to `MAX_NO_EK_TDCRS = 20` transceiver channels.
3. **Synthetic Transmit Pulse & Matched Filter Replication (`maketxpulse_EK80_channel`):** Generates the Hanning-tapered FM chirp (or CW pulse) at the undecimated transceiver clock rate, convolves and decimates it through the Stage 1 and Stage 2 complex filters, takes the time-reversed complex conjugate (`flipcmplxchirp`), and computes its spectral/Frobenius norm for calibrated pulse compression.
4. **Broadband Pulse Compression & Split-Beam Interferometry (`process_EK80_channel`):** Deconvolves (match-filters) the 3 or 4 split-beam quadrant complex $I/Q$ traces (`RAW3`), converts complex voltages into calibrated acoustic power (dB) using transceiver/transducer impedances (`ek80_R_wbt_rx`, `ek80_Ztrd`), and resolves both Fore-Aft (`AngleForAft`) and Port-Starboard (`AnglePorStb`) electrical phase angles.

---

## Key Constants & Data Structures

### Constants & Legacy EK60/EA600 Structures
```c
#define MAX_NO_EK_TDCRS  20           /* Supports up to 20 channels (e.g. 6-freq EK80 + EC150/EC300 ADCP) */
#define MAXEK60TRACELEN  80192        /* Maximum samples per trace */
#define MAXFILTERCOEFFS  2048         /* Max complex coefficients in Stage 1 / Stage 2 FIR filter */
#define EPOCH_DIFF       11644473600LL/* Seconds between 1601-01-01 (Windows FILETIME) and 1970-01-01 (Unix) */
```
* **`ea600_datagram_header`, `ea600_configuration_header`, `ea600_configuration_transducer`, `ea600_sample_datagram`**: Binary structures for legacy Simrad EA600 and EK60 (`CON0`, `RAW0`) datagrams containing 16-bit `Power[8192]` and split-beam `Angle[8192]` arrays.

### EK80 Filter, XML & Trace Structures
* **`ek80_fil`**: Holds `Stage`, `FilterType`, `ChannelID[128]`, `NoOfCoefficients`, `DecimationFactor`, and `fcomplex Coefficients[2048]`. Global instances `EK80_fil1[20]` and `EK80_fil2[20]` store the two cascade filter stages per channel.
* **`ek80_mru`**: Motion Reference Unit record (`dtime`, `heave`, `roll`, `pitch`, `heading`) from `MRU0` datagrams.
* **`ek80_xml_parameters`**: Extracted per-ping XML `Parameter` attributes (`ChannelID`, `ChannelMode`, `PulseForm` [0=CW, 1=FM], `Frequency`, `FrequencyStart`, `FrequencyEnd`, `PulseDuration`, `SampleInterval`, `TransmitPower`, `Slope` [Hanning taper fraction], and `SoundVelocity`).
* **`ek80_raw_header`**: Binary header of a `RAW3` datagram (`ChannelID[128]`, `Datatype` bitmask encoding power/angle/complex16/complex32 and quadrant count in upper byte, `Offset`, and sample `Count`).
* **`ek80_trace`**: Master per-channel processing structure containing `params`, `head`, raw quadrant complex traces `Traces[4]`, match-filtered quadrant traces `TracesMatch[4]`, combined beam sums (`TraceSum`, `PowerSum`, `TraceMatchSum`, `PowerMatchSum`), paired half-beam sums (`TraceMatchFor`, `TraceMatchAft`, `TraceMatchPor`, `TraceMatchStb`), split-beam electrical phase angles (`AnglePorStb`, `AngleForAft`), and the decimated complex conjugate chirp (`cmplxchirp`, `flipcmplxchirp`).

---

## Public Functions & Signatures

### Channel Indexing & XML/RAW3 Parsing
* `int choose_TDCR_WBT(char *ChannelID)`
  Maps an arbitrary 128-byte ASCII `ChannelID` string to a persistent slot `0 .. MAX_NO_EK_TDCRS - 1` in `tdcr_wbt_ID[]`.
* `int unpack_EK80_xml_param(char *rawbytes, int datagramLength, ek80_xml_parameters *next_ek80_params, char *rootname)`
  Parses an `XML0` payload using `libxml2` (`xmlReadFile` / `xmlDocGetRootElement`), identifying the root node (`Configuration`, `Environment`, `Parameter`, `PingSequence`, `InitialParameter`, `Sensor`) and populating `*next_ek80_params` when `<Parameter><Channel .../></Parameter>` is encountered.
* `int unpack_EK80_raw3_channel_header(char *rawbytes, ek80_trace *the_ek80_trace, int verbose)`
  Reads the 140-byte `RAW3` header, verifies `ChannelID` consistency, extracts `noTraces = Datatype >> 8` (1, 3, or 4 sub-beams/quadrants) and sample format (`Datatype & 1` Power, `& 2` Angle, `& 4` ComplexFloat16, `& 8` ComplexFloat32).
* `int unpack_EK80_raw3_channel_traces(char *rawbytes, ek80_trace *the_ek80_trace)`
  Dynamically allocates trace and matched-filter buffers on first sight of a channel, then unpacks either 32-bit float $(I, Q)$ quadrant arrays (`Datatype & 8`) or 16-bit logarithmic power and 8-bit electrical angles (`Datatype & 1` / `& 2`).

### Broadband Matched Filtering & Split-Beam Phase Calculation
* `int maketxpulse_EK80_channel(ek80_trace *the_ek80_trace, int verbose)`
  Synthesizes the ideal transmit chirp at undecimated sampling interval $\Delta t / (D_1 D_2)$ using `make_chirp()`, applies a Hanning taper of fractional width `Slope`, convolves and decimates through `EK80_fil1` and `EK80_fil2` via `cmplx_convolve()`, conjugates and time-reverses the resulting waveform into `flipcmplxchirp`, and computes its normalization factor (`calc_array_norm_squared` / `use_Octave_to_get_l2_norm`).
* `int process_EK80_channel(ek80_trace *the_ek80_trace, int proc_flags)`
  1. Computes the coherent average `TraceSum` across all `noTraces` quadrants and converts it to uncompressed dB power (`PowerSum`) via `calcEK80_volt2power()`.
  2. If matched filtering is enabled (`proc_flags & 1`), convolves each quadrant trace `Traces[qi]` with `whichchirp` using either time-domain `cmplx_convolve()` or fast frequency-domain `cmplx_fft_convolve()` (when `doFFTConv` is set), normalizing by `thel2norm * thel2norm`.
  3. Sums the match-filtered quadrants into `TraceMatchSum` and `PowerMatchSum`.
  4. For 4-quadrant (`ES70-7`, `ES120-7`, `ES200-7`, `ES333-7`) or 3-sector (`ES38-18`, `ES38-7`) split-beam transducers, pairs quadrants into Fore, Aft, Port, and Starboard complex sums and computes `AnglePorStb` and `AngleForAft` via `angle_between_vectors()` (or `Simrad_4_Split` / `Simrad_3_Split`).

---

## How It Fits Into the OMG Architecture
`ek80_parse_proc` is the core processing engine for `readEA600` (`code/knudsen/readEA600.c`) and the interactive broadband split-beam inspection suite `EKlook` (`code/EKlook/EK_funcs.c`), enabling full raw-voltage pulse compression and split-beam target tracking independent of Kongsberg's proprietary software.
