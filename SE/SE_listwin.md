---
layout: default
title: SE_listwin
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 26
tool_name: SE_listwin
source_path: code/SE/SE_listwin.c
category: Interactive QC & Editing (SwathEd)
input_formats:
- .merged
- .sectors
- .sonar_settings
- .watercol
output_formats:
- ping_list.data
related_tools:
- swathed
- SE_mainwin
- SE_omgIOwin
- SE_WaterColumn
---

# `SE_listwin.c` — Interactive Ping Header, Sector & Beam Listing Window

## Overview & Purpose
`SE_listwin.c` (with header `SE_listwin.h`, authored by John E. Hughes Clarke, April 1999) manages the interactive **"Beam Listing"** X11 diagnostic window (`sub_window[14]`) in `swathed`. While the main SwathEd window displays graphical profiles, `SE_listwin.c` provides a detailed numerical and metadata inspection panel for the currently highlighted ping (`in_recnum + selected_swath`).

It decodes and displays:
1. **Ping-Level Navigation & Attitude:** UTC timestamp (with optional GPS 1024-week rollover correction via `-addGPSrolloverwraps`), transducer latitude/longitude, roll, pitch, transducer pitch, heave, heading, tide, and RTK / low-pass / high-pass heave components.
2. **Sonar-Specific Runtime Settings:** Decodes runtime operational parameters for Kongsberg (EM12, EM100, EM950/1000, EM1002, EM300, EM3000/3002, EM120/122, EM302, EM710, EM2040, M3, KMALL), Reson SeaBat (9001, 81xx, 71xx, T20P via `.sonar_settings`), R2Sonic (2022/2024), Teledyne MB1, WASSP, Knudsen 320, EdgeTech 4600, ISIS Submetrix, SeaBeam 2000/2100, Atlas Hydrosweep/Fansweep, and Optech SHOALS Laser.
3. **Multi-Page Tabular Beam Listing (`NOLISTPAGES = 3`):** Displays per-beam geometric, radiometric, snippet/water-column, and KMALL calibration values with interactive scrolling and left/right page switching.
4. **ASCII Ping & Sector Dumping (`write_list`, `plot_sectors`):** Exports complete ping metadata, transmit sector tables, and beam-by-beam geometry to `ping_list.data` or `stdout`.

---

## Key Functions

| Function | Signature | Description |
|---|---|---|
| `view_list` | `void view_list()` | Creates and maps the $600 \times 550$ px `"Beam Listing"` X11 window (`sub_window[14]`) in the lower-right corner of the display if not already open (`got_a_listwindow`). |
| `plot_list` | `void plot_list(int rec_no)` | Reads `OMG_HDCS_profile_header`, `.sectors`, `.sonar_settings`, and raw beams for ping `rec_no`, renders the upper metadata header block, draws the cyan/blue beam-range progress bar, and populates the tabular beam list for the active `beamlist_page` (`0`, `1`, or `2`) and vertical scroll slice (`view_number`, `noperview`). |
| `write_list` | `void write_list(int rec_no)` | Writes a formatted ASCII report for ping `rec_no` to `ping_list.data`, including transducer lat/lon, roll/pitch/heave/heading, Unix & YMD timestamps, all transmit sector parameters (`tilt_angle`, `focus_range`, `signal_length`, `tx_time_offset`, `center_frequency`, `mean_absorp_coeff`, `waveform_id`, `sector_id`, `signal_bandwidth`), and a per-beam table (`beam`, `across`, `along`, `depth`, `samp#`, `TWTTsec`, `SLR`, `RxStr`, `sc#`, `TxStr`, `shotdelay`, `cenFQ`). |
| `plot_sectors` | `void plot_sectors(int rec_no)` | Reads `.sectors` via `load_tx_sectors()` for ping `rec_no` and prints all transmit sector fields to `stdout`. |
| `decipher_EM_filter_bits` | `int decipher_EM_filter_bits(OMG_HDCS_summary_header *summary, OMG_HDCS_profile_header *profile)` | Decodes Kongsberg `profile->filter_ID` and `profile->filter_ID2` bitmasks (Spike Filter, Slope Filter, Sector Tracking, Range Gates, Aeration Filter, Interference Filter, Penetration Filter, Detect Mode, Phase Ramp, TVG type, and `tx_along_tilt_decideg`) to `stdout`. |
| `invert_use_status` | `void invert_use_status()` | Toggles `use_status[i] = !use_status[i]` across all `no_in` loaded survey lines. |

---

## Multi-Page Beam Table Layout (`beamlist_page`)

In `sub_window[14]`, port beams (`i < numDepths / 2`) are shaded **RED** and starboard beams are shaded **GREEN**. Users can scroll vertically through beam subsets (`view_number * noperview`) and switch between three column pages using the Left/Right arrow keys:

| Page (`beamlist_page`) | Displayed Columns in `sub_window[14]` |
|---|---|
| **Page `0` (Default Geometry & Snippets)** | `Beam`, `Depth` (m), `Across` (m), `Along` (m), `Range` (one-way slant range in m, or `1Zconf`/`2nd Z`/`2Zconf` for Optech Laser), `Refl.` (`reflectivity`), `Corr.` (`calibratedBackscatter` or `Q_factor`), `P./A.` (Phase in cyan vs. Amplitude in yellow based on `Q_factor > 127`), `flag.` (`box_status` code in cyan if valid or blue if flagged), `nosam.` (`no_samples`), `cent.` (`centre_no`), `offset` (snippet byte offset in `.ss_data`). |
| **Page `1` (Acoustics, Steering & Water Column)** | `Beam`, `TWTT` (`other_range`), `TxSt.` (`Tx_steer` in deg), `RxSt.` (`Rc_steer` in deg), `Azi.` (`beam_heading_angle`), `Dep.` (`beam_depress_angle`), `Sect` (`TxSector` or `freq`), `P./A.`, `flag.`, `noWCsam.` (water-column samples from `WHOLE_ping_WC`), `WCcent.`, `WCoffset` (`profile.watercol_offset`). (For Optech Laser: `#PMT`, `#GAPD`, `#IR`, `#RAMAN`, `D-timestamp`). |
| **Page `2` (KMALL Radiometric & Angle Calibration)** | `Beam`, `TWTT` ($\mu\text{s}$), `+Corr` (`twtt_correction` in $\mu\text{s}$), `Alpha` (`meanAbsCoeff_dBPerkm`), `ref1` (`reflectivity1_dB`), `ref2` (`reflectivity2_dB`), `RxSens` (`receiverSensitivityApplied_dB`), `SLapp` (`sourceLevelApplied_dB`), `BScal` (`BScalibration_dB`), `TVG+` (`TVG_dB`), `Rxang` (`beamAngleReRx_deg`), `AngCorr` (`beamAngleCorrection_deg`). |

---

## Integration within `swathed`
- **Invocation:** Opened from the `swathed` toolbox/menu via `view_list()`, which sets `got_a_listwindow = 1`.
- **Automatic Synchronization:** Whenever the user steps to a new 100-ping block (`setup_for_next80()` in [`SE_mainwin.c`](SE_mainwin.html)) or selects a different ping in the main editor, `plot_list(in_recnum + selected_swath)` automatically refreshes `sub_window[14]`.
- **Event Handling:** Mouse clicks and keyboard events in `sub_window[14]` (scrolling `view_number`, cycling `beamlist_page`, or dumping `ping_list.data` via `write_list`) are dispatched by [`SE_event_loop.c`](SE_event_loop.html).
