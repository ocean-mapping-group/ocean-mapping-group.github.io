---
layout: default
title: swath_geometry
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/swath_geometry.c
category: Bathymetric & Swath Cleaning
related_tools:
- OMG_HDCS_jversion
- swathed
- autoClean
module_name: swath_geometry
header_path: code/subr/swath_geometry.h
---

# swath_geometry

## Overview
`swath_geometry` (`swath_geometry.c` / `swath_geometry.h`) provides automated geometric quality-control filters for detecting and flagging **common-range ambiguity** (sidelobe/backlobe arc artifacts) and **first water-column multiple** bottom detections in OMG-HDCS multibeam swath profiles (`OMG_HDCS_profile_header` and `OMG_HDCS_beam` arrays).

When an outer beam locks onto a strong specular nadir reflection (via sidelobe leakage) or a second-bounce surface-seafloor multiple, the slant range progression from nadir (`beam = numDepths / 2`) outward to the swath edge exhibits characteristic geometric anomalies. `swath_geometry` identifies these anomalies per ping and flags affected beams with `beam[i].status = 22` (rejected by automated filter).

---

## Global Variables

- `int debug_swath_geometry` — When non-zero, prints per-beam slant range progressions, detected range turning points (`min_range --> max_range`), and counts of flagged port/starboard beams to `stdout`.

---

## Public Functions

| Function | Signature | Description |
|---|---|---|
| `checkCommonRangeAmbiguity` | `int checkCommonRangeAmbiguity(OMG_HDCS_profile_header *profile, OMG_HDCS_beam *beams)` | Scans outward from the nadir beam (`profile->numDepths / 2`) independently toward Port (`i = nadir_beam - 1 .. 1`) and Starboard (`i = nadir_beam + 1 .. numDepths - 1`). On a flat or monotonically sloping seabed, slant range `beams[i].range` should increase monotonically with beam angle away from nadir. Whenever `beams[i].range` reverses direction (`beams[i].range <= last_range_checked`), the function records a turning-point range interval `[min_range, max_range]` and subsequently flags all valid beams on that side whose slant range falls within any turning-point interval by setting `beams[i].status = 22`. |
| `checkMultiple` | `int checkMultiple(OMG_HDCS_profile_header *profile, OMG_HDCS_beam *beams)` | Finds the minimum valid slant range `min_range` across all unflagged beams (`beams[i].observedDepth && !beams[i].status && beams[i].range > 0`) in the ping, computes the first-multiple threshold `max_range = min_range * 2`, and flags every beam with `beams[i].range >= max_range` by setting `beams[i].status = 22`. |

---

## Algorithm Details

### 1. Common-Range Ambiguity (`checkCommonRangeAmbiguity`)
1. Locate the first valid beam near nadir (`nadir_beam = profile->numDepths / 2`).
2. Step outward toward the swath edge, skipping already-flagged or zero-depth beams.
3. Track `last_range_checked`:
   - If `beams[i].range <= last_range_checked`, a range reversal has begun (`direction_change = 1`). Record `max_range = last_range_checked` at the onset of the reversal and track the minimum range `min_range` reached during the reversal.
   - When `beams[i].range > last_range_checked` again (`direction_change` returns to `0`), store the pair `(min_range, max_range)` in `port_turning_points[]` or `stbd_turning_points[]`.
4. Flag all beams on the corresponding half-swath whose `range` lies inside any `[min_range, max_range]` bracket with `status = 22`.

### 2. Water-Column Multiple Rejection (`checkMultiple`)
1. Scan all valid beams in the ping to determine `min_range` (typically the nadir depth/range).
2. Set `max_range = 2 * min_range` (the two-way travel time / range of the first surface-bottom-surface multiple).
3. Any beam with `beams[i].range >= 2 * min_range` is flagged with `status = 22`.

---

## Architectural Role
`swath_geometry` is used by interactive and batch swath-cleaning tools (`swathed`, `autoClean`) to strip sidelobe arcs and double-bounce multiples from OMG-HDCS `.merged` files prior to gridding with `weigh_grid`.
