---
layout: default
title: drawCustom
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 4
tool_name: drawCustom
source_path: code/tests/drawCustom.c
category: Attitude Error & Geometry Plotting (tests)
input_formats:
- Command-line flags only (no input file read)
output_formats:
- draw.ascii (or custom ASCII multi-curve plot file for OMG plot utilities)
related_tools:
- testrot
- twistVRU
- DelayEditor
---

# drawCustom

## Overview
`drawCustom` (`code/tests/drawCustom.c`, authored by John Hughes Clarke in August 1994) is a specialized curve generator that writes multi-column ASCII plot files formatted for the OMG `plot` / `plotlib` suite. It models how vessel attitude and positioning uncertainties translate into angular or spatial sounding errors across two selectable modes:

1. **Default (`YAW = 0`) Mode:** Computes the apparent yaw/azimuth angle error $\Delta\alpha = \arctan(\Delta X / R)$ in degrees as a function of slant range $R \in [1, 499]\text{ m}$ for nine fixed horizontal position/cross-track offsets $\Delta X \in \{-10, -5, -2, -1, 0, +1, +2, +5, +10\}\text{ m}$.
2. **Pitch (`-pitch`, `PITCH = 1`) Mode:** Computes the along-track horizontal displacement error $\Delta X = 100 \tan(\theta_p)$ and vertical depth error $\Delta Z = 100 (1 - \cos\theta_p)$ at a nominal $100\text{ m}$ depth for pitch angles $\theta_p \in [0.01^\circ, 4.99^\circ]$ in $0.01^\circ$ steps.

---

## Syntax & CLI Options

```bash
drawCustom [-v] [-pitch | -roll] [-depth <m>] [<dummy_inname> [<outname>]]
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-pitch` | Select `PITCH` (`convert_flag = 1`) mode: generates 2 curves (horizontal and vertical error at $100\text{ m}$ depth vs. pitch angle $0.01^\circ\text{–}4.99^\circ$). | Default is `YAW` (`0`) |
| `-roll` | Select `ROLL` (`convert_flag = 2`) mode *(stub branch in source; produces an empty output file).* | Disabled |
| `-depth <m>` | Parses an integer depth value via `strtoint()` (retained from template CLI). | Unused in equations |
| `-v` | Enable verbose flag (`verbose_flag++`). | `0` |
| `<inname> <outname>` | Positional arguments: the first non-flag argument is assigned to `inname` (not opened) and the second to `outname`. If `<outname>` is omitted, output defaults to `draw.ascii`. | `draw.ascii` |

---

## Mathematical Formulation & Output Structure

### Mode 1: Default (`YAW`, `convert_flag == 0`)
Writes an OMG ASCII plot header specifying a $20.0 \times 15.0\text{ cm}$ canvas, `9` curves, an X-axis range of $[0.0, 500.0]\text{ m}$, nine Y-axis ranges of $[-10.0^\circ, +10.0^\circ]$, and `499` data rows. For each range step $R = 1, 2, \dots, 499\text{ m}$ and each cross-range offset $\Delta X_k \in \{-10, -5, -2, -1, 0, 1, 2, 5, 10\}\text{ m}$, it evaluates:

$$\theta_k(R) = \frac{180}{\pi} \arctan\!\left(\frac{\Delta X_k}{R}\right)$$

*(with $+0.00001^\circ$ added to the $\Delta X = 0$ curve to avoid zero-line suppression in legacy plotters).*

### Mode 2: Pitch Error (`-pitch`, `convert_flag == 1`)
Writes an OMG ASCII plot header specifying a $20.0 \times 15.0\text{ cm}$ canvas, `2` curves, an X-axis pitch range of $[0.0^\circ, 5.0^\circ]$, Curve 1 Y-range $[0.0, 10.0]\text{ m}$, Curve 2 Y-range $[0.0, 0.5]\text{ m}$, and `499` data rows. For each pitch angle $\theta_p = i / 100.0$ degrees ($i = 1, \dots, 499$) at a reference water depth of $D = 100.0\text{ m}$:

$$\Delta X_{\text{horiz}}(\theta_p) = 100.0 \tan\!\left(\theta_p \frac{\pi}{180}\right), \qquad \Delta Z_{\text{vert}}(\theta_p) = 100.0 \left(1.0 - \cos\!\left(\theta_p \frac{\pi}{180}\right)\right)$$

---

## Example Usage

```bash
# 1. Generate default 9-curve range vs. angular error plot in draw.ascii
drawCustom

# 2. Generate pitch horizontal/vertical error curves into pitch_errors.plt
drawCustom -pitch dummy_in pitch_errors.plt
```
