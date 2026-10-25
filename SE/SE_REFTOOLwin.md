---
layout: default
title: SE_REFTOOLwin
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 14
tool_name: SE_REFTOOLwin
source_path: code/SE/SE_REFTOOLwin.c
category: Interactive QC & Editing (SwathEd)
input_formats:
- .merged
- .ref_coeffs
output_formats:
- .ref_coeffs
related_tools:
- swathed
- RefractEd
- applyRef
- SE_W_TimeSeries
---

# `SE_REFTOOLwin` — Empirical Sound Speed Refraction & Induced Heave Modeling Tool

`SE_REFTOOLwin` (`code/SE/SE_REFTOOLwin.c`, `code/SE/SE_REFTOOLwin.h`) implements the `"Empirical Refraction Modification Tool (And Induced Heave Error Model)"` (`sub_window[REF_OFFSET .. REF_OFFSET + 12]`, where `REF_OFFSET = 61`) in [`swathed`](swathed.html). Authored by John E. Hughes Clarke (July 1999), it enables hydrographers to interactively diagnose and correct outer-beam "smiles" or "frowns" caused by inaccurate sound velocity profiles (SVP) or surface sound speed errors, as well as along-track "ripples" caused by incorrect motion-sensor-to-transducer lever arms (induced heave errors).

---

## Window Architecture & Controls (`sub_window[61..73]`)

Clicking the **`Refr.`** icon (`icon_window[13]`) on the main `swathed` toolbar calls `view_reftool_box()`, creating top-level form `sub_window[61]` (`920 × 620` px), 4 profile plots (`62..65`), 7 parameter sliders (`66..72`), a survey-line coefficient timeline (`73`), and 3 action/mode buttons (`button_window[6..8]`):

### 4 Profile & Residual Graphics Windows

| Window | Dimensions | Function | Description |
| :--- | :--- | :--- | :--- |
| `sub_window[62]` (`REF_OFFSET+1`) | `600 × 150` | `refresh_reftool_window()` | **Original Swath Profiles:** Plots the 80 uncorrected across-track depth profiles (`offsets[j][i]`, `box[j][i]`), highlighting `selected_swath` in `RED`. |
| `sub_window[63]` (`REF_OFFSET+2`) | `600 × 150` | `calc_refract()` | **Synthetic Flat-Bottom Refracted Profile:** Displays the theoretical across-track distortion (`resulting_across[]`, `resulting_depth[]`) produced by the current 2-layer SVP perturbation on an idealized flat seabed at mean water depth `av_depth`. |
| `sub_window[64]` (`REF_OFFSET+3`) | `600 × 150` | `refract_data()` | **Refraction & Heave Corrected Swath Profiles:** Plots the 80 swath profiles after applying the empirical ray-bending correction and lever-arm induced-heave adjustment (`refoff[j][i]`, `refdep[j][i]`). |
| `sub_window[65]` (`REF_OFFSET+4`) | `600 × 120` | `refract_data()` | **Along-Track Induced Heave Residual:** Plots the mean depth residual of the inner half-swath (`no_beams/4` to `3*no_beams/4`) across the 80 pings before (`BLACK`) and after (`RED`) applying the lever-arm induced heave correction (`heave_error[i]`). |
| `sub_window[73]` (`REF_OFFSET+12`) | `300 × 80` | `refresh_reftool_window()` | **Refraction Record Timeline:** Plots the ping locations (`rcoeff[k].rec`) of up to 100 saved empirical refraction coefficient sets along the line (`0` to `no_recs`), marking the active 80-ping window in `RED`. |

### 7 Interactive Parameter Sliders (`sub_window[66..72]`)

