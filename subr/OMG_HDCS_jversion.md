---
layout: default
title: OMG_HDCS_jversion
parent: Core Shared Libraries (subr)
module_name: OMG_HDCS_jversion
source_path: code/subr/OMG_HDCS_jversion.c
header_path: code/subr/OMG_HDCS_jversion.h
category: Core Swath Data Format & I/O Engine
related_tools:
  - swathed
  - jview
  - RT
  - RTLite
  - DelayEditor
  - dumpXYZ
  - unrollOMG
  - makeWC
---

# OMG_HDCS_jversion: The Core OMG Swath Bathymetry, Attitude & Imagery I/O Engine

## Overview & Purpose
`OMG_HDCS_jversion` (`OMG_HDCS_jversion.c` at ~378 KB / >11,000 lines and `OMG_HDCS_jversion.h` at ~2,058 lines) is the foundational data format and I/O library of the entire Ocean Mapping Group (OMG) software ecosystem. First created by John E. Hughes Clarke in November 1991 as an extension of the Nickerson et al. Hydrographic Data Cleaning System (HDCS) format, it evolved through four major format generations to become a universal, extensible binary container (`.merged`) for over **61 distinct acoustic and lidar swath mapping systems** (`NO_TOOLS = 61`).

### Format Evolution
* **Version 1 (1991):** Fixed-size verbose summary, profile, and beam structures with Simrad EM100/EM1000 sidescan imagery extensions.
* **Version 2 (mid-1990s):** Packed binary structures (`OMG_HDCS_packed_profile`, `OMG_HDCS_packed_beam`) reducing storage footprint for 24-hour multi-week surveys by dynamically scaling depths and across/along-track offsets into 16-bit integers.
* **Version 3 (Feb 1998):** Introduced for Kongsberg EM300 yaw stabilization (removing the Version 2 assumption that $\text{alongTrack} < \frac{1}{6}\max(\text{acrossTrack}, \text{depth})$), adding 3D beam depression/heading angles, runtime sonar parameters, and asynchronous attitude (`RPGH`) time series.
* **Version 4 (Nov 2002–2026):** Bitmask-driven self-describing records (`Profile_BitsDefining[20]` and `Beam_BitsDefining[20]`, providing 640 bit-flags each). Only the fields actually present in a given sensor are written to disk, supporting modern Kongsberg `.kmall` (`EM2040`, `EM710`, `EM122`, `EM302`), Reson 7k (`7125`, `7150`, `T20P`), R2Sonic TruePix (`2020`, `2022`, `2024`), Optech SHOALS/CHARTS airborne lidar, Teledyne MB1, WASSP, and Mesotech M3.

---

## Key Data Structures & Constants

### Configuration & Transmit Sector Structures
* **`OMG_HDCS_sonar`, `OMG_HDCS_motion_sensor`, `OMG_HDCS_pos_sensor`, `OMG_HDCS_sonar_params`**: Stores vessel installation lever arms (`Xloc`, `Yloc`, `Zloc`), angular mounting offsets (`dRoll`, `dPitch`, `dHeading`), latency (`dTime`), waterline (`WLZ`), and up to 4 sonar heads, 6 positioning sensors, and 2 IMUs across up to 100 configuration epochs (`configParameter[100]`).
* **`OMG_HDCS_tx_sector` (`OMG_HDCS_TX_SECTOR_SIZE = 24`)**: Stores per-sector transmit steering (`tilt_angle`), `focus_range`, `signal_length`, `tx_time_offset`, `center_frequency`, `mean_absorp_coeff`, `waveform_id`, `sector_id`, `signal_bandwidth`, plus `.kmall` multi-swath/multi-fan descriptors.

### Summary, Profile & Beam Structures
* **`OMG_HDCS_summary_header` (`OMG_HDCS_SUMMARY_HEADER_SIZE = 96`, V4 extra `168` bytes)**: File-level header (`fileID = "HDCS"`, `fileVersion` 1–4, `toolType` 0–60, `numProfiles`, `numDepths`, `refTime`, min/max time, lat/lon bounds in 100-nanoradian units, depth bounds in mm, and V4 bitmasks `Profile_BitsDefining[20]` and `Beam_BitsDefining[20]`).
* **`OMG_HDCS_profile_header`**: Per-ping header containing time/lat/lon offsets, vessel attitude (`vesselHeading`, `vesselHeave`, `vesselPitch`, `vesselRoll`), `tide`, `soundVelocity`, runtime acoustic settings (`tx_pulse_len`, `absorp_coeff`, `tvg_crossover`, `yaw_stab_mode`), RTK/draft corrections, 32-bit and 64-bit `.wcd` water-column pointers (`watercol_offset`, `watercol_offset_64`, `watercol_size`), Reson 7k settings offsets, and R2Sonic TruePix/FTS offsets.
* **`OMG_HDCS_beam`**: Per-beam record containing `status`, `observedDepth`, `processedDepth`, `acrossTrack`, `alongTrack`, `latOffset`, `longOffset` (in mm / nanoradians), backscatter (`reflectivity`, `calibratedBackscatter`), snippet descriptors (`no_samples`, `offset`, `centre_no`), beam geometry (`beam_depress_angle`, `beam_heading_angle`, `Tx_steer`, `Rc_steer`, `TxSector`), Optech lidar waveform metrics (`no_RAMAN`, `no_IR`, `no_GAPD`, `no_PMT`), and `.kmall` radiometric terms (`TVG_dB`, `BScalibration_dB`, `sourceLevelApplied_dB`, `receiverSensitivityApplied_dB`).
* **`OMG_rational_summary`, `OMG_rational_profile`, `OMG_rational_beam`, `OMG_attrib_beam`**: Decoded, floating-point (degrees, meters, seconds) in-memory representations for simplified application access without manual unit scaling.
* **`OMG_HDCS_summary_attitude` & `OMG_HDCS_attitude`**: Asynchronous high-rate attitude/navigation records supporting standard roll/pitch/heading/heave as well as Applanix POS MV (GRP 102) and Kongsberg Seatex (format 23) 3D velocities, angular rates, and accelerations.
* **`OMG_HDCS_bounds`**: Spatial and temporal bounding-box index structure for rapid geographic culling of survey lines.

