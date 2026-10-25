---
layout: default
title: SE_omgIOwin
parent: SwathEd (SE) Tools
nav_order: 28
tool_name: SE_omgIOwin
source_path: code/SE/SE_omgIOwin.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged", ".param", ".ref_coeffs", ".orientation", ".orientation_1", ".orientation_2", ".net_att_1", ".net_att_2", ".sectors", ".extra", ".ss_data", ".ss_data.convert", ".16_data", ".32_data", ".fl_data", ".ph_data", ".ph16_data", ".watercol", ".WC_Phase1", ".vert_prof", ".waveform", ".sonar_settings", ".flag_bk"]
output_formats: [".merged (updated in-place)", ".SE_changes", "cleaned_files.list"]
related_tools: ["swathed", "SE_mainwin", "SE_global", "SE_sswindow", "dumpFlags"]
---

# `SE_omgIOwin.c` — Multibeam File I/O, 100-Ping Buffer Management & Detrending Engine

## Overview & Purpose
`SE_omgIOwin.c` (with header `SE_omgIOwin.h`, authored by John E. Hughes Clarke, July 1999) is the primary data I/O and buffer-management engine of `swathed`. It handles opening survey lines and all associated auxiliary files (`start_file`), reading 100-ping (`SE_NO_SWATHS`) blocks of multibeam bathymetry, navigation, attitude, and backscatter into memory (`prime_array`), computing and applying least-squares planar slope detrending (`calc_Detrend_Slopes`, `apply_Detrend_Slopes`), loading external flag backup files (`load_flags`, `guess_flag_offset`), and writing modified beam status flags back to disk (`dump_array`).

It supports three underlying swath file formats (`file_type`):
- `XOMG_HDCS` (`3`): Standard OMG `.merged` HDCS format (versions 1–4, covering Kongsberg EM series, Reson SeaBat, R2Sonic, Teledyne MB1, WASSP, SeaBeam, Atlas, ISIS Submetrix, Knudsen, EdgeTech, and Optech Laser).
- `USL_HDCS` (`4`): Legacy UNB/CARIS USL HDCS directory format (`ObservedDepths` and `ObservedDepthsTmIdx`).
- `OMG_GL` (`5`): GLORIA long-range sidescan records (`gloria_rec`, 1,024 samples per swath).

---

## Key Functions

