---
layout: default
title: tide_intp_sub
parent: Tide Tools
tool_name: tide_intp_sub
source_path: code/tide/tide_intp_sub.c
category: tide
input_formats: ["C function arguments (z0, z1, xx, yy)"]
output_formats: ["Interpolated tide height (*zz)"]
related_tools: ["mergeTide", "diffTide"]
---

# tide_intp_sub

## Overview

`tide_intp_sub` (`code/tide/tide_intp_sub.c`) is a C subroutine module defining `tide_intp(z0, z1, xx, yy, zz)`, which performs two-station linear spatial tide interpolation by projecting a vessel's position `(xx, yy)` onto the baseline connecting a South-East tide station `(x0, y0)` and a North-West tide station `(x1, y1)`.

This algorithm is the prototype for the `-interpolate` two-station cotidal interpolation built directly into [`mergeTide`](mergeTide.md).

---

## Function Signature & Parameters

```c
void tide_intp(float z0, float z1, float xx, float yy, float *zz);
```

| Parameter | Type | Description |
|---|---|---|
| `z0` | `float` | Contemporaneous tide elevation at the South-East station `(x0, y0)` (default hardcoded prototype coordinates: `43.66°N, -59.25°E`). |
| `z1` | `float` | Contemporaneous tide elevation at the North-West station `(x1, y1)` (default hardcoded prototype coordinates: `45.25°N, -61.75°E`). |
| `xx` | `float` | Latitude of the computation / vessel point. |
| `yy` | `float` | Longitude of the computation / vessel point. |
| `zz` | `float *` | Output pointer receiving the spatially interpolated tide value. |

---

## How It Works

1. **Baseline Vector Calculation:**
   - Computes the angular distance $d_0$ and azimuth $\phi_0$ between Station 0 $(x_0, y_0)$ and Station 1 $(x_1, y_1)$:
     $$d_0 = \sqrt{(x_1 - x_0)^2 + (y_1 - y_0)^2}, \quad \phi_0 = \arctan\left(\frac{y_1 - y_0}{x_1 - x_0}\right)$$
2. **Vessel Vector & Baseline Projection:**
   - Computes the distance $d_d$ and azimuth $\phi$ from Station 0 $(x_0, y_0)$ to the vessel $(xx, yy)$:
     $$d_d = \sqrt{(xx - x_0)^2 + (yy - y_0)^2}, \quad \phi = \arctan\left(\frac{yy - y_0}{xx - x_0}\right)$$
   - Projects $d_d$ onto the inter-station baseline vector:
     $$d_s = d_d \cos(|\phi - \phi_0|)$$
3. **Linear Interpolation:**
   - Evaluates the interpolated tide along the baseline:
     $$zz = z_0 + \frac{d_s}{d_0}(z_1 - z_0)$$

---

## Examples

In production command-line workflows, invoke this algorithm via [`mergeTide`](mergeTide.md) using the `-interpolate`, `-loc1`, and `-loc2` flags:

```bash
mergeTide \
    -interpolate \
    -tide station_SE.bin -loc1 43.66 -59.25 \
    -tide2 station_NW.bin -loc2 45.25 -61.75 \
    merged/JD180/*.merged
```

---

## Workflow Context

- Embedded directly into [`mergeTide`](mergeTide.md) (`-interpolate`) for cotidal zoning between two bounding tide gauges.
