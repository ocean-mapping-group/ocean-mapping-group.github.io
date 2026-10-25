---
layout: default
title: USL_HDCS_hack
parent: Core Shared Libraries (subr)
module_name: USL_HDCS_hack
source_path: code/subr/USL_HDCS_hack.c
header_path: code/subr/USL_HDCS_hack.h
category: Sonar Format Parsers & Binary I/O
related_tools:
  - readHDCS
  - deHump
  - deRefract
  - DelayEditor
  - swathed
---

# USL_HDCS_hack: CARIS HIPS (Universal Systems Ltd.) Observed & Processed HDCS Reader/Writer

## Overview & Purpose
`USL_HDCS_hack` (`USL_HDCS_hack.c` / `USL_HDCS_hack.h`) is an interoperability library written by John E. Hughes Clarke in May 1997 at the request of the Canadian Hydrographic Service (CHS). While OMG's internal `.merged` format (`OMG_HDCS_jversion`) diverged from the original Nickerson/USL HDCS specification to pack imagery and multi-sensor extensions into a single file, CARIS HIPS (Universal Systems Ltd.) stores multibeam survey lines across separate directory-structured files (`ObservedDepths`, `ProcessedDepths`, and `TmIndex` block-indexed files).

`USL_HDCS_hack` enables OMG command-line and interactive tools (such as `deHump`, `deRefract`, `readHDCS`, and `DelayEditor`) to directly read and overwrite CARIS HIPS **Version 2 Observed Depth** (`ObservedDepths`) and **Version 3 Processed Depth** (`ProcessedDepths`) files using their companion `TmIndex` byte-offset index files.

---

## Key Data Structures & Constants

### Summary Header Structures
* **`USL_HDCS_proc_summary_header` (`USL_HDCS_PROC_SUMMARY_HEADER_SIZE = 96`)**: Version 3 Processed Depth summary header (`sensorNumber = 0`, `subFileID = 1`, `fileVersion = 3`), storing profile/depth counts, time/position scales, and geographic/depth bounds in nanoradians and millimeters.
* **`USL_HDCS_obs_summary_header` (`USL_HDCS_OBS_SUMMARY_HEADER_SIZE = 60`)**: Version 2 Observed Depth summary header (`sensorNumber = 4`, `subFileID = 1`, `fileVersion = 2`), storing `numProfiles`, `numDepths`, `timeScale`, `refTime`, `minTime`, `maxTime`, `minObsDepth`, and `maxObsDepth`.
* **`USL_HDCS_proc_index_summary_header` (`52` bytes)** & **`USL_HDCS_obs_index_summary` (`24` bytes)**: Summary headers for the companion `TmIndex` index files (`subFileID = 3`), specifying `noBlocks`.

### Profile & Beam Structures
```c
/* Version 2 Observed Profile Header (20 bytes) */
typedef struct USL_HDCS_obs_profile_header {
    short status;
    short padding;
    short numDepths;
    short startingBeamNumber;
    int   timeOffset;
    int   vesselPitch;
    int   vesselRoll;
} USL_HDCS_obs_profile_header;

/* Version 2 Observed Beam Record (16 bytes) */
typedef struct USL_HDCS_obs_beam {
    short status;
    short timeOffset;
    int   observedDepth;  /* Depth in mm */
    int   acrossTrack;    /* Across-track offset in mm */
    int   alongTrack;     /* Along-track offset in mm */
} USL_HDCS_obs_beam;

/* Version 3 Processed Profile Header (40 bytes) */
typedef struct USL_HDCS_proc_profile_header {
    short status;
    short padding;
    short numDepths;
    short startingBeamNumber;
    int   timeOffset;
    int   vesselLatOffset;
    int   vesselLongOffset;
    int   tide;
    int   minLat, maxLat, minLon, maxLon;
} USL_HDCS_proc_profile_header;

/* Version 3 Processed Beam Record (16 bytes) */
typedef struct USL_HDCS_proc_beam {
    short status;
    short timeOffset;
    int   processedDepth; /* Tidally reduced depth in mm */
    int   latOffset;      /* Latitude offset wrt profile */
    int   longOffset;     /* Longitude offset wrt profile */
} USL_HDCS_proc_beam;
```

### Block Index Structures (`USL_HDCS_index_block` & `TmIndex`)
```c
typedef struct USL_HDCS_index_block {
    int noRecordsInBlock;
    int minTime;
    int maxTime;
} USL_HDCS_index_block;

typedef struct TmIndex {
    int timeOffset;
    int byteOffset;
} TmIndex;
```

---

## Public Functions & Signatures

### `int USL_HDCS_offset(FILE *file, unsigned int record)`
Resolves the exact byte offset in `ObservedDepths` for ping `record` by parsing the CARIS HIPS `TmIndex` file (`file`):
1. Reads the 24-byte `USL_HDCS_obs_index_summary` to obtain `noBlocks`.
2. Loops through all `noBlocks` descriptors (`USL_HDCS_index_block`, 12 bytes each) to sum `totrecs`.
3. Computes `whichblock = record / 512` and `whichrecord = record % 512`.
4. Seeks to the target 512-record block and reads the 8-byte `TmIndex` entry, returning `Irecord.byteOffset` (or `-1` if `record` is out of range).

### `int USL_HDCS_read_summary(FILE *file, USL_HDCS_obs_summary_header *usl_summary)`
Rewinds `file` (`ObservedDepths`) to byte 0 and reads the 60-byte `USL_HDCS_obs_summary_header`. Returns `0`.

### `int USL_HDCS_read_profile(FILE *odfile, FILE *odifile, unsigned int recnum, USL_HDCS_obs_profile_header *usl_profile)`
Looks up the byte offset of ping `recnum` via `USL_HDCS_offset(odifile, recnum)`, seeks to that offset in `odfile`, and reads the 20-byte `USL_HDCS_obs_profile_header`.

### `int USL_HDCS_get_raw_beams(FILE *odfile, FILE *odifile, int recnum, int *no_beams, USL_HDCS_obs_beam *usl_beams)`
Reads the `USL_HDCS_obs_profile_header` for ping `recnum` to determine `*no_beams = usl_profile.numDepths`, then sequentially reads `*no_beams` 16-byte `USL_HDCS_obs_beam` structures into `usl_beams`. Returns `1` on success, `0` if `recnum` is invalid.

### `int USL_HDCS_put_raw_beams(FILE *odfile, FILE *odifile, int recnum, int no_beams, USL_HDCS_obs_beam *usl_beams)`
Seeks directly to `USL_HDCS_offset(odifile, recnum) + USL_HDCS_OBS_PROFILE_HEADER_SIZE` in `odfile` and overwrites `no_beams` 16-byte `USL_HDCS_obs_beam` records in place. Returns `1` on success.

---

## How It Fits Into the OMG Architecture
`USL_HDCS_hack` bridges OMG refraction and artifact-removal algorithms with CARIS HIPS survey directories:
* **`readHDCS` (`code/omg/readHDCS.c`):** Converts CARIS HIPS `ObservedDepths` / `ProcessedDepths` lines into OMG `.merged` format.
* **`deRefract` & `deHump` (`code/omg/deRefract.c`, `code/omg/deHump.c`):** Allows hydrographers to apply OMG sound-velocity refraction corrections directly to CARIS HIPS `ObservedDepths` files via `USL_HDCS_get_raw_beams` and `USL_HDCS_put_raw_beams`.
