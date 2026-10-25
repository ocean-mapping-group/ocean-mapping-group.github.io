---
layout: default
title: diffTide
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: diffTide
source_path: code/tide/diffTide.c
category: tide
input_formats:
- .nav / .bin (binary jcu_nav_rec tide or navigation files)
output_formats:
- .nav / .bin (binary jcu_nav_rec difference/sum file)
- ASCII horizontal offset (dlat_m dlon_m)
related_tools:
- binTide
- mergeTide
- GrafNav_2_OMG
- posProc_2_OMG
---

# diffTide

## Overview

`diffTide` computes the difference (or sum, via `-addit`) between two binary `jcu_nav_rec` tide files (`-tide1` and `-tide2`), or scales and shifts a single binary tide file if `-tide2` is omitted. It preserves the exact time sampling of `-tide1` and linearly interpolates `-tide2` onto each timestamp of `-tide1`.

Additionally, `diffTide` includes a horizontal navigation comparison mode (`-calc_horiz_diff`) that interpolates the latitude and longitude of `-tide2` onto the timestamps of `-tide1` and outputs the north/south and east/west offsets in meters (`dlat_m dlon_m`).

---

## Syntax & CLI Options

```bash
diffTide [OPTIONS] -tide1 <tide1.bin> [-tide2 <tide2.bin>] -out <out.bin>
```

| Option | Description | Default |
|---|---|---|
| `-tide1 <filename>` | **Required.** Primary binary `jcu_nav_rec` tide/nav file whose timestamps define the output sampling. | None |
| `-tide2 <filename>` | Secondary binary `jcu_nav_rec` tide/nav file to interpolate and subtract from (or add to) `-tide1`. If omitted, `-tide1` is simply shifted by `-base_offset` and scaled by `-atten`. | None |
| `-out <filename>` | **Required.** Output binary `jcu_nav_rec` file (or ASCII `dlat_m dlon_m` file when `-calc_horiz_diff` is enabled). | None |
| `-addit` | Add the interpolated `-tide2` value to `-tide1` (`tide1 + approx_tide2`) instead of subtracting (`tide1 - approx_tide2`). | Subtract |
| `-base_offset <m>` | Constant vertical offset (meters) added to `-tide2` (or to `-tide1` if `-tide2` is omitted). | `0.0` |
| `-atten <factor>` | Amplitude scaling factor multiplied against `-tide2` (or against `tide1 + base_offset` if `-tide2` is omitted). | `1.0` |
| `-delay <mins>` | Time shift in **minutes** added to `-tide1` timestamps when searching `-tide2` (`time += delay * 60.0`). | `0.0` |
| `-delay_sec <secs>` | Additional time shift in **seconds** added to `-tide1` timestamps when searching `-tide2`. | `0.0` |
| `-maxtimegap <secs>` | Maximum allowable time gap (in seconds) between bracketing records in `-tide2` before marking the interpolation invalid. | `1800` (30 min) |
| `-set_invalid_to_zero` | Set output `azi` (tide height) to `0.0` whenever `-tide2` interpolation is invalid (e.g., time gap > `maxtimegap`). | Disabled |
| `-flip_sign` | Negate the final output tide height (`azi = -azi`). | Disabled |
| `-valid_diff_range <min> <max>` | Zero out any resulting difference value that falls outside `[min, max]`. | Disabled |
| `-calc_horiz_diff` | Compare horizontal positions (`lat`, `lon`) between `-tide1` and `-tide2`, writing ASCII `dlat_m dlon_m` (in meters) to `-out`. Requires both `-tide1` and `-tide2`. | Disabled |
| `-v` | Print verbose timestamps, interpolation weights (`w1`, `w2`), and bracketing values. | Disabled |

---

## How It Works

1. **Record Iteration:** Determines the number of `JCU_BINNAV_RECLEN` records in `-tide1` and loops over every record $k$.
2. **Temporal Lookup & Linear Interpolation:**
   - Computes target lookup time $t = t_1 + 60 \cdot \text{delay} + \text{delay\_sec}$.
   - Searches `-tide2` via `nav_time_search_double` for bracketing records $t_{\text{before}}$ and $t_{\text{after}}$.
   - If $0 < t_{\text{after}} - t_{\text{before}} \le \text{maxtimegap}$, computes linear weights:
     $$w_1 = \frac{t - t_{\text{before}}}{t_{\text{after}} - t_{\text{before}}}, \quad w_2 = \frac{t_{\text{after}} - t}{t_{\text{after}} - t_{\text{before}}}$$
   - Computes the adjusted secondary tide:
     $$z_{\text{approx}} = \text{base\_offset} + \text{atten} \cdot (z_{\text{before}} w_2 + z_{\text{after}} w_1)$$
3. **Combination & Filtering:**
   - Updates `tide_rec.azi` as `tide_rec.azi - approx_tide` (or `+ approx_tide` with `-addit`).
   - Applies optional `-flip_sign` and `-valid_diff_range` clamping.
4. **Horizontal Offset Mode (`-calc_horiz_diff`):**
   - Linearly interpolates `lat` and `lon` from `-tide2` (ignoring sentinel `999` values) and converts angular differences to meters:
     $$\Delta y_{\text{m}} = \Delta\text{lat} \times 1852 \times 60, \quad \Delta x_{\text{m}} = \Delta\text{lon} \times 1852 \times 60 \cos(\text{lat})$$

---

## Examples

**1. Subtract predicted gauge tide from RTK GPS elevation to isolate residual surge/ellipsoid offset:**

```bash
diffTide -tide1 rtk_elev.bin -tide2 predicted_tide.bin -out residual_tide.bin
```

**2. Apply a datum offset (+0.45 m) and phase delay (12 minutes) to a single binary tide file:**

```bash
diffTide -base_offset 0.45 -atten 0.96 -tide1 station_a.bin -out station_a_adjusted.bin
```

**3. Compute horizontal position differences (in meters) between two navigation files:**

```bash
diffTide -calc_horiz_diff -tide1 posmv_nav.bin -tide2 grafnav_ppk.bin -out horiz_diff.txt
```

---

## Workflow Context

- **Upstream:** Binary tide/navigation files produced by [`binTide`](binTide.html), [`GrafNav_2_OMG`](GrafNav_2_OMG.html), [`posProc_2_OMG`](posProc_2_OMG.html), or `stripNav`.
- **Downstream:** [`mergeTide`](mergeTide.html) or time-series plotting tools.
