---
layout: default
title: dobessel
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 3
tool_name: dobessel
source_path: code/tests/dobessel.c
category: Mathematical & Acoustic Benchmarks (tests)
input_formats:
- Interactive stdin prompts (integer order n, accuracy epsilon)
output_formats:
- besselSeriesPlotn0.txt (2-column tab-separated ASCII table: x, J_n(x))
related_tools:
- testSphereTS
- mkbp
- bpdemo
---

# dobessel

## Overview
`dobessel` (`code/tests/dobessel.c`) is a standalone numerical test utility that computes the cylindrical Bessel function of the first kind $J_n(x)$ of integer order $n$ across the domain $x \in [0.0, 10.0]$ in increments of $\Delta x = 0.1$ using an iterative power-series ratio expansion. It prompts the user interactively for the integer order $n$ and convergence tolerance $\epsilon$ (`eps`), and writes the resulting $(x, J_n(x))$ curve to `besselSeriesPlotn0.txt`.

In the OMG codebase, Bessel functions are fundamental to both circular planar transducer directivity modeling ($J_1(x)$ in [`mkbp`](../labs/mkbp.html) and [`bpdemo`](../bpdemo/BPdemo.html)) and spherical elastic target strength modeling ($j_\ell(x) = \sqrt{\frac{\pi}{2x}} J_{\ell+1/2}(x)$ in [`testSphereTS`](testSphereTS.html)).

---

## Usage & Interactive Inputs

```bash
dobessel
```

The program takes no command-line flags and prompts on `stdin` for two parameters:
1. **`Enter the value of n:`** (`int n`) — Non-negative integer order of the Bessel function $J_n(x)$ (e.g., `0` for $J_0(x)$ or `1` for $J_1(x)$).
2. **`Enter the desired accuracy:`** (`double eps`) — Relative convergence threshold $\left|\frac{t_k}{\text{sum}}\right| \le \epsilon$ used to terminate the infinite series at each $x$ step (e.g., `1e-8`).

### Example Session

```bash
dobessel <<EOF
0
0.000001
EOF
```
This writes 101 tab-delimited lines (`%lf\t%lf\n`) to `besselSeriesPlotn0.txt` in the current working directory.

---

## Mathematical Algorithm

The cylindrical Bessel function of the first kind of integer order $n$ is defined by the Frobenius power series:

$$J_n(x) = \left(\frac{x}{2}\right)^n \sum_{k=0}^{\infty} \frac{(-1)^k}{k!\,(n+k)!} \left(\frac{x}{2}\right)^{2k}$$

Rather than re-evaluating factorials and high powers of $x$ at every iteration $k$, `dobessel` factors out $(x/2)^n$ and computes the inner sum recurrence using the exact term-to-term ratio $R_k$:

1. **Initialization ($k = 0$):**
   $$t_0 = \frac{1}{n!}, \qquad S_0 = t_0$$
   where $n!$ is computed by `double factorial(int n)`.
2. **Iterative Recurrence ($k = 1, 2, \dots$):**
   $$R_k = \frac{t_k}{t_{k-1}} = -\frac{x^2 / 4}{k(n + k)}, \qquad t_k = R_k \, t_{k-1}, \qquad S_k = S_{k-1} + t_k$$
3. **Convergence Check:**
   The loop continues while $\left|\frac{t_k}{S_k}\right| > \epsilon$.
4. **Final Scaling:**
   Once converged, the sum is multiplied by $(x/2)^n$:
   $$J_n(x) = S_k \cdot \left(\frac{x}{2}\right)^n$$
   and written as `x \t J_n(x)` to `besselSeriesPlotn0.txt`.

---

## Output File Format

* **`besselSeriesPlotn0.txt`**: Two-column tab-separated ASCII file containing 101 rows for $x = 0.0, 0.1, 0.2, \dots, 10.0$:

  ```text
  0.000000	1.000000
  0.100000	0.997502
  0.200000	0.990025
  ...
  ```
