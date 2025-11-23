---
layout: default
title: bpick
parent: Slant Tools
grand_parent: sidescan
nav_order: 1
---
# bpick

## Description
`bpick` is a utility designed for bottom picking in JCU GLORIA format sidescan files. It identifies the first arrival of the seafloor by detecting a sustained signal amplitude above a specified `threshold` within a `pick_window`. This tool can be configured to pick for port, starboard, the shallowest, or the deepest returns. Additionally, it provides options to smooth the picked bottom depths using median or averaging filters, useful for removing noise or small-scale irregularities from the profile.

## Usage
```bash
bpick [-v] [-use_existing] [-median <length> | -average <length>] [-pickport | -pickstbd | -pickboth | -pickshallow | -pickdeep] [-pickwin <windowsize> <min_above>] [-minpick <pixels>] [-threshold <value>] -in <infile>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-use_existing` | If specified, the tool will not re-pick the bottom but will rather process existing altitude values in the header with median or average filters. |
| `-median <length>` | Activates a median filter to smooth picked depths. `length` specifies the half-width of the median window. |
| `-average <length>` | Activates an averaging filter to smooth picked depths. `length` specifies the half-width of the averaging window. |
| `-pickport` | Pick the bottom on the port side. | `Default` |
| `-pickstbd` | Pick the bottom on the starboard side. | |
| `-pickboth` | This option is listed but not fully implemented to pick both port and starboard simultaneously in the provided code. | |
| `-pickshallow` | Pick the shallowest of the port/starboard picks. | |
| `-pickdeep` | Pick the deepest of the port/starboard picks. | |
| `-pickwin <windowsize> <min_above>` | Specifies the window size (in pixels) for detecting the first arrival, and the minimum number of pixels within that window that must be above the `threshold` to confirm a pick. | `10 6` |
| `-minpick <pixels>` | Specifies the minimum pixel index from the nadir that a pick can occur. This helps ignore water column noise close to the nadir. | `10` |
| `-threshold <value>` | Specifies the 8-bit digital number (DN) threshold. Pixels with intensity above this value are considered part of the seafloor return. | `20` |
| `-in <infile>` | **Required.** The input JCU GLORIA format sidescan file. |

## How It Works
The tool operates in two main phases: bottom picking and optional smoothing.

**Phase 1: Bottom Picking (`pick_first_arrival` function) (if `-use_existing` is not set):**
1.  **Iterate Records:** The tool reads each GLORIA record from the input file.
2.  **Trace Preparation:** For each record, it prepares an 8-bit trace (either port or starboard, or both, depending on `detect_flag`).
3.  **First Arrival Detection:** The `pick_first_arrival` function searches along the trace starting from `minpick` pixels from the nadir.
    *   It looks for the first pixel whose value exceeds the `threshold`.
    *   Once such a pixel is found, it checks if at least `min_above` pixels within the subsequent `pick_window` also exceed the `threshold`. This ensures a robust detection, preventing false picks from isolated noise spikes.
    *   If these conditions are met, that pixel's index is considered the "break" (first arrival).
4.  **Altitude Update:** The detected break (pixel index) is converted to a physical altitude value (`float pick * header.small_pixel * 750.0`) and stored in `out_record.header.altitude`.
5.  **Write Record:** The modified record is written back to the input file.

**Phase 2: Depth Smoothing (if `-median` or `-average` is set):**
1.  **Load Altitudes:** After (or instead of) picking, the `altitude` values from all records are loaded into an `inpick` array.
2.  **Filter Application:**
    *   **Median Filter (`-median`):** If activated, a median filter of `length` is applied. For each record, its altitude is replaced by the median of altitudes within the window centered on it.
    *   **Averaging Filter (`-average`):** If activated, an averaging filter of `length` is applied. For each record, its altitude is replaced by the average of altitudes within the window centered on it.
3.  **Write Record:** The `out_record.header.altitude` is updated with the smoothed value, and the record is written back to the input file.
