---
layout: default
title: makeSynPing
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: makeSynPing
source_path: code/grid/makeSynPing.c
category: gridding
input_formats:
- CLI acoustic and seafloor geometry parameters
output_formats:
- .TA.r4 (Time-Angle polar water-column grid)
- .XY.r4 (Cartesian cross-track water-column wedge)
- .BP_TX_FA.r4
- .BP_TX_PS.r4
- .BP_RC_FA.r4
- .BP_RC_PS.r4
related_tools:
- r4to8bit
- synSurface
- make_blank
---

# makeSynPing

## Overview

`makeSynPing` simulates a complete 2D multibeam water-column ping by modeling discrete 42-element cosine-shaded transmit and receive transducer array beam patterns (`95 kHz`), seabed grazing-angle backscatter response (Lambertian + specular near-nadir plateau), sinusoidal seabed relief, hemispherical boulders, cast acoustic shadows, mid-water fish schools, non-synchronized bottom-bounce ghost echoes, and external acoustic shot interference.

For a given `<outname>`, it generates six 32-bit floating-point (`.r4`) grids:
1. `<outname>.TA.r4` — Time/Slant-Range ($X$) vs. Beam Angle ($Y$) acoustic intensity in dB.
2. `<outname>.XY.r4` — Polar-to-Cartesian reprojected water-column wedge (`2*range` wide $\times$ `range` deep), showing the classic nadir specular arc and sidelobe artifacts.
3. `<outname>.BP_TX_FA.r4`, `.BP_TX_PS.r4`, `.BP_RC_FA.r4`, `.BP_RC_PS.r4` — Polar radiation pattern plots of the Transmit Fore-Aft, Transmit Port-Starboard, Receive Fore-Aft, and tilted Receive Port-Starboard arrays with 5 dB range rings and $10^\circ$ radials.

---

## Syntax & CLI Options

```bash
makeSynPing [OPTIONS] <outname_prefix>
```

### Swath & Acoustic Pulse Geometry

| Option | Description | Default |
|---|---|---|
| `<outname_prefix>` | **Required.** Output prefix for `.TA.r4`, `.XY.r4`, and `.BP_*.r4` files. | None |
| `-angsect <deg>` | Total angular sector of the multibeam fan (degrees). | `150.0` |
| `-angstep <deg>` | Beam angular spacing step (degrees). | `0.25` |
| `-crop <port_deg> <stbd_deg>` | Restrict simulated beams to `[port_deg, stbd_deg]` (e.g., `-crop -75 75`). | `-90.0 90.0` |
| `-range <m>` | Maximum slant range in meters. | `4.0 * depth` (`120.0`) |
| `-rangeres <m>` | Slant-range bin resolution in meters (`xstep`). | `0.25` |
| `-pulse_length <m>` | Effective acoustic pulse length in meters. | `0.25` |
| `-tx_lateral_steer <deg>` | Lateral steering angle applied to the transmit array. | `0.0` |
| `-tx_array_width <m>` | Active transmit array length (`Along_Array_Length`) in meters. | `0.06` |
| `-maxoffbeam <deg>` | Maximum off-axis angle from beam center over which sidelobe energy is integrated. | `90.0` |
| `-mindB_BP <dB>` | Minimum dB floor for polar beam pattern plots (`.BP_*.r4`). | `-50.0` |
| `-highlight_m <range_m> <width_m>` | Add a `+25 dB` constant-range arc highlight at `<range_m>` of thickness `<width_m>` (to illustrate constant-time arcs). | Disabled (`0.0`) |

### Seafloor Relief, Boulders & Backscatter Angular Response

| Option | Description | Default |
|---|---|---|
| `-depth <m>` | Mean water depth below transducer (meters). | `30.0` |
| `-amplitude <dm>` | Sinusoidal seabed wave amplitude in **decimeters** (divided by `10.0` internally to meters). | `0.0` |
| `-wavelength <m>` | Sinusoidal seabed wavelength across-track (meters). | `100.0` |
| `-phase <deg>` | Sinusoidal seabed phase at nadir (degrees). | `0.0` |
| `-boulder <offset_m> <radius_m>` | Add a hemispherical boulder on the seabed at `<offset_m>` from nadir with radius `<radius_m>`. Can be repeated up to 20 times. | None |
| `-useSHD` | Enable geometric acoustic cast-shadow raytracing across the seabed profile. | Disabled |
| `-useBS` | Enable grazing-angle seabed backscatter angular response modulation (`Angular_Response[0..89]`). | Disabled |
| `-BSo <dB>` | Oblique reference backscatter strength (dB). | `0.0` |
| `-BSn_BSo <dB>` | Nadir-to-oblique specular backscatter boost (dB). | `30.0` |
| `-Lamb_Power <int_x10>` | Lambertian $\sin^p(\theta)$ exponent multiplied by 10 (e.g., `20` $\rightarrow$ $\sin^2\theta$). | `20` (`2.0`) |
| `-Angle_Change <deg>` | Incidence angle transition from specular cosine lobe to Lambertian roll-off (degrees). | `25.0` |
| `-BS_stripes <dB> <spacing_m>` | Superimpose alternating $\pm\text{dB}$ seabed impedance stripes every `<spacing_m>` meters across-track. | Disabled |
| `-show_AR` | Draw an inset plot of the seabed Angular Response curve directly into the `.XY.r4` image. | Disabled |

