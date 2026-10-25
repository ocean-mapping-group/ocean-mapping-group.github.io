---
layout: default
title: fakeAR
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 5
tool_name: fakeAR
source_path: code/tests/fakeAR.c
category: Backscatter & Multi-Spectral Grid Processing (tests)
input_formats:
  - Command-line physical geoacoustic parameters
output_formats:
  - ASCII multi-frequency / grazing-angle backscatter table (gnuplot / asciiplot)
related_tools:
  - comboASCIIParam
  - comboASCIIParam2
  - BatchProcEK
  - EKlook
---

# fakeAR

## Overview
`fakeAR` (`code/tests/fakeAR.c`, authored by John Hughes Clarke in March 2005) generates synthetic seafloor Angular Response (AR) backscatter curves across incidence/grazing angles ($0^\circ$ to $180^\circ$) and acoustic frequencies (`NOFREQS = 80` steps between `-minFkHz` and `-maxFkHz`).

It supports two distinct operating modes:
1. **APL-UW / Jackson Geoacoustic Scattering Mode (`-RG`):** Calls `do_RG_simple_model()` (declared in `rg_jack2.h`, implementing Darrell Jackson's high-frequency composite roughness and sediment volume scattering model) across 80 frequencies using user-specified geoacoustic parameters (sediment-to-water sound speed ratio $\nu$, density ratio $\rho$, loss tangent $\delta$, roughness spectral strength $\beta$, spectral exponent $\gamma$, and volume scattering parameter $\sigma_2$).
2. **Simple Parametric AR Table Mode (default without `-RG`):** Writes a 180-line ASCII table from $0^\circ$ to $179^\circ$ parameterized by normal-incidence backscatter `-BSn`, oblique backscatter `-BSo`, and `-Crossover` angle.

---

## Syntax & CLI Options

```bash
fakeAR [-v] [-RG [-beta <val>] [-gamma <val>] [-loss_tan <val>] [-vol_para <val>] \
                 [-den_ratio <val>] [-ssp_ratio <val>] [-minFkHz <kHz>] [-maxFkHz <kHz>]] \
       [-BSn <dB>] [-BSo <dB>] [-Crossover <deg>] <outfile>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `<outfile>` | **Required.** Output ASCII file path. | None |
| `-RG` | Enable Jackson's Rayleigh-Gassmann / composite roughness & volume scattering model (`do_RG_simple_model`) over `NOFREQS = 80` frequency steps. | `0` (Disabled) |
| `-minFkHz <kHz>` | Minimum frequency in kHz for the 80-step `-RG` sweep. | `10.0` |
| `-maxFkHz <kHz>` | Maximum frequency in kHz for the 80-step `-RG` sweep. | `400.0` |
| `-ssp_ratio <val>` | Sediment-to-seawater sound speed ratio $\nu = c_{\text{sed}} / c_{\text{water}}$ (`In_nu`). | `1600 / 1500 = 1.0667` |
| `-den_ratio <val>` | Sediment-to-seawater bulk density ratio $\rho = \rho_{\text{sed}} / \rho_{\text{water}}$ (`In_rho`). | `2000 / 1028 = 1.9455` |
| `-loss_tan <val>` | Sediment acoustic loss tangent $\delta$ (`In_lt`). | `0.0001445` |
| `-beta <val>` | Bottom relief 2D roughness spectral strength $\beta$ (`In_beta`). | `0.0035` |
| `-gamma <val>` | Bottom relief roughness spectral exponent $\gamma$ (`In_gamma`). | `3.0` |
| `-vol_para <val>` | Sediment volume scattering parameter $\sigma_2$ (`In_sig_2`). | `0.002` |
| `-BSn <dB>` | Normal-incidence backscatter strength (dB) for non-`-RG` mode. | `-30.0` |
| `-BSo <dB>` | Oblique-incidence backscatter strength (dB) for non-`-RG` mode. | `-40.0` |
| `-Crossover <deg>` | Crossover incidence angle (degrees) between specular and oblique regimes. | `25.0` |
| `-v` | Enable verbose output (`verbose_flag++`). | `0` |

---

## Geoacoustic Modeling & Output Formats

### 1. Jackson Composite Roughness & Volume Model (`-RG`)
When `-RG` is specified, `fakeAR` divides the frequency span $[f_{\min}, f_{\max}]$ into `NOFREQS = 80` linear steps:

$$\Delta f = \frac{f_{\max,\text{kHz}} - f_{\min,\text{kHz}}}{80}, \qquad f_i = \left(f_{\min,\text{kHz}} + i\,\Delta f\right) \times 1000\text{ Hz}$$

At each frequency $f_i$, it invokes:
```c
do_RG_simple_model(In_f, In_nu, In_rho, In_lt, In_beta, In_gamma, In_sig_2,
                   Out_sigma_vol[i], Out_sigma_rss[i], Out_deg[i], &Crossover);
```
By default (`printout == 2`, gnuplot 3D surface format), for each frequency $i \in [0, 79]$ and nadir-to-grazing half-swath index $j \in [90, 179]$, it filters out near-zero grazing kick-up artifacts (`Out_sigma_vol[i][j] < Out_sigma_vol[i][j-1]`) and writes space-separated triplets:
```text
<Freq_kHz> <Grazing_Angle_deg> <Total_Backscatter_dB>
```
separated by blank lines between frequency blocks (ideal for `gnuplot splot` or ingestion into [`comboASCIIParam`](comboASCIIParam.md)).

### 2. Default Parametric Output (without `-RG`)
When run without `-RG`, `fakeAR` loops over $j = 0, \dots, 179$ and writes 4-column rows:
```text
<Angle_deg> <BSn> <BSo> 0
```

---

## Example Usage

```bash
# Generate a 10-400 kHz multi-spectral Jackson scattering surface for a sandy seafloor
fakeAR -RG -minFkHz 50 -maxFkHz 350 -ssp_ratio 1.15 -den_ratio 2.0 \
       -beta 0.004 -gamma 3.1 -vol_para 0.003 sand_model_3d.txt
```
