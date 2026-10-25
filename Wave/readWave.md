---
layout: default
title: readWave
parent: Acoustic WAV Processing (Wave)
tool_name: readWave
source_path: code/Wave/readWave.c
category: Passive Acoustics & Hydrophone WAV Processing
input_formats: [".wav (RIFF/WAVE 16-bit PCM)"]
output_formats: [".spec (binary float FFT power spectra)", ".wav (gain-adjusted/subsetted RIFF/WAVE)"]
related_tools: ["extractWaveWindow", "jwave_subr", "four1"]
---

# readWave

## Overview
`readWave` (`code/Wave/readWave.c`, written by John E. Hughes Clarke, June 18, 2018) is a standalone, zero-dependency C utility for parsing 16-bit PCM RIFF/WAVE (`.wav`) hydrophone and acoustic recordings, extracting time-window subsets (`-subset_seconds` / `-subset_offset`), applying Hanning cosine tapers (`-perc_taper`), computing sliding-window Fast Fourier Transform (FFT) power spectra in dB (`-spec`), and writing gain-boosted output `.wav` files (`-wavout` / `-gainout`).

To remain completely self-contained without linking against external OMG libraries, `readWave.c` embeds its own RIFF/WAVE header parser (`Wave_str`), Hanning window generator (`build_weights`), and Numerical Recipes radix-2 1D complex FFT (`four1`).

---

## Usage

```bash
# Compute FFT spectrogram and write gain-boosted WAV subset
readWave -ins recording1.wav [recording2.wav ...] \
  -out summary.out \
  [-spec spectrogram.bin] [-fftsize 8192] [-perc_taper 16.67] \
  [-subset_offset 600 -subset_seconds 30] \
  [-wavout boosted.wav -gainout 100.0]
```

---

## Command-Line Arguments

| Option | Description | Default |
|---|---|---|
| `-ins <wav1> [wav2 ...]` | **Required.** One or more input 16-bit PCM `.wav` files (up to 1,000 files). | None |
| `-out <outfile>` | **Required.** Output summary/log file path. | None |
| `-spec <specfile>` | Compute 1D FFT power spectra (`10 * log10(Power)`) for each 10,000-sample chunk (`MAX_CHUNK`) and write binary `float` half-spectra (`(Num/2) * sizeof(float)`) to `<specfile>`. | Disabled |
| `-fftsize <pow2>` | FFT length (power of 2). Note: `readWave` automatically selects the largest power of 2 less than `MAX_CHUNK` (`Num = 8192` for `MAX_CHUNK = 10000`). | `8192` |
| `-perc_taper <pct>` | Apply a cosine (Hanning) taper across the leading and trailing `<pct>`% of each sample window before FFT calculation (`build_weights`). | `16.67`% (`100/6`) when enabled |
| `-subset_offset <sec>` | Start time offset in seconds from the beginning of the `.wav` stream for subsetting. Must be paired with `-subset_seconds`. | Full file |
| `-subset_seconds <sec>` | Duration in seconds of the extracted subset window. Must be paired with `-subset_offset`. | Full file |
| `-wavout <out.wav>` | Write a new RIFF/WAVE file containing the gain-scaled (and optionally time-subsetted) 16-bit PCM audio. | Disabled |
| `-gainout <mult>` | Linear gain multiplier applied to 16-bit PCM samples written to `-wavout` (clamped to `[-32768, +32767]`). | `100.0` |
| `-test_signal` | Replace input audio samples with a synthetic 4-harmonic test signal ($5 + 10 + 15 + 20\text{ kHz}$ sine waves) to verify FFT frequency calibration. | Disabled |
| `-test_hf_signal` | Replace input audio samples with a synthetic multi-harmonic high-frequency comb ($5\text{ kHz}$ to $90\text{ kHz}$ in $5\text{ kHz}$ steps). | Disabled |
| `-v` | Verbose mode: prints individual sample values and chunk counters. | Disabled |

---

## Internal Data Structures & Functions

* **`Wave_str`:** 44-byte RIFF/WAVE header layout (`riff_head="RIFF"`, `size`, `wave_head="WAVE"`, `fmt_head="fmt "`, `Subchunk1Size`, `AudioFormat`, `NumChannels`, `SampleRate`, `ByteRate`, `BlockAlign`, `BitsPerSample`, `data_head="data"`, `Subchunk2Size`).
* **`do_the_fft()`:** Centers `fftsams` ($2^{13} = 8192$) samples inside the `nosams` ($10000$) chunk, packs real samples into complex interleaved array `intofft`, invokes `four1(intofft - 1, fftsams, 1)`, and computes magnitude in dB:
  $$P_k = 10 \log_{10}\left(\sqrt{\text{Re}_k^2 + \text{Im}_k^2}\right)$$
* **`build_weights()`:** Constructs a raised-cosine Hanning taper over the leading and trailing `frac_tapered = ptaper / 100.0` fraction of each block.
