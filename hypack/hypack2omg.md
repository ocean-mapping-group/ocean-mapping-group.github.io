---
layout: default
title: hypack2omg
parent: Hypack Tools (hypack)
nav_order: 2
tool_name: hypack2omg
source_path: code/hypack/hypack2omg.c
category: Raw Data Unraveling & Format Conversion
input_formats: [".hsx (HYPACK HYSWEEP ASCII)"]
output_formats: [".merged", ".nav", ".tide", ".orientation", ".heading", ".param"]
related_tools: ["dehypack", "mergeNav", "mergeAtt", "newMergeAtt", "mergeTide", "swathed"]
---

# hypack2omg

## Overview

`hypack2omg` (`code/hypack/hypack2omg.c`) is the primary converter for unpacking **HYPACK HYSWEEP `.HSX`** ASCII multibeam hydrographic survey files into the **OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System)** suite of binary and parameter files.

Originally written by Jonathan Beaudoin (`jonnyb`) and updated by John Hughes Clarke in February 2014 (adding support for Kongsberg Mesotech M3 testing, Reson SeaBat 8101, and crude geometric depth/across-track reconstruction), `hypack2omg` parses both the `.HSX` header section (`TND`, `INF`, `HSP`, `DEV`, `DV2`, `OF2`, `SSI`, `MBI`, `SVC`) and the time-tagged sensor data records (`POS`, `TID`, `HCP`, `GYR`, `RMB`). It outputs up to six synchronized OMG files:
1. `<prefix>.param` — Lever-arm offsets (`X`, `Y`, `Z`), angular mounting alignments (`R`, `P`, `H`), latency (`D`), and waterline (`WLZ`) for sonar (`S1..`), MRU (`M1..`), and positioning (`P1..`) devices.
2. `<prefix>.nav` — Vessel navigation records (`jcu_nav_rec`) converted from UTM Easting/Northing to WGS84 Latitude/Longitude via `utmgeo()` (or preserved as raw coordinates with `-raw_coords`).
3. `<prefix>.tide` — Tidal elevation records (`jcu_nav_rec` with scaled tide stored in `tide_rec.azi`).
4. `<prefix>.orientation` — High-rate roll, pitch, and heave records (`OMG_HDCS_attitude`, Version 3, `status = 15`).
5. `<prefix>.heading` — Gyro heading records (`OMG_HDCS_attitude`, Version 3, `status = 4`) filtered for the user-selected gyro device ID (`-gyro`).
6. `<prefix>.merged` *(when `-do_bathy` is specified)* — OMG-HDCS Version 4 (or Version 2 for `-8101`) multibeam bathymetry profiles (`OMG_HDCS_profile_header` and `OMG_HDCS_beam` arrays).

---

## Usage

```bash
hypack2omg [OPTIONS] -gyro <device_id> -hsx <input.hsx> -omg <omg_file_prefix>
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-hsx` | `<input_name>` | **Required.** Input HYSWEEP `.HSX` ASCII file path. |
| `-omg` | `<omg_file_prefix>` | **Required.** Output prefix for generated `.merged`, `.nav`, `.tide`, `.orientation`, `.heading`, and `.param` files. |
| `-gyro` | `<device_id>` | **Required.** Integer HYSWEEP device ID (0-indexed) from which to extract `GYR` heading records (exits with error if omitted). |
| `-do_bathy` | *(none)* | Enables extraction of `RMB` (Raw Multibeam) records into `<prefix>.merged`. Without this flag, only `.nav`, `.tide`, `.orientation`, `.heading`, and `.param` are written. |
| `-force_beams` | `<num_beams>` | Forces `summary.numDepths` in the `.merged` file to `<num_beams>` (e.g., `480`) instead of using the first `RMB` record's `mbes_num_beams`. |
| `-zone` | `<zone> <n\|s>` | Specifies the UTM zone (`1`–`60`) and hemisphere (`n`/`N` or `s`/`S`) used by `utmgeo()` to invert `POS` Easting/Northing into WGS84 geographic coordinates. |
| `-raw_coords` | *(none)* | Preserves raw horizontal coordinates from `POS` records directly (`nav_rec.lat = northing`, `nav_rec.lon = easting`) without UTM inverse projection. |
| `-time_offset` | `<hours>` | Floating-point time correction in hours (e.g., `7.0`) added to `hypack_header.basetime` (`base_time = hypack_header.basetime + time_offset * 3600.0`) to shift local survey time to UTC. |
| `-tide_scale` | `<factor>` | Multiplier applied to `TID` record values (default `1.0`; e.g., `0.3048` to convert US Survey Feet / International Feet to meters). |
| `-M3_test` | *(none)* | Configures `.merged` output for Kongsberg Mesotech M3 testing (`sonar_type = EM3002`, `fileVersion = 4`), injects the latest gyro/attitude into `profile.vesselHeading/Heave/Pitch/Roll`, and uses 3D depression/azimuth geometry when `-crudeCalc` is active. |
| `-8101` | *(none)* | Sets `sonar_type = SeaBat_8101` and `fileVersion = 2` (default without `-M3_test` or `-8101` is `SeaBat_7125`, `fileVersion = 4`). |
| `-crudeCalc` | *(none)* | Recomputes approximate `observedDepth`, `acrossTrack`, and `alongTrack` (in mm) directly from `beams[j].range` and `Rc_steer` (or `beam_depress_angle` / `beam_heading_angle` if `-M3_test` is set). |
| `-sonar` | `<7125\|ES3>` | Accepted on the command line for script compatibility. |
| `-v` | *(none)* | Enables verbose diagnostic logging of header tables, record IDs, and beam bitmasks. |
| `-debug` | *(none)* | Enables debug flag (`debug++`). |

