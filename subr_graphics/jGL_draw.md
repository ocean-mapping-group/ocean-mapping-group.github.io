---
layout: default
title: jGL_draw
parent: Graphics & X11/OpenGL Libraries (subr_graphics)
module_name: jGL_draw
source_path: code/subr_graphics/jGL_draw.c
header_path: code/subr_graphics/jGL_draw.h
category: 3D OpenGL Visualization
related_tools: ["DCM_rthand", "bP_stuff", "swathed", "glSeis", "synSwath"]
---

# jGL_draw

## Overview
`jGL_draw` (`jGL_draw.c` / `jGL_draw.h`, >4,600 lines), written by John Hughes Clarke (originating in `synSwath` in 1995, rationalized as `SYN_oGL_draw` in 2001–2006, and updated through January 2026), is the **3D OpenGL (`GL` / `GLU` / `GLX`) scene-graph, acoustic array, beam-steering cone, and vessel/platform rendering library** for the Ocean Mapping Group software suite.

It powers interactive 3D multibeam and water-column visualization tools including `synSwath` (synthetic swath and transducer array beam-forming simulator), `swathed` (`SE_3D.c` 3D swath editor), and `glSeis` (3D scanning/multibeam water-column viewer). It provides complete 3D models of research vessels, AUVs, ROVs, and over a dozen multibeam transducer geometries alongside real-time animations of element phasing, time-delay beamforming, near-field focusing arcs, non-orthogonal steering cones, and dynamic sea surfaces.

---

## Key Constants & Global State (`jGL_draw.h`)

### Camera & Look-At Modes
- **Viewpoint Presets** (`locate_eye`): `EYE_ABOVE` (`0`), `EYE_AHEAD` (`1`), `EYE_BESIDE` (`2`).
- **Look-At Targets** (`lookat`): `CENTRE` (`0`), `PLATE` (`1`), `SONAR` (`2`), `ANTENNA` (`3`), `MIDDLE` (`4`), `BOTTOM` (`5`), `CUSTOM` (`6`).
- **Spherical Camera State**: `eye_range`, `eye_azi`, `eye_elev`, `eye_x`, `eye_y`, `eye_z`, `eye_horiz`, `lookat_X`, `lookat_Y`, `lookat_Z`, `glwin_width`, `glwin_height`, `glwin_aspect`.

### Vessel Attitude, Stabilization & Swath History
- **6-DOF Platform Motion**: `object_heading`, `object_pitch`, `object_roll`, `object_heave`, `object_surge`, `object_sway`, plus synthetic motion perturbations (`add_wobble`, `wobble_roll`, `wobble_pitch`, `wobble_yaw`).
- **Stabilization Toggles**: `roll_stabilised`, `pitch_stabilised`, `yaw_stabilised`, `mech_pitch_stabilised`.
- **Trailing Swath History**: `fvect swath_history[HIST_LEN][180]` (`HIST_LEN = 288`) and multi-sector history `fvect bysect_swath_history[HIST_LEN][180][MAXSECT]` (`MAXSECT = 10`, added Jan 2026) storing historical seafloor beam footprints for scrolling 3D waterfall rendering.

### Material Properties (`jGL_matprop`)
`matprops[0..5]` controls OpenGL lighting (`diffuse`, `ambient`, `specular`, `shininess`) and alpha blending (`transparency`) for 6 scene categories:
`0: "beam_pattern"`, `1: "object (e.g.: ship)"`, `2: "steered cones"`, `3: "axes"`, `4: "sea surface"`, and `5: "distorted grid"`.

---

## Public Functions

