---
layout: default
title: speedtosalinity
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 15
tool_name: speedtosalinity
source_path: code/tests/speedtosalinity.c
category: Seawater Sound Speed & Oceanographic Functions (tests)
input_formats:
- CSV 3-column profile: depth (m), velocity (m/s), temperature (°C)
output_formats:
- CSV 4-column profile: depth (m), velocity (m/s), temperature (°C), salinity (ppt)
related_tools:
- speed2salinity
- testSV
- testAtten
- one
- two
---

# speedtosalinity

## Overview
`speedtosalinity` (`code/tests/speedtosalinity.c`) is an enhanced version of [`speed2salinity`](speed2salinity.html) that inverts comma-separated `(depth, velocity, temperature)` sound velocity profiler casts to estimate practical salinity (`best_guess_salinity`) at **$0.1\text{ ppt}$ resolution** (400 integer steps of tenths of a part per thousand over $[0.0, 39.9]\text{ ppt}$) and allows the user to select between two classic empirical seawater sound speed equations:

* **`-wilson`:** W. D. Wilson's (1962) equation (`vsw`).
* **`-cml`:** Chen & Millero's (1977) equation (`vchemilli`).

---

## Syntax & CLI Options

```bash
speedtosalinity [-v] (-wilson | -cml) <infile.csv> <outfile.csv>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-wilson` | Use Wilson's (1962) seawater sound speed equation (`vsw`). Mutually exclusive with `-cml` (**one of `-wilson` or `-cml` is required**). | `0` |
| `-cml` | Use Chen & Millero's (1977) seawater sound speed equation (`vchemilli`). Mutually exclusive with `-wilson`. | `0` |
| `<infile.csv>` | **Required.** Input comma-separated ASCII file containing `depth, velocity, temperature` on each line. | None |
| `<outfile.csv>` | **Required.** Output comma-separated ASCII file containing `depth, velocity, temperature, best_guess_salinity`. | None |
| `-v` | Enable verbose output (`verbose++`), printing each step of the $0.1\text{ ppt}$ salinity search. | `0` |

---

## Inversion Algorithm & Implementation Notes

### 1. Fine-Stepped $0.1\text{ ppt}$ Search Loop
To avoid floating-point accumulation rounding errors during the search loop, `speedtosalinity` uses an integer loop counter `int salinity` ranging from `0` to `max_salinity - 1` (`400`, representing tenths of $\text{ppt}$) and passes `(double)salinity / 10.0` to the chosen sound speed function:

$$S^* = \underset{S_k = k/10,\; k \in \{0, \dots, 399\}}{\arg\min} \left| c_{\text{model}}(T, P, S_k) - c_{\text{obs}} \right|$$

where hydrostatic pressure $P$ in $\text{kg/cm}^2$ is evaluated from depth $z$ (m) as:

$$P = 1.0332 + (z \times 100.0) \times \frac{1.027}{1000.0}$$

### 2. Sound Speed Model Comparison (`-wilson` vs. `-cml`)
* **`vsw(t, p, s)` (`-wilson`):** Evaluates Wilson (1962). Note that line 188–193 shares the same `* +p` continuation typo in the small cross-term `vstp` as `speed2salinity.c` (accurate at shallow depths where $p \approx 1\text{ kg/cm}^2$).
* **`vchemilli(t, p, s)` (`-cml`):** Evaluates Chen & Millero (1977). Note that line 227 contains the historical typo `1.0405e-12 + pow(t, 4)` in term `a3` (documented in [`one.md`](one.html) and [`testSV.md`](testSV.html)), which biases `vchemilli` at non-zero temperatures and pressures. Therefore, `-wilson` is recommended when running the unmodified `speedtosalinity` binary, or `a3` on line 227 should be patched to `1.0405e-12 * pow(t, 4)` (as done in [`two.c`](two.html)).

---

## Example Usage

```bash
# Invert a sound velocity and temperature cast for salinity at 0.1 ppt resolution using Wilson (1962)
speedtosalinity -wilson cast_in.csv cast_salinity_out.csv
```
