---
layout: default
title: bP_stuff
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/bP_stuff.c
category: Acoustic Array & Beam Pattern Modeling
related_tools:
- plotBP
- BDplot
- makeSynPing
- synSwath
module_name: bP_stuff
header_path: code/subr/bP_stuff.h
---

# bP_stuff: Acoustic Transducer Array Shading, Beam Pattern & Phase Modeling

## Overview & Purpose
`bP_stuff` (`bP_stuff.c` / `bP_stuff.h`, ~1,342 lines) is a theoretical acoustic transducer modeling library created by John Hughes Clarke in December 1994 (with extensions in 2006 and 2017). It models the directivity patterns (transmit fore-aft, transmit port-starboard, receive fore-aft, and receive port-starboard) and interferometric phase responses of:
* **Continuous line arrays (`LINE`)**
* **Discrete multi-element staves (`DISCRETE`)**
* **Circular/conical piston transducers (`CONE`)**
* **Two-element bathymetric sidescan interferometers (`BATHY_SIDESCAN`)**

The module supports 9 classical aperture shading (apodization) windows—including Dolph-Chebyshev (-20 dB, -30 dB, -40 dB), Binomial, Cosine, Cosine-Squared, Linear, Inverse Linear, and Unshaded—and accounts for electronic beam steering, static roll/pitch, and sound velocity mismatches at the array face (Snell's law refraction error when `Sound_Velocity != Assumed_Sound_Velocity`).

---

## Key Constants & Global State Variables

### Array & Shading Constants

```c
/* Pattern / Direction Indices */
#define TRANSMIT_FORE_AFT  0
#define TRANSMIT_PORT_STBD 1
#define RECEIVE_FORE_AFT   2
#define RECEIVE_PORT_STBD  3

/* Array Calculation Models */
#define LINE     0
#define DISCRETE 1
#define CONE     2

/* Shading (Apodization) Window Types */
#define UNSHADED       0
#define COS_SQUARED    1
#define INVERSE_LINEAR 2
#define LINEAR         3
#define COSINE         4
#define BINOMIAL       5
#define CHEB_20        6
#define CHEB_30        7
#define CHEB_40        8

/* Output Power Units */
#define LOG_POWER       0
#define LINEAR_POWER    1
#define LINEAR_PRESSURE 2

/* Angular Resolution: 5 bins per degree (0.2 deg steps across 180 deg = 900 bins) */
#define DEG_FRACTION 5
```

### Global Transducer & Result Arrays
* **Physical Array Parameters:** `Frequency` (Hz), `Sound_Velocity` (m/s), `Assumed_Sound_Velocity` (m/s), `wavelength` (m), `Along_Array_Length`, `Along_Array_Width`, `Across_Array_Length`, `Across_Array_Width`, `along_wavelets`, `across_wavelets`, `along_spacing`, `across_spacing`, `no_elements[4]`.
* **Beam Steering & Attitude:** `Across_Design_Steering`, `Along_Design_Steering`, `Tx_Across_Steering`, `Static_Roll`, `Static_Pitch`.
* **Interferometric Sidescan Parameters:** `Vernier_Spacing` (in wavelengths), `spacing` (m), `radius` (m).
* **Computed Directivity & Shading Buffers:**
  * `BP_angle[180 * DEG_FRACTION]`: Angular axis in degrees ($0.2^\circ$ increments).
  * `BP[4][3][180 * DEG_FRACTION]`: Directivity response indexed by `[direction][LOG_POWER | LINEAR_POWER | LINEAR_PRESSURE][angle_bin]`.
  * `Phase[180 * DEG_FRACTION]`: Wrapped interferometric phase difference ($-180^\circ \dots +180^\circ$).
  * `Along_Shading[4][1000]`: Normalized element shading weights for each of the 4 array axes.
  * `Transmit_3dB_angle`, `Receive_3dB_angle`, `Transmit_First_Null`, `Receive_First_Null`: Extracted $-3\text{ dB}$ beamwidths and first sidelobe null angles.

---

## Public Functions & Signatures

### Beam Pattern Synthesis & Solvers
* `void recalc_all_models()`
  Calls `calculate(pattern)` sequentially for `TRANSMIT_FORE_AFT`, `TRANSMIT_PORT_STBD`, `RECEIVE_FORE_AFT`, and `RECEIVE_PORT_STBD`.
* `void calculate(int pattern)`
  Determines the effective aperture length (applying $\cos(\theta_{\text{steer}})$ foreshortening for continuous line models), invokes `array_calc` (or `element_2_calc` for 2-element bathymetric sidescan), converts linear pressure into linear power and logarithmic dB (`LOG_POWER`), and calls `find_3dB_and_null()`.
* `void array_calc(int pattern, double Effective_Array_Length, double max_angle)`
  Computes the far-field acoustic response across all $180 \times 5 = 900$ angular bins using `angle_calc`.
* `float angle_calc(int pattern, double Effective_Array_Length, double spec_angle)`
  Evaluates the complex phased-array summation (for `DISCRETE` arrays with `Along_Shading` weights and `Assumed_Sound_Velocity` vs. `Sound_Velocity` phase delays) or $\sin(x)/x$ sinc directivity (for `LINE` / `CONE` apertures) at a single angle `spec_angle`.
* `void element_2_calc(int pattern, double Effective_Array_Length, double max_angle)`
  Models a 2-stave interferometric receiver element response.
* `void recalc_phase()`
  Computes the wrapped phase difference $\Delta\phi = 360^\circ \cdot d_\lambda \sin(\theta - \theta_{\text{steer}})$ across the swath and dumps the output via `print_plotfile()`.
* `void find_3dB_and_null()`
  Scans the computed `BP` curves outward from the mainlobe peak to determine `Transmit_3dB_angle`, `Receive_3dB_angle`, `Transmit_First_Null`, and `Receive_First_Null`.

### Array Design & Shading Functions
* `void calculate_element_spacing()`
  Computes `wavelength = Sound_Velocity / Frequency`, rounds `no_elements` to an even integer based on `along_wavelets` and `across_wavelets` (typically $0.5\lambda$), and updates `along_spacing` and `across_spacing`.
* `void load_shade(int dirn, int type)`
  Populates `Along_Shading[dirn][0..noelem-1]` using the requested window (`UNSHADED`, `COS_SQUARED`, `COSINE`, `LINEAR`, `INVERSE_LINEAR`, `BINOMIAL` via `bico()`, or 42-element `CHEB_20`, `CHEB_30`, `CHEB_40` Dolph-Chebyshev tables).
* `float closest_array_length(double desired_beamwidth, int pattern)`
  Iteratively steps down the array length from 200 (or 500) wavelengths in both inward and outward directions around the steered boresight until the $-3\text{ dB}$ half-beamwidth matches `desired_beamwidth / 2.0`, returning the average required physical array length in meters.

### Mathematical & File I/O Helpers
* `void print_plotfile()` / `void read_bpfile(char *name)` / `void load_in_bp_params()`
  Reads and writes `beamPatt.asciidump` and `beamPatt.params` files.
* `double factrl(int n)`, `double gammln(double xx)`, `double bico(int n, int k)`, `double factln(int n)`
  Numerical Recipes combinatorial functions used to compute Binomial array shading coefficients.

---

## How It Fits Into the OMG Architecture
`bP_stuff` powers the interactive beam-pattern design and visualization tools `plotBP` (`code/plot/plotBP.c`) and `BDplot` (`code/plot/BDplot.c`), as well as synthetic multibeam ping generation in `makeSynPing` (`code/grid/makeSynPing.c`), `synSwath` (`code/gl/SYN_global.h`), and `jGL_draw.c`.
