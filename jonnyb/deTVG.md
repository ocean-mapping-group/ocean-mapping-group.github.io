---
layout: default
title: deTVG
parent: Jonathan Beaudoin (jonnyb) Tools
nav_order: 1
tool_name: deTVG
source_path: code/jonnyb/gom_stuff/deTVG.c
category: Backscatter & Sidescan Processing (jonnyb)
input_formats: [".merged", ".merged.ss_data", ".param", ".tx_sectors", ".r4 (optional DTM or GRA file)", ".depression"]
output_formats: [".merged (updated in-place)", ".merged.ss_data (radiometrically corrected snippets)"]
related_tools: ["makess", "RTlite", "read_kmall", "SE_AnandBS", "newMergeAtt"]
---

# deTVG

## Description
`deTVG` (`code/jonnyb/gom_stuff/deTVG.c`, written by Jonathan Beaudoin and extended by Anand Hiroji and John Hughes Clarke) removes the real-time Time-Varying Gain (`simrad_TVG`), spherical spreading, absorption, and flat-seafloor ensonified-area assumptions applied inside Kongsberg Simrad multibeam echosounders (`EM122`, `EM302`, `EM710`, `EM2040`, `EM3000`, etc.) from `.merged` and `.merged.ss_data` snippet records, replacing them with physically rigorous radiometric and geometric corrections based on true seafloor slope and beam depression angles.

---

## Usage

```bash
deTVG [OPTIONS] -in <filename.merged>
```

### Examples

**1. Standard radiometric TVG removal and grazing-angle correction using a gridded `.r4` DTM:**
```bash
deTVG -use_dtm_for_grazing bay_2m.r4 -in merged/JD100/0001_line.merged
```

**2. Using Anand Hiroji's local 3x3 ($1\text{ ping}\times 1\text{ beam}$) patch grazing angle calculation with `.kmall` OWTT:**
```bash
deTVG -use_ADH_GRZ 1 1 -iskmall_use_realowtt -recalc_NormalIncid -in merged/JD100/0001_line.merged
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <filename.merged>` | Input OMG-HDCS `.merged` file (with companion `.merged.ss_data`, `.param`, and optional `.tx_sectors`). | Required |
| `-use_dtm_for_grazing <file.r4>` | Compute true 3D seabed grazing angles from an external `.r4` bathymetric DTM. | Internal across-track profile slope |
| `-use_ADH_GRZ <n_pings> <n_beams>` | Compute 3D seabed grazing angles directly from the swath mesh using $\pm\text{n\_pings}$ along-track and $\pm\text{n\_beams}$ across-track (e.g., `1 1` uses a $3\times 3 = 9$-sounding neighborhood). | Disabled |
| `-read_GRA <.ext.r4>` | Read pre-computed grazing angles from `<merged_prefix><.ext.r4>` (created by `get_GRA`). | Disabled |
| `-refract` | Incorporate ray-bent beam depression angles from `<prefix>.depression` (dumped by `newMergeAtt`) when computing grazing angles. | Disabled |
| `-flat_seafloor` | Use sonar-relative angles instead of true seabed grazing angles in the pulse-length ensonified area correction. | Disabled |
| `-try_along_track_slope` | Include along-track seafloor slope in pulse-length ensonified area correction. | Disabled |
| `-no_pulse_corr` | Disable pulse-length ensonified area correction (`do_pulse_length_correction = 0`). | Enabled |
| `-try_only_pulse_correction` | Apply only the pulse-length correction. | Disabled |
| `-try_new_BTS` | Compute ensonified area at nadir using the beamwidth-limited case for `BTS` computation. | Disabled |
| `-try_new_BTS_per_beam` | Use `BTS` computed from the one-way travel time (OWTT) to the center sample for all samples in a beam. | Disabled |
| `-try_sector_tx_offsets` | Apply per-sector transmit array offsets from `.tx_sectors` (`EM2040`, `EM710`, `EM302`, `EM122`). | Disabled |
| `-try_sector_pulse_lengths` | Use per-sector effective pulse lengths from `.tx_sectors`. | Disabled |
| `-iskmall_use_realowtt` | Use exact one-way travel time recorded in `.kmall` files rather than reconstructing range from sample numbers. | Disabled |
| `-recalc_NormalIncid` | Recalculate range to normal incidence using true OWTT (`.kmall`) rather than sample-number range. | Disabled |
| `-recalc_range_to_normal_incidence` | Recalculate normal-incidence range from beam range measurements. | Disabled |
| `-digitizer_sample_shift <N>` | Shift digitizer sample index by `N` samples to compensate for water-column offset at nadir. | `0` |
| `-AUV_draft` | Ignore `Zloc + WLZ` transducer draft calculation for AUV datasets. | Disabled |
| `-BSx10` | Multiply backscatter values by 10 (when `-rescale_BSN` was not used in `RTlite`). | Disabled |
| `-debug` / `-debug_ensonification` | Print detailed TVG, grazing angle, and ensonified area diagnostics. | Disabled |