### Mid-Water Targets, Ghosts & Acoustic Interference

| Option | Description | Default |
|---|---|---|
| `-fish_school <xcen> <ycen> <xdiam> <ydiam> <spacing> <TS_dB>` | Add an elliptical school of point scatterers centered at `(xcen, ycen)` with dimensions `(xdiam, ydiam)`, mean spacing `<spacing>` m, and individual target strength `<TS_dB>`. Repeatable up to 20 schools. | None |
| `-ghost <offset_m>` | Add a non-synchronized previous-ping bottom-bounce ghost shifted by `<offset_m>` meters. Repeatable up to 20 ghosts. | None |
| `-ghost_pulse_length <m>` | Pulse length of ghost echoes (meters). | `2.0` |
| `-ghost_power <factor>` | Linear power multiplier for ghost echoes relative to main echo. | `1.0` |
| `-shot <offset_m>` | Add an isotropic external seismic/pinger acoustic shot at slant range `<offset_m>` across all beams. Repeatable up to 20 shots. | None |
| `-shot_pulse_length <m>` | Pulse length of external shot interference (meters). | `0.25` |
| `-shot_power <factor>` | Power multiplier for external shot interference (scaled by $R^4$ TVG). | `1.0` |

---

## How It Works

1. **Array Beam Pattern Synthesis:** Configures a 42-element discrete cosine-shaded `95 kHz` multibeam array (`bP_stuff.h`) and calls `recalc_all_models()` to compute lookup tables of linear and log (dB) transmit/receive directivity (`BP[4][2][180 * DEG_FRACTION]`).
2. **Across-Track Seafloor Profile:** Builds a 4000-point cross-track bathymetric profile (`x_profile`, `z_profile`), superimposes any hemispherical `-boulder` targets, computes slant range (`slr_profile`), elevation angle (`ang_profile`), local grazing slope (`graz_profile`), and cast shadows (`shd_profile` if `-useSHD`).
3. **Time-Angle Integration (`.TA.r4`):** For each steered receive beam angle $\theta_{\text{beam}}$ and slant-range sample $R$, integrates the product of transmit beam pattern, receive beam pattern (including all sidelobes within `-maxoffbeam`), and seabed angular response (`Angular_Response`) over all unshadowed seabed facets whose slant range falls within $R \pm \text{pulse\_length}$. Then adds any elliptical `-fish_school` scatterers, `-ghost` bottom echoes, and `-shot` interference.
4. **Polar Wedge Reprojection (`.XY.r4`):** Maps `(range, angle)` samples into Cartesian cross-track $(X, Z)$ water-column space (`XYbuf`) and outputs the four `.BP_*.r4` polar array directivity plots.

---

## Examples

**Simulate a 150° multibeam water-column ping over a 30 m rippled seabed with a boulder and a fish school:**

```bash
makeSynPing \
    -angsect 150 -angstep 0.25 \
    -depth 30 -amplitude 5 -wavelength 25 \
    -boulder 15 2.0 -useSHD \
    -useBS -BSo -15 -BSn_BSo 20 -Lamb_Power 20 -Angle_Change 25 -show_AR \
    -fish_school -12 18 6 4 0.25 -25 \
    syn_wc_demo
# Convert the polar water-column wedge to 8-bit for viewing:
r4to8bit -low -60 -high 20 syn_wc_demo.XY.r4 syn_wc_demo.XY.8bit
```

---

## Workflow Context

- Used for modeling and teaching multibeam water-column imaging physics (specular sidelobe arcs, minimum slant range, boulder shadows, fish school sidelobe smearing, and transmit/receive beam pattern interactions).
