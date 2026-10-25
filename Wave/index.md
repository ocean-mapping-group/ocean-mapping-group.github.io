---
layout: default
title: Acoustic WAV Waveform Tools (Wave)
parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 3
has_children: true
---

# Passive Acoustic & Hydrophone WAV Processing (`Wave`)

The `Wave` directory contains utilities for time-windowing, gain-scaling, and spectral analysis of 16-bit PCM RIFF/WAVE (`.wav`) hydrophone and underwater acoustic recordings.

---

## Tools in `Wave/`

* [`extractWaveWindow`](extractWaveWindow.html) — Splices and concatenates a specified UTC time window across multiple timestamped `.wav` files (using companion `.wav.datetime` sidecars and [`jwave_subr`](../subr/jwave_subr.html)) into a single contiguous `.wav` file with optional linear gain scaling.
* [`readWave`](readWave.html) — Standalone RIFF/WAVE reader, time-subset extractor, Hanning-windowed radix-2 FFT spectrogram generator (`-spec`), synthetic harmonic test-signal generator (`-test_signal`, `-test_hf_signal`), and gain-booster (`-wavout -gainout`).
