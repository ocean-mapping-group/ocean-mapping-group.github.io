---
layout: default
title: Troubleshooting & Diagnostics Reference
parent: Processing Workflows & Guides
nav_order: 5
category: workflows
related_tools:
- read_kmall
- RTlite
- moveOverWCinfo
- stripNav
- appendNav
- mergeNav
- newMergeAtt
- mergeAtt
- mergeHeave
- mergeTide
- deTVG
- makess
- make_blank
- weigh_grid
- mos2
- swathed
- jview
---

# Troubleshooting & Diagnostics Reference

This guide serves both as a quick diagnostic handbook for graduate students and as a structured symptom-cause-resolution knowledge base for the LocalAI multibeam processing assistant.

---

## 1. Unraveling & File Unpacking Diagnostics (`read_kmall` & `RTlite`)

| Symptom / Error Message | Root Cause | Diagnostic Check | Resolution |
| :--- | :--- | :--- | :--- |
| `NOT Dynamically Recognizing the Echosounder Type : <ID> EXITING Early` in `read_kmall` | Input file is not from one of the 6 supported SIS 5 `.kmall` models (`2040`, `2042`, `2045`, `712`, `304`, `124`), or a legacy `.all` file was passed to `read_kmall`. | Check file extension and header datagram (`#IIP` vs `IIP`). | If the file is `.all` or `.wcd` (EM120, EM122, EM300, EM302, EM710, EM1002, EM3000, EM3002), use `RTlite -simrad` (or `bunravel`). If it is a new Kongsberg `.kmall` model, add its `echoSounderID` to `read_kmall.c` (`lines 910–940`). |
| Outer or deep beams are missing in `.merged` immediately after running `read_kmall` or `RTlite` | The `-maxdepth <m>` flag was set shallower than the actual seafloor depth, or left at a shallow script default. | Run `dumpMerged <line>.merged` or inspect the command line used to run `read_kmall`. | Re-run `read_kmall` / `RTlite` with `-maxdepth <m>` set comfortably deeper than the deepest sounding in the survey area (e.g., `-maxdepth 4000.0`). |
| Water column viewer or `newMergeAtt -wc` complains that water column offsets are zero, even though `.kmwcd` was unpacked | `.kmall` was unpacked *after* `.kmwcd` without saving the `.kmwcd` `.merged` file and running `moveOverWCinfo`, or `.kmwcd` was unpacked *second* (overwriting bathymetry). | Check file size of `<line>.watercol` and check if `moveOverWCinfo` was executed. | 1. Unpack `.kmwcd` first (`read_kmall -d merged/$line -kmall raw/$line.kmwcd`).<br>2. `mv merged/$line.merged merged/justWC_$line.merged`<br>3. Unpack `.kmall` second (`read_kmall -d merged/$line -kmall raw/$line.kmall`).<br>4. Run `moveOverWCinfo merged/$line.merged merged/justWC_$line.merged`. |
| `Can't open ... .nav` when running `stripNav` or `mergeNav` on `.kmall` data | `read_kmall` outputs `.nav_1`, `.nav_2`, `.nav_3` rather than `.nav`. | Run `ls -lh merged/<line>.nav*`. | Copy the active navigation stream (usually `.nav_1`) to `.nav`:<br>`cp merged/<line>.nav_1 merged/<line>.nav` |
| `Can't open ... .orientation` or 0 attitude records merged in `newMergeAtt` / `mergeAtt` | `read_kmall` outputs `.orientation_1`, `.net_att_1`, and `.net_att_2` based on `#SKM` `sensorInputFormat`. | Run `ls -lh merged/<line>.*att* merged/<line>.orientation*` to see which file has non-zero size. | Copy the non-empty attitude file to `.orientation`:<br>• KM Binary (`format=1`): `cp merged/$line.net_att_2 merged/$line.orientation`<br>• POS M/V (`format=7`): `cp merged/$line.net_att_1 merged/$line.orientation`<br>• EM3000 (`format=2`): `cp merged/$line.orientation_1 merged/$line.orientation` |

---

## 2. Navigation, Lever Arms, Attitude & Ray-Tracing Artifacts

