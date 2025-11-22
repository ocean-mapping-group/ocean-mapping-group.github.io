---
layout: default
title: restructure_glo
parent: Convert Tools
grand_parent: sidescan
nav_order: 3
---
# restructure_glo

## Description
`restructure_glo` is a utility designed to restructure a merged JCU format GLORIA file from an Apollo header structure (128 bytes) to a SUN header structure (136 bytes). This conversion involves shifting various data blocks within each record to accommodate the larger header size.

## Usage
```bash
restructure_glo -in <infile> -out <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `-in <infile>` | **Required.** The input JCU GLORIA file in Apollo structure. |
| `-out <outfile>` | **Required.** The output JCU GLORIA file in SUN structure. |

## How It Works
1.  **Read Input File Size:** The tool first determines the number of records in the input Apollo GLORIA file based on its file size and the Apollo record length (1152 bytes).
2.  **Allocate Memory:** It allocates memory for `in_record` (1152 bytes) and `out_record` (1160 bytes) buffers.
3.  **Process Records:** The tool iterates through each record in the input file:
    *   It reads 1152 bytes of the Apollo record into `in_record`.
    *   It then copies data blocks from `in_record` to `out_record` with specific offsets to accommodate the 136-byte SUN header. This essentially "shunts" the data along to make space for the larger header. The process is manual, copying specific byte ranges.
    *   The restructured `out_record` (1160 bytes) is written to the output file.
4.  **Loop:** This process repeats until all records from the input file have been restructured and written to the output file.
