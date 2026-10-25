---
layout: default
title: M3_read
parent: Core Shared Libraries (subr)
module_name: M3_read
source_path: code/subr/M3_read.c
header_path: code/subr/M3_read.h
category: Sonar Format Parsers & Binary I/O
related_tools:
  - M3imb2omg
---

# M3_read: Kongsberg Mesotech M3 Multibeam (.imb / .pmb / .paq) Parser

## Overview & Purpose
`M3_read` (`M3_read.c` / `M3_read.h`, ~1,300 lines) is a binary parser and processing library for Kongsberg Mesotech M3 imaging and profiling multibeam sonar data files. Written by John E. Hughes Clarke in May 2013 and updated through October 2024, the module decodes raw M3 data streams containing:

* **`.imb` (`0x2000` / `0x2003`):** Beamformed In-Phase and Quadrature ($I/Q$) complex water-column image packets (32-bit float $I/Q$ pairs as well as newer 8-bit magnitude `.imb` records).
* **`.pmb` (`0x1008`):** Profiling Multibeam bathymetric detection packets across firmware versions 6, 7, 8, 9, and 10 (including 512-beam M3-HF configurations).
* **`.paq` (`0x2001`):** Retained phase and amplitude snippet window packets associated with profiling detections.
* **OMG M3 Index Files:** Fast random-access index records (`OMG_M3_Index_Record`) to accelerate interactive browsing and conversion of multi-gigabyte `.imb` files.

---

## Key Data Structures & Constants

### Framing Structures (`M3_Packet_Header` & `M3_Packet_Footer`)
```c
#define M3_PACKET_HEADER_SIZE 56
typedef struct {
    unsigned short sync[4];               /* 4x 0x8000 sync words */
    unsigned short data_type;             /* e.g. 0x1008 (PMB), 0x2000 (IMB), 0x2001 (PAQ), 0x2003 (8-bit IMB) */
    unsigned short reserved_field;
    unsigned int   forty_reserved_bytes[10];
    unsigned int   packet_body_size;
} M3_Packet_Header;

#define M3_PACKET_FOOTER_SIZE 44
typedef struct {
    unsigned int packet_body_size;
    unsigned int forty_reserved_bytes[10];
} M3_Packet_Footer;
```

### Imaging Multibeam Structures (`M3_Data_Header`, `M3_Sample`, `M3_Data_Body`)
* **`M3_Data_Header` (`M3_DATA_HEADER_SIZE = 8512`)**: Stores full ping metadata for `.imb` records, including `dwVersion`, `dwSonarID`, `dwTimeSec`, `dwTimeMillisec`, `fVelocitySound`, `nNumSamples`, `fNearRange`, `fFarRange`, `fSWST`, `fSWL`, `nNumBeams`, `fBeamList[1024]`, `dwSonarFreq`, `dwPulseLength`, `TVGParameters` (`M3_TVG_Params`), attitude (`fCompassHeading`, `fPitch`, `fRoll`, `fDepth`), lever-arm offsets, rotator offsets (`M3_Rotator_Offsets[3]`), and lat/lon.
* **`M3_Sample`**: Holds per-beam, per-sample acoustic values:
  ```c
  typedef struct {
      float I, Q;
      float Amp10dB, Phase16bit;
      float Mag, Phase;
      unsigned char Mag8[4];
      unsigned char Phase8;
  } M3_Sample;
  ```
* **`M3_Data_Body`**: Dynamically allocated 2D array (`num_beams * num_samples`) of `M3_Sample` elements (`beamformedIQ`).

### Profiling & Retained Snippet Structures (`M3_PMB_Data_Header`, `M3_PMB_Data_Body`)
* **`M3_PMB_Data_Header` (`M3_PMB_DATA_HEADER_SIZE = 776`)**: Supports PMB versions 6 through 10, including real-time sound speed arrays (`sRealTimeSoundSpeed[4]`), GPS quality parameters (`sGPSQualityParams[3]`), heave (`fHeave`), altitude (`fAltitude`), and `M3_PAQ_Data_Retained retained_data[512]`.
* **`M3_PMB_Solution` & `M3_PMB_Data_Trace`**: Stores up to 10 bottom-detection solutions per beam (`fProfileSampleNo`, `fBeamAngleOffset`, `shAmp10dB`, `byQualityFactor`, `byDetectionInfo`, `wDetWinLenSamples`).

