# mergeHeave

## Description
`mergeHeave` is a command-line utility designed to merge heave data from a separate source onto either an OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) merged bathymetry file (`.merged` for swath) or a tide file (`.bin` for tide). This tool is crucial for correcting depth measurements by applying accurate heave information, often from a dedicated heave sensor. It can either apply the heave correction to the profile header or directly to the individual beam depths in a swath file, and can also invert the heave scale.

## Usage
```bash
mergeHeave [OPTIONS] -heave <heave_file> [-swath <merged_file> | -tide <tide_file>]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-jb` | Use a faster interpolation method (`jb_OMG_HDCS_interpolated_async`) for looking up heave data. | |
| `-delay <seconds>` | Apply a time delay (in seconds) to the heave data before merging. | `0.05` |
| `-time_limit <seconds>` | Maximum time difference (in seconds) between samples to allow for interpolation over. If exceeded, heave is not applied. | `1.0` |
| `-heavescale <factor>` | Apply a scaling factor to the heave values. Can be used to invert heave (e.g., `-1.0`). | `-1.0` |
| `-apply_dheave` | Applies the heave correction directly to the individual beam depths within a swath file, rather than to the profile header. This functionality is enabled. | |
| `-use_realtime_heave` | Uses real-time heave values instead of delayed heave. This applies to both swath and tide modes. | |
| `-get_heave_from_merged` | (Specific to swath files) Uses the heave already present in the merged file's profile header as the reference heave for calculating the correction. | |
| `-heave <heave_file>` | **Required.** Specifies the input file containing heave data. This is typically an OMG-HDCS `.orientation` file or similar. | `my_heave.orientation` |
| `-swath <merged_file>` | Specifies an OMG-HDCS merged bathymetry file (`.merged`) to apply heave corrections to. Mutually exclusive with `-tide`. | `my_survey.merged` |
| `-tide <tide_file>` | Specifies a tide file (`.bin`) to apply heave corrections to (e.g., removing heave from GPS tide data). Mutually exclusive with `-swath`. | `my_tide.bin` |