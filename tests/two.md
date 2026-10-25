---
layout: default
title: two
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 28
tool_name: two
source_path: code/tests/two.c
category: Seawater Sound Speed & Oceanographic Functions (tests)
input_formats:
  - C function arguments: double t (temperature °C), double p (pressure kg/cm²), double s (salinity ppt)
output_formats:
  - Return value: double vchemilli (sound speed in m/s)
related_tools:
  - one
  - testSV
  - speedtosalinity
  - speed2salinity
---

# two (`vchemilli`)

## Overview
`two.c` (`code/tests/two.c`) is a 73-line standalone C function module implementing `double vchemilli(double t, double p, double s)`, the **corrected** empirical equation of **Chen & Millero (1977)** (*"Speed of sound in seawater at high pressures"*, *J. Acoust. Soc. Am.*, Vol. 62, No. 5, pp. 1129–1135) for computing the speed of sound in seawater from temperature $t$ ($^\circ\text{C}$), pressure $p$ ($\text{kg/cm}^2$), and salinity $s$ (parts per thousand / PSU).

In the OMG `code/tests/` directory, `two.c` serves as the debugged companion to [`one.c`](one.md): it fixes the typographical error in polynomial coefficient `a3` (`1.0405e-12 * pow(t, 4)` instead of `1.0405e-12 + pow(t, 4)`), replaces `pow(p, 3)` in `a4` with direct multiplication `p * p * p`, and includes a block of French diagnostic `printf("a1 vaut %lf\n", a1);` statements (lines 55–69, commented out) used to verify each intermediate coefficient (`a1`–`a10`, `cw`, `cc`, `aa`, `bb`, `dd`) against reference tables.

---

## Function Signature & Parameters

```c
double vchemilli(double t, double p, double s);
```

| Parameter | Type | Units | Description |
| :--- | :--- | :--- | :--- |
| `t` | `double` | $^\circ\text{C}$ | In-situ seawater temperature ($0 \le t \le 40^\circ\text{C}$) |
| `p` | `double` | $\text{kg/cm}^2$ | Gauge/hydrostatic pressure in $\text{kg/cm}^2$ ($0 \le p \le 1000\text{ kg/cm}^2$) |
| `s` | `double` | $\text{ppt}$ (PSU) | Practical salinity in parts per thousand ($0 \le s \le 40\text{ ppt}$) |
| **Returns** | `double` | $\text{m/s}$ | Speed of sound in seawater (`vchemilli`) |

---

## Complete Chen & Millero (1977) Polynomial Formulation

The speed of sound $c(t, p, s)$ is evaluated as:

$$c(t, p, s) = C_w(t, p) - C_c(t, p) + A(t, p)\,s + B(t, p)\,s^{3/2} + D(p)\,s^2$$

### 1. Pure-Water Sound Speed $C_w(t, p) - C_c(t, p)$
* **$a_1$ ($0\text{ bar}$ pure-water polynomial):**
  $$a_1 = 1402.388 + 5.03711 t - 5.80852\times 10^{-2} t^2 + 3.3420\times 10^{-4} t^3 - 1.4780\times 10^{-6} t^4 + 3.1464\times 10^{-9} t^5$$
* **$a_2$ (linear pressure term):**
  $$a_2 = \left(0.153563 + 6.8982\times 10^{-4} t - 8.1788\times 10^{-6} t^2 + 1.3621\times 10^{-7} t^3 - 6.1185\times 10^{-10} t^4\right) p$$
* **$a_3$ (quadratic pressure term, corrected on line 22):**
  $$a_3 = \left(3.1260\times 10^{-5} - 1.7107\times 10^{-6} t + 2.5974\times 10^{-8} t^2 - 2.5335\times 10^{-10} t^3 + 1.0405\times 10^{-12} t^4\right) p^2$$
* **$a_4$ (cubic pressure term):**
  $$a_4 = \left(-9.7729\times 10^{-9} + 3.8504\times 10^{-10} t - 2.3643\times 10^{-12} t^2\right) p^3$$
* **Combined pure-water term:** $C_w = a_1 + a_2 + a_3 + a_4$, with high-pressure adjustment $C_c = a_5 + a_6 + 2.68\times 10^{-9} p^3$, where:
  $$a_5 = \left(0.0029 - 2.19\times 10^{-4} t + 1.4\times 10^{-5} t^2\right) p, \qquad a_6 = \left(-4.76\times 10^{-6} + 3.47\times 10^{-7} t - 2.59\times 10^{-8} t^2\right) p^2$$

### 2. Salinity Polynomial Coefficients $A(t, p)$, $B(t, p)$, and $D(p)$
* **$A(t, p) = a_7 + a_8 + a_9 + a_{10}$:**
  * $a_7 = 1.389 - 1.262\times 10^{-2} t + 7.164\times 10^{-5} t^2 + 2.006\times 10^{-6} t^3 - 3.21\times 10^{-8} t^4$
  * $a_8 = \left(9.4742\times 10^{-5} - 1.2580\times 10^{-5} t - 6.4885\times 10^{-8} t^2 + 1.0507\times 10^{-8} t^3 - 2.0122\times 10^{-10} t^4\right) p$
  * $a_9 = \left(-3.9064\times 10^{-7} + 9.1041\times 10^{-9} t - 1.6002\times 10^{-10} t^2 + 7.988\times 10^{-12} t^3\right) p^2$
  * $a_{10} = \left(1.100\times 10^{-10} + 6.649\times 10^{-12} t - 3.389\times 10^{-13} t^2\right) p^3$
* **$B(t, p)$ ($s^{3/2}$ coefficient):**
  $$B(t, p) = -1.922\times 10^{-2} - 4.42\times 10^{-5} t + \left(7.3637\times 10^{-5} + 1.7945\times 10^{-7} t\right) p$$
* **$D(p)$ ($s^2$ coefficient):**
  $$D(p) = 1.727\times 10^{-3} - 7.9836\times 10^{-6} p$$

---

## Comparison with `one.c` and `testSV.c`

| File | Function Name | `a3` Term ($t^4$ coefficient) | Status |
| :--- | :--- | :--- | :--- |
| [`one.c`](one.md) | `this_vchemilli` | `1.0405e-12 + pow(t, 4)` | Buggy (`+` instead of `*`) |
| **`two.c`** | `vchemilli` | `1.0405e-12 * pow(t, 4)` | **Corrected** (includes `a1..dd` debug print block) |
| [`testSV.c`](testSV.md) | `this_vchemilli` / `ChenMillero` | `1.0405e-12 * pow(t, 4)` | **Corrected** standalone executable |
