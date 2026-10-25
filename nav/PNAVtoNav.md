---
layout: default
title: PNAVtoNav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 10
tool_name: PNAVtoNav
source_path: code/nav/PNAVtoNav.c
category: Navigation & Georeferencing
input_formats:
- Kongsberg HUGIN AUV PNAV ASCII exports (TopsideAUVPos, TopsideShipNav, DGPSHiPAPData, GPSData, DepthData, PressureData, DVLData, CTDData, MotionSensorData, HeadingData)
- NavLab Binary Trajectory & Binary Pressure
output_formats:
- .nav (jcu_nav_rec binary)
- .orientation (OMG_HDCS_attitude v3)
- .jwc (OMG watercolumn SVP + ASCII text)
related_tools:
- mergeNav
- mergeAtt
- newMergeAtt
- QNSYtoNav
- stripNav
---

# PNAVtoNav

## Description
`PNAVtoNav` converts Kongsberg HUGIN AUV post-processed navigation (`PNAV`) ASCII export files and NavLab binary trajectory/pressure files into standard OMG data structures:
* **Navigation, Depth, Pressure, and DVL files** are converted into 48-byte binary `jcu_nav_rec` (`.nav`) files.
* **Motion and Heading files** (`-MotionSensorData`, `-HeadingData`) are converted into OMG-HDCS v3 binary attitude files (`.orientation`, `OMG_HDCS_summary_attitude` + `OMG_HDCS_attitude` records).
* **CTD files** (`-CTDData`) are converted into both an ASCII depth/sound-speed listing (`<comp>`) and a binary OMG watercolumn sound velocity profile (`<comp>.jwc`).

---

## Usage

```bash
PNAVtoNav [SUBFORMAT_FLAG] [OPTIONS] -comp <output_file> <input_file(s)>
```

### Common Workflow Examples

**1. Convert HUGIN NavLab binary trajectory into an OMG `.nav` file (with AUV depth stored in `azi`):**

```bash
PNAVtoNav -Binary_Trajectory -comp auv_navlab.nav navlab_traj.bin
```

**2. Convert onboard AUV `DGPSHiPAPData.txt` (radians) or topside `TopsideAUVPos.txt` (degrees) to `.nav`:**

```bash
PNAVtoNav -DGPSHiPAPData -comp hipap_auv.nav DGPSHiPAPData.txt
PNAVtoNav -TopsideAUVPos -comp topside_auv.nav TopsideAUVPos.txt
```

**3. Convert AUV `MotionSensorData.txt` or `HeadingData.txt` into an OMG `.orientation` attitude file:**

```bash
PNAVtoNav -MotionSensorData -comp auv_motion.orientation MotionSensorData.txt
```

**4. Convert AUV `ctd.txt` into an OMG `.jwc` watercolumn SVP file:**

```bash
PNAVtoNav -CTDData -comp auv_ctd.txt ctd.txt
# Produces auv_ctd.txt (ASCII) and auv_ctd.txt.jwc (binary watercolumn SVP)
```

---

## Arguments

### Subformat Selection Flags

