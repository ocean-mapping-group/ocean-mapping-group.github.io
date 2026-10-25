---
layout: default
title: Acoustic WAV Processing (Wave)
nav_order: 32
has_children: true
---

# Passive Acoustic & Hydrophone WAV Processing (`Wave`)

The `Wave` directory contains utilities for time-windowing, gain-scaling, and spectral analysis of 16-bit PCM RIFF/WAVE (`.wav`) hydrophone and underwater acoustic recordings.

---

## Tools in `Wave/`

* [`extractWaveWindow`](extractWaveWindow.md) — Splices and concatenates a specified UTC time window across multiple timestamped `.wav` files (using companion `.wav.datetime` sidecars and [`jwave_subr`](../subr/jwave_subr.md)) into a single contiguous `.wav` file with optional linear gain scaling.
* [`readWave`](readWave.md) — Standalone RIFF/WAVE reader, time-subset extractor, Hanning-windowed radix-2 FFT spectrogram generator (`-spec`), synthetic harmonic test-signal generator (`-test_signal`, `-test_hf_signal`), and gain-booster (`-wavout -gainout`).
