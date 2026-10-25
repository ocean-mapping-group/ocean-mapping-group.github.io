---
layout: default
title: mkbp_skeleton
parent: Graduate Course Lab Exercises (labs)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 4
tool_name: mkbp_skeleton
source_path: code/labs/mkbp_skeleton.c
category: Educational Labs & Transducer Array Acoustics (labs)
input_formats:
- Interactive stdin prompts (frequency, array type, dimensions, element shading)
output_formats:
- ASCII 4-column beam pattern table (Angle, Pressure, Intensity, LogIntensity)
related_tools:
- mkbp
- bpdemo
- dobessel
---

# mkbp_skeleton

## Overview
`mkbp_skeleton` (`code/labs/mkbp_skeleton.c`, authored by John Hughes Clarke in February 2000) is the student assignment skeleton for the [`mkbp`](mkbp.html) acoustic beam pattern modeling lab. It provides the complete command-line parser, interactive parameter acquisition (`scanf`), angular sweep loop ($-90.0^\circ$ to $+89.9^\circ$ in $0.1^\circ$ increments), bore-sight pressure normalization, and 4-column ASCII output formatting (`xmgr` / Excel compatible), while leaving the core acoustic directivity equations blank for students to implement.

---

## Syntax & CLI Options

```bash
# Compile after completing the student exercise sections
cc mkbp_skeleton.c -o mkbp -lm

# Run with output file specified
mkbp [-v] [-mag] [-depth <val>] [-in <paramfile>] -out <beam_pattern.txt>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-out <filename>` | **Required.** Output ASCII file path for the 1,800-point beam pattern table. | None |
| `-mag` | Use complex magnitude $\sqrt{\text{real\_sum}^2 + \text{imag\_sum}^2}$ for discrete array summation (`use_mag++`). | `0` (Real component only) |
| `-depth <meters>` | Sample CLI floating-point argument demonstrating `atof()` parsing. | `10.0` |
| `-in <filename>` | Optional input parameter file name (scaffolded in CLI parser, commented out in file open block). | None |
| `-v` | Enable verbose output (`verbose_flag++`). | `0` |

---

## Student Implementation Tasks in `mkbp_skeleton.c`

Students are instructed to fill in five specific sections of `code/labs/mkbp_skeleton.c`:

### Task 1: Circular Planar Piston (`CIRC_PLANE = 1`, Lines 216–230)
Replace the placeholder `Pressure[i] = cos(angle);` with the baffled circular piston directivity formula using the first-order Bessel function `j1()` from `<math.h>`:

```c
Const = M_PI * Diameter / wavelength;
if (angle == 0.0)
    Pressure[i] = 1.0;
else
    Pressure[i] = 2.0 * j1(Const * sin(angle)) / (Const * sin(angle));
```

### Task 2: Continuous Line Array (`CONT_LINE = 2`, Lines 232–240)
Implement the continuous line source $\text{sinc}$ solution for array length $L$ (`Length`):

```c
Const = M_PI * Length / wavelength;
if (angle == 0.0)
    Pressure[i] = 1.0;
else
    Pressure[i] = sin(Const * sin(angle)) / (Const * sin(angle));
```

### Task 3: Shaded Discrete Line Array Summation (`DISCRETE_LINE = 3`, Lines 241–260)
Inside the `for (j = 0; j < no_elements; j++)` loop, calculate the extra acoustic path length $\Delta r_j$ and phase offset $\Delta\phi_j$ for each element $j$, referencing phase zero either to element $0$ or to the geometric center of the array $(N-1)/2$ so that a wave crest arriving at bore-sight ($\theta = 0^\circ$) sums constructively:

```c
extra_path = ((double)j - (double)(no_elements - 1) / 2.0) * elem_spacing * sin(angle);
dphase = 2.0 * M_PI * extra_path / wavelength;
real_sum += cos(dphase) * shading[j];
imag_sum += sin(dphase) * shading[j];
```

### Task 4: Individual Element Pattern & Product Theorem (Lines 262–268)
Compute `element_pressure[i]` for an individual circular element of diameter `Diameter`, and multiply the array factor `Pressure[i]` by `element_pressure[i]` according to the **Array Product Theorem**:

$$B_{\text{total}}(\theta) = B_{\text{array}}(\theta) \times B_{\text{element}}(\theta)$$

### Task 5: $-3\text{ dB}$ Beamwidth Search (Lines 295–298)
Search outward from the bore-sight bin (`i = 900`, $\theta = 0.0^\circ$) to find the half-power points where `Intensity[i]` drops to $0.5$ (or `LogInt[i]` drops by $-3.01\text{ dB}$) and store the total angular width in `beamwidth`.

---

## Output Format

Once completed and executed, `mkbp_skeleton` writes 1,800 rows covering $[-90.0^\circ, +89.9^\circ]$ to `-out`:

```text
Angle_deg   Normalized_Pressure   Normalized_Intensity   Log_Intensity
```
See [`mkbp`](mkbp.html) for the completed reference code and [`bpdemo`](../bpdemo/BPdemo.html) for the interactive graphical beam-pattern simulator.
