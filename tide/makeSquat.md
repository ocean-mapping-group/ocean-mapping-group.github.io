---
layout: default
title: makeSquat
parent: Tide Tools
tool_name: makeSquat
source_path: code/tide/makeSquat.c
category: tide
input_formats: [".nav (binary jcu_nav_rec navigation file)"]
output_formats: [".nav (modified in-place with squat in azi field)"]
related_tools: ["mergeTide", "diffTide"]
---

# makeSquat

## Overview

`makeSquat` calculates vessel dynamic draft (settlement/squat) as a power-law function of vessel speed (`velocity`) stored in one or more OMG binary `jcu_nav_rec` navigation files, and writes the resulting vertical squat offset into the `azi` field of each navigation record in-place.

Because OMG binary tide files use the exact same `jcu_nav_rec` structure (storing vertical offsets in `azi`), a `.nav` file processed by `makeSquat` can be passed directly into [`mergeTide`](mergeTide.md) (for example with `-DDC` or `-add`) to apply speed-dependent dynamic draft corrections to `.merged` multibeam lines.

---

## Syntax & CLI Options

```bash
makeSquat [OPTIONS] -power <exp> -scaler <coeff> <navfile(s)...>
```

| Option | Description | Default |
|---|---|---|
| `-power <value>` | Exponent $p$ applied to vessel velocity in the power-law squat formula. | Required for valid calculation (e.g., `1.8`) |
| `-scaler <value>` | Multiplier coefficient $a$ applied to `pow(velocity, power)`. | Required for valid calculation (e.g., `0.0018`) |
| `<navfile(s)...>` | **Required.** One or more binary `jcu_nav_rec` files (up to 300 files) to modify **in-place**. | None |
| `-ascii` | Sets internal `ascii_flag` (parsed on CLI). | Disabled |
| `-v` | Print record index, velocity, and computed squat for every navigation record. | Disabled |

---

## How It Works

1. Opens each specified binary `jcu_nav_rec` file in read-update mode (`"r+"`) and determines the total number of records (`ftell(file) / JCU_BINNAV_RECLEN`).
2. For each record $k$, reads `tide_rec` and computes dynamic draft from `tide_rec.velocity`:
   $$\text{squat} = \text{sq\_scaler} \times (\text{velocity})^{\text{sq\_power}}$$
3. Stores the computed value in `tide_rec.azi` and overwrites record $k$ in-place via `nav_write`.

> **Important:** Because `makeSquat` overwrites the `azi` (heading/tide) field of `<navfile(s)>` in-place, always run `makeSquat` on a **copy** of your `.nav` file rather than your primary navigation archive.

---

## Examples

**1. Generate a dynamic draft (squat) correction file from vessel navigation and merge into `.merged` v4 files:**
```bash
cp vessel_nav.bin vessel_squat.bin
makeSquat -power 1.8 -scaler 0.0018 vessel_squat.bin
mergeTide -DDC -tide vessel_squat.bin merged/JD150/*.merged
```

---

## Workflow Context

- **Upstream:** Binary `.nav` files extracted via `stripNav` or `posProc_2_OMG`.
- **Downstream:** [`mergeTide`](mergeTide.md) (using `-DDC` to populate `profile.dynamic_draftCorrection`, or `-add` to combine with water-level tides) or [`diffTide`](diffTide.md).
