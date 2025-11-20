---
layout: default
title: mergeHeading
parent: Attitude Tools
nav_order: 7
---
# mergeHeading

## Description
`mergeHeading` is a command-line utility that merges heading data from a separate gyro file (e.g., from a more accurate or different heading sensor) onto an existing OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) attitude file. It interpolates the heading values from the gyro file based on time and updates the attitude records in the primary orientation file. The output is a new orientation file with the merged heading.

## Usage
```bash
mergeHeading [OPTIONS] -hdg <gyro_file> <orientation_file>
```
The output file will be named `<orientation_file>_with_hdg`.

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-hdg <gyro_file>` | **Required.** Specifies the input gyro file containing heading data. This file is assumed to be in OMG-HDCS `.orientation` format, although it primarily provides heading. | `my_gyro.orientation` |
| `<orientation_file>` | **Required.** The input OMG-HDCS `.orientation` file to which the heading data will be merged. | `original_attitude.orientation` |