| Option | Input File Format & Units | Output Format & Field Mapping |
|---|---|---|
| `-TopsideAUVPos` | **Default.** `TopsideAUVPos.txt` (`Time_us HiPAP_Lat_deg HiPAP_Lon_deg ...`). | Binary `.nav` (`lat`, `lon` in deg; `time = Time_us / 1e6`). |
| `-TopsideShipNav` | `TopsideShipNav.txt` (`Time_us Ship_Lat_deg Ship_Lon_deg ...`). | Binary `.nav` (`lat`, `lon` in deg; `time = Time_us / 1e6`). |
| `-DGPSHiPAPData` | `DGPSHiPAPData.txt` (`Time_us Lat_rad Lon_rad ...`). Converts radians to degrees (`* 180 / M_PI`). | Binary `.nav` (`lat`, `lon` in deg; `time = Time_us / 1e6`). *(Note: `tide_rec_no` is not incremented in this branch, overwriting record 0).* |
| `-GPSData` | `GPSData.txt` (`Time_us GPS_Lat_rad GPS_Lon_rad ...`). Skips zero positions (`0, 0`) and converts radians to degrees. | Binary `.nav` (`lat`, `lon` in deg; `time = Time_us / 1e6`). |
| `-DepthData` | `DepthData.txt` (`Time_us PS_Depth ...`). | Binary `.nav` (`lat = 0`, `lon = 0`, `azi = pressure_depth`). |
| `-PressureData` | `PressureData.txt` (`Time_us PS_PRESSURE ...`). | Binary `.nav` (`lat = 0`, `lon = 0`, `azi = pressure`). |
| `-DVLData` | `DVLData.txt` (`Time_us DVL_FA_BOTM_VEL DVL_PS_BOTM_VEL ...`). Skips blank/zero speeds or timestamps. | Binary `.nav` (`azi = dvl_bottom_FA` fore-aft velocity, `velocity = dvl_bottom_PS` port-stbd velocity). |
| `-MotionSensorData` | `MotionSensorData.txt` (`Time_us MD_ROLL_rad MD_PITCH_rad MD_YAW_rad ...`). Converts radians to degrees. | Binary OMG-HDCS v3 `.orientation` file (`roll`, `pitch`, `heading` in hundredths of a degree; `heave = 0`). |
| `-HeadingData` | `HeadingData.txt` (`Time_us HD_HEADING_rad HD_ROLL_rad HD_PITCH_rad HD_HEAVE ...`). Converts angles from radians to degrees. | Binary OMG-HDCS v3 `.orientation` file (`roll`, `pitch`, `heading`, `heave` in hundredths). |
| `-CTDData` | `ctd.txt` (`Time_us Cond Temp Pressure Sound_Vel Salinity ...`). Filters for `Pressure > 0.5`. | Writes ASCII `rec_no pressure sound_speed` to `<comp>` and binary `watercolumn` v2 structure to `<comp>.jwc` (up to 50,000 samples). |
| `-Binary_Trajectory` | NavLab binary trajectory (`NavLab_Binary_Record`, 168 bytes = 21 `double`s: `rtime_sec`, `lat`, `lon`, `depth`, `roll`, `pitch`, `heading`, `vel_N`, `vel_E`, `vel_D`, `unknown[11]`). | Binary `.nav` (`lat`, `lon` in deg, `azi = depth`, `time = rtime`). |
| `-Binary_Pressure` | NavLab binary pressure (`NavLab_Binary_Pressure`, 16 bytes = 2 `double`s: `rtime_us`, `pressure`). | Binary `.nav` (`lat = 0`, `lon = 0`, `azi = pressure`, `time = rtime_us / 1e6`). |

### General Options

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output filename (`.nav`, `.orientation`, or ASCII + `.jwc` for `-CTDData`). | None |
| `<mergefile(s)>` | **Required.** One or more PNAV input files (up to 300 files). | None |
| `-skip <N>` | Decimation factor parsed on the command line (`skip = strtoint(*argv)`). | `1` |
| `-v` | Enable verbose flag (`verbose_flag`). | Disabled |

---

## How It Works

1. **Timestamp Scaling & Jump Detection:**
   All ASCII PNAV files and `-Binary_Pressure` log timestamps in **microseconds** since the Unix epoch (`1970-01-01 00:00:00 UTC`), which `PNAVtoNav` divides by `1,000,000.0` (whereas `-Binary_Trajectory` timestamps are already in seconds). For each record, `PNAVtoNav` checks `deltime = rtime - oldtime` and warns (`YO time jump at ...`) if `deltime < 0` or `deltime > 500` seconds (`> 5` seconds for motion/heading).
2. **Binary `.nav` Generation:**
   Splits `rtime` into integer seconds (`tide_rec.time`) and hundredths of a second (`tide_rec.centisecs = fracsec * 100.0`) and writes 48-byte `jcu_nav_rec` structures via `nav_write()`.
3. **Attitude (`.orientation`) Generation:**
   For `-MotionSensorData` and `-HeadingData`, initializes an `OMG_HDCS_summary_attitude` header (`sensorNumber = 2`, `fileVersion = 3`, `timeScale = 1000`, `status = 15`, `refTime = (int)(rtime / 100.0)`) on the first record and writes `OMG_HDCS_attitude` records via `OMG_HDCS_write_attitude()`.
4. **CTD (`.jwc`) Generation:**
   For `-CTDData`, accumulates valid depth/sound-speed/temperature/salinity tuples (`pressure > 0.5`) into a dynamically allocated `ZVpair` array and writes `<tidename>.jwc` via `jWC_write()`.
