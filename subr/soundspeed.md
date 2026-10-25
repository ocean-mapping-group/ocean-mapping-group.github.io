---
layout: default
title: soundspeed
parent: Shared Core Libraries (subr)
module_name: soundspeed
source_path: code/subr/soundspeed.c
header_path: code/subr/soundspeed.h
category: Raytracing, Sound Speed & Geolocation
related_tools: ["water", "j_watercolumn", "jb_watercolumn", "svp_tool", "r_atten"]
---

# soundspeed

## Overview
`soundspeed` (`soundspeed.c` / `soundspeed.h`) provides standard empirical oceanographic equations for computing the **speed of sound in seawater** from temperature, salinity, and pressure/depth, as well as hydrostatic pressure-to-depth conversions and inverse salinity estimation from sound velocity sensors (SVP/SV&T probes). Coded by Jason Bartlett (Sept–Oct 2006) from the NPL (National Physical Laboratory) *Technical Guides — Speed of Sound in Sea-Water* and AML Oceanographic white papers, it supports CTD-to-SVP conversion and refraction modeling across the Ocean Mapping Group software suite.

---

## Constants & Unit Conversions

Defined in `soundspeed.h` for converting between MPa, bars, decibars, and $\text{kg/cm}^2$:

| Macro | Value | Description |
|---|---|---|
| `MPA_TO_BARS` | `10` | $1\text{ MPa} = 10\text{ bar}$ (used for `ChenMillero`). |
| `BARS_TO_DBARS` | `10` | $1\text{ bar} = 10\text{ dbar}$. |
| `MPA_TO_KG_PER_CM_SQ` | `10.19716` | $1\text{ MPa} = 10.19716\text{ kg/cm}^2$ (used for `DelGrosso`). |

---

## Public Functions

| Function | Signature | Validity Range & Units | Description |
|---|---|---|---|
| `ChenMillero` | `double ChenMillero(double sal, double temp, double press)` | $T \in [0, 40]\ ^\circ\text{C}$<br>$S \in [0, 40]\text{ PSU}$<br>$P \in [0, 1000]\text{ bar}$ | **UNESCO / Chen & Millero (1977)** international standard equation for sound speed in seawater ($\text{m/s}$): $c(S,T,P) = C_w(T,P) + A(T,P)S + B(T,P)S^{3/2} + D(P)S^2$. Note: `press` is in **bars** ($\text{dbar}/10$). |
| `Mackenzie` | `double Mackenzie(double S, double T, double D)` | $T \in [2, 30]\ ^\circ\text{C}$<br>$S \in [25, 40]\text{ ppt}$<br>$D \in [0, 8000]\text{ m}$ | **Mackenzie (1981)** 9-term polynomial for sound speed ($\text{m/s}$) directly as a function of depth $D$ in **meters**, salinity $S$ in ppt, and temperature $T$ in $^\circ\text{C}$. |
| `DelGrosso` | `double DelGrosso(double S, double T, double P)` | $T \in [0, 30]\ ^\circ\text{C}$<br>$S \in [30, 40]\text{ ppt}$<br>$P \in [0, 1000]\text{ kg/cm}^2$ | **Del Grosso (1974)** NRL equation for open-ocean sound speed ($\text{m/s}$): $c = c_{000} + \Delta c_T + \Delta c_S + \Delta c_P + \Delta c_{STP}$. Note: `P` is gauge pressure in **$\text{kg/cm}^2$**. |
| `Coppens` | `double Coppens(double D, double S, double T)` | $T \in [0, 35]\ ^\circ\text{C}$<br>$S \in [0, 45]\text{ ppt}$<br>$D \in [0, 4000]\text{ km/m}$ | **Coppens (1981)** simplified sound speed formula (note: expects $D$ in kilometers in standard literature; marked in source comments as having a unit scaling issue if meters are passed directly). |
| `press2depth` | `double press2depth(double press, double lat)` | `press`: $\text{MPa}$<br>`lat`: decimal degrees | **Saunders & Fofonoff (1976) / UNESCO** hydrostatic conversion from pressure ($\text{MPa}$) and latitude (`lat`) to depth in **meters**, accounting for latitude-dependent gravity $g(\phi) = 9.780318(1 + 5.2788\times 10^{-3}\sin^2\phi + 2.36\times 10^{-5}\sin^4\phi)$. |
| `depth2press` | `double depth2press(double depth, double lat)` | `depth`: meters<br>`lat`: decimal degrees | Inverse hydrostatic conversion from depth in **meters** and latitude (`lat`) to pressure in **$\text{MPa}$**. |
| `speed_temp2salinity` | `double speed_temp2salinity(double sound_speed, double temperature, double pressure)` | `sound_speed`: $\text{m/s}$<br>`temperature`: $^\circ\text{C}$<br>`pressure`: $\text{dbar}$ | **Tom Dakin / AML Oceanographic (1999)** 17-term polynomial (`Applied Microsystem's Equation for Salinity Calculation from SV, T & P`) that back-calculates practical salinity ($\text{PSU}$) from direct time-of-flight sound velocity (`SV`), temperature (`T`), and pressure (`P`). |

---

## Architectural Role
`soundspeed` works alongside [`water`](water.md) (seawater density, potential temperature, and conductivity-to-salinity) and [`r_atten`](r_atten.md) (Francois-Garrison acoustic absorption). It is used by CTD/SVP import utilities, `svp_tool`, and acoustic backscatter absorption calculators when converting raw CTD casts or AML SV&T probe logs into raytracing sound velocity profiles.