### 1. Camera, Lighting & Primitive Setup
| Function | Signature | Description |
|---|---|---|
| `set_up_lighting` / `set_up_sphere` / `set_up_cylinder` | `void set_up_lighting(void)` | Initializes OpenGL light sources (`GL_LIGHT0`..), `GLUquadricObj` handles (`qobj_cyl`, `qobj_sph`, `qobj_disk`), and material tables. |
| `calc_eye_pos` / `locate_eye` | `void calc_eye_pos(void)` / `void locate_eye(int where)` | Converts spherical camera coordinates `(eye_range, eye_azi, eye_elev)` into Cartesian `(eye_x, eye_y, eye_z)` or snaps the camera to overhead/bow/beam views. |
| `move_the_view` | `void move_the_view(float x, float y, float z, float ex, float ey, float ez)` | Applies `gluPerspective(20.0, glwin_aspect, ...)` and `gluLookAt()` with automatic Z-up/Z-down vector flipping across $\pm 90^\circ$ elevation. |
| `setup_material_properties` / `disable_transparency` | `void setup_material_properties(int object, float r, float g, float b)` | Configures `glMaterialfv` and `GL_BLEND` alpha transparency for scene layer `object` (`0..5`). |
| `do_rotations_in_sequence` | `void do_rotations_in_sequence(void)` | Applies yaw/heading, pitch, and roll `glRotatef` transformations in proper right-handed Euler sequence. |
| `draw_axes` / `draw_sphere` / `draw_shoe_box` / `draw_cylinder_filled` / `draw_tapered_cylinder_filled` / `draw_arc_filled` / `draw_rect_filled` | `void draw_axes(void)` | Renders 3D coordinate axes, alpha-blended spheres, rectangular prisms (`draw_shoe_box`), cylinders, cones, and filled arcs. |
| `do_panel` / `do_triangle` / `get_normal` | `void do_panel(float *v1, float *v2, float *v3, float *v4)` | Computes surface normal vectors (`get_normal`) and emits lit OpenGL quadrilateral/triangular facets. |

### 2. Acoustic Array, Beamforming & Cone Geometry
| Function | Signature | Description |
|---|---|---|
| `draw_line_array` / `draw_transverse_array` | `void draw_line_array(int transp)` | Renders a linear transducer array along with optional interactive visualizations of element spacing, shading weights (`SHOW_SHADING` via [`bP_stuff`](../subr/bP_stuff.md)), incoming phase wavefronts and FFT organ-pipe spectra (`SHOW_TIME_DELAY`), virtual steered array projection (`SHOW_ARRAY_WAVELENGTHS`), and near-field focusing arcs (`SHOW_FOCAL_LENGTH`). |
| `draw_IandQ` | `void draw_IandQ(int phase36th)` | Renders a 3D helix and phasor diagram of complex In-phase ($I$) and Quadrature ($Q$) harmonic signals over 6 wavelengths. |
| `draw_cone` | `void draw_cone(float steering_angle, int axis, float start_angle, float end_angle, int dobeams)` | Renders a 3D hyperbolic/conical transmit or receive beam-steering surface (`axis = X` or `Y`) at `steering_angle` and computes its seafloor intersection curve. |
| `do_ray_fan` | `void do_ray_fan(int nobeams, float *angles, float tilt, float radius, float max_elev, float steer)` | Renders a fan of `nobeams` individual acoustic rays from a tilted/steered array. |
| `draw_T_array` / `draw_X_array` / `draw_30deg_Tpair` / `draw_disc` / `draw_two_row` / `draw_three_row` | `void draw_T_array(float tilt, int style, float max_elev, float steer)` | Renders Mills Cross (`T` and `X`), dual-head $30^\circ$ tilted pair, circular piston (`draw_disc`), and multi-row interferometric transducer arrays. |

### 3. Sonar Heads, Platforms & Oceanographic Environment
| Function | Signature | Description |
|---|---|---|
| `draw_appropriate_object` | `void draw_appropriate_object(void)` | Dispatches 3D rendering for the currently selected vessel/platform (`draw_ship`, `draw_boat`, `draw_ROV`, `draw_hugin`, `draw_buoy`) and sonar head (`draw_EM3000`, `draw_EM3000D`, `draw_EM2040D`, `draw_EM1000`, `draw_8101`, `draw_8111`, `draw_8125`, `draw_Seabat`, `draw_Twin_Seabat`, `draw_SM2000`, `draw_M3`, `draw_SMII`, `draw_Bathyscan`, `draw_AcousticBeacon`, `draw_SubbottomArray`). |
| `init_sea_surface` / `calc_sea_surface` / `draw_sea_surface` | `void draw_sea_surface(void)` | Synthesizes and renders a 100x100 3D ocean wave/swell/internal-wave surface mesh (`sea_surface[100][100]`). |
| `init_ek_profile` / `calc_ek_profile` / `draw_ek_profile` | `void draw_ek_profile(int flag)` | Computes and renders a trailing vertical single-beam/split-beam echogram curtain behind the moving vessel. |
