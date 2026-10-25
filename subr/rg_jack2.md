---
layout: default
title: rg_jack2
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/rg_jack2.c
category: Acoustic Modeling, Backscatter & TVG
related_tools:
- j_ang_resp
- fakeAR
module_name: rg_jack2
header_path: code/subr/rg_jack2.h
---

# `rg_jack2` — Mourad & Jackson (1989) High-Frequency Seafloor Backscatter Model

## Overview & Purpose

The `rg_jack2` module (`code/subr/rg_jack2.c` and `code/subr/rg_jack2.h`) implements the Mourad and Jackson (*Oceans '89*) simplified high-frequency acoustic bottom backscatter and forward reflection loss model, which extends the formalism of Jackson, Winebrenner, and Ishimaru (1986).

Originally written by Rebecca M. Gott (Naval Research Laboratory Code 7441, July 1994) and adapted as a callable C library routine by John Hughes Clarke in November 1994, `do_RG_simple_model()` treats the seafloor sediment as a lossy fluid and combines three physical scattering regimes across grazing angles from $10^\circ$ to $90^\circ$ (mirrored across $90^\circ$ to $169^\circ$):
1. **Kirchhoff Approximation ($\sigma_{\text{kir}}$)**: Dominant at near-normal incidence (steep grazing angles near $90^\circ$).
2. **Composite Roughness Approximation ($\sigma_{\text{cr}}$)**: Dominant at moderate to low grazing angles, incorporating small-roughness perturbation scattering ($s_{\text{pr}}$) modulated by large-scale RMS bottom slope ($s$) and a geometric shadowing function ($S$).
3. **Sediment Volume Scattering ($\sigma_{\text{pv}}$)**: Sub-bottom volume inhomogeneity scattering refracted through the water-sediment interface and modulated by bottom slope shadowing.

---

## Key Data Structures & Constants

- **`#define speed_sound 1528`**: Reference water sound speed ($1528\text{ m/s}$) used to compute the acoustic wavenumber $k_a = 2\pi f / c$.
- **`typedef struct FCOMPLEX { float r, i; } fcomplex`**: Internal single-precision complex number type used for complex wavenumber ratio $K = (1 + i\,\delta)/\nu$ and Rayleigh reflection coefficient $R(\theta)$.

---

## Public Functions & Signatures

### `do_RG_simple_model`

```c
int do_RG_simple_model(
    double In_f,
    double In_nu,
    double In_rho,
    double In_lt,
    double In_beta,
    double In_gamma,
    double In_sig_2,
    float *Out_sigma_vol,
    float *Out_sigma_rss,
    float *Out_deg,
    float *Crossover
);
```

#### Input Geoacoustic Parameters
- **`In_f`**: Sonar acoustic frequency $f$ in Hertz (e.g., `30000.0` for 30 kHz, `95000.0` for 95 kHz).
- **`In_nu`**: Sediment-to-water sound speed ratio $\nu = c_{\text{sed}} / c_{\text{water}}$ (dimensionless, e.g., `1.2`).
- **`In_rho`**: Sediment-to-water bulk density ratio $\rho = \rho_{\text{sed}} / \rho_{\text{water}}$ (dimensionless, e.g., `2.0`).
- **`In_lt`**: Acoustic loss tangent $\delta$ in sediment (dimensionless, e.g., `0.0001445`).
- **`In_beta`**: Isotropic 2D bottom relief power-law spectral strength $\beta$ ($\text{cm}^{4-\gamma}$).
- **`In_gamma`**: Bottom relief 2D spectral exponent $\gamma$ (dimensionless, typically $3.0 \le \gamma \le 3.8$; slope parameter $\alpha = \gamma/2 - 1$).
- **`In_sig_2`**: Sediment volume scattering parameter $\sigma_2$ (ratio of volume scattering cross-section to sediment attenuation coefficient, dimensionless, e.g., `0.002`).

#### Output Arrays & Values
All output arrays must be allocated by the caller with at least 180 `float` elements (indices `10` through `169` are populated at $1^\circ$ increments):
- **`Out_sigma_vol`**: Total bottom backscattering strength in dB ($10 \log_{10}(\sigma_{\text{rcs}} + \sigma_{\text{pv}})$), combining interface roughness and sediment volume scattering.
- **`Out_sigma_rss`**: Interface roughness-only backscattering strength in dB ($10 \log_{10}(\sigma_{\text{rcs}})$), smoothly interpolating between $\sigma_{\text{kir}}$ and $\sigma_{\text{cr}}$ via logistic weight $f(x) = [1 + \exp(80(\cos\theta - \cos\theta_{\text{db}}))]^{-1}$.
- **`Out_deg`**: Grazing angle $\theta$ in degrees (`10.0` to `169.0`).
- **`Crossover`**: Output scalar storing the grazing angle (in degrees) at which the transition between the Kirchhoff approximation and composite roughness approximation occurs ($\theta_{\text{crossover}} = 90^\circ - \cos\theta_{\text{db}} \cdot 180^\circ/\pi$).

### Internal Mathematical Helpers (`rg_jack2.c`)

- **`W(k1, k2, beta, gamma)`**: Evaluates the 2D power-law roughness spectrum $W(k) = \beta k^{-\gamma}$.
- **`R(theta, Kcmplxsqr, rho)`**: Computes the complex plane-wave Rayleigh reflection coefficient $R(\theta)$.
- **`s_pr(theta, Kcmplxsqr, rho, k_a, beta, gamma)`**: Evaluates the small-roughness perturbation cross-section $\sigma_{\text{pr}}(\theta)$ for three-point Gaussian quadrature slope averaging.
- **`sig_pv(theta, Kcmplxsqr, rho, nu, lt, sig_2)`**: Evaluates the sediment volume scattering cross-section $\sigma_{\text{pv}}(\theta)$ (Eq. 39 of Mourad & Jackson).
- **`chsq(alpha, beta, a2)`**: Computes the structure function constant $C_h^2$ (Eq. 6) used in the Kirchhoff integral approximation.
- **Special Functions & Complex Arithmetic**: Self-contained Numerical Recipes implementations of the incomplete gamma function (`gammp`, `gser`, `gcf`), error function (`jg_erff`), log-gamma and gamma functions (`fgammln`, `gamm`), and complex arithmetic (`Cadd`, `Csub`, `Cmul`, `Cdiv`, `Csqrt`, `Cabs`, `Cimg`, `RCmul`).

---

## How It Fits Into the OMG Architecture

- **Angular Response Modeling (`subr/j_ang_resp.c`)**: Called by `j_ang_resp.c` to generate theoretical Jackson model backscatter vs. grazing angle curves for sediment classification and comparison against empirical multibeam angular response data.
- **Synthetic Backscatter Generation (`tests/fakeAR.c`)**: Invoked by `fakeAR` to synthesize realistic angular response lookup tables for testing backscatter processing pipelines.
