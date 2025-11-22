---
layout: default
title: qmips2glo
parent: Q-Mips Tools
grand_parent: Convert Tools
nav_order: 1
---
# qmips2glo

## Description
`qmips2glo` is a utility designed to convert QMIPS sidescan format data to JCU GLORIA format. It handles 8-bit or 16-bit QMIPS data, applies optional logarithmic scaling, and converts it into GLORIA records, generating two output files for different channels (e.g., channel 1 and channel 2).

## Usage
```bash
qmips2glo [-v] [-log] [-reverse] [-swapsides] [-merid <value>] [-timeseries] [-in <infile>] -out <outfile_prefix>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-log` | Apply logarithmic scaling to the input data. |
| `-reverse` | Not implemented. |
| `-swapsides` | Swap port and starboard sides. |
| `-merid <value>` | Specify the central meridian for coordinate conversion. | `-999.0` (default, prompts for input) |
| `-timeseries` | Process data as time series (default). |
| `-in <infile>` | **Required.** The input QMIPS sidescan file. |
| `-out <outfile_prefix>` | **Required.** The prefix for the output JCU GLORIA files. Two files will be created: `<outfile_prefix>.chan1` and `<outfile_prefix>.chan2`. |

## How It Works
1.  **Read QMIPS Header:** The tool first reads the 1024-byte QMIPS header from the input file, extracting crucial parameters like `sampleRate`, `numImageryChannels`, `bitsPerPixel`, `pixelsPerChannelPerPing`, and `numSonarChannels`.
2.  **Initialize Parameters:** Based on `bitsPerPixel`, it sets up either an 8-bit or 16-bit processing path. If `log_flag` is set, it initializes a logarithmic lookup table.
3.  **Process QMIPS Records:** The tool then iterates through the input file, reading QMIPS records:
    *   **Read Imagery Data:** It reads the imagery data for all channels (typically 4 channels) for the number of samples per ping.
    *   **Byte Swapping:** If `bitsPerPixel` is 16, it performs byte swapping on the raw 16-bit data.
    *   **Logarithmic Scaling:** If `log_flag` is set, it applies logarithmic scaling to the imagery data.
    *   **Read Footer Data:** It reads a 256-byte QMIPS footer, extracting time (day, month, year, hour, minute, seconds, thousandsSeconds), ping number, fish depth, heading, altitude, sound velocity, and ship latitude/longitude.
    *   **Time Conversion:** Converts the QMIPS time to a Unix timestamp.
    *   **Populate GLORIA Header:** Populates the fields of the GLORIA record header:
        *   `time`, `centisecs`: From converted QMIPS time.
        *   `lat`, `lon`: From QMIPS ship latitude/longitude.
        *   `small_pixel`: Calculated based on `qfooter.ch1_floatRawRange` and number of samples.
        *   `pixel_size`: Set to 0.
        *   `azi`: From `qfooter.telemFishHeading`.
        *   `altitude`: From `qfooter.telemFishAlt`.
    *   **Convert Sidescan Data:** It processes the imagery data based on `swapsides` flag and `no_samples_per_side` to populate the `stbd_data` and `port_data` fields of two GLORIA records (`out_rec` and `out_rec2`).
    *   **Write GLORIA Record:** The two GLORIA records are written to separate output files (`.chan1` and `.chan2`).
4.  **Loop:** This process repeats until the end of the input QMIPS file.