---

## Internal Data Structures & `RMB` Bitmask Decoding

`hypack2omg` uses `Hypack_HSX_Header` and `Hypack_HSX_Record` (from `omg_hypack.h`) alongside `OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, and `OMG_HDCS_beam` (from `OMG_HDCS_jversion.h`).

When `-do_bathy` is active and an `RMB` record is encountered, `hypack2omg` reads the 16-bit hexadecimal `mbes_beam_data` bitmask (`0x0001` through `0x2000`). For each bit set in `mbes_beam_data`, an immediately following continuation line in the `.HSX` file contains `mbes_num_beams` space-delimited values, which `hypack2omg` maps into `OMG_HDCS_beam`:

| Bitmask (`mask`) | HYSWEEP Field | `OMG_HDCS_beam` Mapping & Scaling |
| :--- | :--- | :--- |
| `0x0001` | Beam ranges (work units, m) | `beams[j].range = (int)(atof(word) * 100.0 + 0.5)` (cm); `beams[j].twtt = 2.0 * atof(word) / mbes_sound_velocity` (s) |
| `0x0002` | Sounding point Easting | Parsed and skipped |
| `0x0004` | Sounding point Northing | Parsed and skipped |
| `0x0008` | Point corrected depth (m) | `beams[j].observedDepth = (int)(atof(word) * 1000.0 + 0.5)` (mm) |
| `0x0010` | Along-track distance (m) | `beams[j].alongTrack = (int)(atof(word) * 1000.0 + 0.5)` (mm) |
| `0x0020` | Across-track distance (m) | `beams[j].acrossTrack = (int)(atof(word) * 1000.0 + 0.5)` (mm) |
| `0x0040` | Beam pitch angles (deg) | `beams[j].Tx_steer = (int)(atof(word) * 100.0 + 0.5)` (0.01 deg) |
| `0x0080` | Beam roll angles (deg) | `beams[j].Rc_steer = (int)(atof(word) * 100.0 + 0.5)` (0.01 deg) |
| `0x0100` | Beam take-off angles (deg) | `beams[j].beam_depress_angle = (int)(atof(word) * 100.0 + 0.5)` (0.01 deg) |
| `0x0200` | Beam direction angles (deg) | `beams[j].beam_heading_angle = (int)(fval * 100.0 + 0.5)` (0.01 deg, wrapped `+360` if `< 0`) |
| `0x0400` | Ping delay times (ms) | Parsed and skipped |
| `0x0800` | Beam intensity data | Scaled `valI /= 128` (from 15-bit `0..32767` to 8-bit) into `beams[j].reflectivity` and `beams[j].intensity` |
| `0x1000` | Beam quality codes | Parsed and logged in verbose mode |
| `0x2000` | Sounding flags (`0` or `129`) | `sflag == 0 ? (beams[j].status = 0) : (beams[j].status = 2)` |

At completion, `hypack2omg` also reports the mean latency in milliseconds (`mean_latency / count_latency`) between `RMB` multibeam timestamps and `HCP` IMU timestamps.
