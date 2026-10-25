---
layout: default
title: applyBDI
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 30
tool_name: applyBDI
source_path: code/SE/applyBDI.c
category: Interactive QC & Editing (SwathEd)
input_formats:
- .merged
- .watercol
- .sectors
- .orientation
- .param
- .svp_001
- .nav
output_formats:
- .merged_BDI
- BDI_non-nMA_<tags>_<prefix>.merged
- BDI_w-nMA_<tags>_<prefix>.merged
related_tools:
- bdi_funcs
- SE_BDI_DP
- swathed
- newMergeAtt
- getBounds
---

# `applyBDI` — Batch Beam-Direction Indicator (BDI) Water Column Bottom Detector

## Overview & Purpose
`applyBDI` (authored by Douglas Bergersen / Douglas and John E. Hughes Clarke, July 2015) is a standalone command-line utility that batch-applies the **Beam-Direction Indicator (BDI)** constant-time-slice angular peak-picking algorithm (defined in [`bdi_funcs.c`](bdi_funcs.html) and interactively tuned in [`SE_BDI_DP.c`](SE_BDI_DP.html)) across every ping of a Kongsberg `.merged` and `.watercol` dataset.

Unlike conventional multibeam bottom detection—which fixes a receive beam angle and searches along the time series for a bottom return (often failing on steep slopes, vertical walls, or complex targets)—BDI steps through **each constant Two-Way Travel Time (TWTT) slice** of the `.watercol` fan and picks up to two across-track amplitude peaks across the receive beam array using 3-point or 5-point parabolic interpolation. `applyBDI` converts these water-column BDI solutions into receiver-relative steering angles and travel times, packs them into `OMG_HDCS_beam` records (up to 400 solutions per output sub-swath), and optionally runs [`getBounds`](../omg/getBounds.html) and [`newMergeAtt`](../omg/newMergeAtt.html) to raytrace full 3D geographic soundings.

> [!IMPORTANT]
> **Supported Sonar Systems & Companion Files:**
> `applyBDI` requires Kongsberg multi-sector water-column data (`EM710`, `EM2040`, `EM302`, or `EM122`) and expects `<prefix>.merged`, `<prefix>.watercol`, `<prefix>.sectors`, `<prefix>.orientation`, and `<prefix>.param` (plus `<prefix>.nav` and `<prefix>.svp_001` when running the full `newMergeAtt` pipeline) in the working directory.

---

## Usage & Command-Line Arguments

```bash
applyBDI -in <line.merged> -parabola <3|5> [OPTIONS]
```

### Example Workflows

**1. Batch-generate a `.merged_BDI` file for direct inspection in `swathed` (`-out_as_bdi_extension`):**

```bash
applyBDI -in 0001_line.merged -parabola 3 -out_as_bdi_extension
```

**2. Run BDI with 5-point parabola, compress into 400 virtual beams per ping, and automatically raytrace via `newMergeAtt`:**

```bash
applyBDI -in 0001_line.merged -parabola 5 -compress -virtual_beams 400
```

**3. Apply a manual dB threshold with slope and manual standard-deviation filter:**

```bash
applyBDI -in 0001_line.merged -parabola 3 -manual_threshold 3.0 -threshold_slope -1 \
         -apply_manual_filter -filter_index 7
```

### Arguments Table