| Symptom / Error Message | Root Cause | Diagnostic Check | Resolution |
| :--- | :--- | :--- | :--- |
| Parallel survey lines show a systematic horizontal shift (along-track or across-track offset of features between opposite headings) | GPS-to-RP or Transducer-to-RP lever arms were not applied, or were applied with the wrong sign convention (`-dx`/`-dy` vs `-param`). | Inspect `merged/<line>.param` (`Nav_X`, `Nav_Y`, `Trans1_X`, `Trans1_Y`) and check how `mergeNav` was called. | Always run `mergeNav -ahead 60.0 -param merged/<line>.param merged/<line>.merged decnav/all_dec.nav`. Do not mix `-param` with manual `-dx`/`-dy` unless intentionally overriding `.param`. |
| First/last few seconds of each survey line have zeroed (`0.0, 0.0`) positions or dropped pings after `mergeNav` | Single-line `.nav` started slightly after the first ping or ended slightly before the last ping, and `mergeNav` could not bracket the ping timestamp. | Check terminal output of `mergeNav` for `Could not bracket time`. | Append all decimated line navigation files into a single master file (`appendNav decnav/all_dec.nav decnav/$line.nav`) and run `mergeNav` against `decnav/all_dec.nav` with `-ahead 60.0`. |
| Navigation timestamps in `.all` or `.nav` are off by ~19.7 years (1024 weeks) | GPS 1024-week rollover bug in the receiver firmware during acquisition. | Inspect `year` and `day` in `.nav` vs `.merged`. | Pass `-addGPSrolloverwraps 1` to `mergeNav` (or `-rollover` to `bunravel`). |
| Swath cross-sections show a persistent "smile" (outer beams curving upward) or "frown" (outer beams curving downward) | Sound velocity profile (`.sv_filtered`) or surface sound speed does not match the true water column, or ray-tracing was not re-run. | Inspect `merged/<line>.sv_filtered` and check whether `newMergeAtt -redoref -recalc_beamVec` was executed. | Replace or edit `merged/<line>.sv_filtered` with a representative CTD/XBT cast (`depth_m  sound_speed_m_s`) and re-run:<br>`newMergeAtt -redoref -recalc_beamVec merged/<line>` |
| Outer beams show periodic "wobble" or ribbing synchronized with vessel roll in rough seas | Roll bias, pitch bias, or motion sensor latency, or attitude was never re-merged with `newMergeAtt`. | Check `.param` `Ref_Roll` / `Ref_Pitch` and verify `merged/<line>.orientation` is non-empty. | Ensure the high-rate `.net_att_2` or `.net_att_1` file was copied to `.orientation` and re-run `newMergeAtt -redoref -recalc_beamVec merged/<line>`. |
| Adjacent survey lines run at different hours have a vertical step offset (0.5 m to 5+ m) | Tide correction was not applied, or `mergeTide` was run with the wrong sign convention (adding tide instead of subtracting tide from positive depths). | Compare overlapping lines against the tide curve in `.tide`. | Run `mergeTide -flip -in merged/<line>.merged -tide area.tide` (use `-flip` when tide heights are positive above datum and `.merged` depths are positive downward). |

---

## 3. Gridding (`make_blank`, `weigh_grid`, `tor4`) & Mosaicking (`makess`, `mos2`) Diagnostics

