---
layout: default
title: mergeNav
parent: Navigation Tools
nav_order: 1
tool_name: mergeNav
source_path: code/nav/mergeNav.c
category: Navigation & Georeferencing
input_formats: [".merged", ".nav", ".param", ".ss", ".svp", ".adcp"]
output_formats: [".merged (modified in-place)", ".ss (modified in-place)", ".svp (modified in-place)", ".llz_post", ".txt"]
related_tools: ["read_kmall", "RTlite", "mergeAtt", "newMergeAtt", "stripNav", "appendNav", "getBounds"]
---

# mergeNav

## Description
`mergeNav` interpolates asynchronous binary navigation records (`jcu_nav_rec`, 48 bytes per fix, stored in `<handle>.nav`) onto the profile headers of an OMG-HDCS multibeam file (`<handle>.merged`), a GLORIA sidescan file (`<handle>.ss`), a Sound Velocity Profile (`<handle>.svp`), an ADCP file, or an underwater camera photo sequence.

In the standard Kongsberg `.kmall` and `.all` unraveling pipelines, `mergeNav` is executed **immediately after** [`mergeAtt`](../omg/mergeAtt.md) (because `mergeNav` requires the ping's roll, pitch, and heading from the profile header to rotate 3D lever-arm offsets between the GPS antenna and the vessel Reference Point / transducer) and **immediately before** [`getBounds`](../omg/getBounds.md) and [`makess`](../omg/makess.md).

> [!IMPORTANT]
> **Sign Convention for Lever Arms (`-ahead`, `-right`, `-below`):**
> In `mergeNav`, the command-line lever arm arguments represent the vector **from the positioning antenna to the Reference Point (RP) / transducer**:
> * If the antenna is **behind** (aft of) the transducer, `-ahead` is **positive (+)**.
> * If the antenna is **left** (port) of the transducer, `-right` is **positive (+)**.
> * If the antenna is **above** the transducer, `-below` is **positive (+)**.
>
> Note that this is the **opposite sign** of the Kongsberg `.param` file (`params.pos[i].Xloc`, `Yloc`, `Zloc`), which defines the vector from the RP to the antenna. When `-use_params` is specified, `mergeNav` automatically negates `Xloc`, `Yloc`, and `Zloc` (`unrot.x = -params.pos[i].Xloc`, etc.).For Kongsberg `.kmall` and `.all` files where SIS has already reduced navigation to the Reference Point, `-ahead 0.0 -right 0.0 -below 0.0` is used.

---

## Usage

```bash
mergeNav [OPTIONS] <datafile_handle> [...]
```

### Common Workflow Examples

**1. Standard Kongsberg `.kmall` / `.all` pipeline (nav already at RP):**
```bash
# Ensure .nav exists (for .kmall, copy .nav_1 to .nav first)
cp merged/JD100/0001_line.nav_1 merged/JD100/0001_line.nav

mergeNav \
    -ahead 0.0 \
    -right 0.0 \
    -below 0.0 \
    -declin 0.0 \
    -delay 0.00 \
    merged/JD100/0001_line
```

**2. Applying lever arms from the `.param` file (Sensor 1):**
```bash
mergeNav -use_params -sensor 1 merged/JD100/0001_line.merged
```

**3. Merging an external navigation file onto a swath file with a latency delay:**
```bash
mergeNav -nav proc_nav/whole_day.nav -delay 0.05 -swath merged/JD100/0001_line.merged
```

**4. Merging navigation onto a sidescan (`.ss`) or SVP (`.svp`) file:**
```bash
mergeNav -ss ss/JD100/0001_line.ss
mergeNav -svp -nav merged/JD100/0001_line.nav merged/JD100/0001_line.svp_001
```

---

## Arguments

### Target File Type Selection

| Option | Description | Default |
|---|---|---|
| `<datafile_handle>` | Base path or filename (e.g., `merged/subdir/line` or `merged/subdir/line.merged`). Automatically looks for `<handle>.merged` (or `.ss`) and `<handle>.nav` unless `-nav` is specified. | Required |
| `-swath <file>` | Explicitly specify the input `.merged` swath file. | Default mode (`merged_flag = 1`) |
| `-ss` | Merge navigation onto a GLORIA format sidescan file (`<handle>.ss`) instead of `.merged`. | Disabled |
| `-svp` | Merge navigation (observation latitude/longitude) onto an OMG Sound Velocity Profile (`.svp`) based on `svp.time_of_obs`. Requires `-nav <navfile>`. | Disabled |
| `-adcp` | Read and inspect ADCP header and records (`jADCP_read_header`). | Disabled |
| `-tseries` | Merge navigation onto a binary time-series file formatted as `jcu_nav_rec` (e.g., surface sound speed track). | Disabled |
| `-onefix` | Merge navigation onto a single ASCII timestamp (`YYYY MM DD hh mm ss.ss`) and write `<prefix>.llz_post`. | Disabled |
| `-for_photo_sequence` | Georeference a sequence of underwater still camera frames using `-start <yr> <jday> <hr> <min> <sec>`, `-frame_period_sec <val>`, and `-skip_initial_frames <num>`. Writes `<prefix>.txt` and `dumpPHOTOtime.llz`. | Disabled |

### Lever Arms, Timing & Coordinate Corrections

| Option | Description | Default |
|---|---|---|
| `-ahead <meters>` | Along-ship distance (m) from antenna to RP/transducer (+ve forward). | `0.0` |
| `-right <meters>` | Across-ship distance (m) from antenna to RP/transducer (+ve starboard). | `0.0` |
| `-below <meters>` | Vertical distance (m) from antenna to RP/transducer (+ve downward). | `0.0` |
| `-use_params` | Read positioning sensor lever arms from `<handle>.param` and negate them (`-Xloc`, `-Yloc`, `-Zloc`) to shift from antenna to RP. Resets manual `-ahead`/`-right`/`-below` to 0. | Disabled |
| `-sensor <1\|2>` | Used with `-use_params`. Selects positioning sensor `1` (`params.pos[0]`) or `2` (`params.pos[1]`) from the `.param` file. | `1` |
| `-delay <sec>` | Time latency correction (seconds) applied to navigation timestamps (`nav_time - delay`). | `0.0` |
| `-addGPSrolloverwraps <N>` | Compensates for 1024-week GPS epoch rollover bugs (e.g., legacy POS MV v4 systems) by subtracting $N \times 619,315,200$ seconds ($1024 \times 7 \times 86400$) from the delay. | `0` |
| `-time_limit <sec>` | Maximum allowable time gap (seconds) between bracketing navigation fixes before a ping is flagged as having no valid navigation. | `300.0` (5 min) |
| `-declin <deg>` | Magnetic declination offset (degrees) added to vessel heading/azimuth. | `0.0` |

### Navigation Source & Flag Handling

| Option | Description | Default |
|---|---|---|
| `-nav <navfile>` | Use a specific `.nav` file instead of `<handle>.nav`. | `<handle>.nav` |
| `-allnavok` | Ignore bad navigation quality flags (`flag[3] != 0`) in the `.nav` file and use all fixes. | Disabled |
| `-really_wipe_nav` | Zero out `vesselLatOffset` and `vesselLongOffset` and set `profile.status = 2` on every ping before attempting to merge new navigation, ensuring no stale positions remain if nav coverage is partial. | Disabled |
| `-hdg` | Overwrite the ping's `vesselHeading` in the `.merged` profile header with the heading/azimuth (`azi`) interpolated from the `.nav` file. | Disabled |
| `-vehicle_altitude` | For AUV surveys: merge RP altitude from the `.nav` file and write diagnostics to `Vehicle_Altitude_Corrections.nav`. Cannot be combined with `-hdg`. | Disabled |
| `-addpitch` | Include vessel pitch in the 3D rotation matrix when computing lever-arm shifts. | Disabled |
| `-check_drift` | Add `profile.clock_drift_millis / 1000.0` to the ping timestamp before searching `.nav`. | Disabled |
| `-v` | Enable verbose output for every ping interpolation. | Disabled |
| `-debug_JDAY` | Interactive utility mode: prompts for `day month year` on stdin and prints Julian day (`jday`) and `stdtime` (seconds since 1970). Enter `0 0 0` to exit. | Disabled |

---

## How It Works

1. **Navigation File Validation:**
   Opens `<handle>.nav` (or the file specified via `-nav`) and checks that its byte size is non-zero (`ftell(navfile) > 0`). Computes the number of records as `filesize / JCU_BINNAV_RECLEN` (48 bytes) and prints the start and end timestamps (`navstart` and `navend`).
2. **Summary Header Reference Coordinates:**
   Reads the `OMG_HDCS_summary_header` from `<handle>.merged`. If `refLat` or `refLong` are not set, initializes them from the navigation track.
3. **Ping-by-Ping Time Interpolation:**
   For each profile $k \in [0, \text{numProfiles}-1]$:
   * Computes exact ping epoch time:
     $$t_{\text{ping}} = \text{timeOffset} \times \text{timeScale} \times 10^{-6} + \text{refTime} \times 100.0$$
   * Searches the `.nav` file for the two valid fixes (`flag[3] == 0`, unless `-allnavok` is set) immediately before ($t_1$) and after ($t_2$) $t_{\text{ping}} + \text{delay}$.
   * If $t_2 - t_1 \le \text{time\_limit}$, linearly interpolates latitude, longitude, speed (`vesselVelocity`), and (if `-hdg` is set) heading.
4. **3D Lever-Arm Rotation (`calc_geo_shifts`):**
   If `ahead`, `right`, or `below` are non-zero, rotates the lever-arm vector `(ahead, right, below)` by the ping's roll, pitch (if `-addpitch`), and heading using a right-handed Direction Cosine Matrix (`DCM_rthand.h`), converts the meter offsets to latitude/longitude shifts (`lat_offset`, `lon_offset`), and applies them to the interpolated antenna coordinates.
5. **In-Place Profile Update:**
   Updates `profile.vesselLatOffset`, `profile.vesselLongOffset`, `profile.vesselVelocity`, and `summary.minLat`/`maxLat`/`minLong`/`maxLong` in `<handle>.merged`.

---

## Troubleshooting

| Error Message | Cause | Resolution |
|---|---|---|
| `Error opening <handle>.nav` | For `.kmall` files, `read_kmall` creates `.nav_1`, `.nav_2`, `.nav_3`, not `.nav`. | Copy the active navigation file first: `cp <handle>.nav_1 <handle>.nav` or pass `-nav <handle>.nav_1`. |
| `Nav file <file> has no data!` | The `.nav` file is 0 bytes (e.g., `cp line.nav_3 line.nav` was run when sensor 3 was inactive). | Check `ls -lh <handle>.nav*` and copy the non-empty `.nav_1` or `.nav_2` file to `<handle>.nav`. |
| `not an HDCS format file (is it .ss or .svp?)` | A `.ss` sidescan or `.svp` file was passed to `mergeNav` without the `-ss` or `-svp` flag. | Add `-ss` for sidescan files or `-svp -nav <navfile>` for SVP files. |
| Pings remain un-navigated or out of time bounds | Navigation timestamps are offset by 1024 GPS weeks (POS MV v4 rollover) or exceed `-time_limit`. | Compare `navstart`/`navend` printed by `mergeNav` against ping times; use `-addGPSrolloverwraps 1` or increase `-time_limit`. |
