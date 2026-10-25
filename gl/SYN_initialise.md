---
layout: default
title: SYN_initialise
parent: gl Tools
module_name: SYN_initialise
source_path: code/gl/SYN_initialise.c
category: 3D OpenGL Swath & Sonar Geometry Simulation
related_tools: ["synSwath", "SYN_launcher", "SYN_event_loop", "SYN_oGL_draw", "SYN_global"]
---

# SYN_initialise

## Overview
`SYN_initialise.c` implements `initialise_SYN_variables()`, the global state initialization routine for the [`synSwath`](synSwath.md) 3D OpenGL acoustic geometry, beam-steering, and bottom-detection simulator (originally created by John E. Hughes Clarke in 1995 and rationalized in 2001).

Before `synSwath` parses command-line options or opens its X11/GLX viewport, `initialise_SYN_variables()` configures default values across all simulation subsystems declared in [`SYN_global.h`](SYN_global.md).

---

## Key Subsystems Initialized

### 1. Non-Orthogonal Cone & Attitude / MRU State
* **Non-orthogonal cone display:** `show_nonortho_cones = 1`, `show_nonortho_plane = 1`.
* **Motion Reference Unit (MRU) state:** Initializes `MRU_at_RP = 1`, `MRU_orientation = RPY_MRU` (Tait-Bryan roll-pitch-yaw), `MRU_Zposition = NED_MRU`, `MRU_XYposition = NED_MRU`, `MRU_grav = 9.81` $\text{m/s}^2$, and sample interval `MRU_dtime = 0.002` s (500 Hz). Enables display of magnetic field, linear accelerations, residual accelerations, and angular rate vectors.

### 2. Swath Animation & Beam-Steering Parameters
* **Beamwidths & Steering:** Default transmit/receive beamwidths `tr_beamwidth = 3.0` deg, `rc_beamwidth = 3.0` deg, zero steering (`tr_steer = rc_steer = gy_steer = 0.0`), beam spacing `mock_beam_spacing = 3.0` deg, vessel speed `speed_knots = 12.0` kn.
* **Swath Geometry:** Angular sector `ang_sect = 120.0` deg, nominal depth `nominal_depth = 20.0` m, two-way travel time multiplier `twtt_multiplier = 3.0`, and computed ping interval:
  $$\Delta t_{\text{ping}} = 3.0 \times \frac{Z_{\text{nom}}}{750.0 \cos(\theta_{\text{sect}} / 2)}$$
* **Stabilization & Wobble Flags:** Disables roll, pitch, yaw, and mechanical pitch stabilization by default (`0`), sets attitude scaling (`roll_scale = pitch_scale = yaw_scale = 3.0`, `heave_scale = 1.0`), enables multi-sector transmit visualization (`show_Tx_multisec = 1`), and configures EK80 split-beam latency parameters (`latent_Rx = 0`, `TxRx_latency = 1.0`).

### 3. OpenGL Material Properties (`matprops[0..5]`)
Configures six named OpenGL material property slots (`diffuse`, `ambient`, `specular`, `shininess`, `transparency`):
1. `mat_name[0]`: `"beam_pattern"` (opaque, `diffuse=1.0`, `specular=1.0`, `shininess=10.0`)
2. `mat_name[1]`: `"object (e.g.: ship)"` (opaque, `diffuse=1.0`, `specular=1.0`)
3. `mat_name[2]`: `"steered cones"` (semi-transparent `transparency=0.4`, `diffuse=0.6`, `shininess=100.0`)
4. `mat_name[3]`: `"axes"`
5. `mat_name[4]`: `"sea surface"` (semi-transparent `transparency=0.4`)
6. `mat_name[5]`: `"distorted grid"` (opaque)

### 4. GLX Window & Camera Defaults
* Sets window title `"OMG/UNB  Syn-Swath"`, viewport dimensions `900 x 900` pixels (`glwin_aspect = 1.0`), double-buffered RGBA visual with 16-bit depth buffer (`GLX_DOUBLEBUFFER`, `GLX_RGBA`, `GLX_DEPTH_SIZE = 16`), and initial camera spherical coordinates (`eye_range = 10.0`, `eye_azi = 0.0`, `eye_elev = 0.0`).

### 5. Seafloor Plate & Bottom Detection (`SYN_doBD`) Parameters
* **Plate Geometry:** Vertical exaggeration `vert_exag = 4.0`, `plate_heading = 90.0` deg, `plate_scale = 3.5`, `use_plate_normals = 1`, `use_plate_phase = 1`.
* **Backscatter & Bottom Detection Model:** Configures default angular response parameters (`BSo = -3.0` dB, `BSn_BSo = 10.0` dB, `Lamb_Power = 2.0`, facet slope transition `Angle_Change = 25.0` deg, illumination limits `-50.0` to `-10.0` dB, `noise_level = 0.001` / `-40` dB).

### 6. Phased Array Transducer Defaults
* Initializes a 95 kHz (`Frequency = 95000.0` Hz, EM1000/EM1002 class) Mills Cross array (`Along_Array_Length = 0.1454` m, `Across_Array_Length = 0.169` m, 42 elements per array, `COS_SQUARED` shading on transmit port/stbd and receive fore/aft, `UNSHADED` elsewhere), sound velocity `1500.0` m/s (assumed `1490.0` m/s), and two-element interferometric sidescan stave defaults (`spacing = 0.17` m, `radius = 0.057` m).

---

## Architectural Role
`initialise_SYN_variables()` is called at startup by `main()` in [`synSwath.c`](synSwath.md) prior to command-line argument parsing and script execution ([`SYN_scripting.c`](SYN_scripting.md)), ensuring deterministic baseline state for interactive X11/OpenGL rendering and batch animation frame dumps.
