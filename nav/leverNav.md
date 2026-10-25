---
layout: default
title: leverNav
parent: Navigation Tools
nav_order: 23
tool_name: leverNav
source_path: code/nav/leverNav.c
category: Navigation & Georeferencing
input_formats: [".nav", ".orientation", ".orientation_1", ".orientation_2"]
output_formats: [".nav.at_RP"]
related_tools: ["mergeNav", "PNAVtoNav", "NMEAtoNav", "stripNav"]
---

# leverNav

## Description
`leverNav` computes a 3D lever-arm translation of a binary OMG navigation file (`<prefix>.nav`, where ellipsoid height is stored in the `azi` field) from a GPS/RTK antenna position to the vessel Reference Point (RP) or transducer using high-rate roll, pitch, and heading interpolated from an OMG binary orientation file (`<prefix>.orientation`, `.orientation_1`, or `.orientation_2`).

It writes a new binary navigation file named `<prefix>.nav.at_RP` containing the translated latitude, longitude, and ellipsoid height (`RP_pos.azi = Antenna_pos.azi - GEO_ant_to_RP.z`) at the Reference Point.

> [!IMPORTANT]
> **Sign Convention & Ellipsoid Height Storage:**
> 1. **Ship Reference Frame (SRF) Sign Convention:** In `leverNav`, `-ant_to_RP X Y Z` represents the vector **from the antenna to the Reference Point (RP)** in a right-handed Ship Reference Frame:
>    * **X (+ve forward / ahead):** Positive if the RP is forward of the antenna.
>    * **Y (+ve starboard / right):** Positive if the RP is starboard of the antenna.
>    * **Z (+ve downward / below):** Positive if the RP is below the antenna.
> 2. **Ellipsoid Height in `azi`:** `leverNav` assumes the input `<prefix>.nav` file stores the antenna's **ellipsoid height (positive upward, in meters)** in the `jcu_nav_rec.azi` field (as produced by RTK importers like [`NMEAtoNav`](NMEAtoNav.md), [`PNAVtoNav`](PNAVtoNav.md), or [`toNav -new`](toNav.md)). Because $Z$ is positive downward, the vertically rotated offset `GEO_ant_to_RP.z` is subtracted from `Antenna_pos.azi` to yield the RP ellipsoid height.

---

## Usage

```bash
leverNav -ant_to_RP <X> <Y> <Z> [-orient <0|1|2>] [-v] <RTK_nav_file_prefix>
```

### Common Workflow Examples

**1. Translate RTK antenna navigation to the vessel Reference Point using `.orientation_1`:**
```bash
# Antenna is 19.5m aft, 2.0m port, and 30.0m above the RP:
# Vector from antenna to RP is (+19.5 forward, +2.0 stbd, +30.0 down)
leverNav -ant_to_RP 19.5 2.0 30.0 -orient 1 merged/JD100/0001_line
# Produces: merged/JD100/0001_line.nav.at_RP
```

**2. Interactive 3D rotation matrix verification (`-test` mode):**
```bash
leverNav -ant_to_RP 10.0 0.0 5.0 -test merged/JD100/0001_line
# Prompts on stdin for: roll pitch heading (enter 0 0 0 to exit)
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<RTK_nav_file_prefix>` | **Required.** Base file prefix (without `.nav`). Opens `<prefix>.nav` and `<prefix>.orientation*`, and writes `<prefix>.nav.at_RP`. | None |
| `-ant_to_RP <X> <Y> <Z>` | **Required.** 3D lever-arm offsets (in meters) from the GPS antenna to the Reference Point:<br>• `X`: +ve forward (along-ship)<br>• `Y`: +ve starboard (across-ship)<br>• `Z`: +ve downward (vertical) | `0.0 0.0 0.0` |
| `-orient <0\|1\|2>` | Selects which orientation file to open:<br>• `0`: `<prefix>.orientation`<br>• `1`: `<prefix>.orientation_1`<br>• `2`: `<prefix>.orientation_2`<br>*(Note: place `-orient` **before** `<RTK_nav_file_prefix>` on the command line so `orient` is set when filenames are constructed).* | `0` (`.orientation`) |
| `-test` | Interactive test mode: repeatedly prompts on `stdin` for `roll pitch heading` (enter `0 0 0` to exit) and prints the rotated geographic offsets `x(lon)`, `y(lat)`, `z(+ve down)` without processing the file. | Disabled |
| `-reverse_motion` | Legacy debug flag: passes `(roll, pitch, heading)` without negation into `jDCM_unrotate` ("old wrong way!"). | Disabled (uses `-roll, -pitch, -heading`) |
| `-reverse_laloshift` | Debug flag: subtracts `GEO_ant_to_RP.x / lat_scale` and `GEO_ant_to_RP.y / lon_scale` instead of adding them. | Disabled |
| `-v` | Verbose mode: prints interpolated roll/pitch/heading, rotated geographic offsets, and latitude/longitude scale factors for every fix. | Disabled |

---

## How It Works

1. **Input/Output Initialization:**
   Appends `.nav` to `<RTK_nav_file_prefix>` for the input navigation file, `.orientation` (or `.orientation_1` / `.orientation_2` according to `-orient`) for the binary attitude file, and `.nav.at_RP` for the output navigation file.
2. **Asynchronous Attitude Interpolation:**
   For each record $i$ in `<prefix>.nav`:
   * Computes exact fix timestamp:
     $$t = \text{Antenna\_pos.time} + \frac{\text{Antenna\_pos.centisecs}}{100.0}$$
   * Calls `OMG_HDCS_get_interpolated_async()` on the orientation file with `time_limit = 1.0` second and `delay = 0.0` to interpolate `roll`, `pitch`, and `heading` at time $t$.
   * If `beyond_att_flag` is set (no valid bracketing attitude within 1.0 s), the navigation fix is skipped.
3. **3D Direction Cosine Matrix Unrotation (`jDCM_unrotate`):**
   * Negates the Euler angles (`rpy.roll = -roll`, `rpy.pitch = -pitch`, `rpy.yaw = -heading`) to unrotate the ship-frame lever arm `SRF_ant_to_RP` into the local geographic NED frame (`GEO_ant_to_RP`, where `.x` is North, `.y` is East, and `.z` is Down in meters).
4. **Geographic Coordinate & Ellipsoid Height Update:**
   * Computes meridional and parallel meter-per-degree scale factors at `Antenna_pos.lat` via `get_lat_lon_scales()`.
   * Updates position and vertical height:
     $$\text{RP\_pos.lat} = \text{Antenna\_pos.lat} + \frac{\text{GEO\_ant\_to\_RP.x}}{\text{lat\_scale}}$$
     $$\text{RP\_pos.lon} = \text{Antenna\_pos.lon} + \frac{\text{GEO\_ant\_to\_RP.y}}{\text{lon\_scale}}$$
     $$\text{RP\_pos.azi} = \text{Antenna\_pos.azi} - \text{GEO\_ant\_to\_RP.z}$$
   * Writes `RP_pos` to `<prefix>.nav.at_RP`.
