---
layout: default
title: getdxf
parent: Grid Tools
nav_order: 34
---
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
Input data is read from `stdin` and output is written to `stdout`.

## Arguments

| Option | Description |
|---|---|
| `-ll` | Switches the parsing logic to a Lat/Lon mode. It looks for pairs of numbers where the first is between -60 and -80 (longitude) and the second is between 30 and 50 (latitude). |
| `-merid <longitude>` | Specifies a central meridian. (Note: This appears to be a legacy option and may not be used in the current processing logic). |

## How It Works
The tool reads ASCII data line by line from standard input and processes it based on the specified mode.

### Default (DXF-like) Mode
1.  It searches for a line containing the number `10`.
2.  It reads the number on the *following* line as an "X" coordinate.
3.  It searches for a line containing the number `20`.
4.  It reads the number on the *following* line as a "Y" coordinate.
5.  It prints the extracted coordinates to standard output as `X Y 0.0`.

### Lat/Lon Mode (`-ll`)
1.  It reads numbers from the input stream.
2.  If a number falls between -60 and -80, it's considered a potential longitude.
3.  The next number read is then checked if it falls between 30 and 50; if so, it's considered a potential latitude.
4.  If both conditions are met, it prints the pair to standard output as `latitude longitude 0.0`.

## Output Files
The tool writes formatted coordinates to standard output. This output can be redirected to a file.

## Dependencies
*   Standard C library functions for input/output and string manipulation.

## Notes
This is a highly specialized utility with hardcoded parsing logic, reflecting its use for very specific legacy data formats. Its utility is limited to matching these precise input patterns. The `-merid` option is present in the usage but its actual effect in the provided code snippet is unclear, suggesting it might be a remnant or non-functional.
