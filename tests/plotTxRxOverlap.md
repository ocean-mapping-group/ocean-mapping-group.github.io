---
layout: default
title: plotTxRxOverlap
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 11
tool_name: plotTxRxOverlap
source_path: code/tests/plotTxRxOverlap.c
category: Backscatter & Transducer Array Acoustics (tests)
input_formats:
  - Optional ASCII input file (-infile) or internal 200-point synthetic cosine beam patterns
output_formats:
  - plot_001.meta .. plot_036.meta (36 OMG plotlib vector graphics metafiles)
related_tools:
  - mkbp
  - bpdemo
  - EKlook
  - BatchProcEK
---

# plotTxRxOverlap

## Overview
`plotTxRxOverlap` (`code/tests/plotTxRxOverlap.c`, authored by John Hughes Clarke in September 2023) is a vector-graphics animation generator built on the OMG `plotlib` library (`plot_open`, `plot_pen`, `plot_move`, `plot_line`, `plot_close`). It models and visualizes the radiometric impact of angular misalignment (`shift`) between a sonar's Transmit (`Tx`) and Receive (`Rx`) beam patterns—such as rotational pitch/roll offset or split-beam sector misalignment on Simrad EK60/EK80 or multibeam transducers.

In a single execution, `plotTxRxOverlap` sweeps through 36 angular shift frames (`k = 0, 10, 20, ..., 350`, corresponding to `shift` values from `-75` to `+70` across a 200-point swath) and writes 36 OMG `plotlib` metafiles named `plot_001.meta` through `plot_036.meta`.

---

## Syntax & CLI Options

```bash
plotTxRxOverlap [-shift <bins>] [-width <val>] [-size <dx_cm> <dy_cm>] [-sparse] [-infile <file>]
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-size <dx> <dy>` | Plot canvas width (`dx`) and height (`dy`) in centimeters passed to `plot_open(dx, dy, synname)`. Requires **two** floating-point arguments. | `40.0 20.0` |
| `-shift <int>` | Initial integer bin shift between Tx and Rx beam patterns (subsequently overridden by the 36-frame loop `shift = ((k/360.0) - 0.5) * 150.0`). | `-50` |
| `-width <float>` | Total swath width plotted (parsed on CLI; initialized inside the frame loop to `nopoints = 200`). | `200.0` |
| `-sparse` | Set `sparse_flag = 1` to suppress title/label text rendering. | `0` |
| `-infile <file>` | Optional input file opened for reading (`grazfile`); if omitted, prints `warning reading input from stdin` and uses the internal cosine beam pattern model. | `stdin` (unused in loop) |

---

## Beam Pattern Overlap & Gain Mismatch Model

### 1. Synthetic Tx and Rx Beam Patterns (Upper Panel)
Across `nopoints = 200` angular bins ($j \in [0, 199]$, mapped to $x \in [-100, +99]$), both the Transmit (`txBP`) and Receive (`rxBP`) beam patterns are modeled as $10\text{ dB}$ cosine arches peaking at $0\text{ dB}$ at bore-sight ($j = 100$) and dropping to $-10\text{ dB}$ at the swath edges ($j = 0, 200$):

$$\text{txBP}[j] = \text{rxBP}[j] = 10.0 \cos\!\left(\frac{j - 100}{100.0} \cdot \frac{\pi}{2}\right) - 10.0\text{ dB}$$

In the upper plot viewport (`yoff = 0.55 * dy`, Y-range $[-10, 0]\text{ dB}$):
* The stationary Receive beam pattern $\text{rxBP}[j]$ is drawn as a triple-thick **blue** curve (`plot_pen(3)`).
* The shifted Transmit beam pattern $\text{txBP}[j]$ is drawn at angular index $j + \text{shift}$ (for $0 \le j + \text{shift} < 200$) as a triple-thick **red** curve (`plot_pen(1)`).

### 2. Gain Mismatch & Mean Swath Gain Loss (Lower Panel)
In the lower plot viewport (`yoff = 0.05 * dy`, Y-range $[-10, +10]\text{ dB}$), for every overlapping bin $j$ where $0 \le j - \text{shift} < 200$, `plotTxRxOverlap` calculates the decibel difference between the shifted Tx beam and the nominal Rx/Tx beam at angle $j$:

$$\Delta G_{\text{dB}}[j] = \text{txBP}[j - \text{shift}] - \text{rxBP}[j]$$

As documented in the inline verification block (lines 272–292), because $\text{rxBP}[j] = \text{txBP}[j]$, this dB subtraction equals the ratio between the actual misaligned two-way product ($G_{\text{Tx,shifted}} \cdot G_{\text{Rx}}$) and the assumed aligned two-way product ($G_{\text{Tx,aligned}} \cdot G_{\text{Rx}}$):

$$10 \log_{10}\!\left(\frac{G_{\text{Tx}}[j - \text{shift}] \cdot G_{\text{Rx}}[j]}{G_{\text{Tx}}[j] \cdot G_{\text{Rx}}[j]}\right) = \text{txBP}[j - \text{shift}] - \text{txBP}[j]$$

Each bin's $\Delta G_{\text{dB}}[j]$ is plotted as a red diamond symbol (with a large blue diamond at nadir $j = 100$). The linear power ratios are averaged across all `count` overlapping bins and converted back to decibels:

$$\overline{G}_{\text{dB}} = 10 \log_{10}\!\left(\frac{1}{N_{\text{overlap}}} \sum_{j} 10^{\Delta G_{\text{dB}}[j] / 10}\right)$$

which is drawn as a horizontal blue line with a central diamond across the overlapping swath sector $[j_{\min}, j_{\max}]$.

---

## Example Usage

```bash
# Generate the 36-frame metafile sequence (plot_001.meta .. plot_036.meta)
plotTxRxOverlap -size 30.0 20.0
```
The resulting `.meta` files can be rendered to X11, PostScript, or GIF using the tools in [`plotlib`](../plotlib/index.md).
