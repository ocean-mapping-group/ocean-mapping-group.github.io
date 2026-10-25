---
layout: default
title: fcv30-2glo
parent: Knudsen Tools
nav_order: 3
tool_name: fcv30-2glo
source_path: knudsen/fcv30-2glo.c
category: format_conversion
input_formats: [HAC_FCV30]
output_formats: [OMG_HDCS, OMG_SS_DATA, JCU_NAV, BINARY_RASTER]
related_tools: [knud2glo, readEA600, makeSeisPlot]
---

# fcv30-2glo

## Overview

`fcv30-2glo` converts hydroacoustic `.hac` tuple files recorded by a **Furuno FCV-30** split-beam scientific echosounder into either OMG HDCS v3 `.merged` and `.merged.ss_data` files (`-omg`) or 5-channel raw raster files (`.chan1`–`.chan5`), along with a JCU binary navigation file (`.nav`).

## Usage

```
fcv30-2glo (-v) (-omg) (-in infile | -ins infile1 [infile2 ...]) -out outfile_prefix
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<infile>` | *required* (or `-ins`) | Single input Furuno FCV-30 `.hac` file. |
| `-ins` | `<file1> [file2 ...]` | none | Multiple input `.hac` files (must be placed at the end of the command line as it consumes all remaining arguments). |
| `-out` | `<outfile_prefix>` | *required* | Output file prefix for `.nav` and either `.merged`/`.merged.ss_data` (`-omg`) or `.chan1`–`.chan5`. |
| `-omg` | none | `0` | Output OMG HDCS v3 `.merged` (`toolType = Knudsen_320`, 2 beams) and 8-bit `.merged.ss_data` instead of `.chan1`–`.chan5`. |
| `-v` | none | `0` | Enable verbose diagnostic output. |

## How It Works

1. **HAC Header Verification**: Reads the initial 4-byte HAC magic word (`0x000000AC` = `172`) to verify byte order and iterates through variable-length tuples (`tuple_size`, `tuple_type`, payload, and 4-byte backlink).
2. **Tuple Decoding**:
   - **Tuple 20 (`fcv30_position`)**: Extracts GPS epoch seconds (`gps_time`), `0.0001 s` fraction, and `0.000001°` latitude/longitude (`lat`, `lon`), writing unique position updates to `<outfile_prefix>.nav`.
   - **Tuple 9001 (`fcv30_channel`)**: Reads channel sampling rate, frequency, TVG parameters, transducer offsets, beamwidth, and calibration settings (`read_fcv30_channel()`).
   - **Tuple 10000 (`fcv30_ping`)**: Unpacks 32-bit sample sequence numbers and sample values (`0.000001` dB or volts), converts to dB (`samp_dB`) and 8-bit unsigned bytes (`char_dB` mapped across `[-120, 0]` dB), extracts bottom detection range (`bottom_detect * 0.001` m), and writes either `.chan1`–`.chan5` or OMG HDCS `.merged` and `.merged.ss_data`.

## Practical Examples

### Convert multiple Furuno FCV-30 `.hac` files to OMG HDCS format

```bash
fcv30-2glo -v -omg -out fcv30_survey -ins file001.hac file002.hac file003.hac
```
