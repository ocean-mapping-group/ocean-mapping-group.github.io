---
layout: default
title: j_wav_io
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_wav_io.c
category: Acoustic Waveform & Audio I/O
related_tools:
- readWave
- hydrophone / acoustic playback tools
module_name: j_wav_io
header_path: code/subr/j_wav_io.h
---

# `j_wav_io` — RIFF WAVE Audio File I/O, Timestamping & ALSA Playback Library

## Overview & Purpose in the OMG Architecture

`j_wav_io` (`code/subr/j_wav_io.c`, `code/subr/j_wav_io.h`), authored by John E. Hughes Clarke in February 2020 (evolving from `readWave.c` in June 2018 and `jwave_subr.c` in March 2019), provides header parsing, writing, external epoch timestamp synchronization (`.wav.datetime`), and direct Linux **ALSA (`libasound`) hardware audio playback** for uncompressed RIFF `.wav` acoustic recordings.

In underwater acoustic experiments, hydrophone arrays and raw sonar stave recorders often store time-series acoustic pressure data in standard RIFF WAVE files alongside a companion `.wav.datetime` file that records the exact UTC start and end Unix epoch timestamps (`1970` seconds). `j_wav_io` reads and writes the 44-byte RIFF/WAVE header, ingests the companion `.wav.datetime` timing file, and interfaces directly with `<alsa/asoundlib.h>` (`snd_pcm_open`, `snd_pcm_set_params`, `snd_pcm_writei`) so interactive OMG tools can play raw acoustic pings or hydrophone recordings through the workstation sound card.

---

## Key Data Structures & Globals (`code/subr/j_wav_io.h`)

### `Wave_str`
Represents the 44-byte RIFF WAVE header along with derived duration and external UTC timing metadata:
- **RIFF & Format Chunk Fields**:
  - `char riff_head[5]`: Null-terminated `"RIFF"` identifier.
  - `int size`: Total RIFF chunk byte size.
  - `char wave_head[5]`: Null-terminated `"WAVE"` identifier.
  - `char fmt_head[5]`: Null-terminated `"fmt "` identifier.
  - `char bytes20[20]`: Raw 20-byte buffer holding the unpacked format subchunk fields:
    - `int Subchunk1Size`: Size of the format chunk (typically 16 for PCM).
    - `short AudioFormat`: Audio format code (`1` = uncompressed linear PCM).
    - `short NumChannels`: Number of interleaved channels (`1` = mono, `2` = stereo).
    - `int SampleRate`: Sampling frequency in Hz.
    - `int ByteRate`: `SampleRate * NumChannels * (BitsPerSample / 8)`.
    - `short BlockAlign`: `NumChannels * (BitsPerSample / 8)`.
    - `short BitsPerSample`: Bit depth (`8`, `16`, `24`, or `32`).
- **Data Chunk Fields**:
  - `char data_head[5]`: Null-terminated `"data"` identifier.
  - `int Subchunk2Size`: Total byte length of the raw PCM sample payload.
- **Derived & External Timing Fields**:
  - `int nosamples`: Total number of sample frames (`size / ((BitsPerSample / 8) * NumChannels)`).
  - `float noseconds`: Total recording duration in seconds (`nosamples / SampleRate`).
  - `double fstarttime`, `fend__time`: Start and end timestamps (seconds since 1970) read from `<prefix>.wav.datetime`.

### ALSA Audio Playback Globals
- `static const char SoundCardPortName[] = "default"`: Target ALSA PCM playback device name.
- `snd_pcm_t *PlaybackHandle`: ALSA PCM stream handle.
- `int audio_open`: State counter (`0` = closed, `1` = device opened, `2` = hardware parameters configured).

---

## Public Functions & Signatures

### WAV Header & Timestamp File I/O
- `int j_read_wav_header(FILE *file, Wave_str *waveStr, int verbose)`
  Reads and validates the 44-byte RIFF WAVE header (`"RIFF"`, `"WAVE"`, `"fmt "`, `"data"`), unpacks the 20-byte format chunk into `waveStr`, and computes `nosamples` and `noseconds`. Returns `1` on valid WAVE header or `0` on format mismatch.
- `int j_write_wav_header(FILE *file, Wave_str *waveStr, int verbose)`
  Writes the 44-byte RIFF WAVE header (`riff_head`, `size`, `wave_head`, `fmt_head`, `bytes20`, `data_head`, `Subchunk2Size`) to `file`.
- `int j_read_wav_datetime(char *name, Wave_str *waveStr, int verbose)`
  Opens a custom two-line `.wav.datetime` sidecar file (`name`) using `getc_line()` (`support.h`) and extracts `waveStr->fstarttime` (from line 0) and `waveStr->fend__time` (from line 1). If the file cannot be opened, issues a `warning()` and defaults `fstarttime = 0.0` and `fend__time = waveStr->noseconds`.

### ALSA Sound Card Playback Functions
- `int open_audio(Wave_str *waveStr)`
  Opens the `"default"` ALSA PCM playback device (`snd_pcm_open`), maps `waveStr->BitsPerSample` (`8`, `16`, `24`, `32`) to the corresponding `SND_PCM_FORMAT_*` enum, and configures interleaved playback at `waveStr->NumChannels` and `waveStr->SampleRate` with a 500,000 $\mu\text{s}$ latency buffer (`snd_pcm_set_params`). Returns `audio_open` (`2` when ready).
- `int play_audio(signed short *data, int nosams)`
  Writes `nosams` 16-bit audio frames to `PlaybackHandle` via `snd_pcm_writei()` and re-prepares the stream (`snd_pcm_prepare()`).
- `int close_audio()`
  Closes `PlaybackHandle` via `snd_pcm_close()` if `audio_open` is non-zero.

---

## How It Fits Into the OMG Architecture

`j_wav_io` extends the basic `.wav` file reader in `jwave_subr` by adding UTC epoch timestamp synchronization (`j_read_wav_datetime`) and real-time ALSA audio output (`open_audio`, `play_audio`, `close_audio`) for interactive acoustic waveform inspection utilities.
