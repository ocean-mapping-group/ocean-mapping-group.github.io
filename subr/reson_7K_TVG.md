---
layout: default
title: reson_7K_TVG
parent: Core Shared Libraries (subr)
module_name: reson_7K_TVG
source_path: code/subr/reson_7K_TVG.c
header_path: code/subr/reson_7K_TVG.h
category: Acoustic Modeling, Backscatter & TVG
related_tools:
  - omg2gsf
  - reson_calibration
  - Echo_calib
---

# `reson_7K_TVG` — Reson 7K Time-Varying Gain (TVG) Lookup Interface

## Overview & Purpose

The `reson_7K_TVG` module (`code/subr/reson_7K_TVG.c` and `code/subr/reson_7K_TVG.h`) defines the data structure and API for constructing and querying Time-Varying Gain (TVG) curves applied by Reson SeaBat 7125 and 7111 multibeam echosounders in 7K data records.

While the public interface (`Reson_7K_TVG`, `build_Reson_7K_TVG`, and `get_Reson_7K_TVG`) is wired into the Reson 7K radiometric calibration pipeline (`reson_calibration.c`, `Echo_calib.c`, and `omg2gsf.c`), the implementation in `reson_7K_TVG.c` is intentionally stubbed out in the UNB SwathEd source tree (issuing a runtime warning `"Reson 7125/7111 TVG is not implemented in UNB SwathEd"` and returning `0`).

---

## Key Constants & Data Structures

### Constants (`reson_7K_TVG.h`)

| Macro | Value | Description |
| :--- | :--- | :--- |
| `RESON_TVG_UNDEFINED` | `-999999` | Sentinel indicating an uninitialized or undefined TVG entry |
| `RESON_TVG_MAX_LENGTH` | `16384` | Number of samples in the precomputed TVG lookup table |
| `RESON_TVG_MAX_TIME` | `1.6384` | Maximum two-way travel time (seconds) covered by the 16,384-element table (100 µs resolution) |
| `RESON_TVG_MAX_GAIN` | `83.0` | Maximum receiver amplifier gain ceiling in dB for Reson 7125/7111 hardware |

### `Reson_7K_TVG` Structure

```c
typedef struct {
    float tvg[RESON_TVG_MAX_LENGTH];
    float gain;
    float absorption;
    float spreading;
} Reson_7K_TVG;
```

- **`tvg[16384]`**: Array storing the precomputed time-varying gain (in dB) indexed by two-way travel time sample bin.
- **`gain`**: Static receiver gain setting (dB) extracted from the Reson 7K Record 7000 (`Reson_7K_7000_Sonar_Settings`).
- **`absorption`**: Absorption coefficient (dB/km) used in the real-time TVG law.
- **`spreading`**: Spreading loss coefficient ($X \log_{10} R$) used in the real-time TVG law.

---

## Public Functions & Signatures

### `build_Reson_7K_TVG`
```c
int build_Reson_7K_TVG(
    Reson_7K_TVG *tvg,
    Reson_7K_7000_Sonar_Settings *sonar_settings
);
```
- **Purpose**: Populates a `Reson_7K_TVG` lookup table from a ping's `Reson_7K_7000_Sonar_Settings` record (`gain`, `absorption`, and `spreading`).
- **Behavior**: In the current UNB SwathEd implementation, logs `warning("Reson 7125/7111 TVG is not implemented in UNB SwathEd")` and returns `0`.

### `get_Reson_7K_TVG`
```c
float get_Reson_7K_TVG(Reson_7K_TVG *tvg, float twtt);
```
- **Purpose**: Returns the real-time TVG gain (in dB) applied by the Reson 7K receiver at a given two-way travel time `twtt` (in seconds).
- **Behavior**: Called by `calibrate_reson_7K()` in `reson_calibration.c` when `remove_reson_tvg` is enabled; currently returns `0.0`.

---

## How It Fits Into the OMG Architecture

- **Reson 7K Backscatter Calibration (`subr/reson_calibration.c`, `subr/Echo_calib.c`)**: `calibrate_reson_7K()` accepts a `Reson_7K_TVG *tvg` pointer and calls `get_Reson_7K_TVG(tvg, beams[beam].twtt)` when removing real-time hardware TVG prior to substituting a post-processed $40\log_{10} R + 2\alpha R$ transmission loss model.
- **Format Export (`gsf/omg2gsf.c`)**: Included alongside `reson_7K.h` and `reson_calibration.h` when exporting calibrated Reson 7K swath data to Generic Sensor Format (GSF).
