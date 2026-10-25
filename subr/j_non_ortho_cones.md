---
layout: default
title: j_non_ortho_cones
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_non_ortho_cones.c
category: Multibeam Geometry & 3D Attitude Kinematics
related_tools:
- mergeAtt
- newMergeAtt
- swathEd
- SYN_ship
module_name: j_non_ortho_cones
header_path: code/subr/j_non_ortho_cones.h
---

# `j_non_ortho_cones` — Non-Orthogonal Mills Cross Multibeam Cone Intersection Library

## Overview & Purpose in the OMG Architecture

`j_non_ortho_cones` (`code/subr/j_non_ortho_cones.c`, `code/subr/j_non_ortho_cones.h`), developed by John E. Hughes Clarke and Jonathan Beaudoin (November 2000, updated November 2010), computes the exact 3D geographic pointing vector of a multibeam echosounder beam formed by the intersection of a **transmit (TX) steering cone** and a **receive (RX) steering cone** when the two linear transducer arrays are **non-orthogonal**.

In a Mills Cross multibeam sonar, the transmit array ( nominally aligned fore-aft along the $X$ axis) steers a fan in pitch ($\theta_{TX}$), while the receive array (nominally aligned athwartships along the $Y$ axis) forms beams steered across-track ($\theta_{RX}$). Even if the arrays are mounted orthogonally on the hull, vessel yaw rotation between the time of transmit ($t_{TX}$) and the time of reception ($t_{RX}$), as well as independent mounting misalignments (`TX_mounting_angles`, `RC_mounting_angles`), causes the TX and RX array axes to depart from $90^\circ$ in geographic space. `j_non_ortho_cones` resolves the exact intersection of these two non-orthogonal hyperbolic cones and rotates the resulting beam vector into the local-level geographic frame.

---

## Key Data Structures, Constants & Coordinate Conventions

### Coordinate & Sign Conventions (`code/subr/j_non_ortho_cones.c`)
- **Axes**: $+X$ is forward, $+Y$ is starboard (right), $+Z$ is downward (right-handed local-level frame from `DCM_rthand.h`).
- **Euler Angles (`fattitude`)**: $+\text{roll}$ is starboard down, $+\text{pitch}$ is bow up, $+\text{yaw}$ is turn to starboard.
- **Beam Steering Angles**: $+Tr\_steer$ (`txSteer`) is forward; $+Rc\_steer$ (`rxSteer`) is to port (left).

### Constants & Globals (`code/subr/j_non_ortho_cones.h`)
- `MB_ORTHO` (`0`), `MB_NONORTHO` (`1`): Selects whether `ortho_calc_type` assumes orthogonal arrays or applies the non-orthogonal yaw-change correction:
  $$y_{\text{off}} = \frac{\sin(\theta_{RX})}{\cos(\Delta\psi)} + \sin(\theta_{TX})\tan(\Delta\psi)$$
- `JOHN` (`0`), `JONB` (`1`): Formula selector (`calc_formula`) between John Hughes Clarke's sequential Euler rotation formulation (`calc_nonorthogonal_cones`) and Jonathan Beaudoin's orthonormal vector-basis cross-product formulation (`calc_nonorthogonal_cones2`).
- **Global Diagnostic State**: `fvect TX_array, RC_array` and `double RC_roll, TX_pitch, TX_azi, RC_azi` store intermediate transformed array axis vectors and angles. Setting `resulting_beam_vector->x = -999.0` on entry activates verbose step-by-step console debugging (`no_ortho_debug = 1`).

---

## Public Functions & Signatures

- `int calc_nonorthogonal_cones_010(fattitude TX_mounting_angles, fattitude RC_mounting_angles, fattitude TX_orientation, fattitude RC_orientation, fvect *resulting_beam_vector, float Tr_steer, float Rc_steer)`
  *(Added November 2010 by JHC)* Computes the unit 3D beam pointing vector `resulting_beam_vector` using sensitized receiver mounting conventions where the unrotated RX array axis is initialized along the athwartships $+Y$ unit vector `(0, 1, 0)` (eliminating the need to specify an artificial $90^\circ$ mounting yaw for the receiver) and the TX array axis starts at `(1, 0, 0)`:
  1. Unrotates the TX `(1, 0, 0)` vector by `TX_mounting_angles` and `TX_orientation` (`jDCM_unrotatef`) to obtain `TX_array` in geographic coordinates.
  2. Unrotates the RX `(0, 1, 0)` vector by `RC_mounting_angles` and `RC_orientation` to obtain `RC_array`.
  3. Determines the geographic pitch (`TX_pitch`) and azimuth (`TX_azi`) of the TX array, rotates `RC_array` into the TX-aligned frame, and extracts the relative receiver roll (`RC_roll`) and non-orthogonality angle (`yaw_change = RC_azi - 90.0`).
  4. Solves the cone intersection `(xoff, yoff, zoff)` on the unit sphere (`sqrt(x^2 + y^2 + z^2) = 1.0`) and unrotates by `(RC_roll, TX_pitch, TX_azi)` into `resulting_beam_vector`.

- `int calc_nonorthogonal_cones(fattitude TX_mounting_angles, fattitude RC_mounting_angles, fattitude TX_orientation, fattitude RC_orientation, fvect *resulting_beam_vector, float Tr_steer, float Rc_steer)`
  Original November 2000 formulation where both TX and RX initial vectors start at `(1, 0, 0)` (requiring `RC_mounting_angles.yaw` to include a nominal $90^\circ$ offset) and the output `resulting_beam_vector` is normalized so that `z = 1.0` (`xoff /= zoff`, `yoff /= zoff`).

- `int calc_nonorthogonal_cones2(fattitude txAlign, fattitude rxAlign, fattitude txAtti, fattitude rxAtti, fvect *beamVectGeo, float txSteer, float rxSteer)`
  Vector-algebraic formulation by Jonathan Beaudoin:
  1. Transforms ideal TX and RX unit vectors into geographic space (`txGeo`, `rxGeo`) via `jDCM_unrotatef()`.
  2. Computes the exact non-orthogonality angle directly from the 3D dot product:
     $$\Delta\psi = \arccos(\mathbf{rx}_{\text{Geo}} \cdot \mathbf{tx}_{\text{Geo}}) \cdot \frac{180}{\pi} - 90^\circ$$
  3. Computes the array-plane relative beam vector `beamVectRel` (normalized to $z = 1.0$).
  4. Constructs an orthonormal basis $(\mathbf{x}', \mathbf{y}', \mathbf{z}')$ using vector cross products ($\mathbf{x}' = \mathbf{tx}_{\text{Geo}}$, $\mathbf{z}' = \mathbf{tx}_{\text{Geo}} \times \mathbf{rx}_{\text{Geo}}$, $\mathbf{y}' = \mathbf{z}' \times \mathbf{x}'$) and projects `beamVectRel` into geographic space.

---

## How It Fits Into the OMG Architecture

`j_non_ortho_cones` is a core geometric building block used by OMG's multibeam attitude integration and raytracing tools (`mergeAtt`, `newMergeAtt`, `swathEd`, `get_ADH_SRA`) and synthetic multibeam simulators (`SYN_ship`). It depends on `DCM_rthand.h` (`fattitude`, `fvect`, `attitude`, `jDCM_rotatef`, `jDCM_unrotatef`).
