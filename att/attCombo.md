# attCombo

## Description
`attCombo` blends two near-synchronous OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) attitude streams (e.g., from different sensors like F180 and MRU-6) into a single, combined attitude file. It allows for combining high-frequency (HF) and low-frequency (LF) components of roll, pitch, and heave from either of the two input files, or setting them to zero. Heading is selected from one of the two sources without blending. The tool uses a cosine-tapered time-domain filter for blending.

## Usage
```bash
attCombo [OPTIONS] <basename>
```
Where `<basename>` refers to attitude files named `<basename>_1.orientation` and `<basename>_2.orientation`. The output file will be named `<basename>_3.orientation` (or `<basename>_3ascii` if `-ascii` is used).

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-ascii` | Output the combined attitude data in ASCII format instead of a binary `.orientation` file. | |
| `-filt_length <seconds>` | Specifies the length (in seconds) of the cosine-tapered time-domain filter used for blending HF and LF components. | `20.0` |
| `-which_heading <source>` | Selects the source for the output heading. `1` for the first input file (`_1`), `2` for the second input file (`_2`), `0` for zero. | `1` |
| `-roll_hf <source>` | Selects the source for the high-frequency (HF) roll component. `1` for `_1`, `2` for `_2`, `0` for zero. | `1` |
| `-roll_lf <source>` | Selects the source for the low-frequency (LF) roll component. `1` for `_1`, `2` for `_2`, `0` for zero. | `1` |
| `-pitch_hf <source>` | Selects the source for the high-frequency (HF) pitch component. `1` for `_1`, `2` for `_2`, `0` for zero. | `1` |
| `-pitch_lf <source>` | Selects the source for the low-frequency (LF) pitch component. `1` for `_1`, `2` for `_2`, `0` for zero. | `1` |
| `-heave_hf <source>` | Selects the source for the high-frequency (HF) heave component. `1` for `_1`, `2` for `_2`, `0` for zero. | `1` |
| `-heave_lf <source>` | Selects the source for the low-frequency (LF) heave component. `1` for `_1`, `2` for `_2`, `0` for zero. | `1` |
| `<basename>` | **Required.** The base name for the input attitude files (e.g., `survey`). The tool expects `survey_1.orientation` and `survey_2.orientation` as input. | `survey` |