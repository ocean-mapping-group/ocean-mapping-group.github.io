---
layout: default
title: bdi_funcs
parent: SwathEd (SE) Tools
nav_order: 31
tool_name: bdi_funcs
source_path: code/SE/bdi_funcs.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".watercol", ".merged"]
output_formats: []
related_tools: ["applyBDI", "SE_BDI_DP", "pdi_funcs", "SE_PDI_LA", "swathed"]
---

# `bdi_funcs.c` — Standalone Beam-Direction Indicator (BDI) Peak-Picking & Filtering Library

## Overview & Purpose
`bdi_funcs.c` and `bdi_funcs.h` (authored by Douglas Bergersen and John E. Hughes Clarke, July 2015) implement the core mathematical algorithms for **Beam-Direction Indicator (BDI)** bottom detection on multibeam water-column fans (`j_EM_watercolumn`).

Shared between the interactive SwathEd BDI analysis window ([`SE_BDI_DP.c`](SE_BDI_DP.md)), the phase-zero-crossing PDI picker ([`pdi_funcs.c`](pdi_funcs.md)), and the batch command-line processor ([`applyBDI.c`](applyBDI.md)), `bdi_funcs.c` processes a full ping's water-column amplitude matrix (`WHOLE_ping_WC`) slice-by-slice in constant Two-Way Travel Time (TWTT) to extract sub-beam-width angular seafloor arrivals.

---

## Core Data Structures & Constants (`bdi_funcs.h`)

```c
#define NO_BDI 2

typedef struct {
    float angle;        /* Interpolated local-level arrival angle (degrees) */
    float Highest_dB;   /* Peak amplitude (dB) at closest_beam */
    float peak_width;   /* Angular width of the peak */
    int closest_beam;   /* Index of the receive beam with local maximum amplitude */
    int sector_no;      /* Transmit sector ID (Tx_sector_no) of closest_beam */
} a_BDI_pick;

a_BDI_pick WC_BDI_pick[J_EM_WC_MAX_WC_TRACE_LENGTH][NO_BDI];
```

- **Peak-Picking Algorithm Constants (`DP_Which_Peak_Picking_Algorithm`):**
  - `DP_LINEAR_WEIGHTING` (`0`)
  - `DP_3_POINT_PARABOLA` (`1`) — Exact 3-beam Lagrange parabolic vertex interpolation.
  - `DP_5_POINT_PARABOLA` (`2`) — 5-beam least-squares parabolic regression ($3 \times 3$ normal matrix inversion).

---

## Key Functions

| Function | Signature | Description |
|---|---|---|
| `DL_pick_parabola_centre` | `float DL_pick_parabola_centre(float *samples, float *angles, int nosamples, int algorithm, int *sector)` | Fits a parabola $y(\theta) = a\theta^2 + b\theta + c$ to 3 or 5 adjacent beam amplitudes `samples[]` and pointing angles `angles[]` (verifying first that all beams belong to the same transmit `sector[]` to avoid sector-boundary phase/amplitude discontinuities) and returns the sub-beam peak angle $\theta_{\text{peak}} = -b / (2a)$. |
| `standalone_BDI_pick_Angle_Peaks` | `int standalone_BDI_pick_Angle_Peaks(j_EM_watercolumn *WHOLE_ping_WC, a_BDI_pick *WC_BDI_pick, ...)` | Executes the full 5-stage BDI detection pipeline across all TWTT time slices (`0 .. MAX_length_WC_TimeSeries - 1`): Minimum Slant Range ($R_0$) estimation, adaptive/manual thresholding, 1st and 2nd angular peak extraction, 3/5-point parabolic refinement, automatic/manual outlier filtering, and optional virtual-beam compression. |

---

## The 5-Stage BDI Algorithm (`standalone_BDI_pick_Angle_Peaks`)

### Stage 1: Local Peak Scan & Minimum Slant Range ($R_0$) Detection
For every TWTT sample index `this_TWTT`:
- Scans across all receive beams `i` (`0 .. total_no_receive_beams - 1`) to identify local amplitude maxima (`peak_dB[this_TWTT][i]`), including flat-topped peaks spanning up to 5 adjacent beams.
- Tracks the highest peak (`max_peak_dB`) and second-highest peak (`second_max_peak_dB`), along with the slice mean peak level `mean_peak_dB[this_TWTT]`.
- Computes a 21-sample running standard deviation of `mean_peak_dB` (for `this_TWTT >= 50` where at least 3 peaks exist per slice); the TWTT slice with the maximum standard deviation jump (`max_std_dev`) minus 5 samples defines the **Minimum Slant Range** (`min_slant_range`, i.e., normal-incidence first bottom arrival $R_0$).

### Stage 2: Adaptive vs. Manual Thresholding & Peak Selection
- **Automatic Threshold (`aut_threshold == 1`):** Compares `mean_peak_dB[this_TWTT]` against the $45\%–55\%$ window between `min_peak_dB` and `max_peak_dB`. When skewed by a strong seafloor return, sets `WC_BDI_variable_threshold[this_TWTT] = max_peak_dB - 0.15 * (max_peak_dB - min_peak_dB)`.
- **Manual Threshold (`aut_threshold == 0`):** Computes a linear threshold line with slope `WC_BDI_threshold_slope`.
- Retains the highest peak in `WC_BDI_pick[this_TWTT][0]` if it exceeds the threshold, and (if `second_peak == 1`) retains the second-highest peak in `WC_BDI_pick[this_TWTT][1]` provided it is separated by at least 4 receive beams from the primary peak.

### Stage 3: Parabolic Sub-Beam Angle Refinement
If `DP_BDI_pick_better == 1`, extracts the 3 or 5 beam amplitudes and pointing angles centered on `closest_beam` for each valid pick and calls `DL_pick_parabola_centre()` to refine `WC_BDI_pick[this_TWTT][0..1].angle`.

### Stage 4: Pre-MSR Blank & Outlier Filtering
1. Rejects all solutions prior to `min_slant_range` (`this_TWTT <= min_slant_range`).
2. Estimates initial water depth `crude_depth` from the first valid detection after `min_slant_range`.
3. **Automatic Footprint Filter (`filter_automatic == 1`):** For each receive beam `this_beam`, calculates the non-overlapping angular footprint $\left[\frac{\theta_{i-1}+\theta_i}{2}, \frac{\theta_i+\theta_{i+1}}{2}\right]$, projects it onto a flat seafloor at `crude_depth` to find the theoretical number of time samples `allowable_number_of_solutions[this_beam] = ceil(num_samples * 1.25)`, computes the intensity-weighted mean sample index `mean_solutions` ($w = 10^{\text{dB}/10}$), and iteratively rejects the farthest outlier until all remaining BDI picks for that beam fall within $\text{MEAN} \pm \text{MAX}/2$.
4. **Manual Std-Dev Filter (`filter_manual == 1`):** Linearly interpolates `allowable_std_dev_solutions[this_beam]` from `1.5` samples at nadir (`beam_of_smallest_angle`) to `filterindex` at the outer swath edge (`beam_of_greatest_angle`), iteratively removing the farthest pick until the amplitude-weighted standard deviation is below the limit.

### Stage 5: Equidistant Virtual-Beam Compression (`compression == 1`)
Divides the total across-track swath width at `crude_depth` into `number_of_virtual_beams` (default `400`) equidistant horizontal bins (`virtual_beam_edge1[ww] .. virtual_beam_edge2[ww]`), and collapses all BDI picks falling within each virtual beam into a single amplitude-weighted mean `(abs_mean_solutions_twtt, mean_solutions_angle)` solution.