---

## Public Functions & Signatures

### Summary & Profile I/O
* `int OMG_HDCS_read_summary(FILE *file, OMG_HDCS_summary_header *summary)`
* `int OMG_HDCS_dump_summary(FILE *file, OMG_HDCS_summary_header *summary)`
* `int OMG_HDCS_initiate_V4_summary(OMG_HDCS_summary_header *summary)`
* `int OMG_HDCS_read_profile(FILE *file, int profile_no, OMG_HDCS_profile_header *profile)`
* `int OMG_HDCS_write_profile(FILE *file, int profile_no, OMG_HDCS_profile_header *profile)`
* `int OMG_HDCS_read_V4_profile(...)` / `int OMG_HDCS_write_V4_profile(...)`
  Reads and writes file summaries and individual ping profiles across HDCS Versions 1–4, handling endian byte-swapping and bitmask-driven V4 field serialization.

### Beam & Snippet Image I/O
* `int OMG_HDCS_get_raw_beams(FILE *file, int recnum, int *no_beams, OMG_HDCS_beam *beams)`
* `int OMG_HDCS_put_raw_beams(FILE *file, int recnum, int no_beams, OMG_HDCS_beam *beams)`
* `int OMG_HDCS_get_V4_raw_beams(...)` / `int OMG_HDCS_put_V4_raw_beams(...)`
* `int OMG_HDCS_get_imagedata(FILE *file, int recnum, char *data)` / `int OMG_HDCS_put_imagedata(...)`
* `int OMG_HDCS_get_xyz_beams(FILE *file, int recnum, int *no_beams, double *xyz)`
* `int OMG_HDCS_get_xyz2_beams(FILE *file, int recnum, int *no_beams, OMG_attrib_beam *abeam)`
  Retrieves or updates per-ping beam arrays, dynamic scale factors (`choose_scaling_factor`, `AUV_choose_scaling_factor`), raw sidescan/snippet byte buffers, or fully georeferenced $(x, y, z)$ soundings (applying tide, RTK, heave, and lever-arm corrections controlled by global flags such as `use_tide_corr_flag`, `use_rawrtk_corr_flag`, and `use_lever_arm_flag`).

### High-Level "Rational" Interface
* `void OMG_get_rational_summary(FILE *file, OMG_rational_summary *ratsum)`
* `void OMG_get_rational_profile(FILE *file, int profnum, OMG_rational_profile *ratprof)`
* `void OMG_get_rational_beams(FILE *file, int profnum, int *no_beams, OMG_rational_beam *ratbeams)`
* `void OMG_get_rational_beams_plus_trace(...)` / `void OMG_put_rational_beams(...)`

### Georeferencing, Asynchronous Attitude & Spatial Bounds
* `void add_beam_location(...)`, `void locate_beam(...)`, `void locate_transducer(...)`
* `int OMG_HDCS_get_interpolated_async(...)` / `int jb_OMG_HDCS_get_interpolated_async(...)`
  Binary-searches (`OMG_HDCS_att_time_search`) and linearly interpolates asynchronous `.att` files at a target ping timestamp plus time delay (`delay`).
* `int OMG_HDCS_bounds_intersect_area(...)`, `int OMG_HDCS_bounds_intersect_area_and_mask(...)`
* `int OMG_HDCS_load_params(char *filename, OMG_HDCS_sonar_params *params, int format, int printit)`

---

## How It Fits Into the OMG Architecture
Virtually every executable in the OMG codebase links against `OMG_HDCS_jversion`:
* **Format Converters (`unb2omg`, `read_kmall`, `s7k2omg`, `r2s2omg`, `M3imb2omg`):** Populate V4 bitmasks and write `.merged`, `.att`, `.ss_raw`, and `.sect` files.
* **Swath Editing & QC (`swathed`, `DelayEditor`, `deRefract`, `unrollOMG`):** Read and modify profiles and beams in-place.
* **Gridding & Export (`weigh_grid`, `dumpXYZ`, `jview`):** Query line bounds (`OMG_HDCS_bounds`) and extract georeferenced soundings via `OMG_HDCS_get_xyz_beams`.
