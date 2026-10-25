---
layout: default
title: gox
parent: GeoSwath+ / Submetrix 2000 CLI (sub2k)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 7
tool_name: gox
source_path: sub2k/gox
category: sub2k
input_formats: []
output_formats:
- wraps (asciiplot data)
- plot.meta (OMG metafile)
related_tools:
- testWrap
- go
- wraps
---

# `gox` — Vernier Interferometer Cross-Phase Trajectory Script

## Overview

`gox` is an 8-line shell script in `sub2k/` that executes [`testWrap`](testWrap.html) with the `-xplot` flag using a here-document (`<< eno`) supplying three stave baselines (`3.0`, `6.00`, and `8.5` wavelengths $\lambda$), plots the resulting 2D phase-difference trajectory in [`wraps`](wraps.html) as discrete points via `asciiplot -points -infile wraps`, and launches `viewmeta plot.meta &`.

Whereas [`go`](go.html) plots wrapped phase as a function of arrival angle $\theta$, `gox` plots the **2D phase-space locus** (`dp12` on the X-axis vs. `dp23` on the Y-axis) across 5,000 steps of $\sin(\theta) \in [-1, +1]$. In this 2D phase space, an interferometric sonar's ambiguity resolution corresponds to identifying which diagonal stripe a noisy `(dp12, dp23)` measurement lies closest to.

---

## Usage

```bash
./gox
```

---

## CLI Options

`gox` takes no command-line arguments. Its internal pipeline is configured as follows:

| Step / Parameter | Value | Description |
| :--- | :--- | :--- |
| `testWrap -xplot << eno` | `3.0 6.00 8.5` | Runs `testWrap` in cross-plot mode (`plot_type = 1`) with stave spacings $d_1 = 3.0\lambda$, $d_2 = 6.00\lambda$, and $d_3 = 8.5\lambda$. |
| `asciiplot -points -infile wraps` | `-points -infile wraps` | Renders the 5,000 `(dp12, dp23)` coordinates in `wraps` as a scatter/point plot in `plot.meta` (avoiding wrap-around connecting lines when phase jumps from $+180^\circ$ to $-180^\circ$). |
| `viewmeta plot.meta &` | `plot.meta` | Launches the OMG X11 metafile viewer in the background. |

---

## How It Works

The complete source of `sub2k/gox` is:

```sh
testWrap -xplot << eno
3.0 6.00 8.5
eno

asciiplot -points -infile wraps

viewmeta plot.meta &
```

1. **Cross-Phase Locus Generation (`testWrap -xplot`):**
   - `testWrap` sets `plot_type = 1` when `-xplot` is passed on the command line.
   - It reads `d1 = 3.0`, `d2 = 6.00`, `d3 = 8.5` from `stdin`.
   - It steps `sin_theta` from `-1.0` to `+1.0` in increments of `0.0004` (5,000 points), computing wrapped phase differences `dp12` and `dp23` in degrees (`[-180.0, +180.0]`) and writing them to `wraps`.
2. **Scatter Plot Rendering (`asciiplot -points`):**
   - Because `dp12` and `dp23` wrap discontinuously at $\pm 180^\circ$, drawing continuous polylines would create false retrace lines across the plot. Passing `-points` to `asciiplot` plots each of the 5,000 samples as an individual point.

---

## Practical Examples

### Generate and View the 2D Phase-Difference Locus

```bash
cd /path/to/code/sub2k
sh ./gox
```
