---
layout: default
title: glreplace
parent: Destripe Tools
grand_parent: sidescan
nav_order: 7
---
# glreplace

## Description
`glreplace` is a utility designed to replace the image data (sidescan pixel values) of one JCU GLORIA format file with the image data from a second GLORIA file, while retaining the header information from the first file. This effectively allows for updating the imagery of a GLORIA file without altering its navigational or other metadata.

## Usage
```bash
glreplace <header_file> <image_file> <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `<header_file>` | **Required.** The input JCU GLORIA file whose header information will be retained. |
| `<image_file>` | **Required.** The input JCU GLORIA file whose image data will be used for replacement. |
| `<outfile>` | **Required.** The output JCU GLORIA file with the header from `<header_file>` and image data from `<image_file>`. |

## How It Works
1.  **Input Files:** The tool takes two JCU GLORIA files as input:
    *   `infile1` (referred to as `<header_file>`)
    *   `infile2` (referred to as `<image_file>`)
2.  **Output File:** It creates a new output JCU GLORIA file (`outfile`).
3.  **File Length Check:** It determines the number of records in `infile1` and assumes `infile2` has the same number of records.
4.  **Record-by-Record Processing:** For each corresponding record in the input files:
    *   It reads a record from `infile1` into `in_rec1`.
    *   It reads a record from `infile2` into `in_rec2`.
    *   It first copies the entire content of `in_rec2` to `out_rec`. This means `out_rec` initially contains the header and image data from `image_file`.
    *   Then, it copies *only* the header portion (`HEADER_LENGTH` or `sizeof(jcu_all_rec)`) from `in_rec1` to `out_rec`. This overwrites the header from `image_file` with the header from `header_file`, while retaining the image data (port and starboard arrays) that was copied from `image_file`.
    *   The resulting `out_rec` now contains the header from `header_file` and the image data from `image_file`.
5.  **Write Output:** The `out_rec` is written to the output file.
6.  **Loop:** This process repeats until all records from both input files have been processed.
