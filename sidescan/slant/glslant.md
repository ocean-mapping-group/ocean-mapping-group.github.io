---
layout: default
title: glslant
parent: Slant Tools
grand_parent: sidescan
nav_order: 3
---
# glslant

## Description
`glslant` is a utility designed to perform slant-range correction on JCU GLORIA format sidescan files. It takes an input GLORIA file, corrects the imagery for slant range distortion based on the vehicle's altitude, a specified pixel size, and the sound speed in water, and then outputs a new GLORIA file with the corrected imagery. It allows for optional pixel skipping on the port and starboard sides.

## Usage
```bash
glslant [-V] [-v <sound_speed>] [-l <port_skip>] [-r <stbd_skip>] [-p <pixel_size>] <infile> <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `-V` | Enable verbose output, printing progress messages. |
| `-v <sound_speed>` | Specifies the sound speed in water (in m/s). | `1500.0` |
| `-l <port_skip>` | Specifies the number of pixels to skip on the port side. | `0` |
| `-r <stbd_skip>` | Specifies the number of pixels to skip on the starboard side. | `0` |
| `-p <pixel_size>` | Specifies the resultant pixel size (in meters) after correction. | `90` |
| `<infile>` | **Required.** The input JCU GLORIA file to be slant-range corrected. |
| `<outfile>` | **Required.** The output JCU GLORIA file with slant-range corrected imagery. |

## How It Works
1.  **Argument Parsing:** The tool parses command-line arguments to configure sound speed, pixel skipping, and output pixel size.
2.  **File Opening:** It opens the input GLORIA file (`infd`) for reading and the output GLORIA file (`outfd`) for writing.
3.  **Record Processing Loop:** The tool reads each GLORIA record (`gl_in`) from the input file:
    *   **Header Copy:** The header information from `gl_in` is copied to `gl_out`.
    *   **Slant-Range Correction for Each Pixel:** For each pixel `j` across the swath (from 0 to 511):
        *   **Across-Track Distance:** `offset` is calculated as the ground distance from the nadir to the pixel (`((float)j + 0.5) * pixel_size`).
        *   **Slant Range:** The `slant_range` to the seafloor is calculated using the Pythagorean theorem: `sqrt(offset^2 + gl_out.header.altitude^2)`.
        *   **Time of Arrival:** `time` is calculated as `2 * slant_range / sound_speed`.
        *   **Original Pixel Index:** `pixel` is the index in the original (un-corrected) image data that corresponds to `time`. This conversion uses either `gl_out.header.small_pixel` or `gl_out.header.ping_rate`.
        *   **Data Transfer:**
            *   If `pixel` is within the valid range and considering `stbd_skip`, the pixel value from `gl_in.stbd_data` at the calculated original index is copied to `gl_out.stbd_data`.
            *   Similarly for the port side, considering `port_skip`.
            *   If `pixel` falls outside valid bounds (e.g., beyond the swath or after skipping), the output pixel is set to 255 (invalid).
    *   **Output Header Update:** `gl_out.header.pixel_size` is set to 0, and `gl_out.header.small_pixel` is updated to the new `pixel_size`.
    *   **Write Record:** The corrected `gl_out` record is written to the output file.
4.  **Loop:** This process repeats until all records in the input file have been processed.
5.  **Error Exit (`err_exit`):** A helper function to print usage information and exit on error.
