---
layout: default
title: glsmudge
parent: Destripe Tools
grand_parent: sidescan
nav_order: 8
---
# glsmudge

## Description
`glsmudge` is a utility designed to "smudge" the low-pass data of a JCU GLORIA format sidescan file. This process aims to remove long-wavelength stripes by linearly interpolating the pixel intensities between two specified reference records (`-first` and `-last`). This is typically applied to the `.low` component resulting from a destriping operation.

## Usage
```bash
glsmudge [-first <record_number>] [-last <record_number>] <infile_prefix>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-first <record_number>` | Specifies the record number to use as the "before" reference for smudging. | `0` |
| `-last <record_number>` | Specifies the record number to use as the "after" reference for smudging. | `0` |
| `<infile_prefix>` | **Required.** The prefix for the input GLORIA low-pass file. The tool assumes the input file has a `.low` extension. The output file will have a `.low_smudge` extension. |

## How It Works
1.  **Input Files:** The tool takes a single JCU GLORIA low-pass file (e.g., `<infile_prefix>.low`) as input.
2.  **Reference Records:**
    *   It seeks to the records specified by `-first` and `-last` and reads them into `before_rec` and `after_rec` respectively. These records serve as the fixed endpoints for the linear interpolation.
3.  **Linear Interpolation:** For each record `i` between the `first` and `last` records (exclusive):
    *   It calculates `before_weight` and `after_weight` based on the current record's position relative to `first` and `last`.
    *   For each pixel (`j`) in the `all_data` array of the current record (`out_rec`):
        *   The pixel's new intensity is calculated as a linear interpolation between the corresponding pixels in `before_rec` and `after_rec`, using `before_weight` and `after_weight`.
        `out_rec.all_data[j] = (unsigned char) ((float) before_rec.all_data[j] * after_weight + (float) after_rec.all_data[j] * before_weight);`
    *   Records outside the `first` and `last` range are written directly without modification.
4.  **Write Output:** The processed (or copied) record (`out_rec`) is written to the output file (e.g., `<infile_prefix>.low_smudge`).
5.  **Loop:** This process repeats for all records in the input file.
