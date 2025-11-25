---
layout: default
title: bpfunc.c
parent: BPdemo
nav_order: 3
---

# bpfunc.c

## Description
`bpfunc.c` is a source code file that provides the core computational functions for the **`bpdemo`** (Beam Pattern Phasor Summation Demo) application. It is not a standalone command-line tool but rather a module that performs the physics-based calculations for the beamforming simulation. The functions in this file calculate the resulting beam pattern based on the number of transducer elements, their spacing, weighting, and steering angle.

## Functionality

This file contains the core logic that the `bpdemo` GUI visualizes. The main functions include:

### `void calc_beam_pattern()`
This is the primary function for calculating the sonar beam pattern. It iterates through a range of look angles (from -90 to +90 degrees) and computes the total acoustic power for each angle.
*   **How it works:** For each angle, it determines the phase difference of the incoming wavefront at each transducer element. It then sums the complex contributions (phasors) from all elements, applying any user-defined weighting and phase shifts. The final power is the squared magnitude of this complex sum.
*   **Output:** The results (power, pressure, and log-power) are stored in global arrays (`bp_power`, `bp_pres`, `bp_log`) that are used by the drawing functions to visualize the beam pattern.

### `void calc_element_positions()`
A helper function that calculates the physical position of each transducer element in the array based on the total number of elements and their spacing. This is used to correctly model the geometry of the sonar.

### `void advance_phase()`
A simple utility function that decrements the `current_phase` global variable. This is called repeatedly to create an animated effect in the phasor diagrams.

### `void prime_settings()`
This function initializes all simulation parameters to a default state when the application starts. This includes:
*   Setting default weightings and phase shifts for all elements to 1.0 and 0.0, respectively.
*   Setting a default number of elements and spacing.
*   Pre-calculating a lookup table of sine and cosine values to speed up the `calc_beam_pattern` function.
*   Calling `calc_beam_pattern()` to compute the initial beam pattern with the default settings.

### `void recalc_phaseshifts()`
This function is called when the user changes the steering angle. It recalculates the required phase shift for each element to electronically "steer" the beam to the desired direction.

Together, these functions form the "engine" of the `bpdemo` application, performing the calculations that are then visualized by the GUI components.