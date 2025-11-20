---
layout: default
title: attedit
parent: Attitude Tools
nav_order: 4
---
# attedit

## Description
`attedit` is a command-line utility designed to display and potentially edit information within an OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) attitude record file. It can perform various checks on the data, fix specific issues like negative time differences or midnight rollovers, and allows for interactive browsing and basic editing of individual attitude records.

## Usage
```bash
attedit [OPTIONS] <filename>.orientation
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-check` | Performs checks on the attitude file, reporting minimum and maximum time differences between records, typical frequency, and the number of negative time differences. | |
| `-remove_negative` | Creates a new attitude file (with `.fixed` appended to the filename) where records with non-positive time differences (indicating a time jump backward or no change) are removed. | |
| `-day_shift <value>` | Shifts the reference time of the attitude file by a specified number of days. **Warning: This modifies the file's header directly.** | `1` |
| `-fix_midnight` | Attempts to fix issues where time offsets might wrap around midnight, causing large negative time differences. | |
| `-v` | Enable verbose output during checks. | |
| `<filename>.orientation` | **Required.** The input OMG-HDCS `.orientation` file to be displayed or edited. | `mydata.orientation` |
