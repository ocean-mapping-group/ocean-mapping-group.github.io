---
layout: default
title: glmerge
parent: Merge Tools
grand_parent: sidescan
nav_order: 4
---
# glmerge

## Description
`glmerge` is a utility designed to merge Seabeam navigation and depth information onto a raw IOS (Institute of Ocean Sciences) format GLORIA file. The processed data, combining the sidescan imagery with accurate navigation and depth, is then written out as a JCU GLORIA record file. This tool performs time-based interpolation to synchronize the two different datasets.

## Usage
```bash
glmerge [-declin <degrees>] [-layback <value>] [-azi] [-isolated <time_gap_window>] [-ping <rate>] [-timehack <seconds>] <cbfile> <iosfile_prefix>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-declin <degrees>` | Apply a magnetic declination correction (in degrees) to the azimuth values. | `0.0` |
| `-layback <value>` | Specifies the layback value (in seconds or units) to account for the offset between the seabeam and sidescan acquisition. | `0` |
| `-azi` | If specified, the azimuth from the Seabeam file will be merged. | (None) |
| `-isolated <time_gap_window>` | If specified, allows for isolated Seabeam depth/offset values to be used if within the specified time gap window. | (None) |
| `-ping <rate>` | Specifies the ping rate. Used for time-related calculations. | `30` |
| `-timehack <seconds>` | A "timehack" value to be subtracted from the `layback`. | `0` |
| `<cbfile>` | **Required.** The input Seabeam file (presumably in `sb_urirec` format) containing navigation and depth. |
| `<iosfile_prefix>` | **Required.** The prefix for the input IOS GLORIA file. The tool assumes the input file has a `.ios` extension. The output file will be named `<iosfile_prefix>.mer`. |

## How It Works
1.  **File Opening and Initialization:** The tool opens the Seabeam file (`cbfile`), the input IOS GLORIA file (`iosfile`), and the output JCU GLORIA file (`merfile`). It initializes various parameters including `layback` and `timehack`.
2.  **Time Synchronization:**
    *   It reads the first IOS GLORIA record to get its raw time. This time is adjusted by `layback` (and `timehack`).
    *   It then searches within the Seabeam file (`cbfile`) to find the closest Seabeam record to this adjusted IOS time, and sets `cb_record` to point to it.
3.  **Process IOS GLORIA Records:** The tool reads each record from `iosfile` one by one:
    *   **Time Adjustment:** The current IOS record's time is retrieved using `getiostime` and adjusted by `layback`. Time is also adjusted based on `ping` rate to avoid duplicate timestamps from IOS data lacking seconds.
    *   **Skip Non-transmissions:** It checks for "non-transmission" or invalid pings by summing a portion of the raw sidescan data; if the sum is below a threshold, the record might be considered a "corner" and handled differently.
    *   **Navigation Interpolation:**
        *   It finds the two Seabeam records (`prev_cb_rec`, `next_cb_rec`) that bracket the adjusted IOS record time.
        *   Linear interpolation weights (`weight1`, `weight2`) are calculated.
        *   **Depth and Offset:** Seabeam depth and offset values (`cb_depth`, `cb_offset`) for various beams are interpolated. The `-isolated` flag provides special handling for using isolated Seabeam data if only one bracketing record is valid and within a specified `time_gap_window`.
        *   **Latitude and Longitude:** Latitude and longitude are interpolated from the Seabeam records.
        *   **Azimuth (Optional):** If the `-azi` flag is set, the azimuth (`mer_rec.header.azi`) is interpolated from the Seabeam course values and corrected for magnetic declination.
    *   **Populate JCU GLORIA Record:** The `mer_rec` is populated with the interpolated header information and the raw sidescan data from the IOS record.
    *   **Write Output:** The merged `mer_rec` is written to `merfile`.
4.  **`getiostime` Function:** A helper function to parse time from the IOS record.
5.  **Loop:** This process repeats until all records in `iosfile` have been processed.
