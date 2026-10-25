---
layout: default
title: twistVRU
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 27
tool_name: twistVRU
source_path: code/tests/twistVRU.c
category: Attitude Error & Lever-Arm Coordinate Rotations (tests)
input_formats:
  - Interactive stdin prompts: direction (1=OBSERVED->REAL, 2=REAL->OBSERVED, 0=QUIT), YAW_misalign (deg), and roll/pitch pair (deg)
output_formats:
  - Converted TRUE or OBSERVED roll and pitch angles (degrees) on stdout
related_tools:
  - testrot
  - DelayEditor
  - getHorizonRollPitch
  - newMergeAtt
---

# twistVRU

## Overview
`twistVRU` (`code/tests/twistVRU.c`, authored by John Hughes Clarke in August 1998) is an interactive command-line solver that models and corrects **Vertical Reference Unit (VRU / MRU / IMU) yaw mounting misalignment** (`YM`).

When a motion sensor is mounted on a survey vessel with a horizontal yaw rotation offset $\psi_m$ (`YM`) relative to the ship's true fore-aft centerline (or transducer array axis), the sensor's roll and pitch axes no longer align with the vessel's roll and pitch axes. Consequently, true vessel pitch leaks into observed roll, and true vessel roll leaks into observed pitch (**roll-pitch cross-coupling**). `twistVRU` solves both the forward problem (`RtoO`: given true vessel roll & pitch, what will a twisted VRU observe?) and the inverse correction problem (`OtoR`: given observed roll & pitch from a twisted VRU, what are the true vessel roll & pitch?).

---

## Usage & Interactive Modes

```bash
twistVRU
```

`twistVRU` takes no command-line flags and runs an interactive menu loop on `stdin`:
```text
 which direction:
    OBSERVED->REAL (1):
    REAL->OBSERVED (2):
    QUIT           (0)
```
* **Option `1` (`OBSERVED->REAL`, calls `OtoR`):** Prompts for `YAW_misalign` (`YM`), `OBSERVED roll` (`OR`), and `OBSERVED pitch` (`OP`) in degrees, and prints `TRUE roll and PITCH` (`TR`, `TP`).
* **Option `2` (`REAL->OBSERVED`, calls `RtoO`):** Prompts for `YAW_misalign` (`YM`), `TRUE roll` (`TR`), and `TRUE pitch` (`TP`) in degrees, and prints `OBSERVED roll and PITCH` (`OR`, `OP`).
* **Option `0` (`QUIT`):** Terminates the program (`exit(0)`).

---

## Mathematical Formulation (`RtoO` & `OtoR`)

Let:
* $\psi_m = \text{YM} \cdot \frac{\pi}{180}$ be the VRU yaw misalignment angle, with $c_m = \cos\psi_m$ and $s_m = \sin\psi_m$.
* $(r_t, p_t) = (\text{TR}, \text{TP})$ be the **true** vessel roll and pitch angles, with $s_{rt} = \sin r_t$ and $s_{pt} = \sin p_t$.
* $(r_o, p_o) = (\text{OR}, \text{OP})$ be the **observed** VRU roll and pitch angles, with $s_{ro} = \sin r_o$ and $s_{po} = \sin p_o$.

### 1. Forward Transformation: Real $\to$ Observed (`RtoO`, Option `2`)
Projecting the gravity/tilt vector components onto the yaw-rotated VRU axes yields the coupled forward equations (lines 138–144):

$$\sin r_o = \cos\psi_m \sin r_t + \sin\psi_m \sin p_t$$

$$\sin p_o = \cos\psi_m \sin p_t - \sin\psi_m \sin r_t$$

$$r_o = \frac{180}{\pi} \arcsin(\sin r_o), \qquad p_o = \frac{180}{\pi} \arcsin(\sin p_o)$$

*(Note: As JHC notes in the source comment on line 137—`/* the standard forward (misquoted in MB notes!) */`—`twistVRU.c` encodes the exact sign convention verified for OMG attitude processing).*

### 2. Inverse Transformation: Observed $\to$ Real (`OtoR`, Option `1`)
Inverting the $2 \times 2$ orthogonal rotation matrix in $(\sin r, \sin p)$ space solves the simultaneous equations for true pitch and true roll (lines 107–114):

$$\sin p_t = \frac{\sin p_o \cos\psi_m + \sin r_o \sin\psi_m}{\cos^2\psi_m + \sin^2\psi_m} = \sin p_o \cos\psi_m + \sin r_o \sin\psi_m$$

$$\sin r_t = \frac{\sin r_o - \sin\psi_m \sin p_t}{\cos\psi_m}$$

$$r_t = \frac{180}{\pi} \arcsin(\sin r_t), \qquad p_t = \frac{180}{\pi} \arcsin(\sin p_t)$$

---

## Example Interactive Session

```text
$ twistVRU
 which direction:
    OBSERVED->REAL (1):
    REAL->OBSERVED (2):
    QUIT           (0)
2
 input YAW_misalign  and TRUE roll and pitch (e.g. 45.0 12.2 14.6)
45.0 10.0 0.0
 OBSERVED roll and PITCH:
 7.053022 -7.053022

 which direction:
    OBSERVED->REAL (1):
    REAL->OBSERVED (2):
    QUIT           (0)
1
 input YAW_misalign and OBSERVED roll and pitch (e.g. 45.0 12.2 14.6)
45.0 7.053022 -7.053022
 TRUE roll and PITCH:
 10.000000 0.000000
```
For interactive motion delay, scale factor, and dual-head yaw misalignment analysis on `.merged` survey lines, see [`DelayEditor`](../DE/DelayEditor.md).
