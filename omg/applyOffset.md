---
layout: default
title: applyOffset
parent: OMG Tools
nav_order: 77
---
---
layout: default
title: applyOffset
parent: OMG Tools
nav_order: 77
---
# applyOffset

## Description
`applyOffset` is a utility designed to adjust the geographic positions of profiles (pings) within OMG-HDCS merged files. Its primary use is to correct for the offset between the navigation antenna and the multibeam transducer, particularly if this correction was not applied during the initial data merging process.

The tool can apply a fixed offset based on user-defined `ahead` and `right` values relative to the vessel's heading, or it can apply corrections from an external offset file (`-offsetfile`) combined with an `ElltoCD` correction.

## Usage
```bash
applyOffset <datafile(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<datafile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place. |
| `-ahead <val>` | Specifies the offset distance (in meters) of the antenna *ahead* of the transducer. | `0.0` |
| `-right <val>` | Specifies the offset distance (in meters) of the antenna to the *right* of the transducer. | `0.0` |
| `-offsetfile <filename>` | Specifies an external file containing custom offsets. This option is used in conjunction with `-elltocd`. |
| `-elltocd <val>` | Used with `-offsetfile`. This value is added to a `oheight` value read from the offset file and applied as a depth correction. | `0.0` |
| `-v` | Enable verbose output. | |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Offset File Handling (`-offsetfile`):** If `-offsetfile` is specified:
    *   It expects a single input merged file.
    *   It reads `ocount`, `otime`, `oheading`, `oroll`, `opitch`, `oheave`, and `oheight` from the `offsetfile`.
    *   For each ping, it modifies the `observedDepth` of all beams by subtracting `profile.vesselHeave` and `(oheight + ElltoCD) * 1000.0`. This means it applies an external heave-like correction to the depths.
3.  **Fixed Offset Handling (Default):** If `-offsetfile` is *not* specified:
    *   For each profile (ping) in the merged file:
        *   It reads the profile header.
        *   Determines the transducer's current geographic location (`lat`, `lon`) using `locate_transducer`.
        *   **Apply Antenna Offset:** If `ahead` or `right` offsets are provided, it calculates `lat_offset` and `lon_offset` based on the vessel's heading (`rad_heading`). These calculated offsets are then added to the current `lat` and `lon`.
        *   **Update Profile Header:** The `vesselLatOffset` and `vesselLongOffset` fields in the `profile` header are updated with the new (offset-corrected) latitude and longitude.
        *   **Update Beam Offsets:** For each beam within the profile, it recalculates `beams[i].latOffset` and `beams[i].longOffset` based on the new vessel heading and the beam's `acrossTrack` distance. This effectively recalculates the individual beam geographic offsets from the transducer position.
4.  **In-Place Modification:** The merged file is modified in place, updating either beam depths (with `-offsetfile`) or profile/beam geographic offsets (with `ahead`/`right`).

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.

## Notes
The tool modifies the merged file in place, so it's advisable to back up files before processing. The `ahead` and `right` offsets are crucial for precise georeferencing of multibeam data, especially when the navigation antenna is not directly over the sonar transducer.

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Offset File Handling (`-offsetfile`):** If `-offsetfile` is specified:
    *   It expects a single input merged file.
    *   It reads `ocount`, `otime`, `oheading`, `oroll`, `opitch`, `oheave`, and `oheight` from the `offsetfile`.
    *   For each ping, it modifies the `observedDepth` of all beams by subtracting `profile.vesselHeave` and `(oheight + ElltoCD) * 1000.0`. This means it applies an external heave-like correction to the depths.
3.  **Fixed Offset Handling (Default):** If `-offsetfile` is *not* specified:
    *   For each profile (ping) in the merged file:
        *   It reads the profile header.
        *   Determines the transducer's current geographic location (`lat`, `lon`) using `locate_transducer`.
        *   **Apply Antenna Offset:** If `ahead` or `right` offsets are provided, it calculates `lat_offset` and `lon_offset` based on the vessel's heading (`rad_heading`). These calculated offsets are then added to the current `lat` and `lon`.
        *   **Update Profile Header:** The `vesselLatOffset` and `vesselLongOffset` fields in the `profile` header are updated with the new (offset-corrected) latitude and longitude.
        *   **Update Beam Offsets:** For each beam within the profile, it recalculates `beams[i].latOffset` and `beams[i].longOffset` based on the new vessel heading and the beam's `acrossTrack` distance. This effectively recalculates the individual beam geographic offsets from the transducer position.
4.  **In-Place Modification:** The merged file is modified in place, updating either beam depths (with `-offsetfile`) or profile/beam geographic offsets (with `ahead`/`right`).
