---
layout: default
title: editfix
parent: Sidescan Tools
grand_parent: azibat
nav_order: 3
---
# editfix

## Description
`editfix` is a utility used to edit the fixes of a JCU format sidescan image. It looks for bad time jumps and corrects the time and fix position.

## Usage
```bash
editfix [-v] [-t <threshold>] <infile>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-t <threshold>` | This option is present in the `USAGE` string but is not implemented in the `main` function. |
| `<infile>` | **Required.** The input JCU format sidescan file. This file is modified in place. |

## How It Works
The tool iterates through the records in the input file and checks for time jumps (i.e., if the timestamp of the current record is less than the previous one). If a time jump is detected, it corrects the timestamp of the current record by adding 30 seconds to the previous record's timestamp. It also interpolates the latitude and longitude of the current record based on the previous and next records. The altitude is replaced with the previous record's altitude. The corrected record is then written back to the file.