| Symptom / Error Message | Root Cause | Diagnostic Check | Resolution |
| :--- | :--- | :--- | :--- |
| `make_blank` creates an 8-bit header instead of float, or ignores `-Dx` / `-Dy` when using `-boundsof` | Flag ordering error: in `make_blank.c`, `-boundsof` consumes **all remaining command-line arguments** as input files, and `-bounds` / `-boundsof` immediately computes grid dimensions using whatever `-Dx`, `-Dy`, and `-float` flags were parsed *prior* to it. | Check the exact argument order passed to `make_blank`. | Always place `<out_prefix> -float -Dx <m> -Dy <m>` **before** `-bounds` or `-boundsof`:<br>`make_blank area -float -Dx 5.0 -Dy 5.0 -boundsof -nav merged/*.merged` |
| `weigh_grid` exits with `Input file is not a floating point grid` | `make_blank` was run without `-float` (defaulting to an 8-bit `data_type = 1` template), or `-float` was placed after `-boundsof`. | Check header with `jview` or `head -c 64 area.blank`. | Re-create `area.blank` with `make_blank area -float ...`, delete the old `area.r4` and `area.weight`, and re-run `tor4`. |
| Bathymetric grid `.r4` has gaps ("holidays") between adjacent beams or ping lines even where coverage exists | Smoothing factor `-smf` is too small for the chosen grid cell size `-Dx`/`-Dy` at that water depth. | Compare beam footprint spacing against `-Dx` and `-smf`. | Increase the smoothing factor in `tor4` (e.g., `tor4 area 2.5 merged/*.merged` or `3.0`) or increase grid cell size `-Dx`/`-Dy`. |
| `mos2` fails with `Cannot open .merged` or `Cannot open .nav` when mosaicking `ss/*.ss` | `.ss` files were moved into `ss/`, so `mos2` looks for `ss/<line>.merged` and `ss/<line>.nav` instead of `merged/<line>.merged`. | Check directory paths of `.ss` vs `.merged`. | Pass `-swap_dirs ss/ merged/` to `mos2`:<br>`mos2 -in area.mos -ran area.ran -smf 1.5 -weight_by_dist -swap_dirs ss/ merged/ -files ss/*.ss` |
| `mos2` exits with `Input file is not an 8-bit image` | `area.blank` was created with `-float` instead of `-8bit -prime 255`. | Check how `make_blank` was invoked for the mosaic. | Create a separate blank file for the mosaic using:<br>`make_blank area_mos -8bit -prime 255 -bounds <W> <E> <S> <N> -Dx 1.0 -Dy 1.0` |
| Sidescan mosaic `.mos` has dark/bright stripes at the Kongsberg central-beam to snippet transition (on `.all` data) | Kongsberg real-time empirical TVG law changes slope between near-nadir beams and outer beams. | Inspect across-track backscatter profile in `ss/<line>.ss`. | Run `deTVG -in merged/<line>.merged` and re-run `makess -use_deTVG -pixel <m> merged/<line>`. |
| `r4to8bit` produces an all-white or all-black `.8bit` image | The `-range <min_depth> <max_depth>` values do not match the actual depth range (or sign) in the `.r4` grid. | Run `r4to8bit -in area.r4` without `-range` first to auto-scale between `zmin` and `zmax`, or inspect depth bounds in `jview area.r4`. | Pass `-range <shallow_m> <deep_m>` matching positive water depths in `.r4` (e.g., `r4to8bit -in area.r4 -range 50.0 400.0`). |

---

## Diagnostic Decision Tree for the LocalAI Assistant

When a user reports an issue with their multibeam processing, follow this 4-stage diagnostic sequence:

1. **Stage 1 — Verify Raw Format & Unpacker Match:**
   - Is the raw data `.kmall`/`.kmwcd` (SIS 5) or `.all`/`.wcd` (SIS 3/4)?
   - Confirm `read_kmall -kmall` is used for `.kmall`/`.kmwcd` and `RTlite -simrad` is used for `.all`/`.wcd`.
   - If water column data (`.kmwcd`/`.wcd`) exists, confirm it was unpacked **before** the bathymetry file and linked via `moveOverWCinfo`.
2. **Stage 2 — Verify Active Companion Files in `merged/`:**
   - Check that `<line>.merged`, `<line>.param`, `<line>.nav`, `<line>.orientation`, and `<line>.sv_filtered` all exist and have non-zero byte sizes (`ls -lh merged/<line>.*`).
   - For `.kmall` lines, verify `.nav_1` was copied to `.nav` and the populated attitude stream (`.net_att_2`, `.net_att_1`, or `.orientation_1`) was copied to `.orientation`.
3. **Stage 3 — Verify Geometric & Environmental Corrections:**
   - Confirm `stripNav` $\rightarrow$ `appendNav` $\rightarrow$ `mergeNav -ahead 60.0 -param <line>.param` completed without `Could not bracket time` warnings.
   - Confirm `newMergeAtt -redoref -recalc_beamVec` ran after `mergeNav`.
   - Check if tidal corrections (`mergeTide -flip`) or delayed heave (`mergeHeave`) are needed.
4. **Stage 4 — Verify Grid / Mosaic Template Type (`make_blank`):**
   - Bathymetric gridding (`weigh_grid` / `tor4`) requires a **32-bit float** template (`make_blank <name> -float ...`).
   - Sidescan mosaicking (`mos2` / `tomos`) requires an **8-bit** template primed to `255` (`make_blank <name> -8bit -prime 255 ...`) and `-swap_dirs ss/ merged/` when `.ss` files are stored in `ss/`.
