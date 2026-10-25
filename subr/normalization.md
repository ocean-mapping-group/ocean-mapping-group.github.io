---
layout: default
title: normalization
parent: Core Shared Libraries (subr)
module_name: normalization
source_path: code/subr/normalization.c
header_path: code/subr/normalization.h
category: Backscatter Calibration & Residual Beam Pattern (RBP) Extraction
related_tools:
  - newGetBP
  - applySectBP
  - get_ADH_SRA
  - correctBS
---

# `normalization` — 4D Multibeam Backscatter Normalization & Residual Beam Pattern (RBP) Library

## Overview & Purpose in the OMG Architecture

`normalization` (`code/subr/normalization.c`, `code/subr/normalization.h`), developed by Anand Hiroji (ADH, 2015–2018) building upon earlier beam-pattern structures (`Beam_Pattern`), implements a comprehensive statistical framework for extracting **Across-Track and Along-Track Residual Beam Patterns (RBP)** from multi-sector, dual-swath, yaw/pitch-steered multibeam echosounders.

Modern multi-sector multibeam sonars (such as Kongsberg EM302, EM710, and EM2040) steer transmit sectors in along-track pitch (`ATBSA`) while vessel roll modulates the relationship between seafloor Grazing Angle (`GRA`) and Sonar-Relative Angle (`SRA`). To separate true seafloor angular backscatter response (`GRA`) from transducer/sector transmit-receive beam patterns (`SRA`, `ATBSA`, and `Sector`), `normalization` allocates a **4D statistical accumulation array (`SRBP_Array_4D`)** indexed by `[Sector][ATBSA][GRA][SRA]`. Using GNU Scientific Library (`GSL`) weighted polynomial regressions, Rayleigh/Kalman/median outlier filtering, sub-function detrending, cross-GRA sub-function stacking, and inter-sector offset adjustment, it extracts calibrated across-track and along-track residual beam pattern tables with full propagated standard deviation (`STDV`) tracking.

---

## Key Data Structures (`code/subr/normalization.h`)

### `Beam_Pattern` & `Beam_Pattern_ADH`
- `Beam_Pattern`: Legacy 1D beam-pattern accumulator (`double sum[180]`, `count[180]`), initialized via `init_bp()`.
- `Beam_Pattern_ADH`: Single cell of the 4D `[Sector][ATBSA][GRA][SRA]` array, storing `sum`, `sum_squar`, dynamic sample buffer `OMG_Buffer_double linear_value1` (`omg_buffer.h`), `average`, `average_stdv`, `modified_average`, `modified_average_stdv`, `modified_average_weight`, `intensity_variation`, `intensity_variation_stdv`, `intensity_variation_stacked_stdv`, `mean_intensity_variation`, `count`, `effective_count`, and `weight`.

### `RBP_flags_ADH`
Control flags governing the statistical extraction and filtering pipeline:
- `data_average_use_rayleigh_distribution`, `data_average_stdv_limit`, `no_defined_sectors`, `reference_SRA_for_stacking`, `write_stats`, `reference_sector`, `master_reference_SRA`, `master_reference_sector`, `do_polynomial_fit`, `polynomial_fit_dof`, `polynomial_fit_range_from_CPA`, `get_STDVs`, `do_Kalman`, `do_Median_filter`, `do_basic_filtering`, `along_nadir_array_index`, `along_start_range`, `do_not_split_central_sector_for_RBP_stacking`.

### `RBP_ADH_stats`, `RBP_ADH_stats_along`, `RBP_ADH_Kalman` & `RBP_Sector_details`
- `RBP_ADH_stats`: Per-`[Sector][SRA]` across-track stacking offsets, propagated standard deviations (`stacking_propagated_stdv`, `mean_int_variation_propagated_stdv_rel`), average GRA response (`average_GRA_response`), and final reference-adjusted RBP (`Final_mean_intensity_variation`).
- `RBP_ADH_stats_along`: Per-`[Sector][ATBSA][GRA]` along-track RBP statistics (`modified_average_of_all_SRAs`, `mean_int_variation_along_track`).
- `RBP_ADH_Kalman`: 1D recursive Kalman filter state (`Kalman_Gain`, `Kalman_Estimate`, `Kalman_Estimate_Error`).
- `RBP_Sector_details`: Per-sector angular bounds (`lowest_VRA`, `highest_VRA`, `is_port_central_stbd`).

