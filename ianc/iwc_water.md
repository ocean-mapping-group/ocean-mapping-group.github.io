---
layout: default
title: iwc_water
parent: Ian Church (ianc) Tools
nav_order: 14
tool_name: iwc_water
source_path: code/ianc/subr/iwc_water.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats: ["watercolumn struct (j_watercolumn.h)", "iwc_watercol / oceanObs structs"]
output_formats: ["watercolumn struct with extra_field", "Binned & derived physical oceanography profiles"]
related_tools: ["oceanReader", "modelAnalysis", "HycomSSP", "modelMerge", "iwc_support", "iwc_adcp"]
---

# iwc_water

## Description

`iwc_water` (`code/ianc/subr/iwc_water.c` and `code/ianc/subr/iwc_water.h`) is the physical oceanography data structure and equation library for the `ianc` suite. Written by Ian Church in March 2013, it defines the `oceanObs` and `iwc_watercol` structures capable of holding full-profile CTD/MVP observations, multi-channel analog sensor voltages (`mV1`–`mV4`), co-located ADCP current velocity vectors, and derived water-column stability parameters.

The module implements standard equations of state and turbulence metrics—including the UNESCO 1983 (Fofonoff & Millard, EOS-80) secant bulk modulus seawater density equation (`density0`, `calcDensity`), Brunt-Väisälä buoyancy frequency (`calcBuoy`), gradient Richardson number (`calcRichard`), internal Froude number (`calcFroude`), and seawater kinematic viscosity / Reynolds number (`calcReynolds`)—along with vertical depth-bin averaging (`binOceanObs`) and two-way conversion (`jwc2iwc`, `iwc2jwc`) between `iwc_watercol` and the standard OMG `watercolumn` structure (`j_watercolumn.h`).

## Public API & Usage

### Header Include

```c
#include "j_watercolumn.h"
#include "iwc_water.h"
#include "iwc_support.h"
```

### Example C Usage

```c
iwc_watercol wc;
watercolumn jwc_out;

/* Convert an OMG watercolumn cast into an iwc_watercol structure */
jwc2iwc(&input_jwc, &wc);

/* Compute EOS-80 density and buoyancy frequency at each observation depth */
for (int i = 0; i < wc.nObs; i++) {
    wc.obs[i].dens = calcDensity(wc.obs[i].sal, wc.obs[i].temp, wc.obs[i].press);
    calcBuoy(&wc.obs[i], wc.lat);
}

/* Bin observations into 20 uniform vertical layers and compute turbulence numbers */
wc.nInterpObs = 20;
binOceanObs(&wc);
calcRichard(&wc, wc.lat);
calcFroude(&wc, wc.lat);
calcReynolds(&wc);

/* Export back to OMG watercolumn format with Richardson number in extra_field */
iwc2jwc(&wc, &jwc_out, IWC_RICHARD);
iwc_waterFree(&wc);
```

## Data Structures & Constants (`iwc_water.h`)

### Extra Variable Selector Macros (`extraVar`)
Used when exporting an `iwc_watercol` to an OMG `watercolumn` via `iwc2jwc()` to select which derived variable is stored in `jwc->raw_zv[m].extra_field`:
* `IWC_OBS` (`1`): Optical Backscatter (`obs`)
* `IWC_DENS` (`2`): Calculated Seawater Density (`dens`, `kg/m^3`)
* `IWC_DENSGRAD` (`3`): Vertical Density Gradient (`densGrad`, `kg/m^4`)
* `IWC_BUOY` (`4`): Brunt-Väisälä Buoyancy Frequency (`buoy`, `rad/s` or `s^-1`)
* `IWC_RICHARD` (`5`): Gradient Richardson Number (`richard`, dimensionless)
* `IWC_FROUDE` (`6`): Internal Layer Froude Number (`froude`, dimensionless)
* `IWC_REYNOLDS` (`7`): Reynolds Number (`reynolds`, dimensionless)

### `oceanObs` Structure
Represents a single depth sample or vertical bin in the water column:
* **CTD & Analog Sensors**: `press` (dbar), `depth` (m), `SV` (m/s), `temp` (°C), `cond`, `sal` (PSU), `density` (raw `.m1` density), `bs` (acoustic backscatter), `volts`, `mV1`, `mV2`, `mV3`, `mV4`.
* **Derived Physical Variables**: `obs`, `densGrad`, `dens`, `buoy`, `richard`, `froude`, `reynolds`, `layerThick` (m).
* **ADCP Velocity Variables**: `velEW` (m/s), `velNS` (m/s), `velMag` (m/s), `velDir` (deg), `velGrad` (`du/dz`, `s^-1`), `percentGood`.

