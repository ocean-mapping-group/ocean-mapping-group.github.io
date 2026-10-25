---
layout: default
title: testNormConv
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 21
tool_name: testNormConv
source_path: code/tests/testNormConv.c
category: Chirp Waveforms, Matched Filtering & Signal Processing (tests)
input_formats:
- -mf (3-column ASCII matched filter replica: index, I, Q)
- -sig (2-column ASCII raw complex receiver trace: I, Q)
output_formats:
- -out (3-column ASCII time-domain complex convolution output: index, I, Q)
- temp.padraw, temp.padmf, temp.fft.padraw, temp.fft.padmf, temp.fft.multi, temp.ifft.multi
related_tools:
- readJSON
- testChirp
- example
- EKlook
---

# testNormConv

## Overview
`testNormConv` (`code/tests/testNormConv.c`, authored by John Hughes Clarke in February 2025) is an acoustic signal-processing verification utility developed for Kongsberg Simrad EK80 broadband (FM) pulse-compression calibration and benchmarking.

When processing EK80 complex baseband ($I/Q$) signals, two critical numerical questions arise:
1. **How is the matched-filter normalization factor ($\ell_2$-norm) defined?** Specifically, how does the GNU Scientific Library (`GSL`) BLAS routine `gsl_blas_dznrm2()` compare against `gsl_blas_dzasum()`, MATLAB's Frobenius/Euclidean norm, and direct C summations of $I^2 + Q^2$?
2. **How does direct time-domain complex convolution (`cmplx_convolve`) compare against radix-2 FFT frequency-domain multiplication (`four1`)?**

`testNormConv` reads an ASCII stage-2 decimated matched-filter file (`-mf`) and a raw complex ping trace (`-sig`), computes seven variations of vector norms on the filter coefficients, executes time-domain complex correlation (`cmplx_convolve` from `ek80_parse_proc.h`), and then zero-pads both vectors to the next power of two (`novalPOW2`) to perform forward FFTs, complex spectral multiplication, and inverse FFT (`four1`), dumping intermediate diagnostic files at every stage.

---

## Syntax & CLI Options

```bash
testNormConv [-v] [-depth <val>] -mf <matched_filter.txt> -sig <raw_trace.txt> -out <conv_out.txt>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-mf <file>` | **Required.** Input 3-column ASCII matched-filter file (`index I Q`, read into `fcomplex *mfstag2dec` and `gsl_vector_complex *gslvc`). | None |
| `-sig <file>` | **Required.** Input 2-column ASCII raw complex trace file (`I Q`, read into `fcomplex *rawtrace`). | None |
| `-out <file>` | **Required.** Output 3-column ASCII file (`index I Q`) containing the direct time-domain complex convolution `mftrace` of length `novalsRAW + novalsMF`. | None |
| `-depth <val>` | Optional numeric parameter parsed via `strtodbl()`. | Unused |
| `-v` | Enable verbose line-reading diagnostics in `getc_line()`. | `0` |

---

## Mathematical & Signal Processing Benchmarks

### 1. Complex Conjugate Time-Reversal of the Matched Filter
For an $N_{\text{MF}}$-sample complex filter $h[k] = I_k + j Q_k$ (`mfstag2dec`), `testNormConv` constructs the time-reversed complex conjugate matched filter `mf_flip`:

$$h_{\text{flip}}[N_{\text{MF}} - 1 - k] = h^*[k] = I_k - j Q_k$$

### 2. Seven Complex Vector Norm Comparisons
To verify the exact matched-filter energy normalization factor $\Vert h \Vert_2 = \sqrt{\sum_{k=0}^{N_{\text{MF}}-1} (I_k^2 + Q_k^2)}$ used in EK80 calibration (e.g., CRIMAC / Demer et al. 2017 equations), `testNormConv` prints:
1. **`gsl_blas_dznrm2(gslvc)`:** Standard BLAS Euclidean $\ell_2$-norm $\sqrt{\sum (|I_k|^2 + |Q_k|^2)}$ (identical to MATLAB's Euclidean/Frobenius vector norm).
2. **`gsl_blas_dzasum(gslvc)`:** BLAS sum of absolute real and imaginary parts $\sum (|I_k| + |Q_k|)$.
3. **`sqmagIQ` & `sqrt(sumsq)`:** Direct C loop computing $\sum (I_k^2 + Q_k^2)$ and $\sqrt{\sum (I_k^2 + Q_k^2)}$ (confirming agreement with `gsl_blas_dznrm2`).
4. **$\ell_1$ radial magnitude sum:** $\sum \sqrt{I_k^2 + Q_k^2}$.
5. **Separate $I$ and $Q$ energy sums:** $\sum I_k^2$, $\sum Q_k^2$, and $\sqrt{\sum I_k^2 + \sum Q_k^2}$.
6. **Maximum component ($\ell_\infty$ on $I, Q$):** $\max_k(\max(I_k, Q_k))$.
7. **Maximum complex modulus ($\ell_\infty$ radial):** $\max_k \sqrt{I_k^2 + Q_k^2}$.

### 3. Time-Domain vs. FFT/IFFT Fast Convolution
1. **Direct Time-Domain Convolution:** Calls `cmplx_convolve(mf_flip, novalsMF, rawtrace, novalsRAW, mftrace)` and writes all `novalsRAW + novalsMF` complex samples to `-out`.
2. **Radix-2 FFT Convolution:**
   * Finds the smallest power of two $N_{2^p} = 2^p \ge N_{\text{RAW}}$.
   * Zero-pads `rawtrace` and `mf_flip` into `padrawtrace` and `padmf_flip` of length $N_{2^p}$ (saved to `temp.padraw` and `temp.padmf`).
   * Transforms both to the frequency domain via `four1(..., novalPOW2, 1)` (saved to `temp.fft.padraw` and `temp.fft.padmf`).
   * Multiplies the complex spectra bin-by-bin:
     $$(a + jb)(c + jd) = (ac - bd) + j(ad + bc)$$
     and writes `temp.fft.multi`.
   * Applies the inverse FFT `four1(..., novalPOW2, -1)`, normalizes by $1 / N_{2^p}$, and writes the compressed time-domain trace to `temp.ifft.multi`.

---

## Example Usage

```bash
# Run norm verification and compare time-domain vs. FFT convolution on EK80 I/Q traces
testNormConv -mf ek80_stage2_mf.txt -sig ek80_raw_ping.txt -out ek80_conv_time.txt
```
