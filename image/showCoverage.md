---
layout: default
title: showCoverage
parent: Image Tools
nav_order: 47
tool_name: showCoverage
source_path: code/image/showCoverage.c
category: Multibeam Water Column & Acoustic Modeling
input_formats: ["ASCII beam directivity table (-angresp)"]
output_formats: ["2D across-track/depth SNR coverage OMG1 8-bit array (-out)"]
related_tools: ["embedBeamSpacing", "TAtoXZ", "stretchacres"]
---

# showCoverage

## Description
`showCoverage` models the 2D vertical cross-section of acoustic echo level / Signal-to-Noise Ratio (SNR) across the water column and seabed for a multibeam or sidescan sonar system. Given an ASCII transducer angular response table (`-angresp`) and sonar equation parameters (source level, absorption coefficient, pulse length, beamwidth, and max sector angle), it outputs an 8-bit `OMG1` (`JHC_header`) vertical cross-section image (`-out`) showing spatial acoustic coverage, sidelobe envelopes, and seabed grazing footprints.

## CLI Options & Usage
```bash
showCoverage -angresp <beam_table> -out <coverage.8bit> \
  [-depth <m>] [-width <m>] [-bathy_sector] [-max_angle <deg>] \
  [-pixel <m>] [-atten <dB_km>] [-source_level <dB>] [-pulse_length <ms>]
```
* **`-angresp <beam_table>`**: ASCII file listing `angle_deg  tx_dB  rx_dB` (interpolated to `0.1°` increments across `-90°..+90°`).
* **`-out <coverage.8bit>`**: Output 8-bit `OMG1` vertical cross-section image.
* **`-depth <m> -width <m>`**: Vertical depth range and horizontal across-track width in meters (defaults: `500 m` depth × `1000 m` width).
* **`-pixel <m>`**: Grid pixel size in meters (default: `1.0 m`).
* **`-bathy_sector` / `-max_angle <deg>`**: Restricts active beam steering to `±max_angle` (default: `60.0°`).
* **`-atten <dB_km>`**: Sea-water acoustic absorption coefficient in $\text{dB/km}$ (default: `30.0 dB/km`, e.g., ~95 kHz).
* **`-source_level <dB>`**: Transmit Source Level in $\text{dB re } 1\ \mu\text{Pa @ 1 m}$ (default: `220.0 dB`).
* **`-pulse_length <ms>`**: Transmit pulse duration in milliseconds (default: `1.0 ms`).

## Algorithm
For every pixel `(x, z)` in the across-track/depth plane, evaluates the active sonar equation:
$$\text{EL} = \text{SL} - 2\text{TL} + \text{BS} + 10\log_{10}(\text{EA}) + \text{DI}_T(\theta) + \text{DI}_R(\theta)$$
where $2\text{TL} = 40\log_{10}(R) + 2\alpha R$, $\text{EA}$ is the instantaneous insonified annulus area, and $\text{BS}$ incorporates Lambertian + specular angular backscatter, scaling $\text{EL}$ (`0..127 dB`) into 8-bit greyscale (`254..0`).