### `iwc_watercol` Structure
Represents a complete vertical profile cast:
* `oceanObs *obs`: Raw depth observations (`nObs` elements).
* `oceanObs *interpObs`: Vertically binned observations (`nInterpObs` elements, active when `interpFlag == 1`).
* `time`, `lat`, `lon`, `x`, `y`, `depth`, `maxObsDepth`, `minObsDepth`: Cast metadata and spatial/vertical bounds.
* `char *filename`: Source filename string.
* `unsigned char sortedFlag`, `interpFlag`: Processing state flags.

## Public Functions (`iwc_water.c`)

| Function | Signature | Description |
| :--- | :--- | :--- |
| `iwc_waterInit` | `int iwc_waterInit(iwc_watercol *wc)` | Zero-initializes an `iwc_watercol` struct (`memset`) and resets `interpFlag` and `sortedFlag` to `0`. |
| `iwc_waterFree` | `void iwc_waterFree(iwc_watercol *wc)` | Frees dynamically allocated `obs`, `interpObs`, and `filename` pointers and resets counts to `0`. |
| `printObs` | `void printObs(oceanObs *obs)` | Prints all 25 fields of an `oceanObs` record to `stdout` for debugging. |
| `jwc2iwc` | `void jwc2iwc(watercolumn *jwc, iwc_watercol *iwc)` | Initializes `iwc`, copies metadata (`time_of_obs`, `lat_obs`, `lon_obs`, min/max depths), allocates `iwc->obs`, and copies `depth`, `speed`, `temperature`, and `salinity` from `jwc->raw_zv`. |
| `iwc2jwc` | `void iwc2jwc(iwc_watercol *iwc, watercolumn *jwc, int extraVar)` | Copies either `iwc->interpObs` (if `interpFlag == 1`) or `iwc->obs` into a newly allocated `jwc->raw_zv` array, maps the variable chosen by `extraVar` (`IWC_OBS`..`IWC_REYNOLDS`) into `raw_zv[m].extra_field`, and updates min/max header bounds. |
| `binOceanObs` | `void binOceanObs(iwc_watercol *wc)` | Divides `[minObsDepth, maxObsDepth]` into `wc->nInterpObs` equal-thickness layers, averages all scalar and velocity fields within each bin into `wc->interpObs`, sets `interpFlag = 1`, and recomputes `layerThick`, `densGrad`, and `velGrad` across adjacent bins. |
| `density0` | `double density0(double s, double t)` | Computes surface (1 atm, `p = 0`) seawater density (`kg/m^3`) from salinity `s` (PSU) and temperature `t` (°C) using the UNESCO 1983 polynomial. |
| `calcDensity` | `double calcDensity(double s, double t, double p)` | Computes in-situ seawater density `d = d0 / (1 - pb/K)` (`kg/m^3`) at salinity `s` (PSU), temperature `t` (°C), and pressure `p` (decibars, converted to bars `pb = p / 10`) using Fofonoff (1983) secant bulk modulus `K` coefficients. |
| `calcBuoy` | `void calcBuoy(oceanObs *obs, double lat)` | Computes Brunt-Väisälä buoyancy frequency `obs->buoy = sqrt(fabs((-gravity(lat) / obs->dens) * obs->densGrad))`. |
| `calcRichard` | `void calcRichard(iwc_watercol *wc, double lat)` | Computes `richard = ((-gravity(lat) / dens) * densGrad) / velGrad` across all `interpObs` (or `obs`) records. Note that `velGrad` in `oceanReader` stores `(du/dz)^2` or vertical shear depending on call site. |
| `calcFroude` | `void calcFroude(iwc_watercol *wc, double lat)` | Computes internal layer Froude number `velMag / sqrt(fabs((dens[i] - dens[i-1]) / dens[i]) * gravity(lat) * layerThick)` for each layer `i >= 1`. |
| `calcReynolds` | `void calcReynolds(iwc_watercol *wc)` | Computes dynamic viscosity `mu = mu_w * (1 + A*S + B*S^2)` and kinematic viscosity `kVis = mu / dens` (adapted from MIT Seawater Thermophysical Properties library `SW_Viscosity.m` / `SW_Kviscosity.m`), then sets `reynolds = (velMag * depth) / kVis`. |

## How It Works

1. **EOS-80 Seawater Equation of State**: `density0(s, t)` evaluates the 1-atmosphere international equation of state of seawater, and `calcDensity(s, t, p)` applies high-pressure secant bulk modulus compression `K(s, t, p)` verified against Fofonoff & Millard (1983) check values.
2. **Uniform Vertical Binning (`binOceanObs`)**: Because CTD/MVP downcasts sample at irregular vertical intervals (e.g., `~0.1` m) while ADCP velocity bins have fixed vertical cell lengths (`1–4` m), `binOceanObs()` averages all sensors into `nInterpObs` uniform layers and computes finite-difference vertical density and velocity gradients (`densGrad`, `velGrad`) between bin `i` and bin `i - 1`.
