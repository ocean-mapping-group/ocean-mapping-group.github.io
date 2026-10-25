---
layout: default
title: fix_TimeSeries
parent: SwathEd (SE) Tools
nav_order: 33
tool_name: fix_TimeSeries
source_path: code/SE/fix_TimeSeries.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged"]
output_formats: [".merged (updated in-place or via write_out_modified)"]
related_tools: ["SE_W_TimeSeries", "swathed", "newMergeAtt", "RefractEd"]
---

# `fix_TimeSeries` — Batch Motion Residual, Latency & Heave Drift Correction Utility

## Overview & Purpose
`fix_TimeSeries` (authored by John E. Hughes Clarke, July 2008) is a standalone command-line utility that batch-applies the attitude, motion-scaling, latency, lever-arm, yaw misalignment, surface sound speed (SSS), and long-period heave drift corrections interactively diagnosed in the `swathed -ts` Time Series analyzer ([`SE_W_TimeSeries.c`](SE_W_TimeSeries.md)) across one or more `.merged` survey lines.

During interactive quality control with `swathed -ts`, a hydrographer can cross-correlate outer-beam seafloor slope residuals against vessel roll, pitch, and heave time series to determine exact motion sensor time delays, RC filter phase lags, amplitude scaling errors, surface sound speed errors/gradients, or long-period heave drift. Once optimal correction parameters are identified on a test line, `fix_TimeSeries` applies those exact fixes in batch mode across an entire survey sheet without requiring an X11 display.

---

## Usage & Command-Line Arguments

```bash
fix_TimeSeries [OPTIONS] <mergedfile(s)...>
```

### Common Workflow Examples

**1. Compute and embed cosine-tapered long-period heave drift (over a $\pm 160\text{ s}$ window) into `.merged` profile headers:**
```bash
fix_TimeSeries -heave_drift -avpings 160.0 merged/JD100/*.merged
```

**2. Batch-apply motion time delay (`0.10 s`), motion scaling (`1.03`), and lever-arm corrections (`X Y Z` in meters) to `.merged` soundings:**
```bash
fix_TimeSeries -delay 0.10 -scale 1.03 -lever_arm 3.1 2.3 0.7 merged/JD100/*.merged
```

**3. Correct a surface sound speed error (`-sss_error`) and across-track SSS gradient (`-sss_gradient`) with transducer draft:**
```bash
fix_TimeSeries -draft 2.50 -sss_error 2.0 -sss_gradient 0.5 merged/JD100/*.merged
```

### Arguments Table

| Option | Description | Default |
|---|---|---|
| `<mergedfile(s)>` | One or more input/output OMG `.merged` files to process (up to 1,000 files). | Required |
| `-draft <m>` | Set transducer draft (`TS_draft`, in meters) for raypath/surface sound speed geometry. | From `init_TimeSeries_variables()` |
| `-lever_arm <X> <Y> <Z>` | Set transducer-to-MRU lever arm offsets `TS_lever_X` (ahead, m), `TS_lever_Y` (starboard, m), and `TS_lever_Z` (down, m). | `0.0 0.0 0.0` |
| `-auto_lag` | Automatically estimate motion sensor RC filter lag (`lag_type = LAG_AUTOMATIC`). | Default |
| `-lag <sec>` | Manually specify motion sensor RC filter time lag (`TS_motion_time_lag`, in seconds; sets `lag_type = LAG_MANUAL`). | Auto |
| `-delay <sec>` | Apply a constant time latency shift (`TS_motion_time_delay`, in seconds) to vessel motion records. | `0.0` |
| `-scale <factor>` | Apply a multiplicative scale factor (`TS_motion_scale`) to roll/pitch/heave motion amplitudes. | `1.0` |
| `-yaw_misalign <deg>` | Apply a yaw misalignment angle correction (`TS_yaw_misalign`, in degrees). | `0.0` |
| `-sss_error <m/s>` | Apply a constant Surface Sound Speed offset (`TS_sss_error`, in m/s) for flat/curved array beam steering correction. | `0.0` |
| `-sss_gradient <val>` | Apply an across-track Surface Sound Speed gradient correction (`TS_sss_gradient`). | `0.0` |
| `-heave_drift` | Compute low-pass filtered heave drift (`insert_heave_drift = 1`) and embed it into `profile.longperiod_heaveCorrection` via `embed_LP_heave(infile)`. | Disabled |
| `-avpings <sec>` | Half-width window duration (`TS_filter_MAXperiod`, in seconds) for the $\cos^2$-tapered weighted moving average used by `-heave_drift`. | Default from `SE_W_TimeSeries` |
| `-apply_heave_drift` | Directly apply the computed heave drift correction to the bathymetric sounding depths (`apply_heave_drift = 1`). | Disabled |
| `-fixfile <file>` | Read time-series correction parameters from `<file>`. | Command-line flags |
| `-v` | Increment verbosity flag (`verbose_flag`). | `0` |

---

## Processing Architecture & Integration with `SE_W_TimeSeries.c`

`fix_TimeSeries.c` links directly against [`SE_W_TimeSeries.c`](SE_W_TimeSeries.md) (providing dummy no-op stubs for `prime_array()` and `dump_array()` to avoid pulling in the interactive X11 GUI event loop of `swathed`).

For each `.merged` file `inname[j]` on the command line:
1. **Initialization (`init_TimeSeries_variables` & `load_TimeSeries_variables`):** Opens `inname[j]` in `"r+"` read-write mode. If `-heave_drift` is specified without angular beam fixes (`insert_heave_drift == 1`), sets `load_beams = 0` so only the `OMG_HDCS_profile_header` sequence is read into memory (dramatically accelerating execution); otherwise sets `load_beams = 1` to load all profile headers and beam arrays.
2. **Mode A — Long-Period Heave Drift Embedding (`-heave_drift`):** Calls `embed_LP_heave(infile)`, which computes a $\cos^2$-tapered moving average of vessel heave over $\pm\text{TS\_filter\_MAXperiod}$ seconds and writes the resulting drift into `profile.longperiod_heaveCorrection` (which can subsequently be applied in `swathed -apply_LPH` or `weigh_grid`).
3. **Mode B — Full Angular & Lever-Arm Beam Re-Computation:** Sets `which_fix_to_apply = FIX_DO_OLD`, executes `TS_apply_fix()` to recompute every beam's depth, across-track, and along-track coordinates using the specified latency, lag, scale, lever-arm, yaw, and SSS corrections, and writes the updated profiles and beams out via `write_out_modified(inname[current_file])`.
4. **Cleanup:** Calls `free_TimeSeries_variables()` and closes `infile` before advancing to the next survey line.
