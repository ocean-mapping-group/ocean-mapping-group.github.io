---
layout: default
title: comboASCIIParam2
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 2
tool_name: comboASCIIParam2
source_path: code/tests/comboASCIIParam2.c
category: Backscatter & Multi-Spectral Grid Processing (tests)
input_formats:
- .xval (ASCII frequency vector in Hz)
- .yval (ASCII 2D backscatter array: N_freq x 90 integer grazing bins)
- .zval (Optional 2-column ASCII frequency-trend calibration file: freq_kHz, BS_dB)
output_formats:
- ASCII 3-column table (freq_kHz, grazing_deg, BS_dB or nan)
- -grz ASCII 2-column frequency response curve (freq_kHz, mean_BS_dB)
- -frq ASCII 2-column angular response curve (grazing_deg, mean_BS_dB)
related_tools:
- comboASCIIParam
- testAtten
- fakeAR
- BatchProcEK
---

# comboASCIIParam2

## Overview
`comboASCIIParam2` (`code/tests/comboASCIIParam2.c`, authored by John Hughes Clarke in June 2020) is an enhanced multi-spectral seafloor backscatter processor created to handle a second MATLAB export format where `-xval` contains $N_x$ frequencies (in Hz, up to 200 bins) and `-yval` contains $N_x \times 90$ backscatter values pre-binned at $1^\circ$ integer grazing angles ($0^\circ$ to $89^\circ$).

Compared to [`comboASCIIParam`](comboASCIIParam.html), `comboASCIIParam2` introduces three advanced acoustic processing capabilities:
1. **Imperfect Frequency Calibration Detrending (`-zval`):** Reads an empirical `(freq_kHz, BS_dB)` trend file, fits a linear regression line via `do_least_squares()` (`j_ang_resp.h`), and subtracts the calibration residual from each corresponding frequency bin across all 90 grazing angles.
2. **Altitude & Seawater Absorption SNR Masking (`-altitude`, `-MinSNR`):** Computes frequency-dependent seawater absorption $\alpha(f)$ in $\text{dB/km}$ via `calc_atten()` (`Echo_calib.h`) and two-way spherical spreading + absorption transmission loss along the slant range $R(\theta_g) = H / \sin\theta_g$, masking cells with `nan` wherever the relative signal level drops below `-MinSNR`.
3. **Marginal Cross-Section Averaging (`-grz` and `-frq`):** Exports 1D mean backscatter vs. frequency averaged over a grazing angle window (`-minGraz` to `-maxGraz`), and 1D mean Angular Response Curves (ARC) vs. grazing angle averaged over a frequency band (`-minFreq` to `-maxFreq`).

---

## Syntax & CLI Options

```bash
comboASCIIParam2 [-v] -xval <freq.xval> -yval <bs_grid.yval> [-zval <cal_trend.zval>] \
                 [-altitude <m> -MinSNR <dB>] \
                 [-minGraz <deg> -maxGraz <deg> -grz <freq_curve.txt>] \
                 [-minFreq <kHz> -maxFreq <kHz> -frq <arc_curve.txt>] \
                 -out <outfile>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-xval <file>` | **Required.** Input ASCII file listing $N_x$ frequencies in **Hz** (up to 200 values; converted internally to kHz via `the_xval[i]/1000.0`). | None |
| `-yval <file>` | **Required.** Input ASCII file containing $N_x \times 90$ backscatter values (in dB) ordered by frequency index $i \in [0, N_x-1]$ and $1^\circ$ grazing angle bin $j \in [0, 89]$. | None |
| `-zval <file>` | Optional 2-column ASCII file (`freq_kHz BS_dB`) used to remove frequency-dependent calibration ripples via linear regression residuals. | Disabled |
| `-out <file>` | **Required.** Output 3-column ASCII table (`freq_kHz grazing_deg BS_dB`). Masked cells are printed as `nan`. | None |
| `-altitude <m>` | Sonar altitude $H$ above the seafloor (in meters). Enables slant-range transmission-loss / SNR masking. | `0.0` (Disabled) |
| `-MinSNR <dB>` | Minimum allowable relative signal-to-noise ratio (two-way transmission loss threshold in dB, negative value) when `-altitude` is non-zero. | `-80.0` |
| `-minGraz <deg>` | Minimum grazing angle (degrees) for computing the frequency response curve (`-grz`). | `0.0` |
| `-maxGraz <deg>` | Maximum grazing angle (degrees) for computing the frequency response curve (`-grz`). | `90.0` |
| `-grz <file>` | Output 2-column ASCII file (`freq_kHz mean_BS_dB`) averaged over `j in [minGraz, maxGraz)`. | Disabled |
| `-minFreq <kHz>` | Minimum frequency (kHz) for computing the mean Angular Response Curve (`-frq`). | `50.0` |
| `-maxFreq <kHz>` | Maximum frequency (kHz) for computing the mean Angular Response Curve (`-frq`). | `400.0` |
| `-frq <file>` | Output 2-column ASCII file (`grazing_deg mean_BS_dB`) averaged over frequencies in `(minFreq, maxFreq)` that pass the SNR threshold. | Disabled |
| `-v` | Enable verbose output (`verbose_flag++`). | `0` |

---

## Mathematical & Signal Processing Algorithms

### 1. Frequency Calibration Residual Removal (`-zval`)
When a calibration curve `(the_zvalf[k], the_zval[k])` is supplied via `-zval`, `comboASCIIParam2` calls `do_least_squares()` to fit a linear trend $\widehat{\text{BS}}(f) = a + b\,f$ and computes the calibration residual at each frequency $k$:

$$\Delta Z_k = \text{BS}_{\text{cal}}(f_k) - (a + b\,f_k)$$

For each frequency bin $i$ in `-xval` matching a calibration frequency within $|f_i/1000 - f_k| < 0.1\text{ kHz}$, the residual $\Delta Z_k$ is subtracted from all 90 grazing angle bins:

$$\text{BS}_{\text{corr}}(i, j) = \text{BS}_{\text{raw}}(i, j) - \Delta Z_k$$

### 2. Slant-Range Transmission Loss & SNR Masking (`-altitude`)
When `-altitude` $H > 0$ is specified, `calc_atten(T=10.0, S=30.0, D=0.0, pH=7.0, f_kHz)` computes the seawater absorption coefficient $\alpha(f_i)$ in $\text{dB/km}$. For each non-zero integer grazing angle $j \in [1^\circ, 89^\circ]$, the flat-bottom slant range and negative two-way transmission loss (`SNR[i][j]`) are calculated as:

$$R_j = \frac{H}{\sin(j \cdot \pi / 180)}, \qquad \text{SNR}(f_i, j) = -\left(40 \log_{10}(R_j) + 2 \cdot 10^{-3} R_j \, \alpha(f_i)\right)$$

Any bin $(i, j)$ where $\text{SNR}(f_i, j) \le \text{MinSNR}$ is written as `nan` in `-out` and excluded from the `-frq` angular response average.

---

## Example Usage

```bash
# Process broadband backscatter with calibration detrending, 20 m altitude SNR cutoff,
# and extract both a 30-60 deg frequency curve and a 90-170 kHz Angular Response Curve
comboASCIIParam2 -xval freq_Hz.xval -yval bs_90graz.yval -zval cal_trend.zval \
                 -altitude 20 -MinSNR -90 \
                 -minGraz 30 -maxGraz 60 -grz freq_response_30_60deg.txt \
                 -minFreq 90 -maxFreq 170 -frq arc_90_170kHz.txt \
                 -out full_calibrated_bs.txt
```
