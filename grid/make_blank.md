---
layout: default
title: make_blank
parent: grid Tools
nav_order: 1
tool_name: make_blank
source_path: code/grid/make_blank.c
category: Gridding & Bathymetric Surface Generation
input_formats: [".merged", ".nav", ".ss", "JHC_header (.r4 / .8bit)"]
output_formats: [".blank"]
related_tools: ["tor4", "tomos", "weigh_grid", "mos2", "edhead", "r4to8bit", "addSUN"]
---

# make_blank

## Description
`make_blank` initializes a blank OMG1 `JHC_header` array file (`<prefix>.blank`) with a specified geographic projection (Mercator, UTM, Rotated UTM, Rotated Mercator, or Lambert Conformal Conic), bounding box, and pixel resolution (meters per pixel, `mpp`).

In the OMG gridding and sidescan mosaicking workflows, `make_blank` is **always Step 1**. Neither [`weigh_grid`](weigh_grid.md) nor [`mos2`](../newmos/mos2.md) creates grid headers from scratch; instead, you run `make_blank` to define the map sheet geometry (`<prefix>.blank`), and then run the helper scripts [`tor4`](../scripts/tor4.md) (which copies `<prefix>.blank` to `.r4`, `.r4_weights`, and `.r4_weight_depth` for `weigh_grid`) or [`tomos`](../scripts/tomos.md) (which copies `<prefix>.blank` to `.mos` and `.ran` for `mos2`).

---

## Usage

```bash
make_blank [OPTIONS] <outfilename_prefix>
```
*(Note: `make_blank` automatically appends `.blank` to `<outfilename_prefix>`. Keep `-boundsof`, `-boundsof_nav`, or `-boundsof_ss` as the **last** option on the command line if used, or pass `<outfilename_prefix>` before `-boundsof` because `-boundsof` consumes all remaining arguments!)*

### Common Workflow Examples

**1. Create a floating-point `.blank` grid automatically bounded by a set of `.merged` files (for bathymetry gridding):**
```bash
# Put the output prefix BEFORE -boundsof because -boundsof reads all trailing arguments!
make_blank -float survey_area -boundsof merged/JD100/*.merged
# Interactive prompt will ask: "input desired mpp :" (e.g. enter 2.0 for 2m grid)

# Prepare .r4, .r4_weights, and .r4_weight_depth files for weigh_grid:
tor4 survey_area.blank
```

**2. Create an 8-bit `.blank` grid primed to `255` (for sidescan mosaicking with `mos2`):**
```bash
make_blank -8bit -prime 255 survey_mos -boundsof_ss ss/JD100/*.ss
# Prepare .mos and .ran files for mos2:
tomos survey_mos.blank
```

**3. Clone the exact projection and bounds of an existing mapsheet (`-area`), changing only resolution or data type:**
```bash
make_blank -float -area existing_map.r4 new_highres_map
```

**4. Create a UTM-projected floating-point `.blank` grid from `.merged` files with central meridian `-66.0`:**
```bash
make_blank -float -utm_boundsof -merid -66.0 fundy_utm -boundsof merged/JD100/*.merged
```

---

## Arguments

### Data Type & Initialization Value

| Option | Description | Default |
|---|---|---|
| `<outfilename_prefix>` | Output filename prefix; `.blank` is appended automatically. (Place **before** `-boundsof*` flags!). | Prompted on stdin if omitted |
| `-float` | Create a 32-bit floating-point array (`header.data_type = 3`, 4 bytes/pixel). Required for `weigh_grid` (`.r4`). | Prompted (`1=8bit, 2=float`) if neither `-float` nor `-8bit` is set |
| `-8bit` | Create an 8-bit unsigned char array (`header.data_type = 1`, 1 byte/pixel). Required for `mos2` (`.mos`). | Prompted if omitted |
| `-prime <value>` | Fill (prime) all pixels in the blank array with `<value>` (use `0.0` for `.r4` bathymetry grids, `255` for `.mos` sidescan mosaics). | `0.0` |
| `-just_header` | Write only the 1024-byte `JHC_header` without allocating or writing the pixel array body. | Disabled |

### Bounding Box & Geographic Extent

