---
layout: default
title: Core Swath & .all Suite (omg)
parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 2
has_children: true
---

# Core Multibeam & Backscatter Processing (`omg`)

The `omg` directory is the central suite of command-line processing programs in the Ocean Mapping Group software tree. These tools operate directly on **OMG-HDCS** swath bathymetry files (`.merged`, v1–v4), water-column archives (`.watercol`), transmit sector logs (`.sectors`), runtime parameter logs (`.param`), and GLORIA sidescan files (`.ss`).

---

## 1. Inspection, Indexing & Format Utilities

* [`readOMG`](readOMG.html) & [`readHDCS`](readHDCS.html) — Inspect and dump OMG-HDCS summary headers, ping profile headers, and per-beam records.
* [`EMlist`](EMlist.html) — Summarizes Kongsberg runtime settings, depth modes, pulse lengths, and ping counts across `.merged` files.
* [`getBounds`](getBounds.html) — Computes `.global_bounds` and `.100_ping_bounds` spatial/temporal index files for fast querying in `jview`, `weigh_grid`, and `mos2`.
* [`inArea`](inArea.html) — Filters a list of `.merged` swath files to those intersecting a target `JHC_header` mapsheet or bounding box.
* [`dumpXYZ`](dumpXYZ.html), [`dumpReflect`](dumpReflect.html), [`dumpFlags`](dumpFlags.html) — Exports georeferenced `(X, Y, Z)` soundings, beam reflectivity, or edit status flags to ASCII/binary streams.
* [`packOMG`](packOMG.html), [`rationalOMG`](rationalOMG.html), [`splitOMG`](splitOMG.html), [`stackOMG`](stackOMG.html), [`reSortOMG`](reSortOMG.html), [`replaceOMG`](replaceOMG.html), [`diffOMG`](diffOMG.html) — File-level packing, version upgrading, splitting, concatenation, chronological sorting, and differencing utilities.

---

## 2. Navigation, Attitude, Lever-Arm & Refraction Re-Integration

* [`mergeAtt`](mergeAtt.html) & [`newMergeAtt`](newMergeAtt.html) — Merges high-rate attitude (`.att`, `.net_att`) and navigation (`.nav`) into `.merged` swath files with time-latency and lever-arm compensation.
* [`repoint`](repoint.html) — Full 3D non-orthogonal cone re-pointing and ray-tracing engine (`j_non_ortho_cones` + `DCM_rthand`) for recalculating beam positions after attitude, mounting-angle, or sound-speed edits.
* [`deRefract`](deRefract.html) & [`RefractEd`](RefractEd.html) — Interactive and batch refraction correction tools for removing sound-velocity profile (SVP) "smiles" and "frowns".
* [`applyOffset`](applyOffset.html), [`unrollOMG`](unrollOMG.html), [`getRollResidual`](getRollResidual.html), [`makeAziTwirl`](makeAziTwirl.html) — Static mounting offset application, roll-bias estimation, and azimuth patch-test analysis.
* [`reSync`](reSync.html), [`smoothTime`](smoothTime.html), [`smthTimeOMG`](smthTimeOMG.html), [`showPingRate`](showPingRate.html), [`useCMG`](useCMG.html), [`guessSwellHeave`](guessSwellHeave.html), [`deHump`](deHump.html), [`deJaw`](deJaw.html) — Clock drift synchronization, timestamp smoothing, course-made-good heading calculation, and motion artifact removal.

---

## 3. Automated Cleaning, Flagging & Target Detection

* [`autorejectSoundings`](autorejectSoundings.html), [`rejectSounding`](rejectSounding.html), [`rejectJIM`](rejectJIM.html), [`preFlag`](preFlag.html), [`deOuterMistrack`](deOuterMistrack.html), [`LPFbeams`](LPFbeams.html) — Automated outlier rejection, outer-beam mistrack cleaning, and along/across-track low-pass filtering.
* [`edReject`](edReject.html), [`edsumm`](edsumm.html), [`checkSD`](checkSD.html) — Summarizes and modifies beam edit flags and standard deviation metrics.
* [`targethunt`](targethunt.html) ([`targethunt.h`](targethunt.h.html)) — Automated hydrographic target and shoal/wreck detector.

---

## 4. Backscatter Calibration, Sidescan Generation & Beam Patterns

* [`makess`](makess.html) & [`updateSSheader`](updateSSheader.html) — Converts `.merged` multibeam snippet/seabed image time series into 1024-sample GLORIA `.ss` sidescan lines (plus `.grz` grazing angle and `.altr` along-track offset files for [`mos2`](../newmos/mos2.html)).
* [`deTVG`](deTVG.html), [`correctBS`](correctBS.html), [`removeAngular`](removeAngular.html), [`understand_KM_BS`](understand_KM_BS.html), [`parse_Bscorr`](parse_Bscorr.html) ([`parse_Bscorr.h`](parse_Bscorr.h.html)) — Reverses manufacturer Time-Varying Gain (TVG), applies radiometric and grazing-angle backscatter corrections, and parses Kongsberg `BScorr.txt` calibration tables.
* [`getBeamPattern`](getBeamPattern.html), [`newGetBP`](newGetBP.html), [`get8101BeamPattern`](get8101BeamPattern.html), [`getSnippetBP`](getSnippetBP.html), [`getSnippetVariance`](getSnippetVariance.html) — Extracts empirical transmit/receive beam directivity patterns from seafloor backscatter.
* [`applySectBP`](applySectBP.html), [`multiMode2Calib`](multiMode2Calib.html), [`filterBP`](filterBP.html), [`smthBP`](smthBP.html), [`stackBP`](stackBP.html), [`traceBP`](traceBP.html), [`diff_MS_bp`](diff_MS_bp.html), [`hackSectors`](hackSectors.html) — Multi-sector beam pattern calibration, smoothing, stacking, and application tools.
* [`getAngularResponse`](getAngularResponse.html), [`getGraz`](getGraz.html), [`get_GRA`](get_GRA.html), [`get_ADH_SRA`](get_ADH_SRA.html), [`classSel`](classSel.html) — Computes true seafloor grazing angles (using a reference `.r4` DTM) and extracts angular response curves.

---

## 5. Water Column Processing

* [`makeWC`](makeWC.html) — Processes and projects multibeam `.watercol` acoustic water-column fans, extracts gas flares/plumes, and generates water-column curtains.
* [`compress_OMG_watercolumn`](compress_OMG_watercolumn.html) & [`moveOverWCinfo`](moveOverWCinfo.html) — Compresses binary `.watercol` files and transfers water-column byte offsets between `.merged` headers.
