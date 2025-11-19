# attSplit

## Description
`attSplit` is a command-line utility designed to separate a single OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) attitude record file into two distinct output files. This tool is useful when a single file contains data from two different orientation sensors (e.g., pushed into one file), and there are identifiable time gaps or negative time differences between consecutive records, which it uses as a heuristic to differentiate the streams.

## Usage
```bash
attSplit [OPTIONS] <filename>.orientation
```
The input file is `<filename>.orientation`. The output files will be named `<filename>_1.orientation` and `<filename>_2.orientation` (or `<filename>_1ascii` and `<filename>_2ascii` if `-ascii` is used).

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-check` | Enables a check mode that reports when records are not written out, useful for debugging the splitting logic. | |
| `-ascii` | Outputs the split attitude data into two ASCII files (`_1ascii` and `_2ascii`) instead of binary `.orientation` files. | |
| `<filename>.orientation` | **Required.** The input OMG-HDCS `.orientation` file containing combined attitude data. | `combined_attitude.orientation` |