| Option | Description | Default |
|---|---|---|
| `-boundsof <files.merged...>` | Automatically scan the summary headers of all listed `.merged` files to determine min/max latitude and longitude. **Must be the last flag on the command line** (consumes all trailing arguments).Prompts only for desired `mpp` (meters per pixel). | Interactive prompt |
| `-boundsof_nav <files.nav...>` | Automatically scan all listed `.nav` files to determine min/max latitude and longitude. **Must be the last flag on the command line.** | Interactive prompt |
| `-boundsof_ss <files.ss...>` | Automatically scan all listed GLORIA `.ss` files to determine min/max latitude and longitude. **Must be the last flag on the command line.** | Interactive prompt |
| `-area <header_file>` | Copy geographic bounds, ellipsoid, and projection from an existing OMG1 array file (`.r4`, `.8bit`, `.blank`, `.mos`). Still prompts for desired `mpp` unless `-centre_expand` or `-maxdimen` is used. | Disabled |
| `-centred_on <file.merged> <ping_num>` | Center the mapsheet on the exact coordinates of `<ping_num>` in `<file.merged>`. | Disabled |
| `-centred_on_nav <file.nav>` | Center the mapsheet on the middle record (`num_nav_recs / 2`) of `<file.nav>`. | Disabled |
| `-centre_expand` | Used with `-area` and `-newxylen <x_m> <y_m>`: expands or contracts the mapsheet around its center coordinate to the new X and Y dimensions in meters. | Disabled |
| `-newxylen <x_m> <y_m>` | Target width (`x_m`) and height (`y_m`) in meters when using `-centre_expand`, `-centred_on`, or `-centred_on_nav`. | None |
| `-maxdimen <pixels>` | Automatically compute `mpp` so that the larger grid dimension (`dx` or `dy`) equals `<pixels>`. Avoids interactive `mpp` prompt! | Prompt for `mpp` |

### Projection Options

| Option | Description | Default |
|---|---|---|
| `-merc` | Use standard Mercator projection (`Proj_Type = 1`, WGS84). | Default (`1`) |
| `-utm` | Use Universal Transverse Mercator (UTM) projection (`Proj_Type = 2`). | Disabled |
| `-utm_boundsof` | Used with `-boundsof*`: use UTM projection (`header.projection = 2`) instead of Mercator. Requires `-merid <lon>`. | Mercator (`1`) |
| `-merid <deg>` | Central meridian (decimal degrees, e.g., `-66.0` for 66°W) for UTM projections. | Prompted if needed |
| `-rotutm` | Use Rotated UTM projection (`Proj_Type = 4`). | Disabled |
| `-rotmerc` | Use Rotated Mercator projection (`Proj_Type = 5`). | Disabled |
| `-force_orthogonal` | Used with `-area`: converts a rotated mapsheet into an unrotated North-up bounding box encompassing all 4 corners. | Disabled |
| `-force_orthogonal_mercator` | Same as `-force_orthogonal`, forcing Mercator projection. | Disabled |
| `-force_rotate90` / `-minus90` | Used with `-area`: rotates a rotated mapsheet by $+90^\circ$ or $-90^\circ$. | Disabled |
| `-force_square` | Forces `dx` and `dy` to be equal on rotated mapsheets. | Disabled |

### Synthetic / Custom Test Surface Generation

| Option | Description |
|---|---|
| `-custom` | Interactive synthetic terrain generator: prompts for `mpp`, `dx`, `dy`, and embeds synthetic 3D shapes (sine waves, cubes, hemispheres, vertical/horizontal cylinders, rectangles, knolls, gridpoints, radiating/embossed sine waves) for algorithm testing. |
| `-colorbar` | Generates a standard color bar array. |
| `-sun` / `-red` / `-green` / `-blue` | Sets `header.rgb_bw` color channel flags. |
| `-v` | Verbose output. |

---

## Important Usage Notes

1. **Argument Order with `-boundsof`:**
   In `make_blank.c` (lines 386–392), `-boundsof`, `-boundsof_nav`, and `-boundsof_ss` loop over `while (*argv)` until the end of the command line! Therefore, if you place the output filename *after* `-boundsof *.merged`, `make_blank` will treat your output filename as a `.merged` input file and then prompt you interactively for the output filename. **Always put the output filename before `-boundsof`:**
   ```bash
   # CORRECT:
   make_blank -float my_grid -boundsof merged/JD100/*.merged
   ```
2. **Non-Interactive Execution in Scripts:**
   When using `-boundsof`, `make_blank` normally prompts stdin for `input desired mpp :`. You can either pipe the resolution via `echo 2.0 | make_blank -float my_grid -boundsof ...` or pass `-maxdimen 2000` to size the grid automatically without stdin prompts.
