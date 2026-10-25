---
layout: default
title: testfn
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 25
tool_name: testfn
source_path: code/tests/testfn.c
category: Backscatter & Ensonified Footprint Geometry (tests)
input_formats:
  - Command-line depth parameter (-depth)
output_formats:
  - Console geometric footprint table from show_footprint()
related_tools:
  - BatchProcEK
  - EKlook
  - deTVG
  - testAtten
---

# testfn

## Overview
`testfn` (`code/tests/testfn.c`, authored by John Hughes Clarke in August 1992) is a concise driver utility written to test the `show_footprint(depth, beam_width, pulse_length)` library function declared in `Echo_calib.h` (`liblocal.a`).

In multibeam and sidescan radiometric backscatter reduction (such as [`deTVG`](../omg/deTVG.md) and [`BatchProcEK`](../EKlook/BatchProcEK.md)), converting raw echo intensity into seafloor backscatter strength per unit area ($S_b$ in $\text{dB re } 1\text{ m}^2/\text{m}^2$) requires computing the instantaneous ensonified seafloor area $A(\theta)$ across the swath. `testfn` calls `show_footprint()` for a given water depth (`depth`, default $100\text{ m}$), two-way beamwidth (`beam_width = 3.3` degrees), and transmit pulse duration (`pulse_length = 0.0002` seconds = $0.2\text{ ms}$) to print the transition from the **beamwidth-limited** (nadir) regime to the **pulse-length-limited** (oblique) regime.

---

## Syntax & CLI Options

```bash
testfn [-v] [-depth <meters>] [<inname> [<outname>]]
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-depth <meters>` | Water depth $D$ in meters passed to `show_footprint(depth, beam_width, pulse_length)` (parsed via `strtoint`). | `100.0` |
| `-v` | Increment verbose flag (`verbose_flag++`). | `0` |
| `<inname> <outname>` | Optional positional arguments stored in `inname` and `outname` (not opened). | Unused |

---

## Ensonified Area Geometry (`show_footprint`)

For a sonar at altitude/depth $D$ above a flat seafloor with along-track beamwidth $\phi_{\text{along}}$ (`beam_width` in radians), across-track beamwidth $\phi_{\text{across}}$, sound speed $c \approx 1500\text{ m/s}$, and effective pulse duration $\tau$ (`pulse_length` in seconds):

1. **Near-Nadir Beamwidth-Limited Regime ($\theta \approx 0^\circ$):**
   At normal incidence, the entire spherical cap within the receiver beam is ensonified simultaneously, and the footprint area is governed by the along-track and across-track beamwidths at slant range $R = D / \cos\theta$:
   $$A_{\text{beam}}(\theta) \approx \frac{R^2 \, \phi_{\text{along}} \, \phi_{\text{across}}}{\cos\theta}$$

2. **Oblique Pulse-Length-Limited Regime ($\theta > \theta_{\text{crit}}$):**
   At incidence angles away from nadir, the across-track width of the instantaneously ensonified annulus is bounded by the projected physical pulse length $\frac{c\tau}{2\sin\theta}$, while the along-track dimension remains $R\,\phi_{\text{along}}$:
   $$A_{\text{pulse}}(\theta) \approx R\,\phi_{\text{along}} \cdot \frac{c\tau}{2\sin\theta}$$

`testfn` calls `show_footprint(depth, 3.3, 0.0002)` to print these geometric footprint dimensions across incidence angles for rapid verification of `Echo_calib` routines.

---

## Example Usage

```bash
# Print ensonified footprint geometry for default 100 m depth, 3.3 deg beamwidth, 0.2 ms pulse
testfn

# Print footprint geometry for 250 m water depth
testfn -depth 250
```
