---
layout: default
title: j_knud
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_knud.c
category: Sonar Format I/O (Sub-bottom & Echosounder)
related_tools:
- knud2glo
- k16to8
- kflto8
- xtf2gloria
module_name: j_knud
header_path: code/subr/j_knud.h
---

# `j_knud` — Knudsen 320 / Chirp Sub-Bottom Profiler (`.keb` / `.kea` B9, D3 & E0) Format Library

## Overview & Purpose in the OMG Architecture

`j_knud` (`code/subr/j_knud.c`, `code/subr/j_knud.h`), authored by John E. Hughes Clarke in September 1999 (with additions for D3 and E0 multi-channel formats), defines the binary structures, global state variables, and record-reading/quantization prototypes for **Knudsen Engineering** dual-frequency and 4-channel sub-bottom profiler / echosounder data files (`.keb` binary and `.kea` indexed archives).

Knudsen echosounders (such as the 320B/R and 3260 series) log high-frequency (HF) bathymetric and low-frequency (LF) chirp sub-bottom envelope traces across several generations of binary packet formats:
- **Format `B9`**: Legacy dual-channel (HF/LF) format with embedded attitude, heave, tide, and fix marks.
- **Format `D3`**: 4-channel multiplexed format (`KEL_D3_Channel D3[4]`) with millisecond time tags and AUV depth support.
- **Format `E0`**: Extended 4-channel chirp/analytic waveform format (`KEL_E0_Channel E0[4]`) with windowing filter and TVG metadata.

`j_knud` unifies all three Knudsen packet revisions into a single `KEL_envelope` header and `KEL_data` sample buffer, and provides linear and logarithmic 16-bit to 8-bit dynamic-range compression so sub-bottom traces can be converted into standard OMG GLORIA (`jcu_glo`) or sidescan formats for display and plotting.

---

## Key Data Structures, Constants & Macros

### Constants & Globals (`code/subr/j_knud.h`, `code/subr/j_knud.c`)
- `PACK16_LINEAR` (`0`), `PACK16_LOG` (`1`): Dynamic range compression modes for `collapse_method`.
- `MAX_KNUD_RECLEN` (`16000`), `KNUD_RECLEN` (`1600`): Maximum and nominal sample counts per trace channel.
- **Global Variables**:
  - `int collapse_method`, `isCompressed`: Controls 16-to-8 bit quantization and `.keb` compression state.
  - `int D3_HF`, `D3_LF`, `noD3chan` & `int E0_HF`, `E0_LF`, `noE0chan`: Active high/low frequency channel indices and total channel counts for `D3` and `E0` records.
  - `float min16_LF`, `max16_LF`, `min16_HF`, `max16_HF`: User-configurable 16-bit amplitude clipping thresholds for LF and HF trace conversion.

### Core Structs (`code/subr/j_knud.h`)

- `KEL_preamble`: File header containing `data[40]`, `"KEB"` magic string (`KEB[4]`), `Program[20]`, `Version[20]`, and `Compression[20]`.
- `KEL_record_info` & `KEL_index`: Packet framing (`record_type_code`, `byte_offset`, `record_size`, `event_mark_code`) and `.kea` index entry (`msec_mdnt`, `byte_offset`, `record_code`, `active_chan_code`, `HF_depth`, `LF_depth`).
- `KEL_D3_Channel` & `KEL_E0_Channel`: Per-channel acoustic transceiver settings and bottom-track picks for `D3` and `E0` formats, including nominal/start/stop frequency, bandwidth, sample rate, pulse length (ms), gain mode and dB value, TVG mode, draft, keel offset, start/end depth window, digitized bottom depth (`D3_Digitized_Depth` / `E0_Digitized_Depth`), echo strength, computed heave, and sample count (`Num_Data_Samples`).
- `KEL_envelope`: Master ping header structure combining `B9` fields (timestamp, roll, pitch, heading, boat speed, sound speed, heave, tide, `lat`, `lon`, fix marks, and HF/LF channel parameters) with `KEL_D3_Channel D3[4]` and `KEL_E0_Channel E0[4]` arrays.
- `KEL_data`: Sample storage arrays holding 8-bit (`HF_data`, `LF_data`) and 16-bit (`HF_data16`, `LF_data16`, `D3_data16[4][16000]`, `E0_data16[4][16000]`) time-series trace amplitudes.

---

## Public Functions & Signatures

- `int jK_get_and_read_index(FILE *file, int recno, KEL_index *the_index)` / `int jK_print_index(KEL_index *the_index, int index_no)`
  Reads and prints a random-access `KEL_index` entry from a Knudsen index file.
- `int jK_get_and_read_record_info(FILE *file, KEL_record_info *rec_info)` / `int jK_print_record_info(KEL_record_info *rec_info, int record_no)`
  Reads and prints the framing header (`KEL_record_info`) preceding a Knudsen data record.
- `int jK_get_and_read_record_B9(FILE *file, KEL_envelope *envelope, KEL_data *kdata, KEL_index *the_index, int recno, int verbose_flag, int ignore_no_bytes, char *uncompdata)`
  Reads and unpacks a `B9` format dual-frequency ping record and its HF/LF sample traces.
- `int jK_get_and_read_record_D3(...)` & `int jK_get_and_read_record_E0(...)`
  Reads and unpacks 4-channel `D3` and `E0` format Knudsen ping headers and 16-bit sample arrays (`D3_data16`, `E0_data16`).
- `int jK_collapse_16_to_8(unsigned short *data16, unsigned char *data8, int novals, float min16, float max16, int method)`
  Compresses unsigned 16-bit acoustic envelope samples into 8-bit (`0..255`) display intensities using either linear scaling (`PACK16_LINEAR`) or logarithmic dB scaling (`PACK16_LOG`) between `[min16, max16]`.
- `int jK_collapse_16_to_8_signed(signed short *data16, unsigned char *data8, int novals, float min16, float max16, int method)`
  Signed 16-bit variant of `jK_collapse_16_to_8` for bipolar/analytic waveform traces.

---

## How It Fits Into the OMG Architecture

`j_knud` is used by the Knudsen sub-bottom conversion tools in `code/knudsen/` (`knud2glo`, `k16to8`, `kflto8`) and `code/xtf/xtf2gloria` to convert raw Knudsen `.keb` profiles into OMG image and GLORIA (`jcu_glo`) records for seismic curtain visualization and horizon picking.
