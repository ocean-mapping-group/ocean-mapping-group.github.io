---
layout: default
title: weigh_grid
parent: grid Tools
nav_order: 2
tool_name: weigh_grid
source_path: code/grid/weigh_grid.c
category: Gridding & Bathymetric Surface Generation
input_formats: [".r4", ".r4_weights", ".r4_weight_depth", ".merged", ".merged.100_ping_bounds", ".merged.global_bounds", "ASCII XYZ"]
output_formats: [".r4 (updated in-place)", ".r4_weights (updated in-place)", ".r4_weight_depth (updated in-place)", ".used", ".regrid"]
related_tools: ["make_blank", "tor4", "getBounds", "r4to8bit", "addSUN", "swathed", "jview"]
---

# weigh_grid

## Description
`weigh_grid` is the core Ocean Mapping Group bathymetric gridding program. It reads soundings from one or more OMG-HDCS `.merged` multibeam files (or MR1 sidescan bathy, or ASCII lon/lat/depth files), projects each unflagged beam into the coordinate system of a pre-initialized floating-point Digital Terrain Model (`<dtmprefix>.r4`), and computes a spatially weighted average depth for every grid cell using a **Butterworth** (default), **reciprocal**, or **linear** distance-weighting function.

Crucially, `weigh_grid` maintains three parallel floating-point array files on disk (initialized from `<dtmprefix>.blank` via the [`tor4`](../scripts/tor4.md) helper script):
1. `<dtmprefix>.r4` — Final weighted-average depth grid ($\sum (w_i z_i) / \sum w_i$).
2. `<dtmprefix>.r4_weights` — Cumulative sum of weights ($\sum w_i$) at every grid node.
3. `<dtmprefix>.r4_weight_depth` — Cumulative sum of weighted depths ($\sum w_i z_i$) at every grid node.

Because `weigh_grid` stores $\sum w_i$ and $\sum (w_i z_i)$ persistently, **you can add new survey lines incrementally to an existing grid** without re-gridding previous lines, or **subtract (`-subtract`) a dirty line**, edit it in [`swathed`](../SE/swathed.md) (which can also live-update `.r4` grids directly via `swathed -locate <dtmprefix>`), and re-add it!

---

## Usage

```bash
weigh_grid [OPTIONS] <dtmprefix> <omgfile(s).merged ...>
```

### Standard Gridding Workflow

```bash
# Step 1: Create a floating-point .blank mapsheet from your .merged files
make_blank -float bay_2m -boundsof merged/JD100/*.merged
# (Enter 2.0 at the "input desired mpp :" prompt)

# Step 2: Copy bay_2m.blank to bay_2m.r4, bay_2m.r4_weights, and bay_2m.r4_weight_depth
tor4 bay_2m.blank

# Step 3: Run weigh_grid with beam weighting to blend outer beams smoothly
weigh_grid -beam_weight bay_2m merged/JD100/*.merged

# Step 4: Convert .r4 to 8-bit and sun-illuminate for viewing in jview
r4to8bit bay_2m
addSUN -azi 315 -elev 45 -vert_exag 5 bay_2m.r4 bay_2m.sun_315
jview bay_2m.8bit -sun bay_2m.sun_315
```

---

## Arguments

### Core Input, Output & Incremental Gridding

| Option | Description | Default |
|---|---|---|
| `<dtmprefix>` | **Required.** Base prefix of the `.r4`, `.r4_weights`, and `.r4_weight_depth` files (e.g., `bay_2m` or `bay_2m.r4`). | None |
| `<omgfile(s)>` | **Required** (unless `-xyzlist` is used). One or more `.merged` (or ASCII/MR1) files to grid (up to 100,000 files). | None |
| `-xyzlist <listfile>` | Read paths of `.merged` (or ASCII) files to grid from a text file (one filepath per line). Up to 5,000 list files can be passed. | Disabled |
| `-fresh_start` / `-fs` | Zero out `.r4`, `.r4_weights`, and `.r4_weight_depth` in memory before gridding, discarding any soundings previously accumulated in the grid. (Without `-fs`, `weigh_grid` *adds* to the existing grid!). | Incremental (adds to existing) |
| `-subtract` | **Subtract** the weighted depth contributions of the specified `.merged` file(s) from `.r4_weights` and `.r4_weight_depth`, then recompute `.r4`. Used to remove a line before or after re-cleaning. | Disabled |
| `-nmap` | Use POSIX `mmap()` memory-mapped file I/O (`do_nmap()`) instead of `calloc()` in-memory buffers—essential for very large regional grids. | Disabled |
| `-no_regrid` | Do not write the `<dtmprefix>.regrid` shell script upon completion. | Writes `.regrid` (`1`) |

