---
layout: default
title: repoint
parent: OMG Tools
nav_order: 58
---
# repoint

## Description
`repoint` is a utility for correcting beam steering angles in OMG-HDCS merged files due to changes in the surface sound speed. When the actual surface sound speed differs from the one assumed during data acquisition, the calculated beam angles can be inaccurate. This tool allows recalculating these angles based on a new (or interpolated) surface sound speed, thereby "repointing" the beams.

It can either use a constant specified sound speed or interpolate from a `.surf_ss` file to determine the correct surface sound speed for each ping.

## Usage
```bash
repoint -in <filename.merged> (-ssp_file <ssp.bin> | -speed <val>) [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-in <filename.merged>` | **Required.** Path to the input OMG-HDCS merged file. This file is modified in place unless `-just_test` is used. |
| `-ssp_file <ssp.bin>` | **Required (one of this or `-speed`).** Path to an SSP file (either `.nav` or `.orientation` format) containing surface sound speed measurements. The tool will interpolate the SSP from this file for each ping. |
| `-speed <val>` | **Required (one of this or `-ssp_file`).** Specifies a constant surface sound speed value (m/s) to use for repointing. |
| `-orig_speed <val>` | Specifies the original surface sound speed value that was used during data acquisition. This is useful if the original speed is not reliably stored in the merged file or if you wish to override it. | Auto-read from merged file |
| `-just_test` | Runs the repointing logic but does *not* write any changes back to the merged file. Useful for previewing changes. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Input Reading:** Opens the target merged file and optionally an SSP file (if `-ssp_file` is used).
2.  **Surface Sound Speed Determination:**
    *   If `-speed` is used, the `new_ssp` is set to the provided constant value.
    *   If `-ssp_file` is used, for each ping in the merged file, the tool interpolates the surface sound speed from the provided SSP file at the ping's timestamp.
    *   The `old_ssp` (original surface sound speed) is determined either from the merged file's profile header (`td_sound_speed` or `soundVelocity`) or overridden by `-orig_speed`.
3.  **Beam Repointing:** For each ping and each beam within that ping:
    *   It retrieves the transmit (Tx) and receive (Rx) steering angles from the beam structure.
    *   It then applies a trigonometric correction (using the `repoint_angle` function) to both the Tx and Rx steering angles based on the `old_ssp` and `new_ssp`. This correction adjusts the angles as if they were originally recorded with the `new_ssp`.
    *   **Special Handling:** For some older sonar types (e.g., ISIS_Submetrix), which might store Rx steering angles in the `beam_depress_angle` field, a "kloodge" (workaround) is applied to ensure the repointed angles are written back correctly.
4.  **In-Place Update:** The corrected Tx and Rx steering angles are written back to the respective `Tx_steer` and `Rc_steer` fields (or `beam_depress_angle` for kloodged sonars) in the beam structures of the merged file. The `td_sound_speed` or `soundVelocity` in the profile header is also updated to the `new_ssp`.