### `SRBP_Array_4D`
Master 4D container holding dimensions (`no_sectors`, `no_ATBSA`, `no_GRA`, `no_SRA`), dynamic 4D pointers (`Beam_Pattern_ADH ****SRBP_stat`, `RBP_ADH_Kalman ****SRBP_Kalman`), 3D summary arrays (`RBP_ADH_stats ***Across_track_stats`, `RBP_ADH_stats_along ***Along_track_stats`), `Ship_motion_stat_ADH`, `RBP_Sector_details *sector_details`, and diagnostic output file handles.

### `SRA_ADH_struc` & `SRA_ADH_struc_for_profile`
Stores computed Sonar-Relative Angles (`Across_float`, `Across_int`, `Along_float`, `Along_int`, `VRA_float`, `VRA_int`) for a single beam or an entire 800-beam ping profile.

---

## Public Functions & Signatures

### Memory Allocation & Deallocation
- `int init_bp(Beam_Pattern *bp)`
- `int allocate_SRBP_4D_array(SRBP_Array_4D *Array_4D)` / `int free_SRBP_4D_array(SRBP_Array_4D *Array_4D)`
- `int allocate_SRBP_sector_detail_memory(SRBP_Array_4D *Array_4D)` / `int free_SRBP_sector_detail_memory(SRBP_Array_4D *Array_4D)`
- `int allocate_Kalman_filter_array(SRBP_Array_4D *Array_4D)` / `int free_Kalman_filter_array(SRBP_Array_4D *Array_4D)`
- `int allocate_Across_track_stats_array(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int allocate_Along_track_stats_array(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`

### Across-Track RBP Extraction Pipeline
- `int remove_outlier_intensities(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int find_middle_sectors(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int compute_sub_functions(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int detrend_sub_functions(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int get_the_reference_SRA_for_stacking(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int stack_RBP_sub_functions(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int compute_average_of_stacked_sub_functions(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int estimate_RBP_functions(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int remove_the_sector_specific_RBP(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int compute_average_GRA_response(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int compute_offsets_between_sectors(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int remove_the_swath_specific_RBP(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int shift_RBP_to_master_reference_SRA(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D)`
- `int write_final_across_track_RBP(RBP_flags_ADH *RBP_flags, SRBP_Array_4D *Array_4D, OMG_HDCS_tx_sector *define_sector_to_mode)`

### Along-Track RBP Extraction & Statistical Helpers
- `int remove_across_track_RBP_and_propagate_error(...)`
- `int Average_intensities_from_all_SRAs(...)`, `int compute_along_track_RBP_sub_functions(...)`, `int compute_along_track_RBP_master_functions(...)`, `int compute_Average_along_track_RBP_master_functions(...)`
- `int write_along_track_RBP_master_functions(...)`, `int write_Modeled_along_track_RBP(...)`, `int write_line_motion_data_along_RBP(...)`
- `int get_SRA(...)` & `int get_SRA_from_geometry(char *file_name, int profile_number_ADH, int beam_number_ADH, SRA_ADH_struc *SRA)`
- `int polynomialfit(int number_of_SRAs, int dof, double *SRA, double *mean_inten, double *coefficients, double *wei, int use_weight)` (via GSL `gsl_multifit_wlinear`)
- `int get_linear_regression(...)` (via GSL `gsl_fit_linear`), `elem_type quick_select(elem_type arr[], int n)`, `filter_and_give_me_Rayleigh_average(...)`, `do_Kalman_filter_and_give_me_absolute_stdv_and_average(...)`.

---

## How It Fits Into the OMG Architecture

`normalization` is the core computational library behind `code/omg/newGetBP`, `code/omg/applySectBP`, and `code/omg/get_ADH_SRA`, enabling sector-by-sector radiometric calibration of multi-sector multibeam backscatter in `OMG_HDCS` datasets.
