# DTMreject

## Description
`DTMreject` is a quality control utility for automated cleaning of multibeam sonar data. It processes one or more OMG-HDCS merged files and compares the depth of each individual beam against a reference Digital Terrain Model (DTM) grid. If a beam's depth differs from the interpolated depth of the reference DTM by more than a user-specified threshold, the beam's status is flagged as invalid within the merged file.

This tool is essential for identifying and rejecting flyers or systematic biases in survey lines by comparing them against a trusted, previously established surface.

## Usage
```bash
DTMreject -area <reference_dtm.r4> -away <threshold_meters> [OPTIONS] <merged_file(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-area <reference_dtm.r4>` | **Required.** Specifies the path to the JHC-format 32-bit floating-point (`.r4`) grid file to be used as the reference DTM. | `-area master_surface.r4` |
| `-away <threshold_meters>` | **Required.** Sets the maximum allowable difference (in meters) between a beam's measured depth and the corresponding depth from the reference DTM. If the absolute difference `|DTM_depth - beam_depth|` exceeds this value, the beam is flagged. | `-away 2.5` |
| `<merged_file(s)>` | **Required.** One or more OMG-HDCS merged files to be processed. The tool modifies these files in place. | `line_001.merged line_002.merged` |
| `-just_show` | Performs a "dry run". The tool will identify and report the beams it would reject but will not make any actual modifications to the input merged files. | |
| `-from_scratch` | Before running the comparison, this option resets the status of all beams in the file to 0. This is useful for ensuring a fresh flagging pass, removing any flags set by previous processing steps. | |
| `-tide` | If specified, the tool applies the tide correction value found in each profile's header to the beam's observed depth before comparing it to the DTM. | |
| `-list_changes` | If specified, creates an ASCII file for each input merged file, named `<merged_filename_prefix>.DTM_reject_changes`, which contains a list of all rejected beams (lat, lon, depth, beam number). | |
| `-v` | Enable verbose output during processing. | |

## How it Works
For each beam in a merged file, `DTMreject` calculates its geographic position, projects it onto the reference DTM grid, and uses bilinear interpolation to find the precise reference depth at that location. It then computes the difference between the beam's depth and the reference depth. If this difference is larger than the `-away` threshold, the beam's status flag is set to `22` (rejected by DTM).
