---
layout: default
title: OMGmod_SEA_phasetoangle
parent: Core Shared Libraries (subr)
module_name: OMGmod_SEA_phasetoangle
source_path: code/subr/OMGmod_SEA_phasetoangle.c
header_path: code/subr/OMGmod_SEA_phasetoangle.h
category: Interferometric Phase-to-Angle Conversion
related_tools:
  - swathed
  - j_SUB2K
---

# OMGmod_SEA_phasetoangle: Submetrix / SEA SwathPlus Multi-Stave Vernier Phase-to-Angle Resolver

## Overview & Purpose
`OMGmod_SEA_phasetoangle` (`OMGmod_SEA_phasetoangle.c` / `OMGmod_SEA_phasetoangle.h`) is an interferometric bathymetric sidescan phase-unwrapping library adapted by John Hughes Clarke in January 2008 from the Systems Engineering & Assessment Ltd (SEA) / Submetrix C++ `CPhaseToAngle` class (originally written in 1998–2007) to compile in pure C within `swathed` and `j_SUB2K`.

Bathymetric sidescan transducers (such as the Submetrix ISIS 100/2000 and SEA SwathPlus Transmit/Receive Electronic Modules, or TEMs) measure the acoustic phase difference between four parallel receive staves ($A, B, C, D$) separated by multiple wavelengths:
* $d_{AB} = 3.0\lambda$
* $d_{BC} = 3.5\lambda$
* $d_{CD} = 2.0\lambda$
* $d_{AC} = 6.5\lambda$
* $d_{AD} = 8.5\lambda$

Because stave spacings greater than $0.5\lambda$ introduce $2\pi$ phase-wrapping ambiguities (e.g., a $2\lambda$ spacing wraps every $\arcsin(1/2) = 30^\circ$), `OMGmod_SEA_phasetoangle` uses a sequential Vernier difference chain—starting from the synthetic $0.5\lambda$ difference $(BC - AB)$ and stepping through progressively wider stave pairs $(AB - CD) \rightarrow CD \rightarrow BC \rightarrow AC \rightarrow AD$—to resolve an unambiguous, high-precision elevation angle $\theta$ and an internal phase consistency error metric.

---

## Key Data Structures, Constants & Macros

### Sample Structure (`cSample`)
```c
typedef struct {
    unsigned char  m_phaseb_a;   /* Phase difference B - A (encoded 0..255 = 0..360 deg) */
    unsigned char  m_phasec_a;   /* Phase difference C - A (encoded 0..255 = 0..360 deg) */
    unsigned char  m_phased_a;   /* Phase difference D - A (encoded 0..255 = 0..360 deg) */
    int            m_samp_stat;  /* Sample status bitmask (e.g. SAMP_KILL = 0x20) */
    float          m_quality;    /* Computed quality factor */
    unsigned short m_amp;        /* Acoustic sample amplitude */
    double         m_angle_s;    /* Resolved sine of elevation angle (-1.0 to +1.0) */
    double         m_angle_deg;  /* Resolved elevation angle in degrees */
} cSample;
```

### Stave Spacing & Scaling Constants
```c
const double STAVE_AB = 3.0;
const double STAVE_BC = 3.5;
const double STAVE_CD = 2.0;
const double STAVE_AC = 6.5;
const double STAVE_AD = 8.5;

const double ANGLE_ENCODE = 32767.0; /* Integer scale factor for sin(angle) == 1.0 */
const int    LUTSZ        = 256;     /* Lookup table size for 8-bit encoded phase */
```

### Phase Unwrapping Macro (`unam`)
```c
#define unam(a, b, r) ((a > b) ? \
  (b + r * ((int)(0.5 + (float)(a - b) / (float)r))) : \
  (b - r * ((int)(0.5 + (float)(b - a) / (float)r))))
```
Shifts an ambiguous fine-stave angle estimate `b` by an integer multiple of its ambiguity sector width `r` so that it aligns with the coarser unambiguous angle estimate `a`.

---

## Public Functions & Signatures

### Initialization & Teardown
* `void Contructor_CPhaseToAngle()`
  Initializes the ambiguity sector widths (`ENC_BC_AB`, `ENC_AB_CD`, `ENC_CD`, `ENC_BC`, `ENC_AC`, `ENC_AD`), allocates six 256-entry integer lookup tables (`m_lut1` through `m_lut6`), and pre-populates each table with the scaled sine-of-angle values for phase values $0 \dots 255$.
* `void Destructor_CPhaseToAngle()`
  Frees the six lookup tables (`m_lut1` .. `m_lut6`).
* `void setFreqKhz(int aFreq)`
  Sets `m_freqKhz` (nominal operating frequency in kHz).

### Phase-to-Angle & Inverse Conversion
* `void SEA_phaseToAngle(int txer__m_noSamps, cSample *samp, const int number, const double sos)`
  *(Declared as `phaseToAngle` in header, implemented as `SEA_phaseToAngle` in `.c`)*
  Iterates over `number` samples in the `samp` array, calls `atomic_pta` on each sample's 8-bit stave phase differences, scales `m_angle_s` by the ratio of actual sound speed `sos` to the nominal transducer design sound speed (`NOMINAL_SOS = 1490.0` m/s), and computes `m_angle_deg = asin(m_angle_s) * 180.0 / M_PI`.
* `int atomic_pta(const unsigned char in_ba, const unsigned char in_ca, const unsigned char in_da, double *ang, double *ang_err)`
  Performs a single-sample Vernier phase unwrapping:
  1. Computes inter-stave 8-bit modulo-256 phase differences `bc = in_ca - in_ba` and `cd = in_da - in_ca`.
  2. Resolves coarse unambiguous angle from `m_lut1[(unsigned char)(bc - ab)]` ($0.5\lambda$ effective spacing).
  3. Sequentially refines the angle through `m_lut2[(unsigned char)(ab - cd)]`, `m_lut3[cd]`, `m_lut4[bc]`, `m_lut5[ac]`, and `m_lut6[ad]` using the `unam()` macro.
  4. Computes the final sine of elevation angle `*ang` as a stave-length-weighted mean of the last three spacings (`STAVE_AD`, `STAVE_AC`, `STAVE_BC`) and calculates the RMS disagreement `*ang_err` across those three decodes.
  5. **Returns:** `1` if the decoded angle is within valid bounds (and passes the confidence filter if `m_filter_on` is enabled), or `0` on rejection.
* `void AngleToPhase(cSample samp, unsigned char *ab, unsigned char *ac, unsigned char *ad)`
  Inverse function that converts a known `samp.m_angle_s` back into modulo-256 8-bit phase differences `*ab`, `*ac`, and `*ad`.

---

## How It Fits Into the OMG Architecture
`OMGmod_SEA_phasetoangle` is directly used by `code/subr/j_SUB2K.c` (`j_SUB2K`) and interactive phase-angle curve diagnostics in `swathed` to reprocess raw Submetrix ISIS / SEA SwathPlus interferometric stave phases into elevation angles and diagnose phase-to-angle kinks in dual-ping TEM hardware.
