---
layout: default
title: iwc_adcp
parent: Ian Church — Hydrodynamic & 3D Ray-Trace Suite (ianc)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 10
tool_name: iwc_adcp
source_path: code/ianc/subr/iwc_adcp.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats:
- ADCP_record struct (j_adcp.h)
output_formats:
- In-memory heading-corrected ADCP_record
related_tools:
- oceanReader
- modelAnalysis
- HycomSSP
- iwc_support
- iwc_water
---

# iwc_adcp

## Description

`iwc_adcp` (`code/ianc/subr/iwc_adcp.c` and `code/ianc/subr/iwc_adcp.h`) is a C subroutine library module written by Ian Church in March 2013 for correcting Acoustic Doppler Current Profiler (ADCP) velocity vector components when an external heading reference (such as an Applanix POS MV / OMG HDCS `.orientation` file or ADCP bottom-track direction) reveals a compass azimuth bias in the raw ADCP ensemble record.

When vessel-mounted ADCPs operate near steel hulls, magnetic anomalies or gyro alignment errors introduce a time-varying azimuth bias (`azi_bias`) between the ADCP's internal heading (`corr_heading`) and true vessel heading. `iwc_adcp` provides `fixADCPBinVel()` to rotate every valid depth bin's velocity direction by `azi_bias` and recompute the eastward (`east_vel_component`) and northward (`north_vel_component`) velocity components from the bin velocity magnitude.

## Public API & Usage

### Header Include

```c
#include "j_watercolumn.h"
#include "j_adcp.h"
#include "iwc_support.h"
#include "iwc_adcp.h"
```

### Function Prototype

```c
int fixADCPBinVel(ADCP_record *adcp_rec);
```

### Example C Usage (from `oceanReader.c` / `modelAnalysis.c`)

```c
/* Match ADCP ensemble time to external HDCS attitude heading array */
indexHead = closeTime((double)adcp_rec[j].dtime, headTime, (size_t)lineCount, &weight1, &weight2);

/* Compute compass bias and update ensemble heading */
adcp_rec[j].azi_bias = adcp_rec[j].corr_heading - heading[indexHead];
adcp_rec[j].corr_heading = heading[indexHead];
if (adcp_rec[j].corr_heading > 360) adcp_rec[j].corr_heading -= 360;
if (adcp_rec[j].corr_heading < 0)   adcp_rec[j].corr_heading += 360;

/* Recalculate all bin velocity directions and E/W, N/S components */
fixADCPBinVel(&adcp_rec[j]);
```

## API Reference

| Function / Symbol | Signature / Type | Description |
| :--- | :--- | :--- |
| `fixADCPBinVel` | `int fixADCPBinVel(ADCP_record *adcp_rec)` | Rotates `bins[k].vel_direction` by `adcp_rec->azi_bias` for all valid bins `k = 0 .. adcp_rec->no_bins - 1` and updates `east_vel_component` and `north_vel_component`. Returns `1` on success, or `0` if `adcp_rec->azi_bias` is zero/unset. |

### Modified `ADCP_record` Fields (`j_adcp.h`)

| Struct Field | Type | Role in `fixADCPBinVel()` |
| :--- | :--- | :--- |
| `adcp_rec->azi_bias` | `float` | **Input**: Compass heading bias in degrees (must be non-zero; otherwise prints `"Heading Bias must exist!!!"` and returns `0`). |
| `adcp_rec->no_bins` | `int` | **Input**: Number of vertical depth cells (bins) in the current ADCP ensemble. |
| `adcp_rec->bins[k].vel_magnitude` | `float` | **Input**: Horizontal current speed in bin `k`. Bins are processed only if `-30000 < vel_magnitude < 30000` (filtering out RDI `-32768` bad-velocity sentinels). |
| `adcp_rec->bins[k].vel_direction` | `float` | **In/Out**: Geographic azimuth of the current vector in degrees. Incremented by `adcp_rec->azi_bias`. |
| `adcp_rec->bins[k].east_vel_component` | `float` | **Output**: Recomputed eastward velocity component: `vel_magnitude * sin(deg2rad(vel_direction))`. |
| `adcp_rec->bins[k].north_vel_component` | `float` | **Output**: Recomputed northward velocity component: `vel_magnitude * cos(deg2rad(vel_direction))`. |

## Data Structures & Formats

`iwc_adcp` operates directly on in-memory `ADCP_record` structures populated by `j_which_ADCP_read_next_rec()` from `j_adcp.h` (supporting both standard RDI PD0 binary files and WinADCP exports). Velocity magnitudes and components in `ADCP_record` are stored in millimeters per second (`mm/s`), with values outside `(-30000, 30000)` representing invalid/flagged ADCP bins.

## How It Works

1. **Bias Verification**: `fixADCPBinVel()` first checks `if (!adcp_rec->azi_bias)`. If `azi_bias` is `0`, no rotation is required (or the caller forgot to set the bias), so the function prints `"Heading Bias must exist!!!"` to `stdout` and returns `0`.
2. **Bin Iteration & Sentinel Filtering**: The function loops over every depth bin `k` from `0` to `adcp_rec->no_bins - 1`. It verifies that `adcp_rec->bins[k].vel_magnitude` lies strictly between `-30000` and `30000` to avoid corrupting bad-data sentinel values (`-32768`).
3. **Azimuth Rotation & Trigonometric Decomposition**:
   * The bin flow direction is adjusted by the compass error:

     ```c
     adcp_rec->bins[k].vel_direction = adcp_rec->bins[k].vel_direction + adcp_rec->azi_bias;
     ```
   * Treating `vel_direction` as a geographic azimuth (clockwise from true North) and calling `deg2rad()` from `iwc_support.c`, the orthogonal velocity components are updated:

     ```c
     adcp_rec->bins[k].east_vel_component  = adcp_rec->bins[k].vel_magnitude * sin(deg2rad(adcp_rec->bins[k].vel_direction));
     adcp_rec->bins[k].north_vel_component = adcp_rec->bins[k].vel_magnitude * cos(deg2rad(adcp_rec->bins[k].vel_direction));
     ```
4. **Return Status**: After updating all valid bins in the ensemble, `fixADCPBinVel()` returns `1`.
