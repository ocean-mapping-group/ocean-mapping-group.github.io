---
layout: default
title: extractWaveWindow
parent: Acoustic WAV Waveform Tools (Wave)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
tool_name: extractWaveWindow
source_path: code/Wave/extractWaveWindow.c
category: Passive Acoustics & Hydrophone WAV Processing
input_formats:
- .wav (RIFF/WAVE 16-bit PCM)
- .wav.datetime
output_formats:
- .wav
- .wav.list
- .wav.datetime
related_tools:
- readWave
- jwave_subr
- j_wav_io
- stdtime
---

# extractWaveWindow

## Overview
`extractWaveWindow` (`code/Wave/extractWaveWindow.c`, written by John E. Hughes Clarke, March 2019) extracts and concatenates a precise UTC time window across a sequence of timestamped hydrophone/acoustic `.wav` files into a single contiguous RIFF/WAVE output file (`-out <new.wav>`), optionally applying a linear amplitude gain multiplier (`-gainout`).

Each input `.wav` file is expected to have a companion `<file>.wav.datetime` two-line ASCII sidecar file containing the file's start and end UTC date/time and 1970 Unix epoch seconds. `extractWaveWindow` classifies each input `.wav` file into one of four overlap cases (`useful[i] = 1..4`: overlaps start of window, overlaps end of window, completely inside window, or completely envelopes window), splices the exact sample ranges using [`jwave_subr`](../subr/jwave_subr.html) (`read_in_wave_head`, `read_in_wave_body`, `write_out_wave_head`, `write_out_wave_body`), and writes provenance metadata to `<out.wav>.list` and `<out.wav>.datetime`.

---

## Usage

```bash
# Specify explicit UTC start and end times (Year JulianDay Hour Min Sec)
extractWaveWindow -time_start 2019 145 16 22 00 -time_end 2019 145 16 28 30 \
  [-gainout 10.0] -out window.wav -ins *.wav

# Or specify a center UTC time and total duration in seconds
extractWaveWindow -time_cen 2019 145 16 25 00 -time_range_sec 390 \
  [-gainout 10.0] -out window.wav -ins *.wav
```

---

## Command-Line Arguments

| Option | Description | Default |
|---|---|---|
| `-time_start <YYYY> <DDD> <HH> <MM> <SS>` | Start of extraction window (4-digit year, Julian day `1..366`, hour, minute, second UTC). Used with `-time_end`. | None |
| `-time_end <YYYY> <DDD> <HH> <MM> <SS>` | End of extraction window (year, Julian day, hour, minute, second UTC). | None |
| `-time_cen <YYYY> <DDD> <HH> <MM> <SS>` | Center of extraction window (year, Julian day, hour, minute, second UTC). Used with `-time_range_sec`. | None |
| `-time_range_sec <sec>` | Total duration of extraction window in seconds around `-time_cen` ($\pm \text{sec}/2$). | None |
| `-gainout <mult>` | Linear amplitude multiplier applied to 16-bit signed PCM samples (clamped to `[-32768, +32767]`). | `1.0` |
| `-out <out.wav>` | **Required.** Output RIFF/WAVE filename. Also generates `<out.wav>.list` and `<out.wav>.datetime`. | None |
| `-ins <wav1> [wav2 ...]` | **Required.** List of up to 100,000 input `.wav` files (each requiring a `<wav>.datetime` companion file). | None |
| `-v` | Verbose diagnostic mode. | Disabled |

---

## Window Overlap Classification (`useful[i]`)

For each input file spanning `[fstarttime, fend__time]` against the requested window `[starttime, end__time]`:
* **Case 1 (`useful[i] == 1`):** File overlaps the **start** of the requested window (`fend__time > starttime && fend__time < end__time`). Skips the leading `the_waveStr.nosamples - how_many_samples` samples and writes the trailing portion.
* **Case 3 (`useful[i] == 3`):** File lies **entirely inside** the requested window (`fstarttime > starttime && fend__time < end__time`). Appends all `the_waveStr.nosamples` samples and verifies `SampleRate` consistency.
* **Case 2 (`useful[i] == 2`):** File overlaps the **end** of the requested window (`fstarttime > starttime && fstarttime < end__time`). Writes the leading `(end__time - fstarttime) * SampleRate` samples.
* **Case 4 (`useful[i] == 4`):** Single file **completely envelopes** the requested window (`fstarttime < starttime && fend__time > end__time`). Skips `(starttime - fstarttime) * SampleRate` samples and writes `(end__time - starttime) * SampleRate` samples.
