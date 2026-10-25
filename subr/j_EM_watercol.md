---
layout: default
title: j_EM_watercol
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_EM_watercol.c
category: Multibeam Water-Column Processing & Visualization
related_tools:
- swathed
- RT
- RTLite
- makeWC
- M3imb2omg
- targethunt
module_name: j_EM_watercol
header_path: code/subr/j_EM_watercol.h
---

# `j_EM_watercol` — Multibeam Water-Column Data Structures, Compression, and Polar Scan-Conversion

## Overview & Purpose
The `j_EM_watercol` module (`code/subr/j_EM_watercol.c`, `code/subr/j_EM_watercol.c.bkup`, and `code/subr/j_EM_watercol.h`) defines the in-memory data structures, `.wcd` disk file layout, JPEG2000 time-angle image compression interface, and polar-to-Cartesian fan scan-conversion API for multibeam echosounder water-column data. Originally created by John Hughes Clarke in June 2005 during the first Kongsberg EM710 trials aboard CCGS *Matthew*, it was expanded by Jonathan Beaudoin in November 2009 to support Version 2 JPEG2000 (`libjasper`) compression and updated in July 2022 to handle trace lengths up to `32,768` samples per beam for high-resolution Kongsberg `.kmall`, Kongsberg M3, and Simrad EK80 systems.

> **Architectural Note:** During a refactor of the water-column subsystem, the active `.wcd` I/O and scan-conversion function implementations were consolidated into `code/subr/j_watercolumn.c` (preserving the original implementation in `j_EM_watercol.c.bkup`), while `j_EM_watercol.c` holds the shared global display and radiometric gain state variables and `j_EM_watercol.h` remains the canonical header included across the codebase.

---

## Constants, Global Controls & Data Structures (`j_EM_watercol.h`)

### 1. Array Bounds & I/O Mode Constants
- `#define J_EM_WC_MAX_WC_TRACE_LENGTH 32768`: Maximum range samples per beam trace (increased from `2048`/`8192` to `32768` in 2022).
- `#define J_EM_WC_MAX_NUM_SECTORS 20`: Maximum transmit sectors per ping.
- `#define J_EM_WC_MAX_NUM_BEAMS 512`: Maximum receive beams per ping.
- **Dual-Head & Update Modes:** `J_EM_READ_FIRST_HEAD (0)`, `J_EM_READ_SECOND_HEAD (1)`, `J_EM_WRITE_INITIAL (0)`, `J_EM_WRITE_UPDATE_ALL (1)`, `J_EM_WRITE_UPDATE_HEAD (2)`, `J_EM_WRITE_INITIAL_SECOND_HEAD (3)`.

### 2. Core Water-Column Structures
- **`j_EM_WC_tx_sector`:** Per-sector transmit metadata (`tilt_angle` in $0.01^\circ$, `center_frequency` in $10\text{ Hz}$, `sector_id`) plus extended Version 2 parameters (`focus_range`, `signal_length`, `tx_time_offset`, `mean_absorp_coeff`, `waveform_id`, `signal_bandwidth`) and interactive per-sector gain calibration offsets (`sector_gain_offset`, `sector_onoff`, `sector_gain_per_km`).
- **`j_EM_WC_Rc_timeseries`:** Single receive-beam water-column record containing `beam_pointing_angle` ($0.01^\circ$), `start_range_sample_no`, `no_samples`, `Tx_sector_no`, `beam_no`, and sample arrays `ts_ampl[32768]` ($0.5\text{ dB}$ signed bytes) and optional split-beam phase arrays `ts_phas1[32768]` / `ts_phas2[32768]`.
- **`j_EM_watercolumn`:** Master ping structure holding navigation/timing (`time_1970`, `lat`, `lon`, `heading`, `tx_tdcr_heave`, `tx_tdcr_depth`), acoustic parameters (`model_no`, `ping_count`, `serial_no`, `no_tx_sectors`, `total_no_receive_beams`, `sound_speed`, `sampling_freq`, `tvg_function_applied`, `tvg_offset`), pointers to `tx_sector` and `watercols`, and Version 2 JPEG2000 fields (`compressed_time_angle_image_size`, `compression_factor`, `compressed_time_angle_image`).
- **`j_EM_WC_dimensions`:** Precomputed polar-to-Cartesian lookup grid (`x`, `y`, `depth_upper`, `depth_lower`, `width_left`, `width_right`, `pixel_size`, `WC_Range`, `WC_Angle`) for rapid fan-image rendering.