### Fast Seek Index (`OMG_M3_Index_Record`)
```c
#define OMG_M3_INDEX_RECLEN 24
typedef struct {
    int recno_in_file;
    int ping_no;
    double d_1970time;
    double byte_offset;
} OMG_M3_Index_Record;
```

---

## Public Functions & Signatures

### Packet Header & Footer Parsing
* `int parse_M3_Packet_Header(M3_Packet_Header *ph, FILE *infile)`
  Reads 56 bytes, verifies the four `0x8000` little-endian sync words (advancing 1 byte on sync loss), and extracts `data_type` and `packet_body_size`.
* `int parse_M3_Packet_Footer(M3_Packet_Footer *pf, FILE *infile)`
  Reads the 44-byte trailing packet footer to verify `packet_body_size`.

### IMB Water-Column Image Loading & Processing
* `int parse_M3_Data_Header(M3_Data_Header *dh, FILE *infile)`
  Decodes the 8,512-byte little-endian `.imb` ping header.
* `int alloc_M3_Data_Body(M3_Data_Body *db, int num_beams, int num_samples)`
  Allocates or resizes the `db->beamformedIQ` sample matrix.
* `int load_M3_Data_Body(M3_Data_Body *db, M3_Data_Header *dh, FILE *infile)`
  Reads complex 32-bit float $(I, Q)$ pairs for all beams and samples (`0x2000`).
* `int load_M3_Data_Body_8bit(M3_Data_Body *db, M3_Data_Header *dh, FILE *infile)`
  Reads 8-bit compressed magnitude samples from newer `0x2003` IMB records.
* `int proc_M3_Data_Body(M3_Data_Body *db, float the_min_dB, float the_max_dB)`
  Computes magnitude $\sqrt{I^2 + Q^2}$, phase angle $\text{atan2}(Q, I)$, linear 8-bit magnitude (`Mag8[0]`), and dB-scaled 8-bit magnitude (`Mag8[1]`) clamped between `the_min_dB` and `the_max_dB`.
* `int dump_M3_Data_Body(M3_Data_Body *db, int dump_type, int samp_pack, char *string, int add_BD, M3_PMB_Data_Body *pmb_body)`
  Writes an OMG array (`JHC_header` `"OMG1"`) raster image of the beam-by-sample acoustic fan, optionally overlaying bottom detections in `BLUE`.

### PMB & PAQ Profiling Functions
* `int parse_M3_PMB_Data_Header(M3_Packet_Header *ph, M3_PMB_Data_Header *pmb_dh, FILE *infile)`
  Parses version-dependent PMB (`0x1008`) and PAQ (`0x2001`) headers (versions 6–10) and retained window descriptors.
* `int alloc_M3_PMB_Data_Body(M3_PMB_Data_Body *db, int num_beams)`
* `int load_M3_PMB_Data_Body(M3_PMB_Data_Body *pmb_db, M3_PMB_Data_Header *pmb_dh, FILE *infile)`
  Reads per-beam bathymetric solutions (`M3_PMB_Data_Trace`).
* `int load_M3_PAQ_Data_Body(M3_Data_Body *db, M3_PMB_Data_Header *pmb_dh, FILE *infile)` & `int proc_M3_PAQ_Data_Body(...)`
  Loads and normalizes sparse retained amplitude/phase windows from `.paq` records.

### Index I/O
* `int read_M3_index_record(FILE *file, OMG_M3_Index_Record *index_rec)`
* `int write_M3_index_record(FILE *file, OMG_M3_Index_Record *index_rec)`

---

## How It Fits Into the OMG Architecture
`M3_read` is the foundational parser for Kongsberg Mesotech M3 data in the OMG workflow. It is directly invoked by `code/M3/M3imb2omg.c` (`M3imb2omg`) to convert raw `.imb`, `.pmb`, and `.paq` files into standard OMG HDCS bathymetry (`.merged`, toolType `M3 = 59`) and Kongsberg-compatible `.wcd` water-column files for interactive inspection in `swathed` and 3D visualization tools.