### Distance & Beam Weighting Options

| Option | Description | Default |
|---|---|---|
| `-butter` | Use Butterworth radial distance weighting: $w(r) = 1 / [1 + (r / \lambda)^{2 p}]$. | **Default** (`BUTTER`) |
| `-recip` | Use reciprocal distance weighting. | Disabled |
| `-linear` | Use linear cone distance weighting. | Disabled |
| `-power <p>` | Exponent $p$ for the Butterworth filter. | `2.0` |
| `-cutoff <pixels>` | Maximum interpolation search radius around each sounding (in grid pixel units). | `2.0 * mpp` (2 pixels) |
| `-lambda <pixels>` | Half-power (wavelength) radius $\lambda$ for the Butterworth filter (in grid pixel units). | `0.5 * mpp` (0.5 pixels) |
| `-beam_weight` | Apply a 60-point cross-swath beam weighting curve that down-weights noisy outer beams in overlap zones while preserving them where no inner-beam coverage exists. | Disabled |
| `-qfactor_weight` | Weight soundings by their Kongsberg / Ifremer quality factor. | Disabled |
| `-cutoff_scaling` | Dynamically expand the interpolation cutoff radius for outer beams (`sec` or `sec^2` of incidence angle) to prevent gaps in equi-angular modes and smooth outer-swath artifacts. | Disabled |
| `-custom_weight <file>` / `-cw <file>` | Load a custom ASCII beam weight and beam mask table from `<file>`. | Disabled |
| `-beamwidth <deg>` | Acoustic beamwidth (degrees) used to scale the footprint radius with water depth. | `3.3` deg |
| `-along` / `-across` / `-asym` | Footprint expansion geometry mode. | `-along` |
| `-shoal_bias` | Favor shoaler soundings within each grid cell (hydrographic safety mode). | Weighted mean |

### Vertical Datum, Tides, RTK & Heave Corrections

| Option | Description | Default |
|---|---|---|
| `-check_tide` | Verify that `profile.tide` is non-zero before gridding; refuses to grid untided lines. | Disabled |
| `-ignore_tide` | Ignore `profile.tide` (grid raw observed depths relative to water surface). | Uses `profile.tide` (`1`) |
| `-tide2` | Use `profile.Lowpass_RTK_at_RP` as the vertical tide correction instead of `profile.tide`. | Disabled |
| `-rawRTK` | Use raw `profile.RTK_at_RP` and remove observed real-time heave. | Disabled |
| `-blendRTK` | Combine low-pass RTK elevation with high-pass inertial heave. | Disabled |
| `-invert_heave_sign` | Invert the sign of heave when applying RTK corrections. | Disabled |
| `-add_dyn_draft_shift` | Apply `profile.longperiod_heaveCorrection` (typically POS MV delayed heave minus real-time heave). | Disabled |
| `-add_dyn_draft_shift2` | Apply `profile.dynamic_draftCorrection` (typically heave difference between orientation sensor 1 and 2). | Disabled |
| `-flip_dyn_draft` | Invert the sign of the dynamic draft / long-period heave shift. | Disabled |
| `-proc` | Use `beam.processedDepth` (if populated) instead of `beam.observedDepth`. | `observedDepth` |
| `-useallZ` | Include flagged/rejected soundings (`beam.status != 0`) when gridding! Use only for diagnostic comparisons. | Unflagged only (`0`) |
| `-coeffs` | Apply interactive refraction tool coefficients (`.ref_coeffs`) during gridding. | Disabled |
| `-xyz2` | Use the updated 3D beam vector geolocator (`OMG_get_rational_beams`) instead of legacy offset approximation. | Disabled |

### Spatial, Angular, Depth & Temporal Filtering