### 3. Global Radiometric & Display State (`j_EM_watercol.c`)
- `int global_wc_offset_ampl`, `int global_wc_ampl_shift`, `int global_wc_gain_per_km`, `int global_wc_add_atten`, `float global_wc_atten_coeff`, `int global_wc_add_spreading`, `int global_wc_spreading_factor`, `int global_wc_despeckle`, `int global_wc_sidelobe_suppression`.

---

## Public Functions & Signatures

```c
int j_EM_init(j_EM_watercolumn *wc);
int j_EM_free(j_EM_watercolumn *wc);
int j_EM_init_dimensions(j_EM_WC_dimensions *wc_dim);
int j_EM_free_dimensions(j_EM_WC_dimensions *wc_dim);

int j_EM_compress(j_EM_watercolumn *wc, int compression_factor);
int j_EM_uncompress(j_EM_watercolumn *wc);

int j_EM_read_watercolumn(FILE *mergefile, FILE *datafile, int recno, j_EM_watercolumn *wc, int which_head);
int j_EM_write_watercolumn(FILE *mergefile, FILE *datafile, int recno, j_EM_watercolumn *wc, int type);

int j_EM_combine_watercolumns(j_EM_watercolumn *WHOLE_ping_WC, j_EM_WC_dimensions *WC_dimen,
                              unsigned char *wcim_c, int output_type, int wrap_8bit,
                              int custom_flag, int whether_to_wipe);
int j_EM_watercolumn_stack(j_EM_watercolumn *outwc, j_EM_watercolumn *inwc, int stack);
int j_EM_decide_WC_sonar_depth_offset(OMG_HDCS_summary_header *summary,
                                      OMG_HDCS_profile_header *profile,
                                      j_EM_watercolumn *wc, float *offset);
```

- **`.wcd` Indexed I/O (`j_EM_read_watercolumn` / `j_EM_write_watercolumn`):** Uses the fixed-stride `.wcd.merge` index file (`mergefile`, 16 bytes per ping holding file byte offsets for Head 1 and Head 2) to seek directly to variable-length ping records in the `.wcd` bulk file (`datafile`).
- **Polar-to-Cartesian Scan Conversion (`j_EM_combine_watercolumns`):** Maps polar `(beam_pointing_angle, sample_range)` traces onto a 2D Cartesian across-track vs. depth pixel grid (`wcim_c`), applying runtime TVG spreading/absorption adjustments, per-sector gain offsets, minimum-slant-range sidelobe suppression, and bilinear interpolation.

---

## How It Fits Into the OMG Architecture
`j_EM_watercol` is the backbone of all water-column visualization and target-detection workflows in OMG:
- **Interactive Swath & Water-Column Editor (`swathed`):** `SE_WaterColumn.c` and `SE_3D.c` use `j_EM_read_watercolumn()`, `j_EM_combine_watercolumns()`, and `j_EM_watercolumn_stack()` to render polar fan displays, stacked curtain views, and 3D plume curtains.
- **Real-Time & Batch Water-Column Builders (`RT`, `RTLite`, `makeWC`, `M3imb2omg`, `targethunt`):** Populate `j_EM_watercolumn` structs from raw Kongsberg, M3, or Simrad telegrams and write indexed `.wcd` / `.wcd.merge` archives.
