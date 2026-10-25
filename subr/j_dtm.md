---
layout: default
title: j_dtm
parent: Core Shared Libraries (subr)
module_name: j_dtm
source_path: code/subr/j_dtm.c
header_path: code/subr/j_dtm.h
category: Bathymetric Gridding & DTM Management
related_tools:
  - weigh_grid
  - r4toz
  - jview
---

# `j_dtm` — Weighted Digital Terrain Model (DTM) Bundle & Header Management Library

## Overview & Purpose in the OMG Architecture

`j_dtm` (`code/subr/j_dtm.c`, `code/subr/j_dtm.h`), authored by John E. Hughes Clarke (September 1989 / September 1998), manages the multi-file **OMG Weighted Digital Terrain Model (`jDTMbundle`)** format used during incremental multibeam bathymetric gridding (`weigh_grid`).

When gridding multibeam soundings into a floating-point Digital Terrain Model (`.r4`), OMG's weighted gridding engine maintains three parallel raster files:
1. `<prefix>.r4`: The normalized depth grid (`z`).
2. `<prefix>.r4_weights`: The accumulated sum of spatial/beam weights (`sum_w`) at each grid node.
3. `<prefix>.r4_weight_depth`: The accumulated sum of weighted depths (`sum_wd = sum(w * z)`) at each grid node.

To ensure that subsequent gridding runs appending additional survey lines to an existing DTM use identical gridding parameters, `j_dtm` packs all gridding metadata, filter parameters, and per-beam weight/mask tables into the unused 768-byte `rgb_cmap` color-table blocks across the three `JHC_header` headers (`768 * 3 = 2304` bytes total).

---

## Key Data Structures, Constants & Macros

### Input Format & Weighting Model Constants (`code/subr/j_dtm.h`)
- **Input Data Formats**: `URI_SEABEAM` (`1`), `LOLADE_ASCII` (`2`), `OMG_EM12` (`3`), `OMG_HDCS` (`4`), `OMG_MR1` (`5`), `OMG_AR` (`6`).
- **Gridding Methods (`method`)**:
  - `SHOALBIAS_METHOD` (`0`): Shoal-biased binning.
  - `PURE_WT_FILTER_METHOD` (`1`): Pure distance-weighted interpolation.
  - `PERC_WT_FILTER_METHOD` (`2`): Depth-percentage scaled distance weighting.
  - `BEAM_WT_FILTER_METHOD` (`3`): True 3D acoustic beam footprint weighting.
- **Weighting Models (`wtmodel`)**: `UNSPEC` (`0`), `LINEAR` (`1`), `BUTTER` (`2` — Butterworth filter), `RECIP` (`3` — reciprocal distance), `BEAMWIDTH` (`4`).
- **Footprint Asymmetry (`along_across_asym`)**: `FT_ALONG` (`1`), `FT_ACROSS` (`2`), `FT_ASYM` (`3`).

### Core Struct: `jDTMbundle`
Encapsulates the file handles, memory pointers, raster headers, and serialized gridding configuration of a weighted DTM:
- **File Pointers & Data Buffers**:
  - `FILE *r4d_fp`, `*r4w_fp`, `*r4wd_fp`, `*r4ww_fp`: File streams for `.r4`, `.r4_weights`, `.r4_weight_depth`, and future variance `.r4_ww`.
  - `float *z`, `*sum_w`, `*sum_wd`, `*sum_ww`: In-memory 2D float arrays.
  - `int opened`, `usenmap`: File open state and `mmap` usage flag.
  - `JHC_header r4head`, `r4whead`, `r4wdhead`, `r4wwhead`: Individual 1024-byte OMG raster headers.
- **Gridding & Filter Parameters**:
  - `unsigned char usetide`, `toolType`, `input_dataformat`, `method`, `wtmodel`, `along_across_asym`.
  - `float beamwidth`: Transducer beamwidth in degrees.
  - `float power`, `lambda`, `cutoff`: Absolute spatial filter decay power, wavelength, and cutoff radius.
  - `float perc_lambda`, `perc_cutoff`: Depth-percentage scaled filter wavelength and cutoff radius.
  - `float zmin`, `zmax`, `zshift`, `pixshift_X`, `pixshift_Y`: Depth clipping bounds and datum/pixel shifts.
- **Per-Beam Weighting & Mask Tables**:
  - `unsigned char beam_mask[256]`: Per-beam accept/reject mask stored in the 3rd header's `rgb_cmap`.
  - `unsigned char cbeam_weight[256]`: Compact 8-bit beam weights (in units of `0.005`, representing `0.0` to `1.0` across 200 levels) stored in the 2nd header's `rgb_cmap`.
  - `float beam_weight[256]`: Expanded floating-point beam weights (`cbeam_weight[i] / 200.0`).

---

## Public Functions & Signatures

- `int jDTM_open_and_loadhead(char *prefix, jDTMbundle *jdtm)`
  Opens `<prefix>.r4`, `<prefix>.r4_weights`, and `<prefix>.r4_weight_depth` in read-update (`"r+"`) mode, reads their three `JHC_header` structures via `read_JHC_header()`, concatenates their three 768-byte `rgb_cmap` arrays into a 2304-byte `combohead` buffer, and unpacks all gridding parameters, `cbeam_weight` (expanding to `beam_weight`), and `beam_mask` using endian-safe `get_swapped_char()` and `get_swapped_float()`. Returns `1` on success, `-1` if `.r4` cannot be opened, `0` if weight files are missing, or `-2` on header read error.

- `int jDTM_dumphead(jDTMbundle *jdtm)`
  Serializes all gridding parameters, quantizes `beam_weight[] * 200.0` into `cbeam_weight[]`, packs `beam_mask[]` into the 2304-byte `combohead` buffer using `put_swapped_char()` and `put_swapped_float()`, distributes the three 768-byte segments back into `r4head.rgb_cmap`, `r4whead.rgb_cmap`, and `r4wdhead.rgb_cmap`, and writes all three headers back to disk via `write_JHC_header()`.

- `int jDTM_closefiles(jDTMbundle *jdtm)`
  Closes `r4d_fp`, `r4w_fp`, and `r4wd_fp`, and resets `jdtm->opened = 0`.

---

## How It Fits Into the OMG Architecture

`j_dtm` is the persistence layer for `weigh_grid` and related DTM manipulation utilities in `code/omg/` and `code/JV/`. By embedding gridding provenance directly inside the `JHC_header` colormap space of the `.r4`, `.r4_weights`, and `.r4_weight_depth` files, it guarantees consistent multi-pass gridding without requiring an external sidecar parameter file.