| Option | Description | Default |
|---|---|---|
| `-try_anyway` | Override the `.merged.global_bounds` / `.100_ping_bounds` bounding-box pre-check and test every ping in every file. Use this if you forgot to run `getBounds` or if bounds metadata is stale. | Uses `getBounds` index |
| `-mindep <m>` / `-maxdep <m>` | Only grid soundings between `<mindep>` and `<maxdep>` (note: OMG depths are negative downward, e.g., `-maxdep -400 -mindep -50`). | `-15000.0` to `+15000.0` |
| `-min_incidence <deg>` / `-max_incidence <deg>` | Restrict gridding to beams with incidence angles between `<min>` and `<max>` degrees. | `0.0` to `90.0` |
| `-leave_outer` | Used with `-max_incidence`: retain outer beams beyond the incidence limit if needed. | Disabled |
| `-etch <N_beams>` | Exclude (etch away) the outermost `<N_beams>` on both port and starboard edges of every swath. | `0` |
| `-port` / `-stbd` / `-both` | Grid only port-side beams, starboard-side beams, or both. | `-both` |
| `-port_2040D` / `-stbd_2040D` | For Dual-Head EM2040D systems: grid only the port or starboard sonar head (`rxFanIndex` / serial number). | Both heads |
| `-azirange <low_deg> <high_deg>` | Only grid pings whose vessel heading falls between `<low_deg>` and `<high_deg>` (supports wrap-around, e.g., `330 30`). | `0` to `360` |
| `-time_start <yr> <jd> <hr> <min> <sec>` | Only grid pings after the specified UTC time. | All times |
| `-time_end <yr> <jd> <hr> <min> <sec>` | Only grid pings before the specified UTC time. | All times |
| `-time_around <unix_sec> <window_sec>` | Only grid pings within $\pm \text{window\_sec}$ of `<unix_sec>`. | Disabled |
| `-select` | Interactively prompt for the first and last ping number to grid for each input file. | Disabled |
| `-skip <N>` | Only grid every $N$-th ping along-track. | `1` |
| `-beamskip <M>` | Only grid every $M$-th beam across-track. | `1` |

### Backscatter, Spectral & ASCII Input Modes

| Option | Description | Default |
|---|---|---|
| `-use_beam_refl` | Grid beam reflectivity values (-64 to +64 dB) instead of bathymetric depth! | Depth |
| `-ar <param_num>` | Grid Angular Response (AR) parameter `<param_num>` (requires `-IArange <min> <max> -bp <bpfile>`). | Disabled |
| `-spect <band>` / `-spectratio <b1> <b2>` | Grid sidescan spectral power bands (`-1` mean, `-2` std dev, `0..6` frequency bands). | Disabled |
| `-ascii` | Input files are ASCII `(lat lon depth)` tables rather than OMG `.merged` files. | `.merged` (`OMG_HDCS`) |
| `-lola` | Used with `-ascii`: input columns are `(lon lat depth)` instead of `(lat lon depth)`. | `(lat lon depth)` |
| `-switchascii` | Used with `-ascii`: negate positive depth values so they conform to OMG's negative-downward convention. | Disabled |
| `-utm` / `-ned` / `-end` | Used with `-ascii`: input coordinates are UTM `(Northing Easting Depth)` or `(Easting Northing Depth)`. Requires `-merid <lon>`. | Geographic |
| `-latshift <min>` / `-lonshift <min>` | Shift input positions by `<min>` arc-minutes. | `0.0` |
| `-llshift <dlat_deg> <dlon_deg>` | Shift input positions by decimal degrees. | `0.0` |
| `-mNmEshift <dN_m> <dE_m>` | Shift input positions by meters North and East. | `0.0` |
| `-depthshift <m>` | Add a constant vertical offset (meters) to all gridded depths. | `0.0` |
| `-hitcount` | Also output a `<dtmprefix>.hits` floating-point grid recording the number of soundings per cell. | Disabled |

---

## Output Files

1. `<dtmprefix>.r4` — Updated 32-bit floating-point bathymetric grid (depths in meters, negative downward; `0.0` = ungridded node).
2. `<dtmprefix>.r4_weights` — Updated 32-bit floating-point sum-of-weights array.
3. `<dtmprefix>.r4_weight_depth` — Updated 32-bit floating-point sum-of-weighted-depths array.
4. `<dtmprefix>.used` — Text log listing all `.merged` files that contributed soundings to the grid.
5. `<dtmprefix>.regrid` — Auto-generated shell script containing the exact `weigh_grid` command line used, making it easy to re-run the grid from scratch with `-fs`.

---

## Troubleshooting

| Symptom / Error | Cause | Resolution |
|---|---|---|
| `Could not open <dtmprefix>.r4_weights` | `weigh_grid` was run on `<dtmprefix>` before `tor4 <dtmprefix>.blank` was executed. | Run `make_blank -float <dtmprefix> ...` followed by `tor4 <dtmprefix>.blank` first. |
| `weigh_grid` finishes immediately and says 0 files contributed (`some_contrib == 0`) | 1) [`getBounds`](../omg/getBounds.md) was not run on the `.merged` files after `mergeNav`, or 2) the `.merged` files lie outside the map bounds of `<dtmprefix>.r4`. | Run `getBounds merged/subdir/*.merged` first, or pass `-try_anyway` to `weigh_grid` to bypass the `.global_bounds` check. |
| Re-running `weigh_grid` doubles the weights of already-gridded lines | By default, `weigh_grid` accumulates into existing `.r4_weights` and `.r4_weight_depth` files. | Pass `-fs` (`-fresh_start`) when re-gridding the entire dataset from scratch, or re-run `tor4 <dtmprefix>.blank` to reset the grid files. |
