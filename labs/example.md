---
layout: default
title: example
parent: labs (Teaching & Coursework Labs)
nav_order: 2
tool_name: example
source_path: code/labs/example.c
category: Educational Labs & Acoustic Signal Processing (labs)
input_formats:
  - ASCII 2-column time-series files (time, amplitude)
output_formats:
  - ASCII 2-column time-series file (time, amplitude)
related_tools:
  - testChirp
  - testNormConv
  - EM_unpack
  - mkbp
---

# example

## Overview
`example` (`code/labs/example.c`, authored by John Hughes Clarke in February 2001) is an educational C program template used in Ocean Mapping Group (OMG) acoustic signal processing labs. It provides the file I/O, command-line argument parsing, and array storage scaffolding for performing discrete 1D time-domain convolution between a transmitted sonar pulse waveform (`-pulse`) and a seabed/target impulse response series (`-impul`).

Students are given `example.c` with a stub function `doconv(float *x, float *h, int range)` and tasked with implementing linear convolution or matched-filter cross-correlation while properly handling array boundary conditions at the start and end of the time series.

---

## Syntax & CLI Options

```bash
example [-v] [-depth <val>] -pulse <pulse.ascii> -impul <impulse.ascii> -out <result.ascii>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-pulse <filename>` | **Required.** Input 2-column ASCII file containing the transmit pulse time series (`pulse[0][i]` = time, `pulse[1][i]` = amplitude; up to 10,000 samples). | None |
| `-impul <filename>` | **Required.** Input 2-column ASCII file containing the target impulse response time series (`impulse[0][i]` = time, `impulse[1][i]` = reflection coefficient; up to 10,000 samples). | None |
| `-out <filename>` | **Required.** Output 2-column ASCII file where the processed time series is written for plotting. | None |
| `-depth <meters>` | Example numeric parameter parsed via `atof()` (`entered depth value %f`). | `10.0` |
| `-v` | Enable verbose output (`verbose_flag++`). | `0` |

---

## Mathematical & Signal Processing Formulation

### 1. Input Time-Series Representation
The program allocates three static 2D floating-point arrays capable of holding up to `10,000` samples each:
* `float pulse[2][10000]`: Stores time $t_k$ in `pulse[0][k]` and transmit waveform amplitude $h[k]$ in `pulse[1][k]` for $0 \le k < N_{\text{pulse}}$ (`no_pulse_samples`).
* `float impulse[2][10000]`: Stores time $t_n$ in `impulse[0][n]` and target reflection impulse series $x[n]$ in `impulse[1][n]` for $0 \le n < N_{\text{impulse}}$ (`no_impulse_samples`).
* `float result[2][10000]`: Pre-allocated buffer for storing the convolved output waveform $y[n]$.

### 2. Discrete Time-Domain Convolution (`doconv`)
In the main loop (`for (i = 0; i < no_impulse_samples; i++)`), the program invokes:
```c
doconv(impulse[1] + i, pulse[1], no_pulse_samples);
```
In the student exercise, completing `doconv()` implements the discrete convolution sum between the impulse response $x[n]$ and the transmit pulse $h[k]$ of length $M = \text{no\_pulse\_samples}$:

$$y[n] = (x * h)[n] = \sum_{k=0}^{M-1} x[n - k]\, h[k]$$

or, for pulse-compression / matched-filter correlation of a frequency-modulated (FM) chirp pulse, the cross-correlation with the time-reversed reference replica:

$$R_{xh}[n] = \sum_{k=0}^{M-1} x[n + k]\, h[k]$$

Students must also ensure that index offsets $n - k$ or $n + k$ do not overrun the `[0, no_impulse_samples - 1]` bounds of the `impulse` array and store the output in `result[1][i]` before writing the final `outfile`.

---

## Workflow Context & Examples

### Pairing with `testChirp` for Lab Exercises
In OMG coursework, [`testChirp`](../tests/testChirp.md) (`code/tests/testChirp.c`) is used to generate synthetic CW or FM chirp waveforms (`pulse.ascii`) and multi-target seabed reflection series (`impulse.ascii`):

```bash
# 1. Generate pulse.ascii and impulse.ascii using testChirp
testChirp -pulse_length_ms 1.0 -start_freq_kHz 10 -stop_freq_kHz 100

# 2. Run the lab convolution program on the generated ASCII files
example -pulse pulse.ascii -impul impulse.ascii -out convolved_output.ascii
```

For production complex-valued ($I/Q$) matched filtering and FFT-accelerated convolution on Simrad EK80 broadband data, see [`testNormConv`](../tests/testNormConv.md) (`code/tests/testNormConv.c`).
