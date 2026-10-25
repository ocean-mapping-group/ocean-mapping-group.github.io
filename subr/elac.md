---
layout: default
title: elac
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/elac.c
category: Sonar Format Parsers & Binary I/O
related_tools:
- elac2omg
module_name: elac
header_path: code/subr/elac.h
---

# elac: Honeywell / L-3 ELAC Nautik HydroStar Bathymetry Parser

## Overview & Purpose
`elac` (`elac.c` / `elac.h`, 234 lines) is a binary file parser for Honeywell / L-3 ELAC Nautik BottomChart and SeaBeam 1180 / HydroStar Online bathymetric data files. It provides structures and little-endian binary reading routines (`get_LE_*` from `jb_endian.h`) to decode ping headers (`HYDROSTARBATHYHEADER`), individual multibeam sounding records (`HYDROSTARBEAMDATA`), and dynamically sized full-ping containers (`ELAC_BATHY`).

---

## Key Constants & Data Structures

### `HYDROSTARBATHYHEADER` (`HYDROSTARBATHYHEADER_SIZE = 72` bytes)

```c
typedef struct {
    int            iSizeofThisStruct;      /* sizeof(HYDROSTARBATHYHEADER) */
    unsigned long  ulNumberOfBeams;        /* Number of bathymetric beams in ping */
    unsigned long  ulPingNumber;           /* Sonar-supplied sequential ping number */
    unsigned long  ulFrameTimeUTCSeconds;  /* Frame time in UTC seconds since 00:00 1.1.1901 */
    unsigned long  ulFrameTimeMicroseconds;/* Microsecond fraction of UTC frame time */
    double         dFrequency;             /* Acoustic frequency in Hz (-1.0 if not supplied) */
    double         dTxPulseLength;         /* Transmit pulse length in seconds */
    double         dTxPower;               /* Transmit power in dB */
    double         dFilterBandwidth;       /* Receiver filter bandwidth in Hz */
    double         dSampleInterval;        /* Sample interval in seconds */
    double         dSwath;                 /* Swath angular width in radians */
    unsigned short unScale;                /* Compression scale factor */
    unsigned short unFanCode;              /* Fan configuration code */
} HYDROSTARBATHYHEADER;
```

### `HYDROSTARBEAMDATA` (`HYDROSTARBEAMDATA_SIZE = 57` bytes)

```c
typedef struct {
    int           iBeamNumber;   /* Absolute beam index within the swath */
    double        dTravelTime;   /* Two-way travel time in seconds */
    unsigned char ucQuality;     /* Quality flag (1..8: 1..4 = good, >4 = bad, 0 mapped to 8) */
    float         fAmplitude;    /* Backscatter echo amplitude in dB */
    double        dDelay;        /* Time offset of beam relative to ping frame time (seconds) */
    double        dBeamAngle;    /* Beam launch angle in radians (-ve = port, +ve = starboard) */
    double        dRoll;         /* Instantaneous roll angle in radians */
    double        dPitch;        /* Instantaneous pitch angle in radians */
    double        dHeave;        /* Instantaneous heave in meters */
} HYDROSTARBEAMDATA;
```

### `ELAC_BATHY` Container Structure
Combines all header fields of `HYDROSTARBATHYHEADER` with a dynamically allocated array `HYDROSTARBEAMDATA *beam`, plus in-memory housekeeping fields `bytesOnDisk` and `currentNumberOfBeams`.

---

## Public Functions & Signatures

### Low-Level Header & Beam Readers
* `void readHYDROSTARBATHYHEADER(HYDROSTARBATHYHEADER *header, FILE *infile)`
  Reads 72 bytes (`HYDROSTARBATHYHEADER_SIZE`) from `infile` and unpacks each little-endian integer, long, double, and short field into `*header`.
* `void printHYDROSTARBATHYHEADER(HYDROSTARBATHYHEADER *header)`
  Prints a human-readable dump of all `HYDROSTARBATHYHEADER` fields to `stdout`.
* `void readHYDROSTARBEAMDATA(HYDROSTARBEAMDATA *beam, FILE *infile)`
  Reads 57 unaligned packed bytes (`HYDROSTARBEAMDATA_SIZE`) from `infile` and unpacks `iBeamNumber`, `dTravelTime`, `ucQuality`, `fAmplitude`, `dDelay`, `dBeamAngle`, `dRoll`, `dPitch`, and `dHeave` into `*beam`.
* `void printHYDROSTARBEAMDATA(HYDROSTARBEAMDATA *beam)`
  Prints the contents of a single `HYDROSTARBEAMDATA` beam record to `stdout`.

### High-Level `ELAC_BATHY` Lifecycle & Ping Reader
* `void elacInit(ELAC_BATHY *bathy)`
  Initializes `bathy->beam = NULL` and `bathy->currentNumberOfBeams = 0`.
* `void readELACHEADER(ELAC_BATHY *bathy, FILE *infile)`
  Reads the 72-byte ping header directly into the header fields of an `ELAC_BATHY` struct.
* `void readELAC_BATHY(ELAC_BATHY *bathy, FILE *infile)`
  Reads a complete ping from `infile`:
  1. Calls `readELACHEADER(bathy, infile)` and increments `bathy->bytesOnDisk` by 72.
  2. Checks if `bathy->beam == NULL` or `bathy->currentNumberOfBeams != bathy->ulNumberOfBeams`; if so, dynamically resizes `bathy->beam` via `realloc()`.
  3. Loops over `0 .. bathy->ulNumberOfBeams - 1`, calling `readHYDROSTARBEAMDATA(&bathy->beam[i], infile)` and updating `bathy->bytesOnDisk`.
* `void printELAC_BATHY(ELAC_BATHY *bathy)`
  Prints the ping header followed by all `ulNumberOfBeams` beam records.
* `void freeELAC_BATHY(ELAC_BATHY *bathy)`
  Frees `bathy->beam` if non-NULL.

---

## How It Fits Into the OMG Architecture
`elac` provides the binary parsing layer for converting Honeywell / L-3 ELAC BottomChart (`toolType = 1`) and SeaBeam 1180 MkII (`toolType = 21`) HydroStar files into OMG HDCS `.merged` files. Note that ELAC's multi-ping swath sequence (where each beam carries its own `dDelay`, `dRoll`, `dPitch`, and `dHeave`) is preserved in `OMG_rational_profile` (`multiRoll`, `multiPitch`, `multiHeave`, `multiTime`).
