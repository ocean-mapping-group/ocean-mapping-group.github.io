---
layout: default
title: OMG Tools
nav_order: 11
has_children: true
---

# Core Multibeam & Backscatter Processing (`omg`)

The `omg` directory is the central suite of command-line processing programs in the Ocean Mapping Group software tree. These tools operate directly on **OMG-HDCS** swath bathymetry files (`.merged`, v1–v4), water-column archives (`.watercol`), transmit sector logs (`.sectors`), runtime parameter logs (`.param`), and GLORIA sidescan files (`.ss`).

---

## 1. Inspection, Indexing & Format Utilities

* [`readOMG`](readOMG.md) & [`readHDCS`](readHDCS.md) — Inspect and dump OMG-HDCS summary headers, ping profile headers, and per-beam records.
* [`EMlist`](EMlist.md) — Summarizes Kongsberg runtime settings, depth modes, pulse lengths, and ping counts across `.merged` files.
* [`getBounds`](getBounds.md) — Computes `.global_bounds` and `.100_ping_bounds` spatial/temporal index files for fast querying in `jview`, `weigh_grid`, and `mos2`.
* [`inArea`](inArea.md) — Filters a list of `.merged` swath files to those intersecting a target `JHC_header` mapsheet or bounding box.
* [`dumpXYZ`](dumpXYZ.md), [`dumpReflect`](dumpReflect.md), [`dumpFlags`](dumpFlags.md) — Exports georeferenced `(X, Y, Z)` soundings, beam reflectivity, or edit status flags to ASCII/binary streams.
* [`packOMG`](packOMG.md), [`rationalOMG`](rationalOMG.md), [`splitOMG`](splitOMG.md), [`stackOMG`](stackOMG.md), [`reSortOMG`](reSortOMG.md), [`replaceOMG`](replaceOMG.md), [`diffOMG`](diffOMG.md) — File-level packing, version upgrading, splitting, concatenation, chronological sorting, and differencing utilities.

---

## 2. Navigation, Attitude, Lever-Arm & Refraction Re-Integration

* [`mergeAtt`](mergeAtt.md) & [`newMergeAtt`](newMergeAtt.md) — Merges high-rate attitude (`.att`, `.net_att`) and navigation (`.nav`) into `.merged` swath files with time-latency and lever-arm compensation.
* [`repoint`](repoint.md) — Full 3D non-orthogonal cone re-pointing and ray-tracing engine (`j_non_ortho_cones` + `DCM_rthand`) for recalculating beam positions after attitude, mounting-angle, or sound-speed edits.
* [`deRefract`](deRefract.md) & [`RefractEd`](RefractEd.md) — Interactive and batch refraction correction tools for removing sound-velocity profile (SVP) "smiles" and "frowns".
* [`applyOffset`](applyOffset.md), [`unrollOMG`](unrollOMG.md), [`getRollResidual`](getRollResidual.md), [`makeAziTwirl`](makeAziTwirl.md) — Static mounting offset application, roll-bias estimation, and azimuth patch-test analysis.
* [`reSync`](reSync.md), [`smoothTime`](smoothTime.md), [`smthTimeOMG`](smthTimeOMG.md), [`showPingRate`](showPingRate.md), [`useCMG`](useCMG.md), [`guessSwellHeave`](guessSwellHeave.md), [`deHump`](deHump.md), [`deJaw`](deJaw.md) — Clock drift synchronization, timestamp smoothing, course-made-good heading calculation, and motion artifact removal.

---

## 3. Automated Cleaning, Flagging & Target Detection

* [`autorejectSoundings`](autorejectSoundings.md), [`rejectSounding`](rejectSounding.md), [`rejectJIM`](rejectJIM.md), [`preFlag`](preFlag.md), [`deOuterMistrack`](deOuterMistrack.md), [`LPFbeams`](LPFbeams.md) — Automated outlier rejection, outer-beam mistrack cleaning, and along/across-track low-pass filtering.
* [`edReject`](edReject.md), [`edsumm`](edsumm.md), [`checkSD`](checkSD.md) — Summarizes and modifies beam edit flags and standard deviation metrics.
* [`targethunt`](targethunt.md) ([`targethunt.h`](targethunt.h.md)) — Automated hydrographic target and shoal/wreck detector.

---

## 4. Backscatter Calibration, Sidescan Generation & Beam Patterns

* [`makess`](makess.md) & [`updateSSheader`](updateSSheader.md) — Converts `.merged` multibeam snippet/seabed image time series into 1024-sample GLORIA `.ss` sidescan lines (plus `.grz` grazing angle and `.altr` along-track offset files for [`mos2`](../newmos/mos2.md)).
* [`deTVG`](deTVG.md), [`correctBS`](correctBS.md), [`removeAngular`](removeAngular.md), [`understand_KM_BS`](understand_KM_BS.md), [`parse_Bscorr`](parse_Bscorr.md) ([`parse_Bscorr.h`](parse_Bscorr.h.md)) — Reverses manufacturer Time-Varying Gain (TVG), applies radiometric and grazing-angle backscatter corrections, and parses Kongsberg `BScorr.txt` calibration tables.
* [`getBeamPattern`](getBeamPattern.md), [`newGetBP`](newGetBP.md), [`get8101BeamPattern`](get8101BeamPattern.md), [`getSnippetBP`](getSnippetBP.md), [`getSnippetVariance`](getSnippetVariance.md) — Extracts empirical transmit/receive beam directivity patterns from seafloor backscatter.
* [`applySectBP`](applySectBP.md), [`multiMode2Calib`](multiMode2Calib.md), [`filterBP`](filterBP.md), [`smthBP`](smthBP.md), [`stackBP`](stackBP.md), [`traceBP`](traceBP.md), [`diff_MS_bp`](diff_MS_bp.md), [`hackSectors`](hackSectors.md) — Multi-sector beam pattern calibration, smoothing, stacking, and application tools.
* [`getAngularResponse`](getAngularResponse.md), [`getGraz`](getGraz.md), [`get_GRA`](get_GRA.md), [`get_ADH_SRA`](get_ADH_SRA.md), [`classSel`](classSel.md) — Computes true seafloor grazing angles (using a reference `.r4` DTM) and extracts angular response curves.

---

## 5. Water Column Processing

* [`makeWC`](makeWC.md) — Processes and projects multibeam `.watercol` acoustic water-column fans, extracts gas flares/plumes, and generates water-column curtains.
* [`compress_OMG_watercolumn`](compress_OMG_watercolumn.md) & [`moveOverWCinfo`](moveOverWCinfo.md) — Compresses binary `.watercol` files and transfers water-column byte offsets between `.merged` headers.
