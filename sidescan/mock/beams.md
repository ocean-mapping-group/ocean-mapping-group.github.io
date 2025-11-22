---
layout: default
title: beams
parent: Mock Tools
grand_parent: sidescan
nav_order: 3
---
# beams

## Description
`beams` is a utility designed to calculate GLORIA's beam directivity functions, commonly known as beam patterns. It can compute either horizontal or vertical beam patterns, taking into account various physical parameters of the GLORIA sonar system, such as array length, array width, transducer spacing, and operating frequency. The output can be presented in linear power, linear pressure, or decibel (dB) scale.

## Usage
```bash
beams [-l] [-p] [-h] [-s] [-i <increment>] [-m <max_angle>]
```

## Arguments

| Option | Description |
|---|---|
| `-l` | Output in dB scale (logarithmic power). |
| `-p` | Output in linear pressure scale. |
| `-h` | Calculate the horizontal beam pattern. By default, it calculates the vertical beam pattern. |
| `-s` | Use starboard side frequency (6287.5 Hz). By default, it uses port side frequency (6762.5 Hz). |
| `-i <increment>` | Specifies the angular increment (in degrees) for the calculation. |
| `-m <max_angle>` | Specifies the maximum angle (in degrees) up to which the beam pattern is calculated. |

## How It Works
1.  **Parameter Initialization:** The program initializes physical parameters of the GLORIA array, such as `array_length` (5.33m), `array_width` (0.31m), `radius` (0.057m), `spacing` (0.17m), and `freq` (6762.5 Hz for port, 6287.5 Hz for starboard).
2.  **Argument Parsing:** Command-line arguments modify these parameters and select the output scale and beam pattern type (horizontal or vertical).
3.  **Wavenumber Calculation:** It calculates the wavenumber `k = 2. * M_PI * freq / 1500.`, where 1500 m/s is assumed to be the speed of sound in water.
4.  **Horizontal Beam Pattern (`-h`):**
    *   If `-h` is specified, it iterates `thi` (angle) from 0 to `max_angle` with `increment`.
    *   The directivity `D` is calculated using the formula `sin(const * sin(thi)) / (const * sin(thi))`, where `const = k * array_length / 2.`.
5.  **Vertical Beam Pattern (Default):**
    *   If `-h` is not specified, it iterates `theta` (angle) from 0 to `max_angle` with `increment`.
    *   The directivity `D` is calculated as a product of two terms:
        *   A 2-point array pattern: `sin(2. * values) / (2. * sin(values))` where `values = spacing * k * sin(theta) / 2.`.
        *   A circular transducer pattern: `2. * j1(x) / x` where `x = k * radius * sin(theta)` and `j1` is the Bessel function of the first kind of order 1 (though `j1` is not explicitly defined in the provided code, it's a standard mathematical function).
6.  **Output Scaling:**
    *   **Linear Power (Default):** Prints `D * D`.
    *   **Linear Pressure (`-p`):** Prints `D`.
    *   **dB Scale (`-l`):** Prints `10. * log10(D * D)`.
7.  **Loop:** The calculations and output are performed for each angular step up to `max_angle`.
