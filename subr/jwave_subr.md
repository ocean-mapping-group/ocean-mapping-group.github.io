---
layout: default
title: jwave_subr
parent: Core Shared Libraries (subr)
module_name: jwave_subr
source_path: code/subr/jwave_subr.c
header_path: code/subr/jwave_subr.h
category: Acoustic Waveform & Audio I/O
related_tools:
  - readWave
  - waveform slicing & conversion utilities
---

# `jwave_subr` — RIFF WAVE Header & 16-Bit PCM Body Reader/Writer Library

## Overview & Purpose in the OMG Architecture

`jwave_subr` (`code/subr/jwave_subr.c`, `code/subr/jwave_subr.h`), written by John E. Hughes Clarke in March 2019, provides straightforward C functions for reading and writing both the 44-byte **RIFF WAVE header** and the **16-bit signed PCM sample payload** of `.wav` acoustic waveform files.

Unlike `j_wav_io` (written a year later in February 2020, which links against Linux ALSA `<alsa/asoundlib.h>` for sound card playback), `jwave_subr` has **no external audio library dependencies** and includes dedicated payload functions (`read_in_wave_body`, `write_out_wave_body`) for reading the entire sample buffer into memory or appending sample slices to an output `.wav` file.

---

## Key Data Structures & Globals (`code/subr/jwave_subr.h`)

### `Wave_str` (and global instance `Wave_str waveStr`)
```c
typedef struct {
    char  riff_head[5];   /* "RIFF" chunk descriptor (null-terminated in memory) */
    int   size;           /* Overall chunk size (file size - 8 bytes)            */
    char  wave_head[5];   /* "WAVE" format identifier                            */
    char  fmt_head[5];    /* "fmt " subchunk identifier                          */

    int   Subchunk1Size;  /* Format subchunk size (16 for linear PCM)            */
    short AudioFormat;    /* Audio format (1 = uncompressed PCM)                 */
    short NumChannels;    /* Number of channels (1 = mono, 2 = stereo)           */
    int   SampleRate;     /* Sampling frequency in Hz                            */
    int   ByteRate;       /* SampleRate * NumChannels * (BitsPerSample / 8)      */
    short BlockAlign;     /* NumChannels * (BitsPerSample / 8)                   */
    short BitsPerSample;  /* Bits per sample (e.g., 16)                          */

    char  data_head[5];   /* "data" subchunk identifier                          */
    int   Subchunk2Size;  /* Byte length of the raw sample data payload          */

    /* Derived runtime fields (not written to disk): */
    int   nosamples;      /* Total samples = Subchunk2Size / (BitsPerSample / 8) */
    float noseconds;      /* Duration in seconds = nosamples / SampleRate        */
} Wave_str;
```

---

## Public Functions & Signatures

### WAVE Header I/O
- `int read_in_wave_head(FILE *infile, Wave_str *waveStr, int verbose)`
  Seeks to the beginning of `infile` (`offset 0`), reads and validates the `"RIFF"`, `"WAVE"`, `"fmt "`, and `"data"` chunk identifiers, reads each format parameter (`Subchunk1Size`, `AudioFormat`, `NumChannels`, `SampleRate`, `ByteRate`, `BlockAlign`, `BitsPerSample`, `Subchunk2Size`) directly into `waveStr`, and computes `waveStr->nosamples` and `waveStr->noseconds`. Returns `0` to `stderr` if any chunk magic string is invalid.
- `int write_out_wave_head(FILE *outfile, Wave_str *waveStr, int verbose)`
  Seeks to `offset 0` of `outfile` and writes all 44 bytes of the RIFF/WAVE header fields from `waveStr`.

### WAVE Sample Payload I/O
- `int read_in_wave_body(FILE *infile, Wave_str *waveStr, short *data)`
  Seeks past the 44-byte header (`fseek(infile, 44, 0)`), verifies that the caller-supplied `data` pointer is non-null (calling `error()` from `support.h` if unallocated), and reads `waveStr->nosamples * sizeof(signed short)` bytes of 16-bit PCM waveform samples into `data`.
- `int write_out_wave_body(FILE *outfile, Wave_str *waveStr, short *data, int sam_offset, int nosams)`
  Seeks to the end of `outfile` (`fseek(outfile, 0, 2)`) and appends `nosams * (waveStr->BitsPerSample / 8)` bytes of waveform data from `data`.

---

## How It Fits Into the OMG Architecture

`jwave_subr` is used by standalone acoustic waveform slicing, filtering, and format conversion utilities in the OMG repository that manipulate `.wav` files without requiring ALSA sound-card headers.
