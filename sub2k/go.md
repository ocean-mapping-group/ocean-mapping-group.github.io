---
layout: default
title: go
parent: Submetrix ISIS (sub2k) Interferometric Sonar Tools
nav_order: 6
tool_name: go
source_path: sub2k/go
category: sub2k
input_formats: []
output_formats:
  - wraps (asciiplot data)
  - plot.meta (OMG metafile)
related_tools:
  - testWrap
  - gox
  - wraps
---

# `go` — Vernier Interferometer Phase-Wrap Simulation Script

## Overview

`go` is an 8-line shell script in `sub2k/` that executes [`testWrap`](testWrap.html) using a here-document (`<< eno`) supplying three receive stave spacing baselines (`3.5`, `6.75`, and `8.5` acoustic wavelengths $\lambda$), converts the resulting [`wraps`](wraps.html) output table into an OMG plot metafile (`plot.meta`) via `asciiplot`, and launches the X11 metafile viewer `viewmeta`.

It is used to visualize how a 3-baseline Vernier interferometric sonar unwraps phase across a $\pm 90^\circ$ receive sector when the baseline pair difference $(8.5 - 6.75 = 1.75\lambda)$ and $(6.75 - 3.5 = 3.25\lambda)$ form a Vernier scale.

---

## Usage

```bash
./go
```

---

## CLI Options

`go` takes no command-line arguments. Its parameters are embedded directly in the script:

| Step / Parameter | Value | Description |
| :--- | :--- | :--- |
| `testWrap << eno` | `3.5 6.75 8.5` | Runs `testWrap` in standard angle-sweep mode (`plot_type = 0`) with stave spacings $d_1 = 3.5\lambda$, $d_2 = 6.75\lambda$, and $d_3 = 8.5\lambda$. |
| `asciiplot -infile wraps` | `-infile wraps` | Reads the `wraps` ASCII plot file written by `testWrap` and generates `plot.meta`. |
| `viewmeta plot.meta &` | `plot.meta` | Opens `plot.meta` asynchronously in the OMG `viewmeta` X11 graphics viewer. |

---

## How It Works

The complete source of `sub2k/go` is:

```sh
testWrap << eno
3.5 6.75 8.5
eno

asciiplot -infile wraps

viewmeta plot.meta &
```

1. **Phase-Wrap Calculation (`testWrap`):**
   - `testWrap` reads `d1 = 3.5`, `d2 = 6.75`, `d3 = 8.5` from `stdin`.
   - Because `-xplot` is not passed, `testWrap` sweeps receive angle $\theta$ from $-90^\circ$ to $+90^\circ$ in $0.1^\circ$ increments (1,800 steps) and writes wrapped phase curves (`p1`, `p2`, `p3`), differential phases (`dp12`, `dp23`), and double-difference Vernier phase (`ddp`) into the output file `wraps`.
2. **Metafile Rendering (`asciiplot`):**
   - `asciiplot -infile wraps` reads the `x:` / `y:` header directives and coordinate series from `wraps` and renders `plot.meta`.
3. **Interactive Display (`viewmeta`):**
   - `viewmeta plot.meta &` displays the multi-curve phase plot on screen.

---

## Practical Examples

### Run the Standard Vernier Phase-Wrap Simulation
```bash
cd /path/to/code/sub2k
sh ./go
```
