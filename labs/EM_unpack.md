---
layout: default
title: EM_unpack
parent: Graduate Course Lab Exercises (labs)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 1
tool_name: EM_unpack
source_path: code/labs/EM_unpack.c
category: Educational Labs & Binary Datagram Parsing (labs)
input_formats:
- .all (Kongsberg Simrad EM3000 binary telegram stream)
output_formats:
- ASCII diagnostic log (stdout and -out file)
related_tools:
- unravel
- read_kmall
- example
- mkbp
---

# EM_unpack

## Overview
`EM_unpack` (`code/labs/EM_unpack.c`, authored by John Hughes Clarke in February 2001) is an educational C program designed for hydrographic surveying laboratory exercises. It demonstrates how to scan a raw Kongsberg Simrad EM3000 binary `.all` file byte-by-byte, synchronize on Start-of-Transmission (`EM_STX = 0x02`) framing bytes, validate the preceding 32-bit byte-count header (`check_len()`), handle big-endian vs. little-endian byte swapping (`-swap`), and unpack the common 14-byte `em3000_head` header structure for key multibeam telegram types.

Unlike production OMG tools that depend on `support.h` and `swapio.h`, `EM_unpack.c` is completely self-contained and links only against the standard C and math libraries (`cc EM_unpack.c -o EM_unpack -lm`).

---

## Syntax & CLI Options

```bash
EM_unpack [-v] [-swap] [-depth <val>] -in <input.all> -out <output_file>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-in <filename>` | **Required.** Input Kongsberg Simrad binary telegram file (e.g., `.all`). | None |
| `-out <filename>` | **Required.** Output file path opened for writing (`"w"`). | None |
| `-swap` | Enable 16-bit and 32-bit byte-order swapping (`do_swap++`) via union-based `swap_short()` and `swap_int()` routines when reading on opposite-endian architectures (e.g., Sun SPARC / SGI MIPS vs. x86). | Disabled (`0`) |
| `-depth <meters>` | Example floating-point CLI parameter parsed via `atof()` to illustrate command-line argument parsing to students. | `10.0` |
| `-v` | Increment verbose flag (`verbose_flag++`). | `0` |

---

## Telegram Framing & Header Decoding Algorithm

### 1. Kongsberg EM3000 Datagram Synchronization
In Simrad `.all` files, each datagram is preceded by a 4-byte unsigned integer length field (`len`), followed by `EM_STX` (`0x02`) and a 1-byte ASCII/hexadecimal telegram identifier code:

| Macro Name | Hex Code | ASCII | Kongsberg Telegram Type |
| :--- | :--- | :--- | :--- |
| `EM3000_DEPTH_CODE` | `0x44` | `'D'` | Depth datagram *(decoded by `EM_unpack`)* |
| `EM3000_RAW_TANG_CODE` | `0x46` | `'F'` | Raw Range and Beam Angle (`RAW_TANG`) *(decoded by `EM_unpack`)* |
| `EM3000_NAV_CODE` | `0x50` | `'P'` | Position / Navigation datagram *(decoded by `EM_unpack`)* |
| `EM3000_IMAGE_CODE` | `0x53` | `'S'` | Seabed Image / Backscatter datagram *(decoded by `EM_unpack`)* |
| `EM3000_ATTITUDE_CODE` | `0x41` | `'A'` | Attitude (roll, pitch, heave, heading) |
| `EM3000_CLOCK_CODE` | `0x43` | `'C'` | Clock datagram |
| `EM3000_SINGLE_BEAM_CODE` | `0x45` | `'E'` | Single-beam echo sounder depth |
| `EM3000_SURF_SS_CODE` | `0x47` | `'G'` | Surface sound speed |
| `EM3000_HEADING_CODE` | `0x48` | `'H'` | Heading datagram |
| `EM3000_START_PARAMETER_CODE` | `0x49` | `'I'` | Installation parameters (start) |
| `EM3000_MECH_TILT_CODE` | `0x4a` | `'J'` | Mechanical transducer tilt |
| `EM3000_ECHOGRAM_CODE` | `0x4b` | `'K'` | Central beam echogram |
| `EM3000_RUNTIME_PARAMETER_CODE` | `0x52` | `'R'` | Runtime parameters |
| `EM3000_TIDE_CODE` | `0x54` | `'T'` | Tide datagram |
| `EM3000_NEW_SSP_CODE` | `0x55` | `'U'` | Sound Speed Profile (new format) |
| `EM3000_SSP_CODE` | `0x56` | `'V'` | Sound Speed Profile |
| `EM3000_HEIGHT_CODE` | `0x68` | `'h'` | Height (ellipsoidal/dynamic) |
| `EM3000_STOP_PARAMETER_CODE` | `0x69` | `'i'` | Installation parameters (stop) |
| `EM3000_REMOTE_INSTALL_CODE` | `0x70` | `'p'` | Remote installation parameters |
| `EM3000_INPUT_SSP_CODE` | `0x76` | `'v'` | Input Sound Speed Profile |

### 2. Backward Seek Length Verification (`check_len`)
Because `0x02` can appear randomly inside binary payload bytes, `EM_unpack` verifies candidate `STX` + `CODE` pairs by calling `check_len()`:
1. Seeks backward 6 bytes from the current stream position (`fseek(infile, -6, SEEK_CUR)`), positioning the file pointer at the 4-byte unsigned integer length field preceding `EM_STX`.
2. Reads the 4-byte `len` value and optionally byte-swaps it with `swap_int(len)` if `-swap` is active.
3. Advances 2 bytes (`fseek(infile, 2, SEEK_CUR)`) past `EM_STX` and the telegram ID code.
4. Accepts the telegram if `len < 20000`, returning `len` so the caller can read the remaining `len - 2` bytes into `raw_telegram[10000]`.

### 3. Header Structure Unpacking (`parse_EM_telegram_header`)
For every validated `0x50` (Nav), `0x53` (Image), `0x46` (Raw Time & Angle), or `0x44` (Depth) telegram, `parse_EM_telegram_header()` copies the first 10 bytes of `raw_telegram` into `struct em3000_head`:
* `model_no` (`unsigned short`, 2 bytes, offset 0): Sonar model number (e.g., `3000` for EM3000, `300` for EM300).
* `ymd` (`unsigned int`, 4 bytes, offset 2): Date encoded as `YYYYMMDD` integer (e.g., `20010215`).
* `mdnt_time` (`unsigned int`, 4 bytes, offset 6): Time since midnight in milliseconds.

---

## Workflow Context & Examples

### Inspecting an EM3000 `.all` File in a Student Lab

```bash
# Parse an EM3000 raw file recorded with opposite byte order
EM_unpack -swap -in 0001_20010214_120000.all -out unpack_test.txt
```
Sample console output:

```text
poss len is 148 -   ---  yo possible NAV telegram 
 model 3000 ymd 20010214 time 43200150
poss len is 1624 -   ---  yo possible DEPTH telegram 
 model 3000 ymd 20010214 time 43200200
```

### Extending `EM_unpack` in Coursework
Students use `EM_unpack.c` as a starting point to write custom payload decoders (such as extracting vessel latitude/longitude from `EM3000_NAV_CODE` or beam depths and across-track distances from `EM3000_DEPTH_CODE`) and writing those values to `outfile`. In production OMG workflows, full Kongsberg `.all` decoding is handled by [`unravel`](../workflows/kongsberg-all-unraveling.html).
