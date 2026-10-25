---
layout: default
title: tomos
parent: Helper Scripts
nav_order: 4
tool_name: tomos
source_path: code/scripts/tomos
category: Backscatter & Sidescan Mosaicking
input_formats: [".blank"]
output_formats: [".mos", ".ran"]
related_tools: ["make_blank", "mos2", "tor4"]
---

# tomos

## Description
`tomos` is a `tcsh` helper script that initializes the two 8-bit array files required by [`mos2`](../newmos/mos2.md) from a single `<prefix>.blank` file created by [`make_blank -8bit -prime 255`](../grid/make_blank.md).

For each `<prefix>` (or `<prefix>.blank`) passed on the command line, `tomos` verifies that `<prefix>.blank` exists and copies it to:
1. `<prefix>.mos` — The 8-bit backscatter mosaic array.
2. `<prefix>.ran` — The 8-bit across-track range/weight priority buffer used for autoseaming overlapping swaths.

---

## Usage

```bash
tomos <prefix_or_blank_file> [...]
```

### Example
```bash
# 1. Create an 8-bit blank mapsheet primed to 255 (background)
make_blank -8bit -prime 255 bay_mos -boundsof_ss ss/JD100/*.ss

# 2. Initialize bay_mos.mos and bay_mos.ran
tomos bay_mos.blank

# 3. Mosaic sidescan lines with mos2
mos2 -swap_dirs ss/ merged/ bay_mos ss/JD100/*.ss
```

> [!CAUTION]
> Always pass `-8bit -prime 255` to `make_blank` before running `tomos`. If you omit `-prime 255`, the `.mos` and `.ran` arrays will be primed with `0` instead of `255` (`MOS_BACKGROUND` / `RAN_BACKGROUND`), which prevents `mos2`'s autoseaming logic from recognizing empty background pixels!
