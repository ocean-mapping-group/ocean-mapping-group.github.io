---
layout: default
title: SYN_doBD
parent: GL Tools
nav_order: 4
---

# SYN_doBD

## Description
`SYN_doBD.c` is a source code file that provides the core bottom detection (BD) algorithms and related processing for the `glSeis` application. It is not a standalone command-line tool.

This module simulates how sonar systems detect the seafloor (or other targets) using both amplitude and phase characteristics of the simulated echo time series. It can also apply corrections like Time-Varying Gain (TVG) removal.

## Functionality

### `void init_BD()`
*   **Purpose:** Initializes global variables related to bottom detection.
*   **Action:** Sets default values for parameters such as `noise_level`, `min_acceptable_phase_residual`, and the `BDs_to_plot` flag (which controls what type of bottom detections are displayed).

### `void do_BD()`
*   **Purpose:** Executes the main bottom detection algorithm on the simulated sonar time-series data.
*   **Action:**
    1.  **Amplitude Detection:**
        *   Smooths the echo intensity profile using a running average (`nogain[]`).
        *   Identifies the peak amplitude (`maxval`) within the smoothed profile.
        *   Calculates a "center of mass" for the echo envelope, which provides a robust range estimate.
        *   Records these amplitude-based detections as `BD` (Bottom Detection) records of `type 0` (peak amplitude) and `type 1` (center of mass).
    2.  **Phase Detection:**
        *   Analyzes the phase data (`Phase_Series[]`) to identify zero-phase crossings.
        *   Performs a least-squares fit on sections of the phase data to estimate the slope and intercept.
        *   Filters solutions based on fit residuals and identifies robust phase-based detections.
        *   Records these phase-based detections as `BD` records of `type 2` (main zero-phase crossing) and `type 3` (high-definition solutions).
    *   The algorithm iteratively refines search windows and applies criteria to select the most reliable detections.

### `void removeTVG()`
*   **Purpose:** Applies a simulated Time-Varying Gain (TVG) removal to the time-series data.
*   **Action:** It corrects the intensity values in the simulated echo (`Time_Series[]`) by subtracting a range-dependent gain, effectively compensating for spreading loss and absorption. This process allows for a more accurate assessment of target strength or bottom backscatter.

This module is essential for simulating and analyzing fundamental aspects of sonar operation within the `glSeis` visualization tool. It provides a means to understand how bottom detectors work and how various echo characteristics influence detection.