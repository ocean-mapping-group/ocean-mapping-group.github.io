---
layout: default
title: filterAerial
parent: Optech Tools
nav_order: 112
---
# filterAerial

## Description
`filterAerial` is a utility designed to process multiple 8-bit aerial image files (presumably representing intensity or depth data, potentially from Optech systems) and compute an average image. This average image can then be used to remove low-frequency noise, such as solar radiation effects, from individual aerial photographs.

The tool reads multiple input 8-bit image files, sums their pixel values, and then divides by the number of input files to get an average for each pixel.

## Usage
```bash
filterAerial -out <outfile> <8bitfile(s)>
```

## Arguments

| Option | Description |
|---|---|
| `-out <outfile>` | **Required.** The path for the output averaged 8-bit image file. |
| `<8bitfile(s)>` | **Required.** One or more paths to input 8-bit image files. All input files are assumed to have identical dimensions and JHC headers. |

## How It Works
1.  **Initialization:** Initializes variables and an array `sum_matrix` (1201x1601) to accumulate pixel sums.
2.  **Output File Creation:** Creates the specified output file (`-out`) for writing the averaged image.
3.  **Header Processing:**
    *   Opens the first input 8-bit image file to read its JHC header (`head_in`).
    *   Copies `head_in` to `head_out` (which will be the header for the output file).
    *   Verifies that `head_in.data_type` is 1 (indicating an 8-bit file).
    *   Allocates memory for `fout` (output row buffer) and `fsum` (row sum buffer, though `sum_matrix` is used for 2D sums).
    *   Writes `head_out` to the `outfile`.
4.  **Input File Iteration (Accumulate Pixel Sums):** Loops through each input 8-bit image file:
    *   Opens the current input file.
    *   Reads its JHC header (`head_in`) (ensuring consistency in case headers differ subtly between inputs, though dimensions are assumed identical).
    *   Allocates memory for `fin` (input row buffer).
    *   Iterates through each row (`i`) and column (`j`) of the image:
        *   Reads a row of pixel data into `fin`.
        *   Adds the value of each pixel `*(fin + j)` to `sum_matrix[i][j]`.
    *   Closes the current input file.
5.  **Average Pixel Values and Write Output:**
    *   Seeks to the data section of the `outfile` (after the JHC header).
    *   Iterates through each row (`i`) and column (`j`) of the image:
        *   Calculates the average pixel value `(unsigned char)(sum_matrix[i][j] / noin)`.
        *   Writes this averaged pixel value to `fout`.
        *   After processing a row, writes `fout` to `outfile`.
6.  **Cleanup:** Closes the output file.
```