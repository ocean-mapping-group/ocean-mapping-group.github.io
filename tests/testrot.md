---
layout: default
title: testrot
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 26
tool_name: testrot
source_path: code/tests/testrot.c
category: Attitude Error & Lever-Arm Coordinate Rotations (tests)
input_formats:
  - Interactive stdin prompts: 3D vector (x0, y0, z0), rotation direction (1, 2, or 0), and attitude Euler angles (roll, pitch, heading)
output_formats:
  - Rotated 3D vector coordinates (x1, y1, z1) on stdout
related_tools:
  - twistVRU
  - DelayEditor
  - RTlite
  - newMergeAtt
---

# testrot

## Overview
`testrot` (`code/tests/testrot.c`, authored by John Hughes Clarke in July 1994) is an interactive command-line verification utility for testing 3D rigid-body Euler angle coordinate transformations implemented in `DCM_rthand.h` (`DCM_rotate` and `DCM_unrotate` in `liblocal.a`).

In multibeam sonar ray-tracing and lever-arm motion compensation (such as [`RTlite`](../RTLite/RTlite.md), [`DelayEditor`](../DE/DelayEditor.md), and [`swathed`](../SE/swathed.md)), 3D vectors—such as GPS-to-transducer lever-arm offsets $(x_0, y_0, z_0)$ or unit beam pointing vectors—must be rotated accurately between the vessel/sonar reference frame (`SONAR`) and the local level geographic reference frame (`GEO`) using instantaneous roll ($r$), pitch ($p$), and heading/yaw ($h$). `testrot` allows the user to interactively enter any 3D vector `(x0, y0, z0)` and attitude triplet `(roll, pitch, heading)` and transform it either forward (`GEO -> SONAR` via `DCM_rotate`) or inverse (`SONAR -> GEO` via `DCM_unrotate`).

---

## Syntax & CLI Options

```bash
testrot [-v] [-roll <deg>]
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-v` | Increment verbose flag (`verbose_flag++`). | `0` |
| `-roll <deg>` | Optional initial roll value parsed on CLI (overridden by interactive `scanf` prompt). | Interactive |

---

## Interactive Prompts & Direction Cosine Matrix (DCM) Math

### 1. Interactive Loop (`yetagain:`)
At each iteration, `testrot` prompts on `stdin` for:
1. **Starting 3D Vector:** `input x, y z of starting vector` (`scanf("%lf %lf %lf", &x0, &y0, &z0)`), stored in `location vectin`.
2. **Transformation Direction (`foreback`):**
   * `1`: Rotate **`from GEO to SONAR`** (`DCM_rotate(vectin, rpy, &vectout)`).
   * `2`: Rotate **`from SONAR to GEO`** (`DCM_unrotate(vectin, rpy, &vectout)`).
   * `0`: **`exit`** (`exit(0)`).
3. **Rigid Frame Attitude:** `input roll, pitch heading of rigid frame` (in degrees, stored in `attitude rpy` = `{roll, pitch, yaw}`).

### 2. Right-Handed Direction Cosine Matrix (`DCM_rthand.h`)
In the OMG right-handed vessel coordinate convention ($+X$ forward/North, $+Y$ starboard/East, $+Z$ down), with $\phi = \text{roll}$, $\theta = \text{pitch}$, and $\psi = \text{heading}$ (in radians), the forward rotation matrix $\mathbf{R} = \mathbf{R}_z(\psi)\,\mathbf{R}_y(\theta)\,\mathbf{R}_x(\phi)$ documented in `testrot.c` (lines 196–217) is:

$$\begin{bmatrix} x_1 \\ y_1 \\ z_1 \end{bmatrix} = \begin{bmatrix} \cos\theta\cos\psi & \cos\theta\sin\psi & -\sin\theta \\ \sin\phi\sin\theta\cos\psi - \cos\phi\sin\psi & \sin\phi\sin\theta\sin\psi + \cos\phi\cos\psi & \sin\phi\cos\theta \\ \cos\phi\sin\theta\cos\psi + \sin\phi\sin\psi & \cos\phi\sin\theta\sin\psi - \sin\phi\cos\psi & \cos\phi\cos\theta \end{bmatrix} \begin{bmatrix} x_0 \\ y_0 \\ z_0 \end{bmatrix}$$

Because $\mathbf{R} \in \text{SO}(3)$ is orthogonal ($\mathbf{R}^{-1} = \mathbf{R}^\top$, $\det\mathbf{R} = +1$), the Euclidean norm of any lever-arm vector is strictly invariant under rotation:

$$\Vert\mathbf{v}_1\Vert = \sqrt{x_1^2 + y_1^2 + z_1^2} = \sqrt{x_0^2 + y_0^2 + z_0^2} = \Vert\mathbf{v}_0\Vert$$

*(A secondary code block at label `again:` in `testrot.c` lines 171–250 explicitly checks this norm preservation by computing `perc_diff = (1.0 - final_length / orig_length) * 100.0` and applying `DCM_rotate` followed immediately by `DCM_unrotate` to confirm round-trip identity).*

---

## Example Interactive Session

```text
$ testrot
 input x, y z of starting vector
0.0 0.0 10.0
 entered 0.000000 0.000000 10.000000


 do you want to rotate:
    from GEO to SONAR (1)
    from SONAR to GEO (2)
     exit             (0)
2
 input roll, pitch heading of rigid frame
10.0 0.0 90.0
 10.000000 0.000000 90.000000
 rot back -1.736482 0.000000 9.848078
```
To analyze coupled roll/pitch cross-talk caused by VRU yaw mounting misalignment, see [`twistVRU`](twistVRU.md).
