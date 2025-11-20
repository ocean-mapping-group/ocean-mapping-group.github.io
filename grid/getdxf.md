---
layout: default
title: getdxf
parent: Grid Tools
nav_order: 34
---
# getdxf

## Description
`getdxf` is a legacy command-line utility for reformatting specialized ASCII coordinate data streams, likely originating from or intended for DXF (Drawing Exchange Format) files. The tool reads text from standard input, parses it according to a specific hardcoded logic, and writes the formatted coordinates to standard output.

This tool is designed for very specific data-massaging tasks and is not a general-purpose format converter.

## Usage
```bash
getdxf [OPTIONS] < input_file > output_file
```

## Arguments

| Option | Description |
|---|---|
| `-ll` | Switches the parsing logic to a Lat/Lon mode. It looks for pairs of numbers where the first is between -60 and -80 (longitude) and the second is between 30 and 50 (latitude). |
| `-merid <longitude>` | Specifies a central meridian. (Note: This appears to be a legacy option and may not be used in the current processing logic). |

## Modes of Operation

### Default (DXF-like) Mode
In its default mode, `getdxf` parses an ASCII stream looking for specific key-value pairs:
1.  It searches for a line containing the number `10`.
2.  It reads the number on the *following* line as an "X" coordinate.
3.  It searches for a line containing the number `20`.
4.  It reads the number on the *following* line as a "Y" coordinate.
5.  It prints the extracted coordinates to standard output as `X Y 0.0`.

### Lat/Lon Mode (`-ll`)
When the `-ll` flag is used, the tool reads a stream of numbers and applies a hardcoded geographic filter:
1. It reads a number. If it is between -60 and -80, it's considered a longitude.
2. It then reads the next number. If it is between 30 and 50, it's considered a latitude.
3. If both conditions are met, it prints the pair to standard output as `latitude longitude 0.0`.
