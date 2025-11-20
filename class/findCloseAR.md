---
layout: default
title: findCloseAR
parent: Classification Tools
nav_order: 4
---
# findCloseAR

## Description
`findCloseAR` is a command-line utility that searches through multiple Angular Response (AR) files to find AR records that are geographically close to a given list of sample station coordinates. It takes a list of sample locations (latitude/longitude) and a search radius, then identifies AR records falling within that radius. The primary output is a file detailing which AR records (file number, record number, side) are close to each sample station.

## Usage
```bash
findCloseAR [OPTIONS] -samples <sample_file> -radius <meters> -arnames <ar_list_file>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-samples <sample_file>` | **Required.** An ASCII file containing sample station coordinates and possibly other geological parameters. The tool expects latitude and longitude as the first two values per line. | `geological_samples.txt` |
| `-radius <meters>` | Specifies the search radius (in meters) around each sample station. AR records within this radius are considered "close". | `100.0` |
| `-arnames <ar_list_file>` | **Required.** An ASCII file listing the paths to all Angular Response (AR) files to be searched. | `list_of_AR_files.txt` |
