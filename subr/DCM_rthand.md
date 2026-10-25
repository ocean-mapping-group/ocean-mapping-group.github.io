---
layout: default
title: DCM_rthand
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/DCM_rthand.c
category: Coordinate Geometry & 3D Attitude Transformations
related_tools:
- unrollOMG
- makeWC
- DelayEditor
- synSwath
- swathed
- makeSeisPlot
module_name: DCM_rthand
header_path: code/subr/DCM_rthand.h
---

# DCM_rthand: Direction Cosine Matrix (Right-Handed) Attitude & Vector Transformations

## Overview & Purpose
`DCM_rthand` provides the core data types, constants, and function declarations for right-handed 3D coordinate system rotations and Direction Cosine Matrix (DCM) transformations across the Ocean Mapping Group (OMG) codebase. Written by John Hughes Clarke in September 1995, it standardizes the ship/sensor reference frame convention used throughout OMG multibeam, laser, and water-column processing tools:

* **+X axis:** Forward (bow)
* **+Y axis:** Starboard (right)
* **+Z axis:** Downward (nadir)
* **+Pitch:** Bow up
* **+Roll:** Port up (starboard down)
* **+Yaw (Heading):** Turn to starboard (clockwise viewed from above)

While `DCM_rthand.c` defines the global `rotation_sequence` state variable (supporting Tait-Bryan and Hippy conventions in synthetic swath and OpenGL rendering tools), `DCM_rthand.h` is one of the most widely included headers in the entire repository, defining the fundamental `location`, `fvect`, `svect`, `attitude`, `fattitude`, and `fphase` structures used by `OMG_HDCS_jversion` and nearly all geometric raytracing and lever-arm modules.

---

## Key Data Structures, Constants & Macros

### Rotation Sequence Constants
Used primarily by `synSwath` and 3D OpenGL visualization tools (`jGL_draw.c`) to switch between Euler/Tait-Bryan rotation orders:

```c
extern int rotation_sequence;

#define ROT_YPR_TB 0   /* Standard Tait-Bryan Yaw-Pitch-Roll sequence */
#define ROT_HIPPY  1   /* Hippy sensor convention */
#define ROT_YRP    2   /* Yaw-Roll-Pitch */
#define ROT_PRY    3   /* Pitch-Roll-Yaw */
#define ROT_RPY    4   /* Roll-Pitch-Yaw */
#define ROT_RYP    5   /* Roll-Yaw-Pitch */
#define ROT_PYR    6   /* Pitch-Yaw-Roll */
```

### Attitude & Vector Structures

```c
typedef struct {
    double roll;
    double pitch;
    double yaw;
} attitude;

typedef struct {
    float roll;
    float pitch;
    float yaw;
} fattitude;

typedef struct {
    double x;
    double y;
    double z;
} location;

typedef struct {
    float x;
    float y;
    float z;
} fvect;

typedef struct {
    short x;
    short y;
    short z;
} svect;

typedef struct {
    float I;
    float Q;
} fphase;
```
* **`attitude` / `fattitude`**: Double- and single-precision 3-axis Euler orientation angles (roll, pitch, yaw/heading), typically expressed in degrees or radians depending on the calling routine.
* **`location` / `fvect` / `svect`**: Double-precision, single-precision, and 16-bit integer 3D Cartesian coordinate/lever-arm vectors $(x, y, z)$.
* **`fphase`**: In-phase ($I$) and Quadrature ($Q$) complex acoustic sample pair.

---

## Public Functions & Signatures

### Double-Precision DCM Rotations

```c
void DCM_rotate(location orig, attitude rotate, location *final);
void DCM_unrotate(location orig, attitude rotate, location *final);

void jDCM_rotate(location orig, attitude rotate, location *final);
void jDCM_unrotate(location orig, attitude rotate, location *final);
```
* **Purpose:** Rotates (`DCM_rotate` / `jDCM_rotate`) or inverse-rotates (`DCM_unrotate` / `jDCM_unrotate`) a 3D double-precision vector `orig` by the Euler angles in `rotate`, writing the transformed vector to `*final`. Used to map lever arms and beam vectors between the Ship Reference Frame (SRF) and the Local Level / Geographic Reference Frame.

### Single-Precision DCM Rotations

```c
void DCM_rotatef(fvect orig, attitude rotate, fvect *final);
void DCM_unrotatef(fvect orig, attitude rotate, fvect *final);

void jDCM_rotatef(fvect orig, attitude rotate, fvect *final);
void jDCM_unrotatef(fvect orig, attitude rotate, fvect *final);
```
* **Purpose:** Single-precision (`fvect`) counterparts to the double-precision DCM rotation routines, heavily used in real-time OpenGL rendering, cone/beam intersections (`j_non_ortho_cones.c`), ADCP beam transformations (`SYN_ADCP.c`), and internal wave raytracing (`SYN_internal_wave.c`).

### Yaw Misalignment Cross-Coupling Solvers

```c
int OtoR(double ym, double or, double op, double *tr, double *tp);
int RtoO(double ym, double tr, double tp, double *or, double *op);
```
* **Parameters:**
  * `ym`: Yaw misalignment angle between the motion sensor and vessel/sonar frame.
  * `or`, `op`: Observed roll and pitch angles.
  * `tr`, `tp`: True roll and pitch angles.
* **Purpose:** Computes how a yaw mounting misalignment (`ym`) cross-couples observed roll and pitch (`or`, `op`) into true roll and pitch (`tr`, `tp`) and vice versa during patch test calibration.

---

## How It Fits Into the OMG Architecture
`DCM_rthand.h` is directly included by `OMG_HDCS_jversion.h`, making its `location`, `fvect`, and `attitude` types ubiquitous across the entire OMG software suite:
* **Core I/O & Lever Arm Compensation (`OMG_HDCS_jversion.c`, `unrollOMG.c`):** Uses `DCM_rotate` and `location lever_arm` to compute motion-induced lever-arm displacements between the IMU, GPS antenna, and multibeam transducer.
* **Patch Test & Delay Editing (`DelayEditor.c`, `SE_PATCHwin.c`):** Resolves angular mounting offsets and time delays between attitude sensors and multibeam sonar heads.
* **3D Visualization & Synthetic Modeling (`synSwath.c`, `jGL_draw.c`, `SYN_internal_wave.c`, `SYN_ADCP.c`):** Applies `DCM_rotate` and `DCM_rotatef` to orient 3D beam cones, water column fans, and vessel models in real time.