| Window | Label | Range | Backing Variable | Physical Meaning |
| :--- | :--- | :--- | :--- | :--- |
| `sub_window[66]` | `transducer depth (m)` | `0.0` .. `10.0` m | `trans_depth` | Draft of the multibeam transducer below the waterline. |
| `sub_window[67]` | `sss. err. (m/s)` | `-20.0` .. `+20.0` m/s | `surf_ss_error` | Surface sound speed error ($\Delta c_0$) affecting initial beam steering angle at the array face (`Horiz.`, `EM1000`, `Twin.`, `EM1002`). |
| `sub_window[68]` | `Step Function Depth (m)` | *Dynamic depth range* | `layer_depth` | Depth of a discrete thermocline/halocline step-function interface in the water column. |
| `sub_window[69]` | `Sound Speed Change (m/s)` | `-30.0` .. `+30.0` m/s | `ss_change` | Sound speed jump ($\Delta c_1$) across the step-function interface at `layer_depth`. |
| `sub_window[70]` | `Induced Hv Lever X (m)` | `-20.0` .. `+20.0` m | `lever_x` | Fore-aft lever arm error (m) coupling pitch into induced vertical heave. |
| `sub_window[71]` | `Induced Hv Lever Y (m)` | `-20.0` .. `+20.0` m | `lever_y` | Athwartships lever arm error (m) coupling roll into induced vertical heave. |
| `sub_window[72]` | `Induced Hv Lever Z (m)` | `-20.0` .. `+20.0` m | `lever_z` | Vertical lever arm error (m) coupling roll and pitch into induced vertical heave. |

---

## Mathematical Formulation (`calc_refract` & `refract_data`)

1. **Surface Sound Speed Steering Error ($\Delta c_0 = \text{surf\_ss\_error}$):**
   * Depending on transducer array geometry (`trans_type`), `calc_refract()` models how an error in surface sound speed $c_0$ alters the launch angle $\theta_0$ relative to instantaneous roll $\phi$:
     * `HORIZ_TRANSDUCER` (`Horiz.`): Flat horizontal array; steering angle follows Snell's law at the array face ($\sin\theta_{\text{new}} = \frac{c_0 + \Delta c_0}{c_0}\sin(\theta - \phi) + \phi$).
     * `CIRC_TRANSDUCER` (`EM1000`): Circular barrel array; beams are steered electronically only beyond $\pm 30^\circ$ (`steer_rel_td`).
     * `TWIN_TRANSDUCER` (`Twin.`): Dual tilted flat arrays mounted at $\pm 40^\circ$ (`port`/`stbd`).
     * `CURV_TRANSDUCER` (`EM1002`): Curved array where inner beams ($\pm 30^\circ$) are unsteered and outer beams experience progressive electronic steering.
2. **Two-Layer Step-Function Snell's Law Ray Tracing:**
   * Above `layer_depth`, rays propagate at $c_0 + \Delta c_0$. Below `layer_depth`, rays refract according to Snell's law into a lower layer with sound speed $c_0 + \Delta c_0 + \text{ss\_change}$, yielding perturbed across-track (`refoff[j][i]`) and depth (`refdep[j][i]`) coordinates.
3. **Induced Heave Lever-Arm Residual (`heave_error`):**
   * For each swath $i$, `refract_data()` rotates the lever-arm vector `(lever_x, lever_y, lever_z)` by `roll[i]`, `pitch[i]`, and `0.0` yaw via `rotate()`, subtracting the vertical component (`heave_error[i]`) from all beam depths in swath $i$.

---

## Action & Mode Buttons (`button_window[6..8]`)

* **`button_window[6]` (`Dump`):** Calls `write_out_refract_coeffs()` (`ref_coeffs.h`), inserting or updating a `ref_coeff` record at the center ping (`in_recnum + SE_NO_SWATHS/2`) with `trans_depth`, `surf_ss_error`, `layer_depth`, `ss_change`, and `trans_type`, and writing `<line_prefix>.ref_coeffs` to disk for batch application via [`applyRef`](../omg/deRefract.html).
* **`button_window[7]` (`Horiz.` / `EM1000` / `Twin.` / `EM1002`):** Cycles `trans_type` and recalculates `calc_refract()` and `refract_data()`.
* **`button_window[8]` (`Str.Heave` / `Flip1Heave` / `Flip2Heave`):** Cycles the sign convention (`heave_sense`) used when computing `heave_error[i]`.
