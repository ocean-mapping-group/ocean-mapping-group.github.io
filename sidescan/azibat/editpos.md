---
layout: default
title: editpos
parent: Sidescan Tools
grand_parent: azibat
nav_order: 4
---
# editpos

## Description
`editpos` is a utility used to edit the position fixes of a JCU format sidescan image. It looks for bad position jumps and corrects the fix position.

## Usage
```bash
editpos [-v] [-t <threshold>] <infile>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-t <threshold>` | This option is present in the `USAGE` string but is not implemented in the `main` function. |
| `<infile>` | **Required.** The input JCU format sidescan file. This file is modified in place. |

## How It Works
The tool iterates through the records in the input file and checks for large jumps in position. It calculates the change in latitude and longitude between consecutive records and if the change is greater than 500 meters, it considers it a bad fix. It then corrects the position by interpolating the latitude and longitude between the previous and next valid records. The corrected record is then written back to the file.
