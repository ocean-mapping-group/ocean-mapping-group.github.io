---
layout: default
title: testAtten
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 18
tool_name: testAtten
source_path: code/tests/testAtten.c
category: Seawater Sound Speed & Acoustic Attenuation (tests)
input_formats:
  - Interactive stdin (Temp, Salinity, Depth, Frequency, pH)
  - 8-column ASCII CTD cast (-convert)
  - OMG j_watercolumn SVP/CTD file (-custom122, -custom710)
output_formats:
  - Interactive absorption coefficient on stdout (dB/km)
  - OMG ASCII multi-curve plot files (<outfile>, <outfile>.sal, <outfile>.tem, <outfile>.cum)
related_tools:
  - testSV
  - speed2salinity
  - speedtosalinity
  - comboASCIIParam2
  - BatchProcEK
---

# testAtten

## Overview
`testAtten` (`code/tests/testAtten.c`, authored by John Hughes Clarke in August 1993) is a versatile seawater acoustic absorption calculator and water-column profile analyzer built around `calc_atten(temp, salinity, depth, pH, freq)` from `Echo_calib.h` (which implements Francois & Garrison's 1982 boric acid, magnesium sulfate, and pure water relaxation equations in $\text{dB/km}$) and the `j_watercolumn` (`jWC_read`) library.

It supports five operating modes selected via command-line flags:
1. **Interactive Mode (Default):** Repeatedly prompts on `stdin` for `Temp Salinity Depth Frequency PH` and prints the resulting absorption coefficient in $\text{dB/km}$.
2. **8-Column CTD Profile Conversion (`-convert`):** Reads an 8-column ASCII CTD file, computes absorption at $95.0\text{ kHz}$ ($\text{pH} = 7.0$), and writes a 4-curve OMG plot file (`Depth, Temp, Salinity, Velocity, Atten`).
3. **2D Temperature–Salinity Look-Up Table (`-table`):** Generates a 30-curve OMG plot file of absorption at $95.0\text{ kHz}$ ($\text{pH} = 7.0$, fixed `-depth`) across Salinity $S \in [0.0, 39.5]\text{ ppt}$ ($0.5\text{ ppt}$ steps) and Temperature $T \in [0, 29]^\circ\text{C}$ ($1^\circ\text{C}$ steps).
4. **Kongsberg EM122 Deep-Water Multi-Sector Profile (`-custom122`):** Reads an OMG `j_watercolumn` cast via `jWC_read()`, interpolates $T(z)$ and $S(z)$ from $0$ to $5000\text{ m}$ in $50\text{ m}$ steps, and outputs both local and cumulative layer-averaged absorption across 16 EM122 transmit sector frequencies ($11.00\text{ kHz}$ to $13.25\text{ kHz}$ in $0.15\text{ kHz}$ steps).
5. **Kongsberg EM710 Shallow/Mid-Water Multi-Sector Profile (`-custom710`):** Reads a `j_watercolumn` cast, interpolates $T(z)$ and $S(z)$ from $0$ to $300\text{ m}$ in $3\text{ m}$ steps, and writes local (`<out>`), cumulative (`<out>.cum`), and $T/S$ (`<out>.sal`) plot files across 8 EM710 sector frequencies ($73, 75, 77, 79, 81, 85, 89, 97\text{ kHz}$).

---

## Syntax & CLI Options

```bash
# Interactive mode
testAtten

# Print expected physical units and exit
testAtten -units

# Batch / profile modes
testAtten [-v] (-convert | -table [-depth <m>] | -custom122 | -custom710) [<infile>] <outfile>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-units` | Prints the expected physical units (`temp in deg celcius`, `salinity in ppt`, `depth in metres`, `pH in range 0 to 14`, `freq in kHz`) and exits. | — |
| `-convert` | (`convert_flag = 1`) Read 8-column ASCII CTD file `<infile>` (`id depth temp d1 d2 sal d3 vel`) and write $95\text{ kHz}$ attenuation profile to `<outfile>`. | `0` |
| `-table` | (`convert_flag = 2`) Generate a $T \in [0, 29]^\circ\text{C}$ by $S \in [0, 39.5]\text{ ppt}$ absorption table at $95\text{ kHz}$ and fixed `-depth` into `<inname>`/`<outname>` (note: requires two positional args so `outname` is populated). | `0` |
| `-custom122` | (`convert_flag = 3`) Read `j_watercolumn` file `<infile>`, interpolate to $5000\text{ m}$ ($50\text{ m}$ steps), and compute local and cumulative harmonic-mean absorption for 16 Kongsberg EM122 frequencies ($11.00\text{–}13.25\text{ kHz}$). | `0` |
| `-custom710` | (`convert_flag = 4`) Read `j_watercolumn` file `<infile>`, interpolate to $300\text{ m}$ ($3\text{ m}$ steps), and compute local (`<outfile>`) and cumulative (`<outfile>.cum`) absorption for 8 Kongsberg EM710 frequencies ($73\text{–}97\text{ kHz}$), plus `<outfile>.sal`. | `0` |
| `-depth <m>` | Fixed depth in meters used in `-table` mode (parsed via `strtoint`). | `10.0` |
| `-v` | Increment verbose flag (`verbose_flag++`). | `0` |

---

## Water-Column Interpolation & Cumulative Absorption (`-custom122` / `-custom710`)

In multibeam backscatter radiometric correction (such as [`deTVG`](../omg/deTVG.md) or [`read_kmall`](../kmall/read_kmall.md)), a constant absorption coefficient set in the sonar runtime parameters often differs from the true depth-integrated absorption along a ray path through a stratified thermocline/halocline.

In `-custom122` and `-custom710` modes, `testAtten` reads `wc_in.raw_zv[k]` from the input SVP/CTD file and performs linear depth interpolation for each depth step $z_i$:

$$w_1 = \frac{z_i - z_k}{z_{k+1} - z_k}, \qquad w_2 = \frac{z_{k+1} - z_i}{z_{k+1} - z_k}$$

$$T(z_i) = w_2\, T_k + w_1\, T_{k+1}, \qquad S(z_i) = w_2\, S_k + w_1\, S_{k+1}$$

At each depth $z_i$ and frequency $f_m$, it evaluates the local absorption $\alpha_m(z_i) = \text{calc\_atten}(T(z_i), S(z_i), z_i, 7.0, f_m)$ and updates the running depth-averaged cumulative absorption from the surface to depth $z_i$:

$$\overline{\alpha}_m(z_i) = \frac{1}{N(z_i)} \sum_{n=0}^{i} \alpha_m(z_n)$$

---

## Example Usage

```bash
# 1. Interactive point calculation (T=10°C, S=35 ppt, Z=100 m, f=300 kHz, pH=8.0)
testAtten <<EOF
10.0 35.0 100.0 300.0 8.0
EOF

# 2. Compute EM710 multi-sector local and cumulative absorption profiles from an SVP/CTD cast
testAtten -custom710 station04.svp em710_atten.plt
```
