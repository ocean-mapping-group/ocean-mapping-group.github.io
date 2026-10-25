---
layout: default
title: xtf_utils
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/xtf_utils.c
category: Sonar Format Parsers & Hardware Drivers
related_tools:
- omg_xtf
- xtf2omg
- reson
- simrad_utils
- OMG_HDCS_jversion
module_name: xtf_utils
header_path: code/subr/xtf_utils.h
---

# xtf_utils

## Overview
`xtf_utils` (`xtf_utils.c` / `xtf_utils.h`) implements the **timestamp synchronization (`synchro`), base-time recovery, and OMG-HDCS summary header initialization** logic for Triton Elics eXtended Triton Format (`.xtf`) sonar files.

As explained in `xtf_utils.h`, XTF packets carry relative millisecond attitude/ping time tags (`AttitudeTimeTag`) that are not always referenced to an absolute UTC epoch, while embedded raw sonar packets (Reson 81-P, Kongsberg/Simrad EM, R2Sonic, Q-Multibeam, or sidescan) may or may not have 1PPS/UTC clock synchronization enabled. `xtf_utils` inspects the indexed `.xtf` packet stream (`XTFFileIndex` from [`omg_xtf`](omg_xtf.html)) to automatically determine the appropriate synchronization mode, establish the Unix epoch `baseTime` corresponding to `0 ms` of the relative timer, and initialize OMG-HDCS `.merged` and `.orientation` summary headers.

---

## Synchronization Modes (`synchro` Codes)

Defined in `xtf_utils.h` (with human-readable strings in `synchro_labels[0..7]`) and selectable via `-force_synch <code>` in `xtf2omg`:

| Macro | Code | Label | Synchronization Formula & Use Case |
|---|---|---|---|
| `INVALID` | `-2` | — | File contains no recognizable bathymetry or sidescan frames. |
| `XTF_SYNCHRO` | `0` | `"XTF SYNCHRO"` | **Reson 81-P without UTC input**: Uses the first XTF Bathy header timestamp (`Year/JulianDay/H:M:S.HS`) minus `(xtfBathy.AttitudeTimeTag - resonBathy.latency) / 1000.0`. Removes acquisition latency (`resonBathy.latency`). |
| `RESON_SYNCHRO` | `1` | `"RESON SYNCHRO"` | **Reson 81-P with 1PPS/UTC input**: Uses the Reson packet's accurate UTC timestamp (`Seconds + Millisecs/1000.0`) minus `xtfBathy.AttitudeTimeTag / 1000.0`. |
| `RESON_ORIENTATION_SYNCHRO` | `2` | `"RESON ORIENTATION SYNCHRO"` | **Reson 81-P with ms-since-midnight attitude tags**: Sets `baseTime` to `00:00:00.000 UTC` of the day indicated by the Reson UTC timestamp (`floor(reson_time / 86400) * 86400`). |
| `SIDESCAN_SYNCHRO` | `3` | `"SIDESCAN SYNCHRO"` | **Pure Sidescan XTF**: Uses the first `XTF_HEADER_SONAR` header timestamp minus `AttitudeTimeTag / 1000.0` (no Reson latency subtraction). |
| `SIMRAD_SYNCHRO` | `4` | `"SIMRAD SYNCHRO"` | **Simrad EM in XTF**: Uses the first XTF Bathy header UTC timestamp minus the millisecond timestamp (`raw_ms_time / 1000.0`) inside the embedded Simrad Raw Range/Angle (`0x46` / `0x66`) or Image (`0x53`) datagram. |
| `RESON_STIEGLITZ_SYNCHRO` | `5` | `"RESON STIEGLITZ SYNCHRO"` | Legacy special-case Reson synchronization mode (`abs(latency - AttitudeTimeTag) <= 100 ms`). |
| `Q_MULTIBEAM_SYNCHRO` | `6` | `"Q MULTIBEAM"` | Uses packet type `28` (`Q_MULTIBEAM`) header timestamp minus `AttitudeTimeTag / 1000.0`. |
| `R2SONIC_SYNCHRO` | `7` | `"R2SONIC SYNCHRO"` | Uses packet type `65` (`R2SONIC`) header timestamp minus `AttitudeTimeTag / 1000.0`. |

---

## Public Functions

| Function | Signature | Description |
|---|---|---|
| `get_xtf_synchro` | `int get_xtf_synchro(FILE *infile, XTFFileIndex *theIndex)` | Inspects `theIndex` and the first bathymetry/sonar packet in `infile`, compares the XTF packet header timestamp against any embedded Reson 81-P UTC timestamp (`tolerance = 0.100 s`), and returns the optimal synchronization code (`0..7` or `INVALID`). |
| `getBaseTime` | `double getBaseTime(FILE *infile, XTFFileIndex *theIndex, int synchro)` | Computes and returns the Unix epoch `baseTime` (seconds since `1-Jan-1970`) for the given `synchro` mode (`0..7`), auto-detecting little-endian vs. big-endian Simrad datagrams when `synchro == SIMRAD_SYNCHRO`. |
| `initSummary` | `void initSummary(FILE *infile, OMG_HDCS_summary_header *summary, int version, XTFFileIndex *theIndex, double baseTime, int sonar_type, int beam_count)` | Populates an `OMG_HDCS_summary_header` (`sensorNumber = 1`, `timeScale = 1000`, `refLat`, `refLong` from the first `XTFBATHHEADER`, `refTime = baseTime / 100.0`) and optionally initializes Version 4 extended profile/beam byte sizes via `OMG_HDCS_initiate_V4_summary()`. |
| `initAttitudeSummary` | `void initAttitudeSummary(OMG_HDCS_summary_attitude *att_summary, XTFFileIndex *theIndex, double baseTime, int toolType)` | Populates an `OMG_HDCS_summary_attitude` header (`sensorNumber = 2`, `fileVersion = 3`, `timeScale = 1000`, `status = 15` for RPH+heave, `refTime = baseTime / 100.0`). |

---

## Architectural Role
`xtf_utils` works directly with [`omg_xtf`](omg_xtf.html) inside the XTF conversion tools (`xtf2omg`), solving the notorious clock-drift and relative-millisecond tagging ambiguities found in multi-vendor `.xtf` survey recordings.
