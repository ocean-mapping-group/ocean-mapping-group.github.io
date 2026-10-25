---
layout: default
title: interpMRU
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 9
tool_name: interpMRU
source_path: code/tests/interpMRU.c
category: Attitude & Serial Sensor Diagnostics (tests)
input_formats:
  - /dev/ttyd2 (Serial binary stream with 'q' 25-byte MRU frames)
output_formats:
  - Console diagnostic stream (pitch, roll, yaw, X/Y/Z accelerations, checksum)
related_tools:
  - twistVRU
  - testrot
  - testFIR
  - newMergeAtt
---

# interpMRU

## Overview
`interpMRU` (`code/tests/interpMRU.c`, authored by John Hughes Clarke in October 1997) is a real-time serial port diagnostic listener designed to test and decode binary packets from a Motion Reference Unit (MRU / TSS / Seatex attitude sensor) connected to SGI IRIX serial device `/dev/ttyd2`.

It continuously polls the serial stream for packet synchronization character `'q'` (`0x71`), verifies a 25-byte payload length (`length == 25`), extracts a 1-byte token identifier, unpacks six 32-bit IEEE-754 floating-point values representing 3-axis angular orientation (`angP`, `angR`, `angY`) and 3-axis linear acceleration (`accelX`, `accelY`, `accelZ`), and reads the trailing 1-byte checksum.

---

## Syntax & CLI Options

```bash
interpMRU [-v] [-pitch] [-roll] [-depth <m>] <logbinfile> <asciioutfile>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `<logbinfile>` | **Required on CLI.** Positional argument 1 (`inname`). Note that the source code hardcodes `infile = fopen("/dev/ttyd2", "r");` and only uses `inname` in the error message if `/dev/ttyd2` cannot be opened. | `/dev/ttyd2` |
| `<asciioutfile>` | **Required on CLI.** Positional argument 2 (`outname`), opened in `"w"` mode. | None |
| `-v` | Increment verbose flag (`verbose_flag++`). | `0` |
| `-pitch`, `-roll`, `-depth <m>` | Template CLI flags parsed into `convert_flag` and `depth`. | Unused |

---

## Binary MRU Packet Structure

`interpMRU` synchronizes on the following 29-byte binary datagram layout over `/dev/ttyd2`:

| Byte Offset | Field | Type | Size | Description |
| :--- | :--- | :--- | :--- | :--- |
| `0` | Sync Byte | `char` | 1 byte | ASCII `'q'` (`0x71`, decimal `113`) |
| `1` | `length` | `unsigned char` | 1 byte | Payload byte count; must equal `25` (`1` token + `24` data bytes) |
| `2` | `token` | `unsigned char` | 1 byte | Packet type token identifier (printed as `%d %c`) |
| `3..6` | `angP` | `float` | 4 bytes | Pitch angle (`memcpy(&angP, &data[0], 4)`) |
| `7..10` | `angR` | `float` | 4 bytes | Roll angle (`memcpy(&angR, &data[4], 4)`) |
| `11..14` | `angY` | `float` | 4 bytes | Yaw / heading angle (`memcpy(&angY, &data[8], 4)`) |
| `15..18` | `accelX` | `float` | 4 bytes | X-axis linear acceleration (`memcpy(&accelX, &data[12], 4)`) |
| `19..22` | `accelY` | `float` | 4 bytes | Y-axis linear acceleration (`memcpy(&accelY, &data[16], 4)`) |
| `23..26` | `accelZ` | `float` | 4 bytes | Z-axis linear acceleration (`memcpy(&accelZ, &data[20], 4)`) |
| `27` | `checksum` | `unsigned char` | 1 byte | Trailing packet checksum byte |

*(Note: Because `fread(data, 25, 1, infile)` reads 25 bytes after `token` has already been read with `getc(infile)`, the 25th byte read into `data[24]` is followed by `checksum = getc(infile)`).*

---

## Example Console Output

```text
length 25
token 65 A
 ang rots P 1.245000 R -3.412000 Y 184.500000
 accels   X 0.041000 Y -0.112000 Z 9.814000
checksum 142
```
For offline processing and merging of attitude data into OMG `.merged` files, see [`mergeAtt`](../att/mergeAtt.md) and [`newMergeAtt`](../att/newMergeAtt.md).
