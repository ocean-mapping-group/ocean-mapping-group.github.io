---
layout: default
title: gl Tools
has_children: true
nav_order: 9
---

# 3D OpenGL Swath & Sonar Geometry Simulation (`gl`)

The `gl` directory contains **`synSwath`** and its modular C subsystems—an interactive 3D OpenGL/GLX acoustic geometry, phased-array beamforming, attitude coordinate frame, and seafloor backscatter/bottom-detection simulation environment developed by John E. Hughes Clarke.

---

## Main Executable & Test Harness

* [`synSwath`](synSwath.md) — Main interactive 3D OpenGL multibeam, sidescan, split-beam, and inertial reference frame simulator.
* [`testNONORTHO`](testNONORTHO.md) — Standalone CLI verification tool for non-orthogonal transmit/receive cone intersections (`calc_nonorthogonal_cones_010`).

---

## Core Architecture & Rendering Modules

* [`SYN_global`](SYN_global.md) — Central header declaring global simulation state, array geometry, OpenGL materials, and viewport flags.
* [`SYN_initialise`](SYN_initialise.md) — Initializes all default transducer, attitude, material, camera, and bottom-detection state variables.
* [`SYN_launcher`](SYN_launcher.md) — X11/Motif control panel launcher for interactive parameter adjustment.
* [`SYN_event_loop`](SYN_event_loop.md) — X11/GLX mouse, keyboard, and window event dispatcher for interactive 3D manipulation.
* [`SYN_oGL_draw`](SYN_oGL_draw.md) — High-level OpenGL scene assembly and coordinate-frame rendering pipeline.
* [`SYN_jGL_draw`](SYN_jGL_draw.md) / [`SYN_jGL_draw.h`](SYN_jGL_draw.h.md) — 3D geometric primitives (vessels, transducers, axes, spheres, vectors, and cones).
* [`SYN_animate`](SYN_animate.md) — Multi-ping swath propagation, vessel motion (roll/pitch/yaw wobble), and frame-capture animation engine.
* [`SYN_scripting`](SYN_scripting.md) — Batch script parser and keyframe interpolation engine for automated lecture animations.

---

## Specialized Acoustic & Kinematic Modules

* [`SYN_NONORTHO`](SYN_NONORTHO.md) — 3D visualization of non-orthogonal transmit and receive cones and their hyperboloid/vector intersections.
* [`SYN_ROT`](SYN_ROT.md) — Euler angle and Tait-Bryan rotation sequence (`DCM_rthand`) demonstrations.
* [`SYN_RefFrame`](SYN_RefFrame.md) — Local-level, vessel, and sensor reference frame transformations.
* [`SYN_MRU`](SYN_MRU.md) — Motion Reference Unit (accelerometers, gyroscopes, magnetometers, and lever-arm centripetal accelerations) visualization.
* [`SYN_doBD`](SYN_doBD.md) — Synthetic amplitude and split-beam phase bottom detection across 3D seafloor facets.
* [`SYN_plate_select`](SYN_plate_select.md) — Seafloor target plate loading, normal computation, and facet illumination.
* [`SYN_Ripple`](SYN_Ripple.md) & [`SYN_internal_wave`](SYN_internal_wave.md) — Synthetic seabed ripple and oceanographic internal wave surfaces.
* [`SYN_EK`](SYN_EK.md) — Simrad EK60/EK80 split-beam echosounder phase and target-location simulation.
* [`SYN_M3`](SYN_M3.md) — Kongsberg Mesotech M3 imaging sonar geometry.
* [`SYN_SAS`](SYN_SAS.md) — Synthetic Aperture Sonar (SAS) along-track synthetic array geometry.
* [`SYN_ADCP`](SYN_ADCP.md) & [`SYN_currents`](SYN_currents.md) — Janus 4-beam ADCP geometry and 3D current vector fields.
* [`SYN_LBL`](SYN_LBL.md), [`SYN_LLZ`](SYN_LLZ.md), [`SYN_navSect`](SYN_navSect.md), [`SYN_TCtrajectory`](SYN_TCtrajectory.md) — Long-Baseline acoustic positioning, local-level navigation, and tide-corrected trajectory modules.
