---
layout: default
title: r4to8bit
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 3
tool_name: r4to8bit
source_path: code/grid/r4to8bit.c
category: Gridding & Bathymetric Surface Generation
input_formats:
- .r4
output_formats:
- .8bit
related_tools:
- weigh_grid
- addSUN
- jview
- stretchacres
- edhead
---

# r4to8bit

## Description
`r4to8bit` converts an OMG1 `JHC_header` 32-bit floating-point grid (`<prefix>.r4`, where `header.data_type == 3`) into an 8-bit unsigned char grid (`<prefix>.8bit`, where `header.data_type == 1`), scaling the floating-point values into the 0–255 byte range so the surface can be displayed in [`jview`](../JV/jview.html) or combined with a sun-illuminated shaded relief image from [`addSUN`](addSUN.html).

If `-low` and `-high` depth limits are not specified on the command line, `r4to8bit` automatically scans the entire `.r4` array to find the minimum and maximum non-zero values, updates `min_value` and `max_value` in both the `.r4` and `.8bit` file headers, and linearly (or piecewise-linearly via `-middle`) maps values to `[0, 255]`. Unpopulated grid cells matching `-ignore` (default `0.0`) are mapped to `0`.

---

## Usage

```bash
r4to8bit [OPTIONS] <floatfile_or_prefix> [8bitfile]
```
*(If `[8bitfile]` is omitted, `r4to8bit` automatically reads `<prefix>.r4` and writes `<prefix>.8bit`.)*

### Common Workflow Examples

**1. Auto-scale a `.r4` bathymetry grid to `.8bit` using its full depth range:**

```bash
r4to8bit bay_2m
# Reads bay_2m.r4, finds min/max depth, writes bay_2m.8bit
```

**2. Convert a `.r4` grid over a fixed depth window (-150 m to -10 m), reserving DN 0–15 for UI colors:**

```bash
r4to8bit -low -150.0 -high -10.0 -no16 -no255 bay_2m.r4 bay_2m_clipped.8bit
```

**3. Scale a grid within $\pm 5\text{ m}$ of its mean depth (`-range_about_mean 10`):**

```bash
r4to8bit -range_about_mean 10 bay_2m
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<floatfile_or_prefix>` | **Required.** Input `.r4` filename or prefix (e.g., `bay_2m` or `bay_2m.r4`). | None |
| `[8bitfile]` | **Optional.** Output `.8bit` filename. If omitted, `<prefix>.8bit` is generated automatically. | `<prefix>.8bit` |
| `-low <val>` | Minimum floating-point value (deepest depth, e.g., `-2500.0`) mapped to `-bot`. If both `-low` and `-high` are `0.0`, `r4to8bit` auto-computes min and max from the data. | Auto-detected |
| `-high <val>` | Maximum floating-point value (shoalest depth, e.g., `-100.0`) mapped to `-top`. | Auto-detected |
| `-middle <val>` | Intermediate floating-point pivot value mapped to the midpoint `(top - bot) / 2` for piecewise two-slope scaling. | `(low + high) / 2.0` |
| `-range_about_mean <span_m>` | Automatically compute the mean of all non-zero grid cells and set `low = mean - span/2` and `high = mean + span/2`. | Disabled |
| `-ignore <val>` | Floating-point null/background value in the `.r4` file; cells equal to `<val>` are set to `0` in the `.8bit` output. | `0.0` |
| `-bot <DN>` | Minimum output byte value (0–255). | `0` |
| `-top <DN>` | Maximum output byte value (0–255). | `255` |
| `-nozero` | Clamp valid scaled pixels that round to `0` up to `1` so `0` remains strictly reserved for `-ignore` background cells. | Disabled |
| `-no16` | Clamp valid scaled pixels below `16` up to `16` (reserving indices 0–15 for X11/OMG overlay colors). | Disabled |
| `-no255` | Clamp valid scaled pixels equal to `255` down to `254` (reserving `255` for invalid/background markers). | Disabled |
| `-log` | Apply $\log_{10}(z)$ transformation to non-zero float values before scaling. | Disabled |
| `-sqrt` | Apply $\sqrt{|z|}$ transformation to non-zero float values before scaling (useful for compressing dynamic range of slope grids). | Disabled |

---

## Notes
* Because OMG bathymetric grids store depth as **negative numbers downward** (e.g., `-2500.0` m is deeper than `-100.0` m), `-low` should always be the **more negative (deeper)** value and `-high` should be the **less negative (shoaler)** value (e.g., `-low -2500 -high -100`).
* `r4to8bit` opens the input `.r4` file in `rb+` (read/write) mode so it can update `JHChead.min_value` and `JHChead.max_value` in the `.r4` header at the end of execution. Ensure you have write permissions on the `.r4` file.
