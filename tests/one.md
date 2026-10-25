---
layout: default
title: one
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 10
tool_name: one
source_path: code/tests/one.c
category: Seawater Sound Speed & Oceanographic Functions (tests)
input_formats:
- C function arguments: double t (temperature °C), double p (pressure kg/cm²), double s (salinity ppt)
output_formats:
- Return value: double vchemilli (sound speed in m/s)
related_tools:
- two
- testSV
- speedtosalinity
- speed2salinity
---

# one (`this_vchemilli`)

## Overview
`one.c` (`code/tests/one.c`) is a standalone 60-line C function module containing `double this_vchemilli(double t, double p, double s)`, an early implementation of the **Chen & Millero (1977)** empirical equation for the speed of sound in seawater as a function of temperature $t$ ($^\circ\text{C}$), pressure $p$ ($\text{kg/cm}^2$), and salinity $s$ (parts per thousand / PSU).

In the OMG repository history, `one.c` and [`two.c`](two.html) were created side-by-side in `code/tests/` to isolate and debug a subtle typographical error in the quadratic pressure coefficient `a3` of the pure-water sound speed polynomial $C_w(t,p)$—a bug documented by Jason Bartlett (`JDB`) in [`testSV.c`](testSV.html) (`/* This had a boo-boo in it... */`).

---

## Function Signature & Parameters

```c
double this_vchemilli(double t, double p, double s);
```

| Parameter | Type | Units | Description |
| :--- | :--- | :--- | :--- |
| `t` | `double` | $^\circ\text{C}$ | In-situ seawater temperature |
| `p` | `double` | $\text{kg/cm}^2$ | Hydrostatic/total gauge pressure in $\text{kg/cm}^2$ ($1\text{ bar} \approx 1.019716\text{ kg/cm}^2$) |
| `s` | `double` | $\text{ppt}$ (PSU) | Practical salinity in parts per thousand |
| **Returns** | `double` | $\text{m/s}$ | Computed speed of sound in seawater (`vchemilli`) |

---

## Mathematical Formulation & Historical Bug Analysis

The Chen & Millero (1977) equation expresses seawater sound speed as:

$$c(S, T, P) = C_w(T, P) - C_c(T, P) + A(T, P)\,S + B(T, P)\,S^{3/2} + D(P)\,S^2$$

where:
1. **Pure-Water Sound Speed Term (`cw = a1 + a2 + a3 + a4`):**
   * $a_1 = 1402.388 + 5.03711 t - 5.80852\times 10^{-2} t^2 + 3.3420\times 10^{-4} t^3 - 1.4780\times 10^{-6} t^4 + 3.1464\times 10^{-9} t^5$
   * $a_2 = \left(0.153563 + 6.8982\times 10^{-4} t - 8.1788\times 10^{-6} t^2 + 1.3621\times 10^{-7} t^3 - 6.1185\times 10^{-10} t^4\right) p$
   * $a_3$ **(Buggy in `one.c` lines 19–21):**

     ```c
     a3 = (3.1260e-5 - 1.7107e-6 * t + 2.5974e-8 * t * t - 2.5335e-10 * pow(t, 3) +
           1.0405e-12 + pow(t, 4)) * p * p;
     ```
     Notice `+ 1.0405e-12 + pow(t, 4)` instead of `+ 1.0405e-12 * pow(t, 4)`. Because `+ pow(t, 4)` is added unscaled before multiplying by $p^2$, any non-zero temperature and pressure causes $a_3$ to explode by $t^4 p^2\text{ m/s}$!
   * $a_4 = \left(-9.7729\times 10^{-9} + 3.8504\times 10^{-10} t - 2.3643\times 10^{-12} t^2\right) p^3$

2. **Pressure Correction Term (`cc = a5 + a6 + 2.68e-9 * pow(p, 3)`):**
   * $a_5 = \left(0.0029 - 2.19\times 10^{-4} t + 1.4\times 10^{-5} t^2\right) p$
   * $a_6 = \left(-4.76\times 10^{-6} + 3.47\times 10^{-7} t - 2.59\times 10^{-8} t^2\right) p^2$

3. **Salinity Terms (`aa`, `bb`, `dd`):**
   * $A(t,p) = a_7 + a_8 + a_9 + a_{10}$
   * $B(t,p) = -1.922\times 10^{-2} - 4.42\times 10^{-5} t + \left(7.3637\times 10^{-5} + 1.7945\times 10^{-7} t\right) p$
   * $D(p) = 1.727\times 10^{-3} - 7.9836\times 10^{-6} p$

---

## Relationship to Other OMG Files

* **[`two.c`](two.html):** Contains the corrected version of this function (`1.0405e-12 * pow(t, 4)`).
* **[`speedtosalinity.c`](speedtosalinity.html):** Retains the `1.0405e-12 + pow(t, 4)` typo in its local copy of `vchemilli()`.
* **[`testSV.c`](testSV.html):** Documents the bug (`/* This had a boo-boo in it...I fixed it... JDB, September 2004 */`) and replaces it with the validated `ChenMillero()` function from `soundspeed.c`.
