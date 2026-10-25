---
layout: default
title: tor4
parent: Automated Processing Scripts (scripts)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 3
tool_name: tor4
source_path: code/scripts/tor4
category: Gridding & Bathymetric Surface Generation
input_formats:
- .blank
output_formats:
- .r4
- .r4_weights
- .r4_weight_depth
related_tools:
- make_blank
- weigh_grid
- tomos
---

# tor4

## Description
`tor4` is a `tcsh` helper script that prepares the three floating-point array files required by [`weigh_grid`](../grid/weigh_grid.html) from a single `<prefix>.blank` file created by [`make_blank -float`](../grid/make_blank.html).

For each `<prefix>` (or `<prefix>.blank`) passed on the command line, `tor4` verifies that `<prefix>.blank` exists and copies it to:
1. `<prefix>.r4` — The output weighted-mean depth grid.
2. `<prefix>.r4_weights` — The sum-of-weights accumulator array.
3. `<prefix>.r4_weight_depth` — The sum-of-weighted-depths accumulator array.

---

## Usage

```bash
tor4 <prefix_or_blank_file> [...]
```

### Example

```bash
# 1. Create a 2-meter floating-point blank mapsheet
make_blank -float bay_2m -boundsof merged/JD100/*.merged

# 2. Initialize the three .r4 files for weigh_grid
tor4 bay_2m.blank

# 3. Run weigh_grid
weigh_grid -beam_weight bay_2m merged/JD100/*.merged
```

> [!CAUTION]
> Running `tor4` on an existing grid prefix **overwrites** `<prefix>.r4`, `<prefix>.r4_weights`, and `<prefix>.r4_weight_depth` with the empty `.blank` file, wiping out any soundings previously gridded into that surface.
