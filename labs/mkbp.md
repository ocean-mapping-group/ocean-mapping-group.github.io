---
layout: default
title: mkbp
parent: labs (Teaching & Coursework Labs)
nav_order: 3
tool_name: mkbp
source_path: code/labs/mkbp.c
category: Educational Labs & Transducer Array Acoustics (labs)
input_formats:
  - Interactive stdin prompts (frequency, array type, dimensions, element shading)
output_formats:
  - ASCII 4-column beam pattern table (Angle, Pressure, Intensity, LogIntensity)
related_tools:
  - mkbp_skeleton
  - bpdemo
  - dobessel
  - plotTxRxOverlap
---

# mkbp

## Overview
`mkbp` (`code/labs/mkbp.c`, authored by John Hughes Clarke in February 2000) is an interactive command-line acoustic transducer beam pattern calculator used in Ocean Mapping Group (OMG) hydrographic acoustics courses. It computes the far-field directivity pattern across 1,800 angular steps from $-90.0^\circ$ to $+89.9^\circ$ (in $0.1^\circ$ increments) assuming a nominal water sound speed of $c = 1500.0\text{ m/s}$, and outputs normalized acoustic pressure, intensity, and logarithmic intensity to an ASCII file.

`mkbp.c` is the complete reference implementation corresponding to the student assignment template [`mkbp_skeleton`](mkbp_skeleton.md).

---

## Compilation & CLI Syntax

```bash
# Compile with the standard math library (-lm required for j1() Bessel function)
cc mkbp.c -o mkbp -lm

# Run interactively and write beam pattern to ASCII file
mkbp [-v] [-mag] [-depth <val>] [-in <paramfile>] -out <beam_pattern.txt>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-out <filename>` | **Required.** Path to the output 4-column ASCII beam pattern file. | None |
| `-mag` | For discrete line arrays (`array_type == 3`), compute the full complex phasor magnitude $\sqrt{(\sum R)^2 + (\sum I)^2}$ rather than only the real part $\sum R$. | `0` (Real sum only) |
| `-depth <meters>` | Optional depth parameter parsed from the command line (`-depth` demonstration flag). | `10.0` |
| `-in <filename>` | Optional parameter filename pointer (parsed on CLI; interactive `scanf` prompts are used by default). | Unused |
| `-v` | Enable verbose mode (`verbose_flag++`). | `0` |

---

## Interactive Prompts & Acoustic Array Formulations

Upon startup, `mkbp` prompts the user on `stdin` for the acoustic frequency $f$ (in Hz), computes wavelength $\lambda = \frac{1500.0}{f}\text{ m}$, and asks the user to select one of three transducer array geometries:

### 1. Circular Planar Piston (`CIRC_PLANE = 1`)
Prompts for piston diameter $D$ (in meters). For each angle $\theta \in [-90^\circ, +90^\circ)$, `mkbp` evaluates the theoretical far-field directivity of a baffled circular piston using the first-order Bessel function of the first kind $J_1(x)$ (`j1()` in `<math.h>`):

$$k_{\text{const}} = \frac{\pi D}{\lambda}, \qquad P(\theta) = \frac{2\, J_1\!\left(k_{\text{const}} \sin\theta\right)}{k_{\text{const}} \sin\theta}$$

*(Note: In `mkbp.c` line 214, an undeclared diagnostic variable `bessel = j1(Const);` is present; removing or declaring `double bessel;` allows clean compilation on modern C compilers).*

### 2. Continuous Line Array (`CONT_LINE = 2`)
Prompts for line length $L$ (in meters). Evaluates the $\text{sinc}$ directivity function of a uniform continuous line source:

$$k_{\text{const}} = \frac{\pi L}{\lambda}, \qquad P(\theta) = \frac{\sin\!\left(k_{\text{const}} \sin\theta\right)}{k_{\text{const}} \sin\theta}$$

### 3. Discrete Multi-Element Line Array (`DISCRETE_LINE = 3`)
Prompts for:
1. Element center-to-center spacing $d$ (`elem_spacing`, in meters).
2. Number of elements $N$ (`no_elements`, up to 100).
3. Amplitude shading weight $w_j$ (`shading[j]`) for each element $j = 0, \dots, N-1$ (e.g., uniform, binomial, Dolph-Chebyshev, or Hanning weights).
4. Diameter $D$ of the individual elements (in meters).

For each look angle $\theta$, `mkbp` accumulates the real and imaginary phasor components across all $N$ elements:

$$\Delta r_j = j \cdot d \cos\theta, \qquad \Delta\phi_j = \frac{2\pi\,\Delta r_j}{\lambda}$$

$$R(\theta) = \sum_{j=0}^{N-1} w_j \cos(\Delta\phi_j), \qquad I(\theta) = \sum_{j=0}^{N-1} w_j \sin(\Delta\phi_j)$$

If `-mag` is specified, $P_{\text{array}}(\theta) = \sqrt{R(\theta)^2 + I(\theta)^2}$; otherwise $P_{\text{array}}(\theta) = R(\theta)$ (which illustrates phase asymmetry if the phase reference is placed at element $j=0$ instead of the array center). Finally, the **Product Theorem** multiplies the array factor by the individual element response `element_pressure[i]`.

---

## Normalization & Output Format

After sweeping all 1,800 angles, `mkbp` normalizes pressure by the maximum absolute pressure $P_{\max} = \max_\theta |P(\theta)|$ and writes 1,800 lines to `-out`:

```text
<Angle_deg> <Normalized_Pressure> <Normalized_Intensity> <LogInt>
```
where:
* `Angle[i]` $= (i - 900)/10.0$ degrees ($-90.0^\circ$ to $+89.9^\circ$).
* `Pressure[i]` $= P(\theta_i) / P_{\max}$.
* `Intensity[i]` $= \left(\text{Pressure}[i]\right)^2$.
* `LogInt[i]` $= 10.0 \ln(\text{Intensity}[i])$ *(note: uses natural log `log()` in C; use `log10()` for standard decibels $\text{dB}$).*

---

## Example Usage (Scripted Input)

```bash
# Compute beam pattern of a 0.30 m continuous line array at 100 kHz
mkbp -out line_100kHz.bp <<EOF
100000
2
0.30
EOF
```
To interactively visualize these array patterns and side-lobe shading effects in an X11 GUI, see [`bpdemo`](../bpdemo/bpdemo.md).