| Function | Signature | Description |
|---|---|---|
| `start_file` | `void start_file(int file_no)` | Opens `inname[file_no]` (attempting `"r+"` read-write first and gracefully falling back to `"r"` read-only with `got_read_only = 1`), loads `<prefix>.param`, `<line>.ref_coeffs`, and opens all available companion files (`.orientation`, `.sectors`, `.extra`, `.ss_data`, `.16_data`, `.32_data`, `.fl_data`, `.ph_data`, `.ph16_data`, `.watercol`, `.WC_Phase1`, `.vert_prof`, `.waveform`, `.sonar_settings`). Configures default swath coverage (`coverage`), depth grid interval (`line_interval`), and ping interval (`ping_int`) for the specific `summary.toolType`. |
| `prime_array` | `void prime_array(int *recnum)` | Reads `SE_NO_SWATHS` (`100`) consecutive profiles starting at `*recnum` into the global `box[][]`, `offsets[][]`, `sigs[][]`, `cleansigs[][]`, `across_sigs[][]`, `along_sigs[][]`, `detect_mode[][]`, `qfactors[][]`, `geo_cen[][]`, and `geo_pos[][][]` arrays. Applies depth gates (`Shoallest_Allowed`, `Deepest_Allowed`, and `follow_terrain`), optional refraction corrections (`use_proc_flag == 1`), long-period heave (`use_proc_flag == 2`), and pre-filters (`prefluff_flag`, `premedian_flag`, `predetrench`, `using_powell`, `auto_flag`, `preweekley`). |
| `dump_array` | `void dump_array(int *recnum)` | Writes any modified sounding rejection flags (`some_flagged > 0`) in the current 100-ping block back to `infile` (unless `got_read_only` is set). Updates bit 1 (`0x02`, manual edit flag) of `beams[j].status` while respecting bit 6 (`0x40`, Kongsberg interpolated beam), and optionally logs every changed sounding (`lat`, `lon`, `depth`, `beam`, `+1/-1`) to `<prefix>.SE_changes` when `list_changes` is active. |
| `load_full_orientation` | `void load_full_orientation(int *recnum)` | Searches the high-rate `.orientation` file (`OMG_HDCS_att_time_search`) at each ping's exact timestamp and populates `roll[]`, `pitch[]`, and `heave[]`. |
| `calc_Detrend_Slopes` / `apply_Detrend_Slopes` | `void calc_Detrend_Slopes()` / `void apply_Detrend_Slopes()` | Computes linear least-squares along-track slope (`Detrend_Along_Slope`, meters per ping) and across-track slope (`Detrend_Across_Slope`) across the 100-ping block, and rotates `unrot_box[][]` and `unrot_offsets[][]` into `rot_box[][]` and `rot_offsets[][]`. |
| `update_for_detrend` | `int update_for_detrend(int refresh)` | Synchronizes flag polarity between `box[][]`, `unrot_box[][]`, and `rot_box[][]`, recalculates detrend slopes, swaps between `load_Detrend_bathy()` and `load_Regular_bathy()`, and triggers `setup_for_next80()`. |
| `load_up_strip` | `void load_up_strip()` | Builds the $900 \times 80$ pixel sidescan waterfall strip image (`strip_image`, `strip_data`) for `sub_window[15]` in [`SE_sswindow.c`](SE_sswindow.md) by calling `make_ss()` (or decoding ISIS Submetrix / SeaBeam 2000 traces) across the loaded swaths. |
| `load_flags` / `guess_flag_offset` | `void load_flags()` / `void guess_flag_offset()` | Reads external 8-bit flag backup files (`<prefix>.flag_bk` created by [`dumpFlags`](../omg/dumpFlags.md) or HIPS export), determines any ping index offset (`HIPS_ping_offset`), and applies the saved rejection flags to `box[][]`. |
| `write_file_list` | `void write_file_list()` | Writes the list of active/cleaned survey line filenames (`done_status[i]`) to disk. |

---

## Bitwise Beam Status Flag Convention (`dump_array`)

In May 2019, `prime_array()` and `dump_array()` were updated from the legacy monolithic `status = 22` convention (`16 + 4 + 2`) to a structured 8-bit `beams[j].status` bitmask:
- **Bit 1 (`0x02 = 2`):** Manually flagged in `swathed` (`beams[j].status |= (1 << 1)` when `box[j][i] < 0.0`; cleared via `&= ~(1 << 1)` when unflagged).
- **Bit 2 (`0x04 = 4`) & Bit 4 (`0x10 = 16`):** Historical components of legacy status `22`.
- **Bit 5 (`0x20 = 32`):** Flagged by automated filter.
- **Bit 6 (`0x40 = 64`):** Interpolated beam from Kongsberg real-time bottom detector (treated as flagged on load, and protected from being unflagged during `dump_array`).

---

## Integration within `swathed`
- **Line Stepping & Geographic Sub-Windows:** Called whenever the user opens a line, steps forward/backward by 80 pings (`SE_NO_SWATHS - 20`), jumps to a record number (`-jump_to_recnum`), or selects a line from [`SE_GEOwindows.c`](SE_GEOwindows.md) or [`SE_LineListwin.c`](SE_LineListwin.md).
- **Batch Utilities:** Linked directly by [`newAutoRejectSoundings`](newAutoRejectSoundings.md) to batch-load 100-ping blocks (`prime_array`), run `check_data()`, and save flags (`dump_array`) without an X11 display.
