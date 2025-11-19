# heaveCombo

## Description
`heaveCombo` is a specialized command-line utility designed to combine heave data from two near-synchronous OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) attitude streams. It primarily aims to merge one stream with "delayed heave" and another with "real-time heave," bringing over Roll, Pitch, Heading (RPGH) from a reference file and interpolating heave from another. The output is a new attitude file that consolidates the best available data from both sources.

## Usage
```bash
heaveCombo [OPTIONS] -ref <ref_att_file> -other <other_att_file> -out <output_att_file>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-ref <ref_att_file>` | **Required.** Specifies the reference attitude file. RPGH (Roll, Pitch, Heading) data will primarily be taken from this file. | `seapath_realtime.orientation` |
| `-other <other_att_file>` | **Required.** Specifies the "other" attitude file, typically containing delayed or interpolated heave data to be blended with the reference. | `delayed_heave.orientation` |
| `-out <output_att_file>` | **Required.** Specifies the name of the output `.orientation` file where the combined attitude data will be written. | `combined_heave.orientation` |