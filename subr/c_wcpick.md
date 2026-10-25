---
layout: default
title: c_wcpick
parent: Core Shared Libraries (subr)
module_name: c_wcpick
source_path: code/subr/c_wcpick.c
header_path: code/subr/c_wcpick.h
category: Water Column Target Detection & Picking
related_tools:
  - swathed
  - targethunt
---

# c_wcpick: 3D Water-Column Target Hunting, Sidelobe Suppression & Picking Interface

## Overview & Purpose
`c_wcpick` (`c_wcpick.h` / `c_wcpick.c`) defines the data structures, constants, Dolph-Chebyshev array shading lookup coefficients, and function prototypes for automated 3D target detection and sidelobe artifact suppression in multibeam water-column data (`j_EM_watercolumn`). Authored by Carlos Marques in January 2012 for the OMG water-column target-hunting workflow (`targethunt` and `swathed`), the module models 3D transmit/receive beam patterns in the water column to distinguish true mid-water acoustic targets (such as gas flares, wrecks, fish shoals, or mastheads) from Minimum Slant Range (MSR) specular sidelobe arcs and across/along-track beam-pattern leakage.

---

## Key Constants, Global Parameters & Data Structures

### Detection & Shading Constants
```c
#define C_RESET_THRESHOLD -127
#define C_MAXTARGETSIZE     20
#define C_MAXSAMPLES      8000
#define C_MAXBEAMS        1024
#define C_MAXSWATHS       1000
#define C_MAXSECTORS      1024
#define C_MAXAMPLITUDE     128
#define C_HIGHSCATTERTARGET -10

/* Array Shading Function Identifiers */
#define CHEBY_SHADELEVEL          30
#define C_DEFAULT_ARRAY_ELEM_MULT 0.2
#define C_SHADINGFUN_UNSHADED     0
#define C_SHADINGFUN_LINEAR       1
#define C_SHADINGFUN_COS          2
#define C_SHADINGFUN_COS_SQUARED  3
#define C_SHADINGFUN_DOLPH        4
```
*(Note: `c_wcpick.c` contains the hardcoded high-index tail of the `arrDolph[]` Dolph-Chebyshev shading coefficient table, while the full target-hunting implementation resides in `code/omg/targethunt.c` and `code/SE/SE_WaterColumn.c`.)*

### User Search & Threshold Control Globals
* **Thresholding:** `c_user_amplOffset`, `c_user_thresMult`, `c_user_thresDepthMult`, `c_user_ithreshold`.
* **3D Neighborhood Box & Beamwidths:** `c_user_checkSample` (range samples to each side), `c_user_checkBeam` (beams to each side), `c_user_checkSwath` (pings/swaths to each side), `c_user_PL` (pulse length), `c_user_tx_BW` (transmit beamwidth), `c_user_rc_BW` (receive beamwidth).
* **Search Volume Bounds:** `c_user_nsectors`, `c_user_sectors[1024]`, `c_user_minSwath`, `c_user_maxSwath`, `c_user_minBeam`, `c_user_maxBeam`, `c_user_minSamples`, `c_user_maxSamples`, `c_user_minRange`, `c_user_maxRange`.
* **Filtering & Pattern-Matching Flags:**
  * `c_user_noMSR`: Exclude samples beyond the Minimum Slant Range (seafloor specular echo).
  * `c_user_MSRbySector`: Compute MSR independently for each transmit sector.
  * `c_user_noPatternMatchRange`, `c_user_noPatternMatchAcross`, `c_user_noPatternMatchAlong`: Toggle 3D point-spread-function (PSF) sidelobe pattern matching in range, across-track, and along-track dimensions.

### Target Shape Modeling Structures (`targetPiece` & `targetShape`)
```c
typedef struct {
    double sizex;        /* Expected size of target piece across-track (m) */
    double sizey;        /* Expected size of target piece along-track (m) */
    double sizez;        /* Expected vertical size of target piece in Z (m) */
    double dist;         /* Distance from this piece to the next piece */
    double angleAcross;  /* Across-track angle to next piece (0 = down, +stbd, -port) */
    double angleAlong;   /* Along-track angle to next piece (0 = down, +fwd, -aft) */
    double stretchCoef;  /* Depth-dependent stretching coefficient (%) */
} targetPiece;

typedef struct {
    int          nPieces;  /* Number of connected pieces composing the target */
    targetPiece *pieces;   /* Array of target pieces */
    double       seafloor; /* Distance from last piece to seafloor (-1 for floating) */
} targetShape;
```

---

## Public Functions & Signatures

### Main Target & Detection Hunting Functions
* `int c_hunt_for_targets(j_EM_watercolumn *hunt_wcs, int nowcs, OMG_Target_List *SE_targetList, OMG_HDCS_profile_header *hunt_WC_profile, OMG_HDCS_summary_header hunt_WC_summary, double geo_cen[][3], float *heading, double *pingtime, int recnum, short *ApplyedThresholds)`
  Scans a sequence of `nowcs` water-column swaths (`hunt_wcs`), applies dynamic amplitude thresholding and 3D beam-pattern sidelobe rejection, clusters contiguous 3D detections into targets, georeferences them using `geo_cen` and `heading`, and appends them to `*SE_targetList`.
* `int c_hunt_for_detections(...)`
  Performs raw sample-level detection hunting across `nowcs` water-column records without multi-ping target clustering.
* `int c_mark_targets(j_EM_watercolumn *hunt_wcs, int nowcs, OMG_Target_List *SE_targetList, int startWc)`
  Marks detected targets back into the water-column display buffers for visual overlay.

### Filtering & Beam Pattern Modeling Helpers
* `int c_excludeDetections(OMG_Target_List *SE_targetList, int verbose)`
* `int c_excludeTargets(OMG_Target_List *SE_targetList, int verbose)`
  Filters out false-positive detections and sidelobe ghost targets from `*SE_targetList`.
* `short c_findSwathType(j_EM_watercolumn *hunt_wcs, int nowcs)`
  Determines whether the water-column dataset uses single-swath, dual-swath, or multi-swath frequency diversity.
* `int c_resetUserVars()`
  Resets all `c_user_*` search bounds and threshold parameters to defaults.
* `int c_loadWclSpecs(j_EM_watercolumn *hunt_wcs, OMG_HDCS_profile_header *hunt_WC_profile, OMG_HDCS_summary_header *hunt_WC_summary, double *pingtime, int nowcs, int recnum)`
  Extracts array element spacing, beamwidths, and sector parameters from the HDCS and water-column headers.
* `float **c_getBPat(...)`, `float **c_getBPat2(...)`, `float **c_getBPatTx(...)`
  Computes 2D across-track/along-track expected sidelobe levels at a given `(swath, beam, sample)` voxel for 3D PSF suppression.

---

## How It Fits Into the OMG Architecture
`c_wcpick.h` provides the shared interface between the command-line water-column target detector `targethunt` (`code/omg/targethunt.c`) and the interactive water-column viewer inside `swathed` (`code/SE/SE_WaterColumn.c` and `code/SE/c_wcl_TOOLBOX.h`), where hydrographers interactively tune threshold and sidelobe rejection parameters to pick wreck masts and gas seeps.
