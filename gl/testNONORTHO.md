---
layout: default
title: testNONORTHO
parent: gl Tools
tool_name: testNONORTHO
source_path: code/gl/testNONORTHO.c
category: 3D OpenGL Swath & Sonar Geometry Simulation
related_tools: ["synSwath", "SYN_NONORTHO", "j_non_ortho_cones", "DCM_rthand"]
---

# testNONORTHO

## Overview
`testNONORTHO` is an interactive command-line diagnostic utility written by John E. Hughes Clarke (November 2000) to test and verify 3D non-orthogonal transmit/receive cone intersection geometry (`calc_nonorthogonal_cones_010` from [`j_non_ortho_cones`](../subr/j_non_ortho_cones.md)).

In multibeam echosounders where the transmit line array and receive line array are mounted on separate hull frames, tilted separately, or evaluated at distinct transmit and receive instants (dynamic motion between transmit and receive), the transmit and receive acoustic cones are no longer mutually orthogonal. `testNONORTHO` allows interactive entry of arbitrary mounting angles, instantaneous platform orientations, and steering angles to inspect the resulting 3D unit beam vector $(X, Y, Z)$ and geographic azimuth/depression angle in the local-level reference frame.

---

## Usage

```bash
testNONORTHO [-v]
```

### Interactive Prompts
When executed, `testNONORTHO` enters a loop prompting for six sets of angles (in degrees) from `stdin`:
1. **Transmit array mount angles:** `Tx_mount.roll`, `Tx_mount.pitch`, `Tx_mount.yaw`
2. **Receive array mount angles:** `Rc_mount.roll`, `Rc_mount.pitch`, `Rc_mount.yaw`
3. **Instantaneous vessel orientation at Transmit:** `Tx_orient.roll`, `Tx_orient.pitch`, `Tx_orient.yaw`
4. **Instantaneous vessel orientation at Receive:** `Rc_orient.roll`, `Rc_orient.pitch`, `Rc_orient.yaw`
5. **Conical steering angles:** `cone_pitch` (transmit fore-aft steering angle) and `cone_roll` (receive port-starboard steering angle)

---

## Computation & Output

1. Sets `ortho_calc_type = MB_NONORTHO` and sets `LL_beam_vect.x = -999.0` to enable verbose internal step-by-step debug output inside [`j_non_ortho_cones`](../subr/j_non_ortho_cones.md).
2. Calls:
   ```c
   calc_nonorthogonal_cones_010(Tx_mount, Rc_mount, Tx_orient, Rc_orient,
                                &LL_beam_vect, (float)cone_pitch, (float)cone_roll);
   ```
3. Converts the returned local-level Cartesian beam unit vector `(LL_beam_vect.x, LL_beam_vect.y, LL_beam_vect.z)` into spherical coordinates:
   * $\text{Azimuth} = \text{atan2}(Y, X) \times \frac{180}{\pi}$
   * $\text{Radial} = \sqrt{X^2 + Y^2}$
   * $\text{Depression} = \arctan\left(\frac{Z}{\text{Radial}}\right) \times \frac{180}{\pi}$
4. Prints the Cartesian components and derived azimuth and depression angles:
   ```text
   X <x> Y <y> Z <z> -- azi <deg> dep <deg>
   ```

---

## Architectural Role
`testNONORTHO` serves as the standalone mathematical verification harness for [`j_non_ortho_cones.c`](../subr/j_non_ortho_cones.md) and [`SYN_NONORTHO.c`](SYN_NONORTHO.md), which underpin both 3D cone intersection visualization in [`synSwath`](synSwath.md) and operational multibeam re-pointing in [`repoint`](../omg/repoint.md).
