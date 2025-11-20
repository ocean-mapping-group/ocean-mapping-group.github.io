---
layout: default
title: fixarray
parent: Grid Tools
nav_order: 33
---
# fixarray

## Description
`fixarray` is a command-line utility for converting legacy JHC grid files into the modern, standardized "OMG1" JHC grid format. The tool reads the header information from an old-format binary array, creates a new standard 1024-byte JHC header, and combines it with the original data into a new, compliant file.

This tool is primarily used for data archeology to ensure backward compatibility with older datasets.

## Usage
```bash
fixarray [-really_old] <-8bit | -float> <badfile> <goodfile>
```

## Arguments

| Option | Description |
|---|---|
| `<badfile>` | **Required.** The path to the input legacy JHC-format grid file. |
| `<goodfile>` | **Required.** The path for the new, corrected, standard-format JHC grid file. |
| `-8bit` | **Required (or `-float`).** Specifies that the data type of the input file is 8-bit character. |
| `-float` | **Required (or `-8bit`).** Specifies that the data type of the input file is 32-bit float. |
| `-really_old` | A flag indicating the input file is from a very old format that is missing the `ystep` (Y pixel size) field in its header. If this is set, the tool assumes `ystep` is equal to `xstep`. |
| `-v` | Enable verbose output. |
