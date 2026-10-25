---
layout: default
title: speed2salinity
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 14
tool_name: speed2salinity
source_path: code/tests/speed2salinity.c
category: Seawater Sound Speed & Oceanographic Functions (tests)
input_formats:
- CSV 3-column profile: depth (m), velocity (m/s), temperature (°C)
output_formats:
- CSV 4-column profile: depth (m), velocity (m/s), temperature (°C), salinity (ppt)
related_tools:
- speedtosalinity
- testSV
- testAtten
- one
- two
---

# speed2salinity

## Overview
`speed2salinity` (`code/tests/speed2salinity.c`) is a hydrographic water-column utility that estimates seawater salinity (in parts per thousand, $\text{ppt}$) for Sound Velocity Profiler (SVP) casts that record depth ($m$), sound speed ($m/s$), and temperature ($^\circ\text{C}$), but lack a conductivity cell to measure salinity directly (a common configuration on expendable bathythermographs/sound velocity probes or legacy AML SV+T profilers).

For each `(depth, velocity, temperature)` record in the comma-separated input file, `speed2salinity` converts depth to hydrostatic pressure in $\text{kg/cm}^2$ and performs an exhaustive grid search over integer salinities $S \in [0, 39]\text{ ppt}$ in $1.0\text{ ppt}$ steps using **Wilson's (1962)** empirical sound speed equation (`vsw`), selecting the salinity that minimizes $|c_{\text{Wilson}}(T, P, S) - c_{\text{obs}}|$.

*(For $0.1\text{ ppt}$ resolution and a choice between Wilson and Chen-Millero equations, see [`speedtosalinity`](speedtosalinity.html)).*

---

## Syntax & CLI Options

```bash
speed2salinity [-v] <infile.csv> <outfile.csv>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `<infile.csv>` | **Required.** Input comma-separated ASCII file with 3 columns per line: `depth, velocity, temperature`. | None |
| `<outfile.csv>` | **Required.** Output comma-separated ASCII file with 4 columns per line: `depth, velocity, temperature, best_guess_salinity`. | None |
| `-v` | Enable verbose output: prints every read sample, the depth-to-pressure conversion, and a `"Warmer..."` / `"Colder..."` trace at each $1.0\text{ ppt}$ step. | `0` (Disabled) |

---

## Mathematical & Inversion Algorithm

### 1. Hydrostatic Pressure Conversion
Given depth $z$ in meters, atmospheric pressure $P_{\text{atm}} = 1.0332\text{ kg/cm}^2$, and nominal seawater density $\rho = 1.027\text{ g/cm}^3$, total absolute pressure $P$ in $\text{kg/cm}^2$ is computed as:

$$P = P_{\text{atm}} + (z \times 100.0) \times \frac{\rho}{1000.0} = 1.0332 + 0.1027\,z\quad [\text{kg/cm}^2]$$

### 2. Integer Salinity Grid Search ($0\text{–}39\text{ ppt}$)
For each sample, `salinity` is stepped from $0.0$ to $39.0\text{ ppt}$ (`salinity < max_salinity` where `max_salinity = 40`, step `1.0`):

$$S^* = \underset{S \in \{0, 1, \dots, 39\}}{\arg\min} \left| v_{\text{sw}}(T, P, S) - c_{\text{obs}} \right|$$

### 3. Wilson (1962) Sound Speed Equation (`vsw`)
The function `double vsw(double t, double p, double s)` implements W. D. Wilson's (*J. Acoust. Soc. Am.*, Vol. 34, p. 866, 1962) empirical formula:

$$v_{\text{sw}}(t, p, s) = 1449.14 + v_t(t) + v_p(p) + v_s(s) + v_{stp}(s, t, p)$$

* $v_t = 4.5721 t - 4.4532\times 10^{-2} t^2 - 2.604\times 10^{-4} t^3 + 7.9851\times 10^{-6} t^4$
* $v_p = 1.60272\times 10^{-1} p + 1.0268\times 10^{-5} p^2 + 3.5216\times 10^{-9} p^3 - 3.3603\times 10^{-12} p^4$
* $v_s = 1.39799(s - 35) + 1.69202\times 10^{-3}(s - 35)^2$
* $v_{stp}$: Cross-product polynomial in $(s - 35)$, $t$, and $p$.
  *(Note: In `speed2salinity.c` lines 149–155, several continuation lines in `vstp` use `* +p` instead of `+ p *`, which alters the high-pressure cross-term; this was corrected to `+ p *` in [`testSV.c`](testSV.html) lines 430–436).*

---

## Example Input & Output

**Input (`svp_cast.csv`):**

```text
5.000000, 1489.200000, 10.500000
25.000000, 1485.100000, 8.900000
```

**Command:**

```bash
speed2salinity svp_cast.csv svp_with_sal.csv
```

**Output (`svp_with_sal.csv`):**

```text
5.000000, 1489.200000, 10.500000, 34.000000
25.000000, 1485.100000, 8.900000, 35.000000
```
The resulting salinity profile can then be used to compute frequency-dependent acoustic absorption in [`testAtten`](testAtten.html) or [`BatchProcEK`](../EKlook/BatchProcEK.html).
