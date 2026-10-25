---
layout: default
title: grazing_angle
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/grazing_angle.c
category: Acoustic Backscatter, Radiometry & Calibration
related_tools:
- Echo_calib
- jview
- EKlook
- DelayEditor
- getAngularResponse
- get_ADH_SRA
- applySectBP
module_name: grazing_angle
header_path: code/subr/grazing_angle.h
---

# `grazing_angle` — 3D Beam-Seafloor Incidence and Grazing Angle Engine

## Overview & Purpose
The `grazing_angle` module (`code/subr/grazing_angle.c` and `code/subr/grazing_angle.h`, ~2,015 lines) computes the true acoustic grazing angle (and its complement, the angle of incidence) between an arriving refracted multibeam ray vector and the local 3D seafloor surface normal. Originally written by Jonathan Beaudoin (~2009–2010), expanded by Anand Hiroji (`ADH`, 2014–2017) to separate sonar-relative angles (`SRA`) from seafloor grazing angles (`GRA`), and unified by John Hughes Clarke in June 2021, this library is critical for removing topographic slope artifacts from seafloor backscatter mosaics and extracting angular response curves (`ARC`).

---

## Key Constants, Structures & Global Controls (`grazing_angle.h`)

### 1. Angle Determination Mode Constants
- `#define ADM_ORIGINAL 0`: Compute grazing angles on the fly from HDCS bathymetry or a reference DTM.
- `#define GET_FROM_VRAFILE 1`: Read Vertically Referenced Angles (`VRA`) from an auxiliary `.r4` file.
- `#define GET_FROM_SRAFILE 2`: Read Sonar-Relative Angles (`SRA`) from an auxiliary `.r4` file.
- `#define GET_FROM_GRAFILE 3`: Read precomputed Grazing Angles (`GRA`) from an auxiliary `.r4` file.

### 2. Core Data Structures

```c
typedef struct {
    int ping_number;
    int beam_no;
    double lat, lon;
    float depth;
    double lat_scale, lon_scale;
} gra_beam;

typedef struct {
    int beamcalc_method;        /* 0: flat, 1: straight-line, 2: raytraced, 3: precalc */
    vector_3D sonar_to_seabed;  /* Metric displacement from transducer to sounding */
    double slant_range_m;
    vector_3D launch_vector_Tx;
    vector_3D return_vector_Rx;
    vector_3D arriving_vector;  /* Refracted acoustic ray vector arriving at seabed */
    int grazcalc_method;        /* 0: flat, 1: 2D profile, 2: 3D swath patch, 3: 3D DTM */
    vector_3D seabed_normal;    /* Unit 3D normal vector of the local seafloor */
    float launch_angle;
    float incidence;
    float sonar_relative;
} beam_seabed_geometry;
```

---

## Public Functions & Signatures

### 1. 2D Across-Track Profile Grazing Angles

```c
int get_grazing_angles(OMG_HDCS_summary_header summary, OMG_HDCS_profile_header profile,
                       OMG_HDCS_beam *beams, float *grazing_angles,
                       int apply_local_slope, OMG_HDCS_sonar_params *sonar_parameters);
```
- **Purpose:** Fast 1D/2D calculation for a single ping. Computes nominal flat-bottom grazing angle $\theta_g = \arctan(Z / R_{\text{horiz}})$ (accounting for transducer draft, heave, and AUV depth via `GA_AUV_draft`). When `apply_local_slope` is non-zero, estimates local across-track seabed slope from the nearest valid port and starboard neighbor beams and subtracts the apparent slope angle.

### 2. Full 3D Swath-Patch Plane-Fit Grazing Angles

```c
int get_full_grazing_angles(FILE *infile, float *grazing_angles, int ping_number,
                            int max_no_pings, OMG_HDCS_sonar_params *sonar_parameters);
int get_full_grazing_angles_ADH(FILE *infile, float *grazing_angles, float *beam_depression_angles,
                                float *beam_azimuth_angles, float *sonar_relative_angles_across,
                                float *sonar_relative_angles_along, int ping_number,
                                int max_no_pings, OMG_HDCS_sonar_params *sonar_parameters);
fvect least_square_plane(fvect *points, int num_points, int *valid_points);
fvect least_square_plane_ADH(fvect **points, int **valid_points);
```
- **Purpose:** Computes true 3D grazing angles directly from ungridded HDCS swath bathymetry without requiring an external DTM.
- **Algorithm:**
  1. Caches a sliding window of pings (`prev_ping`, `this_ping`, `next_ping` in `get_full_grazing_angles`, or a configurable $(2N_p+1) \times (2N_b+1)$ neighborhood controlled by `NoPings_for_FullGrazing` and `NoBeams_for_FullGrazing` in the `_ADH` variant).
  2. Converts geographic coordinates of the neighborhood soundings into local metric offsets relative to the center beam using `get_lat_lon_scales()`.
  3. Fits a 3D plane $z = ax + by + c$ via ordinary least squares (`least_square_plane`) or 3D covariance eigenvector decomposition (`least_square_plane_ADH`) to obtain the outward unit seafloor normal $\hat{\mathbf{n}}$.
  4. Computes the dot product between the incoming 3D beam vector and $\hat{\mathbf{n}}$ to derive the true 3D grazing angle.

### 3. Reference DTM 3D Grazing Angles

```c
int get_dtm_grazing_angles(FILE *infile, JHC_header *dtm_header, float *dtm,
                           float *grazing_angles, int ping_number,
                           OMG_HDCS_sonar_params *sonar_parameters);
int get_dtm_grazing_angles_ADH(FILE *infile, JHC_header *dtm_header, float *dtm, ...);
```
- **Purpose:** Projects each beam's geographic position onto a gridded `.r4` digital terrain model (`Project()`), constructs 3D surface vectors to the adjacent North, South, East, and West DTM grid nodes, averages the resulting cross-product surface normals across the four quadrants, and computes the 3D beam-normal dot product.

---

## How It Fits Into the OMG Architecture
`grazing_angle` bridges swath geometry and radiometric backscatter normalization:
- **Backscatter Calibration & Normalization (`Echo_calib`, `jview`, `getAngularResponse`, `get_ADH_SRA`, `applySectBP`):** Separates transducer beam-pattern effects (governed by `SRA`) from seafloor intrinsic angular response (governed by `GRA`).
- **Water-Column & Echosounder Analysis (`EKlook`, `DelayEditor`):** Supplies local seabed slope and incidence angles for bottom-echo compensation.
