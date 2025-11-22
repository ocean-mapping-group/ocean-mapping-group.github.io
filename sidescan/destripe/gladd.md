---
layout: default
title: gladd
parent: Destripe Tools
grand_parent: sidescan
nav_order: 3
---
# gladd

## Description
`gladd` is a utility designed to combine two JCU GLORIA format merged sidescan files. It was originally developed for destriping purposes, allowing for the addition of high and low-frequency components. A more recent use case involves removing the topographic component of backscatter, often by combining a backscatter (BS) file with a grazing angle (graz) file.

## Usage
**Original Usage (Destriping):**
```bash
gladd <infile_prefix>
```
(Assumes `<infile_prefix>.high`, `<infile_prefix>.low`, `<infile_prefix>.mer` exist, and outputs to `<infile_prefix>.des`)

**General Usage (2015 version):**
```bash
gladd -degraz -bs <bs_file> -graz <graz_file> -out <outfile> [-retain255]
```

## Arguments

| Option | Description |
|---|---|
| `-weight1 <value>` | Weight for the first input file (not currently implemented in the main logic). |
| `-weight2 <value>` | Weight for the second input file (not currently implemented in the main logic). |
| `-replace` | If specified, the output will simply be a copy of the second input file (`in_rec2`). |
| `-retain255` | If specified, any pixel in the original undestriped file (`.mer`) that had a value of 255 (unassigned) will also be 255 in the output. Requires the original file to be present. |
| `-degraz` | Use the de-grazing logic: `output = bs_file - (128 - graz_file)`. This mode requires `-bs` and `-graz` and produces a topographic-corrected backscatter image. |
| `-bs <bs_file>` | Input backscatter file (used with `-degraz`). |
| `-graz <graz_file>` | Input grazing angle file (used with `-degraz`). |
| `-out <outfile>` | Output JCU GLORIA file. |
| `<infile_prefix>` | **(Original Usage)** The prefix for input files. The tool expects `<infile_prefix>.high` and `<infile_prefix>.low` as input, and `<infile_prefix>.mer` if `-retain255` is used. Output will be `<infile_prefix>.des`. |

## How It Works
The tool operates in two main modes, either a legacy destriping mode or a more modern de-grazing mode.

**Legacy Destriping Mode (when using `<infile_prefix>`):**
1.  **Input Files:** Reads three files: `<infile_prefix>.high` (high-frequency component), `<infile_prefix>.low` (low-frequency component), and optionally `<infile_prefix>.mer` (original merged file for `-retain255`).
2.  **Pixel-wise Addition:** For each corresponding pixel across all records:
    *   It adds the high-frequency component (`in_rec1`) to the low-frequency component (`in_rec2`), after subtracting 128 from `in_rec1` (assuming `in_rec1` is a difference image centered around 128).
    *   `stbd_value = (int)in_rec1.stbd_data[k] - 128 + (int)in_rec2.stbd_data[k];`
    *   The result is clamped between 0 and 254.
3.  **Retain 255:** If `-retain255` is specified, any pixel that was 255 in the original `.mer` file is set to 255 in the output.

**General Usage / De-grazing Mode (when using `-degraz`):**
1.  **Input Files:** Reads two files: a backscatter file (`-bs <bs_file>`) and a grazing angle file (`-graz <graz_file>`).
2.  **Pixel-wise Correction:** For each corresponding pixel across all records:
    *   If the pixel in the grazing angle file (`in_rec2`) is not 255:
        *   It calculates a correction factor based on the grazing angle file: `corr = 128 - (int)in_rec2.stbd_data[k]`.
        *   It subtracts this correction from the backscatter value: `outbs = inbs - corr;`.
        *   The result is clamped between 1 and 254.
    *   If the grazing angle pixel is 255, the output backscatter pixel is also 255.
3.  **Output:** The corrected backscatter data is written to the specified output file (`-out <outfile>`).

**`replace` Option:**
*   If `-replace` is used, the tool simply copies the contents of the second input file (`in_rec2` or `-graz <graz_file>`) directly to the output file, ignoring other processing logic.
