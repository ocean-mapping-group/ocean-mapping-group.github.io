---
layout: default
title: azimerge
parent: Merge Tools
grand_parent: sidescan
nav_order: 3
---
# azimerge

## Description
`azimerge` is a utility designed to merge azimuth (heading) and optionally navigation (latitude and longitude) information from a navigation file (JCU NAV format) onto an existing JCU GLORIA record file. It performs time-based interpolation of navigation data to update the GLORIA records, ensuring accurate positional and heading information.

## Usage
```bash
azimerge [-declin <degrees>] [-timegap <seconds>] [-pixsiz <m>] [-layback <seconds>] [-nav] [-v] [-timehack <seconds>] <navfile> <beforefile> <afterfile>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-declin <degrees>` | Apply a magnetic declination correction (in degrees) to the azimuth values. | `0.0` |
| `-timegap <seconds>` | Specifies a maximum time gap in seconds between navigation records. If exceeded, the GLORIA record is skipped. | `10000000000.0` (effectively no limit) |
| `-pixsiz <m>` | Overrides the pixel size (in meters) in the GLORIA header. | `0.0` (uses existing) |
| `-layback <seconds>` | Specifies a time offset (in seconds) to apply to the GLORIA record's time before interpolating with navigation data. | `0` |
| `-nav` | If specified, latitude and longitude from the navigation file will also be merged onto the GLORIA records. | (None) |
| `-v` | Enable verbose output. | (None) |
| `-timehack <seconds>` | A "timehack" value to be subtracted from the `layback` before applying it. | `0` |
| `<navfile>` | **Required.** The input navigation file (JCU NAV format) containing azimuth and position data. |
| `<beforefile>` | **Required.** The input JCU GLORIA file to which the azimuth and navigation will be merged. |
| `<afterfile>` | **Required.** The output JCU GLORIA file with updated azimuth and navigation. |

## How It Works
1.  **File Opening and Initialization:** The tool opens the navigation file (`navfile`), the input GLORIA file (`beforefile`), and the output GLORIA file (`afterfile`). It also initializes various parameters and flags.
2.  **Process GLORIA Records:** The tool reads each record from `beforefile` one by one:
    *   **Time Adjustment:** The GLORIA record's time (`before_rec.header.time`) is adjusted by subtracting the `layback` (which can be further modified by `timehack`). This adjusted time is used to find corresponding navigation data.
    *   **Navigation Search:** It performs a time-based search within the `navfile` to find the two navigation records (`prev_nav_rec`, `next_nav_rec`) that bracket the adjusted GLORIA record time.
    *   **Time Gap Check:** If the time gap between `prev_nav_rec` and `next_nav_rec` exceeds `timegap`, the current GLORIA record is skipped.
    *   **Interpolation Weights:** Linear interpolation weights (`weight1`, `weight2`) are calculated based on the GLORIA record's time relative to `prev_nav_rec` and `next_nav_rec`.
    *   **Azimuth Interpolation:**
        *   The azimuths from `prev_nav_rec` and `next_nav_rec` are corrected for magnetic declination (`-declin`).
        *   These corrected azimuths are then linearly interpolated using `weight1` and `weight2` to derive the `after_rec.header.azi` for the current GLORIA record. Special handling for zero azimuths is present.
    *   **Navigation Interpolation (Optional):** If the `-nav` flag is set, `after_rec.header.lat` and `after_rec.header.lon` are similarly interpolated from `prev_nav_rec` and `next_nav_rec`.
    *   **Pixel Size Override (Optional):** If `-pixsiz` is specified, `after_rec.header.small_pixel` is updated.
    *   **Write Output:** The modified GLORIA record (`after_rec`) is written to `afterfile`.
3.  **Loop:** This process repeats until all records in `beforefile` have been processed.