| Option | Description | Default |
|---|---|---|
| `-in <file.merged>` | **Required.** Input OMG `.merged` file path. | Required |
| `-parabola <3\|5>` | **Required.** Number of adjacent receive beams (`3` or `5`) used for parabolic peak-center interpolation (`DP_3_POINT_PARABOLA` or `DP_5_POINT_PARABOLA`). | Required |
| `-out_as_bdi_extension` | Write output directly to `<inname>_BDI` (e.g., `line.merged_BDI`) without copying companion files or invoking `getBounds` / `newMergeAtt`. | Disabled (creates `BDI_non-nMA_*` and `BDI_w-nMA_*` suites) |
| `-manual_threshold <dB>` | Override automatic thresholding (`aut_threshold = 0`) with a manual dB threshold. | Automatic threshold (`aut_threshold = 1`) |
| `-threshold_slope <val>` | Slope of the manual threshold line across the TWTT trace (only used with `-manual_threshold`). | `0` |
| `-no_second_peak` | Restrict BDI picking to only 1 peak solution per TWTT time slice (`the_second_peak = 0`). | Up to 2 peaks per TWTT slice (`NO_BDI = 2`) |
| `-apply_manual_filter` | Use manual standard-deviation outlier filtering (`filter_manual = 1`, `filter_automatic = 0`) instead of footprint-based automatic filtering. | Automatic footprint filter (`filter_automatic = 1`) |
| `-filter_index <val>` | Maximum allowable standard deviation of solutions at the outermost beam angle (only used with `-apply_manual_filter`). | `9.0` |
| `-compress` | Compress multiple BDI time-slice solutions into equidistant across-track virtual beams (`the_compression = 1`). | Uncompressed (up to 400 solutions per sub-swath) |
| `-virtual_beams <N>` | Number of equidistant virtual beams across the swath when `-compress` is enabled. | `400` |
| `-v` / `-debug` | Enable verbose progress (`BDI_verbose_flag = 1`) or detailed per-solution angle/attitude debug output (`debug = 1`). | Disabled |

---

## Processing Pipeline & Raytracing Geometry

For each ping `i` (`0 .. summary.numProfiles - 1`), `applyBDI` executes:
1. **Water Column Read & Peak Picking:** Reads the profile, transmit sectors (`.sectors`), raw beams, and water-column fan (`j_EM_read_watercolumn`), then invokes `standalone_BDI_pick_Angle_Peaks()` from [`bdi_funcs.c`](bdi_funcs.html) to populate `WC_BDI_pick[this_TWTT][0..1]`.
2. **TWTT & Range Calculation:** For every valid BDI pick (`WC_BDI_pick[this_TWTT][ii].angle != 0`), converts the sample index into true Two-Way Travel Time (`twtt`) by adding `start_range_sample_no` of the `closest_beam` and dividing by `WHOLE_ping_WC->sampling_freq / 100.0`. Populates `BDI_beams[jj].twtt`, `other_range = twtt * profile.samp_rate`, and `range = 0.5 * twtt * profile.samp_rate`.
3. **Receive-Time Attitude Un-Stabilization (`Rc_steer`):** Because water-column beam pointing angles are stored relative to local vertical (`calc_angle = WC_BDI_pick[this_TWTT][ii].angle`), `applyBDI` reconstructs the raw array-relative receive steering angle required by `newMergeAtt`:
   - Adds the transducer roll mounting angle `mount_angle` from `<prefix>.param` (`sonar[1].dRoll` or `sonar[2].dRoll` for dual-head EM2040).
   - Computes exact receive time: `receive_time = first_sector_transmit_time + tx_sectors[sector].tx_time_offset + twtt`.
   - Interpolates exact vessel roll at `receive_time` from `<prefix>.orientation` via `OMG_HDCS_get_interpolated_async()` and subtracts `rx_orientation.roll` (`BDI_beams[jj].Rc_steer = calc_angle * 100.0`).
4. **Multi-Swath Packing & `newMergeAtt` Execution:** Because an uncompressed ping may yield more than 400 BDI solutions across all time slices, `applyBDI` flushes a new `OMG_HDCS_profile_header` and 400-beam block (`OMG_HDCS_write_profile`, `OMG_HDCS_put_raw_beams`) whenever `jj == 400`. When `-out_as_bdi_extension` is not set, it copies `.orientation`, `.nav`, `.sectors`, `.param`, `.svp_001`, and `.watercol` to `BDI_non-nMA_<tags>_<prefix>.*` and `BDI_w-nMA_<tags>_<prefix>.*`, runs `getBounds`, and executes `newMergeAtt -in <BDI_w-nMA>.merged -svp <BDI_w-nMA>.svp_001`.
