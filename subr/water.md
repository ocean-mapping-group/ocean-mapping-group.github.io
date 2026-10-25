---
layout: default
title: water
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/water.c
category: Raytracing, Sound Speed & Geolocation
related_tools:
- soundspeed
- r_atten
- j_watercolumn
- jb_watercolumn
- svp_tool
module_name: water
header_path: code/subr/water.h
---

# water

## Overview
`water` (`water.c` / `water.h`) implements the **UNESCO (Fofonoff & Millard, 1983) / EOS-80 physical oceanography algorithms** for computing fundamental thermodynamic properties of seawater: adiabatic temperature gradient, potential temperature, in-situ temperature, practical salinity (PSS-78) from electrical conductivity, seawater density ($\rho$ and $\sigma_t$), and the freezing point of seawater.

Together with [`soundspeed`](soundspeed.html) and [`r_atten`](r_atten.html), `water` enables CTD profile ingestion, water-mass property analysis, and physical-oceanographic preprocessing for acoustic raytracing and absorption modeling.

---

## Public Functions

| Function | Signature | Inputs & Units | Description |
|---|---|---|---|
| `adtg` | `double adtg(double S, double T, double P)` | `S`: salinity (PSU)<br>`T`: temp ($^\circ\text{C}$)<br>`P`: pressure (dbar) | **Adiabatic Temperature Gradient** $\Gamma(S,T,P)$ in $^\circ\text{C/dbar}$ from Fofonoff & Millard (1983, UNESCO Tech. Paper 44). |
| `potential_temperature` | `double potential_temperature(double T, double S, double P, double PR)` | `T`: in-situ temp ($^\circ\text{C}$)<br>`S`: salinity (PSU)<br>`P`: in-situ pressure (dbar)<br>`PR`: ref pressure (dbar) | **Potential Temperature** $\theta(S,T,P,P_r)$ in $^\circ\text{C}$ computed via a 4th-order Runge-Kutta integration of `adtg()` from pressure `P` to reference pressure `PR` (Fofonoff & Millard, 1983). |
| `insitu_temperature` | `double insitu_temperature(double T, double S, double P)` | `T`: potential temp ($^\circ\text{C}$)<br>`S`: salinity (PSU)<br>`P`: pressure (MPa) | **In-Situ Temperature** ($^\circ\text{C}$) recovered from potential temperature `T` by iteratively stepping temperature in $0.0001\ ^\circ\text{C}$ increments until `potential_temperature(temp, S, P*100, 0)` matches `T` within $10^{-4}\ ^\circ\text{C}$. |
| `conductivity2salinity` | `double conductivity2salinity(double conductivity, double pressure, double temperature)` | `conductivity`: $\text{S/m}$<br>`pressure`: dbar<br>`temperature`: $^\circ\text{C}$ | **PSS-78 Practical Salinity** (PSU) from electrical conductivity (`C` in Siemens/meter, internally multiplied by `10.0` to convert to $\text{mS/cm} = \text{mmho/cm}$ and normalized by standard seawater conductivity $42.914\text{ mS/cm}$ at $S=35, T=15^\circ\text{C}, P=0$), pressure, and temperature (Fofonoff & Millard, 1983). |
| `density0` | `double density0(double s, double t)` | `s`: salinity (PSU)<br>`t`: temp ($^\circ\text{C}$) | **One-Atmosphere Seawater Density** $\rho(S,T,0)$ in $\text{kg/m}^3$ at the sea surface ($P = 0$) from the EOS-80 International Equation of State of Seawater. |
| `density` | `double density(double s, double t, double p)` | `s`: salinity (PSU)<br>`t`: temp ($^\circ\text{C}$)<br>`p`: pressure (dbar) | **In-Situ Seawater Density** $\rho(S,T,P) = \frac{\rho(S,T,0)}{1 - (P/10)/K(S,T,P)}$ in $\text{kg/m}^3$, using the secant bulk modulus $K(S,T,P)$ with $P_{\text{bar}} = p / 10$. |
| `sigma_t` | `double sigma_t(double T, double S, double P)` | `T`: temp ($^\circ\text{C}$)<br>`S`: salinity (PSU)<br>`P`: ignored | **Density Anomaly** $\sigma_t = \rho(S,T,0) - 1000.0$ in $\text{kg/m}^3$ at atmospheric pressure. |
| `freezing_point` | `double freezing_point(double salinity, double pressure)` | `salinity`: PSU ($4..40$)<br>`pressure`: dbar | **UNESCO Seawater Freezing Point** $T_f(S,P) = -0.0575 S + 1.710523\times 10^{-3} S^{3/2} - 2.154996\times 10^{-4} S^2 - 7.53\times 10^{-4} P$ in $^\circ\text{C}$ (Millero, 1978). |

---

## Architectural Role
`water` is paired with [`soundspeed`](soundspeed.html) in CTD and Oceanographic model readers (such as [`j_SalishSeaCast`](j_SalishSeaCast.html), [`j_SSCOFS`](j_SSCOFS.html), and [`svp_tool`](../JV/JV_svpedit.html)) where model outputs or CTD casts provide potential temperature or conductivity rather than in-situ temperature and practical salinity.
