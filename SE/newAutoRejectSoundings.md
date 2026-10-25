---
layout: default
title: newAutoRejectSoundings
parent: SwathEd (SE) Tools
nav_order: 34
tool_name: newAutoRejectSoundings
source_path: code/SE/newAutoRejectSoundings.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", "SwathEd auto-flag criteria file"]
output_formats: [".merged (beam status flags updated in-place)"]
related_tools: ["SE_AUTOFLAGwin", "swathed", "SE_omgIOwin", "dumpFlags"]
---

# `newAutoRejectSoundings` — Batch Automated Sounding Outlier Flagging Utility

## Overview & Purpose
`newAutoRejectSoundings` (originally `autorejectSounding.c` by John E. Hughes Clarke, January 1994; rebuilt September 2009 during the CCGS *Amundsen* Ajuarak block survey) is a standalone command-line batch processor that applies `swathed` **Auto-Flag Parameters** across one or more `.merged` multibeam files without launching the X11 graphical interface.

In a typical quality-control workflow, a processor opens a representative `.merged` survey line in `swathed`, opens the **Auto-Flag Parameters** window ([`SE_AUTOFLAGwin.c`](SE_AUTOFLAGwin.md)), interactively tunes the across-track and along-track two-slope limits, beam masks, spike sense, and isolated-neighbor ("Fore-Aft", "Left-Right", "Any 2") rules, and saves the configuration to an ASCII criteria file via `dump_auto_parameters()`. `newAutoRejectSoundings` then reads that criteria file (`-criteria <filename>`) and steps through up to 200 `.merged` lines in 100-ping (`SE_NO_SWATHS`) overlapping blocks to batch-flag outliers in place.

---

## Usage & Command-Line Arguments

```bash
newAutoRejectSoundings [-v] -criteria <criteria_file> <mergedfile(s)...>
```

### Example Workflow

```bash
# 1. Back up existing manual flags before batch auto-flagging (optional safety step):
for f in merged/JD250/*.merged; do dumpFlags "$f"; done

# 2. Run batch auto-rejection using criteria saved from SwathEd's Auto-Flag window:
newAutoRejectSoundings -v -criteria petrel_autoflag.params merged/JD250/*.merged
```

### Arguments Table

| Option | Description | Default |
|---|---|---|
| `-criteria <file>` | **Required.** Path to the ASCII auto-flag parameter file parsed by `parse_auto_parameters()` in [`SE_AUTOFLAGwin.c`](SE_AUTOFLAGwin.md). | Required |
| `<mergedfile(s)>` | **Required.** One or more OMG `.merged` files (up to 200 files per invocation) to clean in-place. | Required |
| `-v` | Enable verbose diagnostic output (`verbose_flag++`). | Disabled |

---

## Criteria File Keywords (`parse_auto_parameters`)

The `-criteria <file>` argument accepts standard SwathEd auto-flag parameter files containing the following directives:

| Keyword in Criteria File | Effect in `SE_AUTOFLAGwin.c` |
|---|---|
| `UNFLAG_ON` / `UNFLAG_OFF` | Enables (`pre_unflag = 1`) or disables clearing existing flags before running the auto-flag pass. |
| `PHASE_ONLY` / `AMPL_ONLY` / `AMP_PHASE` | Restricts auto-flagging to phase detections (`AF_PHASE_ONLY`), amplitude detections (`AF_AMPL_ONLY`), or all detections (`AF_ALL_DETECTS`). |
| `UP_DOWN` / `UP_ONLY` / `DOWN_ONLY` | Sets `spike_sense` to flag both shoal and deep spikes, shoal spikes only, or deep spikes only. |
| `ANY_2_ON` / `ANY_2_OFF` | Enables or disables the iterative 4-neighbor `any_2` isolation check. |
| `MULTI_PASS <1..5>` | Sets the number of iterative neighbor-cleaning passes (`multi_pass`). |
| `ACROSS_TWO_SLOPE_ON <limit>` / `_OFF` | Enables across-track two-slope spike detection with angle limit `ACROSS_twoslopelimit` (degrees). |
| `ALONG_TWO_SLOPE_ON <limit>` / `_OFF` | Enables along-track two-slope spike detection with angle limit `ALONG_twoslopelimit` (degrees). |
| `FOREAFT_ON` / `FOREAFT_OFF` | Flags soundings lacking valid along-track neighbors in both ping $i-1$ and ping $i+1$. |
| `LEFTRIGHT_ON` / `LEFTRIGHT_OFF` | Flags soundings lacking valid across-track neighbors in both beam $j-1$ and beam $j+1$. |
| `BEAM <beam_idx> <use_beam> <use_twoslope>` | Configures per-beam mask `use_beam[beam_idx]` (`0` = reject entire beam) and `use_two_slope[beam_idx]`. |

---

## Batch Execution Pipeline

1. **Parameter Parsing & GUI Suppression:** Calls `parse_auto_parameters(tidename)` and zeroes all interactive GUI flags (`got_a_sswindow = 0`, `Lines_flag = 0`, `follow_terrain = 0`, `hdcs_flag = 0`, `full_att = 0`, `preload_flags = 0`) so [`SE_omgIOwin.c`](SE_omgIOwin.md) (`prime_array`) runs purely in headless memory mode without X11 calls.
2. **4-Ping Overlapping Block Stepping:** For each input `.merged` file `name[j]`, opens `infile` in `"r+"` mode, reads `OMG_HDCS_summary_header`, and loops over all profiles in steps of `SE_NO_SWATHS - 4` (`96` pings per step):
   ```c
   for (k = 0; k < summary.numProfiles; k += SE_NO_SWATHS - 4)
   ```
   The 4-ping overlap between consecutive 100-ping blocks ensures that along-track two-slope (`use_ALONG_two`) and fore-aft neighbor (`use_FOREAFT`, `any_2`) tests have valid along-track context at block boundaries.
3. **Load, Check & Write-Back:** Calls `prime_array(k)`, runs `check_data()` from [`SE_AUTOFLAGwin.c`](SE_AUTOFLAGwin.md), and writes updated `beam.status` flags back to disk via `dump_array(k)`.
