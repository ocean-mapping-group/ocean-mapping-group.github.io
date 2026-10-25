---
layout: default
title: pdi_funcs
parent: SwathEd (SE) Tools
nav_order: 35
tool_name: pdi_funcs
source_path: code/SE/pdi_funcs.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".WC_Phase1", ".watercol", ".merged"]
output_formats: []
related_tools: ["SE_PDI_LA", "bdi_funcs", "SE_BDI_DP", "SE_WaterColumn", "swathed"]
---

# `pdi_funcs.c` — Phase-Direction Indicator (PDI) Constant-Time-Slice Zero-Crossing Picker

## Overview & Purpose
`pdi_funcs.c` and `pdi_funcs.h` (authored by Leo and John E. Hughes Clarke, October 2019) implement the standalone **Phase-Direction Indicator (PDI)** sub-beam angle refinement algorithm for Kongsberg `.kmall` / `.kmwcd` water-column differential phase data (`<prefix>.WC_Phase1`).

Introduced following the June 2019 USNS *Bowditch* EM124 trials (where Kongsberg `.kmwcd` datagrams began providing full split-beam differential phase time series for every receive beam in addition to amplitude), `pdi_funcs.c` builds directly on top of the amplitude-based **Beam-Direction Indicator (BDI)** picks from [`bdi_funcs.c`](bdi_funcs.md). Whereas conventional multibeam phase detection fixes a receive beam and fits a linear phase ramp across time samples (which fails near normal incidence or on steep/vertical features where the echo is only 1–2 samples long), **PDI operates at a constant Two-Way Travel Time (TWTT) slice across adjacent receive beams**, locating the exact zero-crossing of the split-beam phase difference across the receive array around each BDI amplitude peak.

---

## Core Data Structures (`pdi_funcs.h`)

```c
#define NO_PDI 2

typedef struct {
    float angle;          /* Linearly interpolated zero-crossing arrival angle (degrees) */
    float fit_residual;   /* Residual of the across-beam phase fit */
    int closest_beam;     /* Receive beam index closest to the pick */
    int sector_no;        /* Transmit sector ID */
} a_PDI_pick;

a_PDI_pick WC_PDI_pick[J_EM_WC_MAX_WC_TRACE_LENGTH][NO_PDI];
```

---

## Key Function

| Function | Signature | Description |
|---|---|---|
| `after_BDI_PDI_pick_Angle_Peaks` | `int after_BDI_PDI_pick_Angle_Peaks(j_EM_watercolumn *WHOLE_ping_WCP, a_BDI_pick *WC_BDI_pick, a_PDI_pick *WC_PDI_pick, int first_arrival, int MAX_length_WC_TimeSeries)` | Scans every TWTT time slice from `first_arrival` to `MAX_length_WC_TimeSeries - 1`. Wherever a valid BDI amplitude peak exists (`WC_BDI_pick[this_TWTT][j].angle != 0`), extracts the 5 across-array phase samples centered on `bpick->closest_beam` from `WHOLE_ping_WCP`, identifies the adjacent beam pair straddling $0^\circ$ phase difference, and computes the linearly interpolated zero-crossing angle `ppick->angle`. |

---

## The Constant-TWTT Phase Zero-Crossing Algorithm

For each time slice `this_TWTT > first_arrival` and each candidate BDI peak `j` (`0 .. NO_BDI - 1`):

1. **BDI Seed Gate:** Checks whether `bpick = &WC_BDI_pick[this_TWTT][j]` has a non-zero `bpick->angle`. Time slices without an initial BDI amplitude detection are skipped.
2. **5-Beam Across-Array Phase Extraction:** Extracts 5 split-beam phase samples at the **exact same TWTT sample index** (`this_TWTT`) across the 5 receive beams `bpick->closest_beam - 2` through `bpick->closest_beam + 2` from the water-column phase structure `WHOLE_ping_WCP`:
   $$\phi_k = \text{ (signed char) }\texttt{WHOLE\_ping\_WCP->watercols[closest\_beam + kk].ts\_ampl[this\_TWTT]} \times \frac{180^\circ}{128}$$
   and retrieves each beam's pointing angle $\theta_k$ (`beam_pointing_angle / 100.0`) for $k \in \{0, 1, 2, 3, 4\}$ (`kk = -2 .. +2`).
3. **Zero-Crossing Pair Detection:** Scans the 4 adjacent beam intervals `(kk, kk+1)` for a sign change across $0^\circ$ phase (either a positive-slope crossing $\phi_k < 0 \land \phi_{k+1} > 0$ or a negative-slope crossing $\phi_k > 0 \land \phi_{k+1} < 0$), recording the straddling index `cenpair = kk`.
4. **Inverse-Phase Linear Interpolation:** If a zero-crossing pair `cenpair` is found, computes the exact sub-beam arrival angle `PDI_angle` via linear interpolation between $\theta_{\text{cenpair}}$ and $\theta_{\text{cenpair}+1}$:
   $$w_1 = \frac{\phi_{\text{cenpair}+1}}{\phi_{\text{cenpair}+1} - \phi_{\text{cenpair}}}, \qquad w_2 = \frac{-\phi_{\text{cenpair}}}{\phi_{\text{cenpair}+1} - \phi_{\text{cenpair}}}$$
   $$\theta_{\text{PDI}} = w_1 \, \theta_{\text{cenpair}} + w_2 \, \theta_{\text{cenpair}+1}$$
   and stores the result in `WC_PDI_pick[this_TWTT][j].angle`.

---

## Integration within `swathed`
- **Interactive Water Column Phase Inspection ([`SE_PDI_LA.c`](SE_PDI_LA.md) & [`SE_WaterColumn.c`](SE_WaterColumn.md)):** When `.WC_Phase1` is loaded (`GOT_WCP == 1` in [`SE_omgIOwin.c`](SE_omgIOwin.md)), `after_BDI_PDI_pick_Angle_Peaks()` is invoked after BDI peak picking so the user can compare BDI amplitude parabola picks (`WC_BDI_pick`) directly against PDI across-beam phase zero-crossing picks (`WC_PDI_pick`) on the 2D water-column fan and constant-time-slice diagnostic plots.
