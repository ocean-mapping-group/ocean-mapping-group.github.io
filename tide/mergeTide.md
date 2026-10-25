---
layout: default
title: mergeTide
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 1
tool_name: mergeTide
source_path: code/tide/mergeTide.c
category: Vertical Datum & Tide Correction
input_formats:
- .merged
- .nav (binary tide series)
output_formats:
- .merged (modified in-place)
related_tools:
- weigh_grid
- swathed
- stripNav
- mergeHeave
---

# mergeTide

## Description
`mergeTide` interpolates a time series of tidal heights (stored in the `azi` field of an OMG binary `jcu_nav_rec` file) and writes the resulting vertical offset into each ping's profile header (`profile.tide`, in millimeters) inside one or more OMG-HDCS `.merged` files.

In addition to traditional water-level tides, `mergeTide` supports OMG-HDCS v4 extended vertical fields, allowing it to populate **RTK GPS elevation at the Reference Point (`-RTK`)**, **low-pass filtered RTK (`-filtRTK`)**, **long-period heave correction (`-LPHC`)**, **dynamic draft correction (`-DDC`)**, or **AUV transducer depth replacement (`-TXZ`)**. It can also perform spatial two-station cotidal interpolation (`-interpolate`) between two tide gauge files (`-tide` and `-tide2`) based on the vessel's real-time latitude and longitude.

---

## Usage

```bash
mergeTide [OPTIONS] -tide <tidefile.bin> <mergefile(s).merged>
```

### Common Workflow Examples

**1. Standard predicted or observed tide merge (as used in Kongsberg unravel scripts):**

```bash
mergeTide -tide ../Tides/Predicted_Fort_Point_May_2021.bin merged/JD100/0001_line.merged
```

**2. Two-station spatial and temporal tide interpolation:**

```bash
mergeTide \
    -interpolate \
    -tide station1_SE.bin -loc1 45.120 -66.050 \
    -tide2 station2_NW.bin -loc2 45.450 -66.320 \
    merged/JD100/*.merged
```

**3. Merging GPS RTK tide while removing real-time vessel heave (to avoid double-correcting heave):**

```bash
mergeTide -RTK -remove_heave -tide rtk_height_series.bin merged/JD100/*.merged
```

**4. Clearing (zeroing out) previously merged tides:**

```bash
mergeTide -zero_tide merged/JD100/*.merged
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-tide <filename>` | **Required** (unless `-zero_tide` is set). Binary `jcu_nav_rec` file where `time`/`centisecs` is UTC epoch time and `azi` holds the tide height in meters. | None |
| `<mergefile(s)>` | **Required.** One or more OMG-HDCS `.merged` files (up to 1000 files) to modify in-place. | None |
| `-zero_tide` | Zero out the target tide field (`profile.tide = 0`, or the field selected by `-RTK`/`-filtRTK`/`-LPHC`/`-DDC`) across all pings without reading a tide file. | Disabled |
| `-add` | Add the newly interpolated tide to the existing `profile.tide` value instead of overwriting it. | Overwrite (`0`) |
| `-base_offset <meters>` | Constant vertical datum offset (in meters) added to every interpolated tide value (`int_base_offset = base_offset * 1000.0` mm). | `0.0` |
| `-atten <factor>` | Amplitude scaling / attenuation factor multiplied against the interpolated tide height (`atten * tide_interp`). | `1.0` |
| `-delay <minutes>` | Time shift (in **minutes**) applied when looking up tide for a ping (`time += delay * 60.0`). | `0.0` |
| `-addGPSrolloverwraps <N>` | Compensates for 1024-week GPS rollover in ping timestamps by adding $N \times 619,315,200$ seconds when searching the tide file. | `0` |
| `-maxtimejump <minutes>` | Warn if the time interval between consecutive bracketing tide records exceeds `<minutes>`. | `30.0` min |
| `-interpolate` | Enable spatial linear interpolation along the baseline between two tide stations. Requires `-tide`, `-tide2`, `-loc1 <lat1> <lon1>`, and `-loc2 <lat2> <lon2>`. | Disabled |
| `-tide2 <filename>` | Second binary tide file for two-station spatial interpolation. | None |
| `-loc1 <lat> <lon>` | Decimal latitude and longitude of the first (`-tide`) station (typically South-East station). | None |
| `-loc2 <lat> <lon>` | Decimal latitude and longitude of the second (`-tide2`) station (typically North-West station). | None |
| `-RTK` | Store result in `profile.RTK_at_RP` (cm, OMG-HDCS v4 only) instead of `profile.tide`. | `PUT_IN_TIDE` |
| `-filtRTK` | Store result in `profile.Lowpass_RTK_at_RP` (cm, OMG-HDCS v4 only). | `PUT_IN_TIDE` |
| `-LPHC` | Store result in `profile.longperiod_heaveCorrection` (mm, OMG-HDCS v4 only). | `PUT_IN_TIDE` |
| `-DDC` | Store result in `profile.dynamic_draftCorrection` (cm, OMG-HDCS v4 only). | `PUT_IN_TIDE` |
| `-TXZ` | Replace transducer draft (`profile.deepdraftoffset_in_metres` and `profile.draft_at_Tx`) with the interpolated value—used for AUV depth sensor replacement. | `PUT_IN_TIDE` |
| `-abs_coeff` | Store value in `profile.params[1].nrActualGainSets` (used for Reson absorption coefficient injection). | `PUT_IN_TIDE` |
| `-remove_heave` | Adds `(heave_sign * profile.vesselHeave / 1000.0)` to the interpolated tide height so real-time heave is backed out when applying GPS/RTK water level heights. | Disabled |
| `-invert_heave` | Used with `-remove_heave`; flips `heave_sign` from `+1` to `-1`. | `+1` |
| `-check_drift` | Add `profile.clock_drift_millis / 1000.0` to ping time before searching the tide record. | Disabled |
| `-date <yr> <mo> <day>` | Override `summary.refTime` in the `.merged` file using the specified date. | Disabled |
| `-jb` | Enable sequential time-cursor caching (`jb_flag`) to speed up lookup on monotonically increasing pings. | Disabled |
| `-dont_writeout` | Dry-run / test mode: perform interpolation and print diagnostics without writing changes to the `.merged` file. | Disabled |
| `-v` | Print verbose interpolation weights (`w1`, `w2`) and bracketing timestamps for every ping. | Disabled |

---

## Troubleshooting

| Warning / Error | Cause | Resolution |
|---|---|---|
| `Got time out of bounds!` | The ping timestamp falls before the first record or after the last record of the `-tide` binary file. | Check the time span of the tide file using `appendNav -ascii` or `sumNav`, or check if `-addGPSrolloverwraps 1` is needed. Note: `mergeTide` skips writing to pings that are out of bounds! |
| `Yo, can only use RTK fields for V4 data` | `-RTK`, `-filtRTK`, `-LPHC`, or `-DDC` was used on a legacy OMG-HDCS v1–v3 `.merged` file. | Unpack the raw data with `-v4` (in `RTlite`) or `read_kmall` (which always writes v4). |
| `tide get of more than 30.0 minutes` | Gap between consecutive records in the `.bin` tide file exceeds `maxtimejump`. | Pass `-maxtimejump <minutes>` if using hourly tide tables, or resample the tide curve to a finer interval (e.g., 5–15 minutes). |
