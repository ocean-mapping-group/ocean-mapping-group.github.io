---
layout: default
title: testSphereTS
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 24
tool_name: testSphereTS
source_path: code/tests/testSphereTS.c
category: Backscatter & Target Strength Calibration (tests)
input_formats:
  - Command-line frequency (-freq) and hardcoded 38.1 mm tungsten carbide sphere constants
output_formats:
  - Spherical Bessel diagnostic values and acoustic Target Strength (TS in dB re 1 m²) on stdout
related_tools:
  - dobessel
  - EKlook
  - BatchProcEK
  - testNormConv
---

# testSphereTS

## Overview
`testSphereTS` (`code/tests/testSphereTS.c`, authored by John Hughes Clarke in June 2023) is a C translation and testbed of David Macaulay's `sphereTS.py` Python package, which calculates the exact theoretical acoustic backscattered **Target Strength ($\text{TS}$)** of an elastic calibration sphere immersed in a fluid using the normal-mode series solution of **MacLennan (1981)** (*"The theory of solid spheres as sonar calibration targets"*) and the spherical Bessel derivative recurrences of **Rudgers (1967)** (*NRL Report 6551*).

In hydrographic and fisheries acoustics (such as calibrating Kongsberg Simrad EK60/EK80 split-beam echosounders in [`EKlook`](../EKlook/index.md)), a standard $38.1\text{ mm}$ tungsten carbide ($\text{WC}$ with $6\%$ cobalt binder) sphere is suspended beneath the transducer to verify on-axis gain and broadband frequency response.

---

## Syntax & CLI Options

```bash
testSphereTS [-v] [-freq <Hz>] [<infile> [<outfile>]]
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-freq <Hz>` | Acoustic frequency in Hz parsed on the command line (overridden at the start of the `yetagain:` block by `f = 100000.0`). | `100000.0 Hz` (`100 kHz`) |
| `-v` | Increment verbose flag (`verbose_flag++`). | `0` |
| `<infile> <outfile>` | Optional positional filename arguments (stored in `inname`, `outname`). | Unused |

---

## Elastic Sphere Modal Scattering Formulation

### 1. Physical Constants ($38.1\text{ mm}$ Tungsten Carbide Sphere in Seawater)
Lines 129–135 initialize the physical parameters for a standard calibration sphere:
* **Acoustic frequency ($f$):** $100,000\text{ Hz}$ ($100\text{ kHz}$)
* **Sphere radius/diameter parameter ($a$):** $0.0381\text{ m}$ ($38.1\text{ mm}$)
* **Surrounding fluid sound speed ($c$):** $1500.0\text{ m/s}$
* **Sphere longitudinal wave speed ($c_1$):** $6853.0\text{ m/s}$ (tungsten carbide compressional wave velocity)
* **Sphere transverse/shear wave speed ($c_2$):** $4171.0\text{ m/s}$ (tungsten carbide shear wave velocity)
* **Surrounding fluid density ($\rho$):** $1025.0\text{ kg/m}^3$
* **Sphere material density ($\rho_1$):** $14,900.0\text{ kg/m}^3$

### 2. Dimensionless Wavenumbers & Material Ratios
From these parameters, the fluid wavenumber $k$, dimensionless size parameter $q = ka$, internal longitudinal/transverse size parameters $q_1, q_2$, and Lamé impedance parameters $\alpha, \beta$ are defined as:

$$k = \frac{2\pi f}{c}, \qquad q = ka, \qquad q_1 = q\frac{c}{c_1}, \qquad q_2 = q\frac{c}{c_2}$$

$$\alpha = 2\left(\frac{\rho_1}{\rho}\right)\left(\frac{c_2}{c}\right)^2, \qquad \beta = \left(\frac{\rho_1}{\rho}\right)\left(\frac{c_1}{c}\right)^2 - \alpha$$

### 3. Spherical Bessel Recurrences & Modal Form Function $f_\infty$
For each partial wave mode $\ell = 0, 1, 2, \dots, 49$ until relative convergence $|\text{newterm}/\text{form}| \le 10^{-10}$, the spherical Bessel functions of the first and second kind $j_\ell(x) = \sqrt{\frac{\pi}{2x}}\,J_{\ell+1/2}(x)$ and $y_\ell(x) = \sqrt{\frac{\pi}{2x}}\,Y_{\ell+1/2}(x)$ and their first and second derivatives ($j'_\ell, j''_\ell, y'_\ell$) are combined into boundary-condition determinants $A_1, A_2, B_1, B_2$ and phase-shift angles $\eta_\ell$:

$$A_2 = (\ell^2 + \ell - 2) j_\ell(q_2) + q_2^2 j''_\ell(q_2), \qquad A_1 = 2\ell(\ell+1)\big(q_1 j'_\ell(q_1) - j_\ell(q_1)\big)$$

$$B_2 = A_2 q_1^2 \big(\beta j_\ell(q_1) - \alpha j''_\ell(q_1)\big) - A_1 \alpha \big(j_\ell(q_2) - q_2 j'_\ell(q_2)\big)$$

$$B_1 = q \big(A_2 q_1 j'_\ell(q_1) - A_1 j_\ell(q_2)\big), \qquad \tan\eta_\ell = -\frac{B_2 j'_\ell(q) - B_1 j_\ell(q)}{B_2 y'_\ell(q) - B_1 y_\ell(q)}$$

The modal form function $F$, backscattering cross-section $\sigma_{\text{bs}}$, and Target Strength ($\text{TS}$) in $\text{dB re } 1\text{ m}^2$ are then:

$$F = -\frac{2}{q} \sum_{\ell=0}^{\infty} (-1)^\ell (2\ell + 1) \sin\eta_\ell\, e^{i\eta_\ell}, \qquad \sigma = \pi a^2 |F|^2, \qquad \text{TS} = 10 \log_{10}\!\left(\frac{\sigma}{4\pi}\right)$$

*(Implementation Note: In `testSphereTS.c` lines 164–165, the loop currently prints `j0(q)` and `j1(q)` and calls `exit(0)` while transitioning from Python's `scipy.special.jv(l+0.5, q)` to GSL's spherical Bessel routines `gsl_sf_bessel_jl` / `gsl_sf_bessel_yl`).*

---

## Example Usage

```bash
# Run the testSphereTS benchmark
testSphereTS -freq 100000
```
