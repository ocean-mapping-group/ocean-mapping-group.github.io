---
layout: default
title: beam_foot
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/beam_foot.c
category: Acoustic Array & Beam Pattern Modeling
related_tools:
- makeFoot
- downHill
- plotBP
- synSwath
- swathed
module_name: beam_foot
header_path: code/subr/beam_foot.h
---

# beam_foot: Multibeam Swath Geometry & Beam Footprint Specification I/O

## Overview & Purpose
`beam_foot` (`beam_foot.c` / `beam_foot.h`) defines the `BeamFoot` data structure and ASCII configuration file parser/writer used to describe the nominal angular geometry, beam spacing mode, multi-ping/multi-sector transmit offsets, and per-beam across-track and along-track beamwidths of a multibeam echosounder. Written by John Hughes Clarke in September 1996, it supports both single-sector (or multi-ping interleaved) sonars and modern multi-sector yaw/pitch-stabilized multibeams (up to 20 sectors and 1,440 beams).

---

## Key Constants & Data Structures

### Beam Spacing Mode Constants

```c
#define SG_EQUIANGULAR      1   /* Equiangular beam spacing */
#define SG_EQUIDISTANT     -1   /* Equidistant across-track beam spacing */
#define SG_BOOM             0   /* Vertical boom sweep system (e.g., ROSS Sweep) */
#define SG_MULTISECTOR_EA   2   /* Multi-sector equiangular mode */
#define SG_MULTISECTOR_EDBS -2  /* Multi-sector equidistant beam spacing */
```

### `BeamFoot` Structure

```c
typedef struct {
    char  *toolType;                   /* Sonar model name string */
    char  *operatingMode;              /* Operating mode description string */
    float  shot_interval;              /* Ping repetition interval (seconds) */
    int    spacing_type;               /* 1: equiangular, -1: equidistant, 0: boom */
    int    nobeams;                    /* Total beams (0 indicates new multi-sector format) */
    int    nopings;                    /* Number of pings per swath cycle */
    int    interleave;                 /* Interleaved ping flag */
    float  ping_offset[14];            /* Along-track/pitch offset per ping */
    float  beamangle[1440];            /* Depression/launch angle per beam (degrees) */
    float  beamwidth[1440];            /* Across-track 3dB beamwidth per beam (degrees) */
    float  beamheight[1440];           /* Along-track 3dB beamwidth per beam (degrees) */
    float  offset_dirn[1440];          /* Azimuthal/steering direction offset per beam */

    /* Multi-sector specification (used when nobeams == 0 in file) */
    int    nosectors;                  /* Number of transmit sectors (up to 20) */
    int    sector_nobeams[20];         /* Number of beams in each sector */
    float  sector_Tx_shift[20];        /* Transmit along-track tilt/shift per sector */
    float  sector_port_angle[20];      /* Port angular boundary of sector */
    float  sector_stbd_angle[20];      /* Starboard angular boundary of sector */
    float  sector_beamangle[20][1440]; /* Launch angle per sector and beam */
    float  sector_beamwidth[20][1440]; /* Across-track beamwidth per sector and beam */
    float  sector_beamheight[20][1440];/* Along-track beamwidth per sector and beam */
} BeamFoot;
```

---

## Public Functions & Signatures

### `void load_BF_characteristics(char *name, BeamFoot *bf)`
Reads a beam footprint specification file from path `name` into `*bf`.
* **Parameters:**
  * `name`: Path to the ASCII beam footprint specification file.
  * `bf`: Pointer to the `BeamFoot` structure to populate.
* **File Format & Parsing Logic:**
  1. Reads two newline-terminated header lines into dynamically allocated strings `bf->toolType` and `bf->operatingMode`.
  2. Reads `bf->shot_interval` (`float`), `bf->spacing_type` (`int`), and `bf->nobeams` (`int`).
  3. **Multi-Sector Branch (`bf->nobeams == 0`):** Reads `bf->nosectors` and sets `bf->nopings = 1`. For each sector `j`, reads `sector_nobeams[j]`, `sector_Tx_shift[j]`, `sector_port_angle[j]`, and `sector_stbd_angle[j]`, followed by `sector_nobeams[j]` lines of `(beam_index, sector_beamangle[j][i], sector_beamwidth[j][i], sector_beamheight[j][i])`.
  4. **Single-Sector / Multi-Ping Branch (`bf->nobeams > 0`):** Reads `bf->nopings`, sets `bf->nosectors = 1`, reads `nopings` pairs of `(ping_index, ping_offset[j])`, and then reads `nobeams` lines of `(beam_index, beamangle[i], beamwidth[i], beamheight[i], offset_dirn[i])`.

### `void dump_BF_characteristics(char *name, BeamFoot *bf)`
Writes a `BeamFoot` structure `*bf` out to an ASCII specification file at path `name` using the exact symmetric format expected by `load_BF_characteristics` (automatically branching on `bf->nobeams == 0` for multi-sector vs. single-sector output).

---

## How It Fits Into the OMG Architecture
`beam_foot` provides the geometric beam footprint models used across OMG simulation, plotting, and bottom-detection analysis tools:
* **`makeFoot` & `downHill` (`code/plot/makeFoot.c`, `code/plot/downHill.c`):** Generates and visualizes projected 3D beam footprints on sloped seafloors.
* **`plotBP` (`code/plot/plotBP.c`):** Synthesizes theoretical beam footprint files directly from `bP_stuff` array models and exports them via `dump_BF_characteristics`.
* **`synSwath` (`code/gl/SYN_global.h`) & `swathed` (`code/SE/bdi_funcs.c`):** Loads `BeamFoot` models via `load_BF_characteristics` to simulate multibeam swath coverage and evaluate bottom-detection footprints.
