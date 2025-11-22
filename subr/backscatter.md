---
layout: default
title: backscatter
parent: Subr Tools
grand_parent: code
nav_order: 4
---
# backscatter

## Description
`backscatter.c` is a C utility library providing core functions related to backscatter calculations, primarily for sonar data processing and modeling within the GEMINI project. This library encapsulates mathematical and acoustic physics functions used in simulating, analyzing, or correcting sidescan sonar data. Key functionalities include calculating angles between vectors (essential for determining grazing angles relative to seafloor slope), handling acoustic propagation parameters like Time-Varying Gain (TVG), and converting between different digital representations of intensity data (e.g., 8-bit to 12-bit).

## Functions

### `float cosangle(float pixlen, float elev, float azi, float pixel, float peast, float psouth)`
(This function is commented as "not complete yet" in the source). Intended to calculate an angle related to sun illumination, likely between a light source vector and a surface normal.

### `float vectangle(float pixlen, float elev, float azi, float pixel, float peast, float psouth)`
Calculates the angle between the insonification direction (sonar beam) and the normal to a local seafloor facet.
*   `pixlen`: Pixel length (grid cell size).
*   `elev`: Elevation angle of the insonification direction.
*   `azi`: Azimuth of the insonification direction.
*   `pixel`: Depth (or Z-value) of the current pixel.
*   `peast`: Depth (or Z-value) of the pixel to the East.
*   `psouth`: Depth (or Z-value) of the pixel to the South.
*   **Returns:** The angle (in degrees) between the two vectors. Returns `-1` if the surface is unimageable (e.g., in shadow).

### `void dget360offsets(double azi, double *xoffset, double *yoffset)`
Calculates `x` and `y` offset components (direction vectors) from a given azimuth (in radians), ensuring the azimuth is mapped to a 0-360 degree range internally.

### `void get360offsets(float azi, float *xoffset, float *yoffset)`
A wrapper for `dget360offsets`, but taking a float azimuth and returning float offsets.

### `double bit8_to_bit12(unsigned char bit8_value)`
Converts an 8-bit unsigned integer value (e.g., from sidescan imagery) to its equivalent 12-bit floating-point representation, following a specific non-linear compression scheme (likely the "BELL 255 law" or similar).
*   `bit8_value`: The 8-bit input value.
*   **Returns:** The corresponding 12-bit float value.

### `double inverse_TVG(double distance, double DB)`
Calculates the inverse Time-Varying Gain (TVG) as a voltage ratio for a given acoustic `distance` and a `DB` (decibel) constant.
*   `distance`: Acoustic path length.
*   `DB`: TVG constant (related to two-way spreading loss and absorption).
*   **Returns:** A voltage ratio (`tvg`).

### `int tvg_shading_loss(double tvg_shade[496], int ping_rate)`
Calculates and populates an array (`tvg_shade`) with TVG and pulse shading loss factors.
*   `tvg_shade`: An array to store the calculated TVG values for different range bins.
*   `ping_rate`: The ping rate (in seconds), used to determine constants for TVG calculation.
*   **Returns:** `0` on success.

### `void get360azi(double dx, double dy, double *azi)`
Calculates the azimuth (in radians, 0 to 2*PI) from given `dx` (easting component) and `dy` (northing component) vectors.

## How It Works
The `backscatter` library provides tools for fundamental geometric and acoustic calculations required in quantitative sonar processing.
1.  **Vector Geometry (`vectangle`, `get360offsets`, `get360azi`):** These functions enable the calculation of surface normals from gridded depth data, the direction of insonification, and the angle between these two. This is critical for determining the effective grazing angle, a key parameter in backscatter modeling.
2.  **Data Transformation (`bit8_to_bit12`):** This function performs a non-linear expansion from 8-bit to 12-bit, effectively reversing a compression often applied to sonar intensity data to preserve dynamic range.
3.  **Acoustic Corrections (`inverse_TVG`, `tvg_shading_loss`):** These functions implement the Time-Varying Gain (TVG) and pulse shading loss models. TVG compensates for signal spreading and absorption losses as a function of range, ensuring that differences in received intensity primarily reflect seafloor properties rather than range effects.
The library's algorithms often involve trigonometric functions and logarithmic scales (for dB conversions), reflecting the physics of underwater acoustics.
