---
layout: default
title: readSB_SEGY
parent: SEGY Tools
nav_order: 3
tool_name: readSB_SEGY
source_path: segy/readSB_SEGY.c
category: format_conversion
input_formats: [SEGY]
output_formats: [OMG_HDCS, OMG_SS_DATA, JCU_NAV, BINARY_RASTER]
related_tools: [upKnudSEGY, upsegy, upAGCDIG, makeSeisPlot]
---

# readSB_SEGY

## Overview

`readSB_SEGY` unpacks single- or multi-beam sub-bottom profiler data stored in SEG-Y format—originally written for the SeaBeam 2112.04 4 kHz sub-bottom profiler and later extended to support Kongsberg SBP 120 (`-sbp120_ll`, `-just_cdp`), SonarWiz heave-tagged SEG-Y (`-extract_heave`), and AUV sub-bottom datasets (`-get_AUV_depth`). It outputs 8-bit waterfall trace imagery (`.chan1`), binary navigation (`.nav`), and optionally full OMG HDCS v1 sub-bottom files (`.merged`, `.merged.ss_data`, and `.merged.fl_data` / `.merged.16_data` / `.merged.32_data`) via `-out_as_OMG`.

## Usage

```
readSB_SEGY (-v) (-log | -lin | -sqrt) (-hilbert) (-log_range 25) \
            (-extra_nttr 13) (-nohead) (-show_rawtrace | -minMS 800 -maxMS 1000 | -mindepth 50 -maxdepth 300) \
            (-just_cdp 0) (-nosam 500) (-force_year 2016) \
            (-richardo_ll -sbp120_ll -fliplong) (-extract_heave -use_rwdepth) (-get_AUV_depth) \
            (-min 1 -max 2048 -autoscale -autoplus -skipblanktrace) \
            (-isfloat | -isshort | -isint) (-out_as_OMG) \
            (-inpath ../raw/area/) -in infile(s) -out outfile_prefix
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<file1> [file2 ...]` | *required* | One or more input SEG-Y files. |
| `-out` | `<outfile_prefix>` | *required* | Output file prefix for `.chan1`, `.nav`, and (with `-out_as_OMG`) `.merged` and `.merged.*_data`. |
| `-inpath` | `<dir_path>` | none | Directory path prepended to every filename listed after `-in`. |
| `-out_as_OMG` | none | `0` | Write OMG HDCS v1 `.merged` (`toolType = Knudsen_320`, 2 beams), `.merged.ss_data` (8-bit), and `.merged.fl_data` / `.16_data` / `.32_data`. Also enables `-show_rawtrace`. |
| `-isfloat` | none | *default* | Input SEG-Y trace samples are 32-bit IEEE floats (`ISFLOAT`). |
| `-isshort` | none | `0` | Input SEG-Y trace samples are 16-bit integers (`ISSHORT`). |
| `-isint` | none | `0` | Input SEG-Y trace samples are 32-bit integers (`ISINT`). |
| `-nohead` | none | `0` | Skip the 3600-byte (3200 EBCDIC + 400 binary) SEG-Y tape header at the start of each file. |
| `-lin` | none | *default* | Use linear amplitude scaling to 8-bit. |
| `-log` | none | `0` | Use logarithmic amplitude scaling to 8-bit. |
| `-sqrt` | none | `0` | Use square-root amplitude scaling to 8-bit. |
| `-log_range` | `<dB>` | `1000.0` | Dynamic range in dB for logarithmic compression. |
| `-hilbert` | none | `0` | Apply a Hilbert transform envelope detector (`do_Hilbert = 1`) to bipolar waveform traces. |
| `-show_rawtrace` | none | `0` | Output raw trace samples directly without depth/millisecond window resampling. |
| `-minMS` / `-maxMS` | `<ms>` | `0` / `1000` | Minimum and maximum two-way travel time window in milliseconds for `.chan1` raster output. |
| `-mindepth` / `-maxdepth` | `<meters>` | `0` / `1000` | Minimum and maximum depth window in meters (converted to ms assuming 750 m/s one-way sound speed). |
| `-nosam` | `<samples>` | `1000` | Number of output vertical pixels per trace (`bytes_per_trace`) in `.chan1`. |
| `-min` / `-max` | `<val>` | `0` / `2e8` | Minimum and maximum amplitude values for 8-bit quantization. |
| `-autoscale` / `-autoplus` | none | `0` | Automatically determine min/max trace amplitude scaling (`1` or `2`). |
| `-skipblanktrace` | none | `0` | Skip traces containing all zeros. |
| `-just_cdp` | `<beam_no>` | all | Process only traces matching the specified `cdpno` (e.g., a single Kongsberg SBP 120 beam). |
| `-extra_nttr` | `<samples>` | `0` | Add `NTTR_shift` extra samples to the trace header's `nttr` sample count. |
| `-force_year` | `<year>` | header year | Override the year field in the SEG-Y trace header. |
| `-sbp120_ll` | none | `0` | Decode Kongsberg SBP 120 arc-second coordinates from `xsc`/`ysc`. |
| `-richardo_ll` | none | `0` | Decode packed `DDDMMSSSSS` coordinates from `xsc`/`ysc`. |
| `-fliplong` | none | `0` | Negate longitude values. |
| `-extract_heave` | none | `0` | Extract 16-bit heave stored at trace header byte offset 188 (SonarWiz convention). |
| `-use_rwdepth` | none | `0` | Use receiver water depth (`trcrec.rwdepth`) from the trace header. |
| `-get_AUV_depth` | none | `0` | Extract vehicle depth for AUV sub-bottom surveys. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Header & Trace Parsing**: For each input SEG-Y file, optionally reads the 3600-byte tape header (`read_segy_tape_headers()`) and iterates over 240-byte trace headers (`ctrace`), byte-swapping fields into `trcrec` and writing navigation fixes to `<outfile_prefix>.nav`.
2. **Envelope & Scaling**: Reads trace samples as `float`, `int`, or `short`, optionally computes the analytic signal envelope via a Hilbert transform (`-hilbert`), and quantizes amplitudes to 8-bit using linear, logarithmic (`-log`), or square-root (`-sqrt`) scaling.
3. **Raster & OMG HDCS Output**: Writes windowed traces into `<outfile_prefix>.chan1` and, when `-out_as_OMG` is enabled, populates 2-beam OMG HDCS `Knudsen_320` profiles (`beams[0]` = 8-bit envelope in `.merged.ss_data`, `beams[1]` = full-resolution float/short/int trace in `.merged.fl_data` / `.16_data` / `.32_data`) with trace delay encoded in `beams[0].range`.

## Practical Examples

### Convert Kongsberg SBP 120 SEG-Y files into OMG HDCS sub-bottom format

```bash
readSB_SEGY -sbp120_ll -just_cdp 6 -hilbert -log -out_as_OMG \
            -in line01.sgy line02.sgy -out sbp120_line01
```
