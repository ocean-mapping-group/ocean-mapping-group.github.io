---
layout: default
title: getCR
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 7
tool_name: getCR
source_path: code/tests/getCR.c
category: File Format & Line-Ending Utilities (tests)
input_formats:
  - ASCII text file (Mac CR, DOS CRLF, or Unix LF)
output_formats:
  - Converted ASCII text file (Unix LF or DOS CRLF)
related_tools:
  - stripRawDoc
  - read4bit
---

# getCR

## Overview
`getCR` (`code/tests/getCR.c`, authored by John Hughes Clarke in August 1994) is a byte-level ASCII line-ending conversion utility used when transferring hydrographic tide files, navigation logs, or CTD profiles between classic Mac OS / MS-DOS systems and Unix workstations.

* **Default Mode (Mac/DOS `CR` $\to$ Unix `LF`):** Reads `<infile>` byte-by-byte (`getc`) and converts every Carriage Return byte (`ASCII 13`, `\r`) into a Unix Line Feed byte (`ASCII 10`, `\n`), writing the result to `<outfile>` and echoing to `stdout`.
* **Reverse Mode (`-reverse`, Unix `LF` $\to$ DOS `CR+LF`):** Converts every Unix Line Feed byte (`ASCII 10`, `\n`) into a two-byte Carriage Return + Line Feed sequence (`ASCII 13` followed by `ASCII 10`, `\r\n`) for PC/DOS compatibility.

---

## Syntax & CLI Options

```bash
getCR [-v] [-reverse] [-pitch] [-roll] [-depth <m>] <infile> <outfile>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `<infile>` | **Required.** Input ASCII file to convert. | None |
| `<outfile>` | **Required.** Output ASCII file with converted line endings. | None |
| `-reverse` | Convert Unix `LF` (`10`) to PC/DOS `CR+LF` (`13` + `10`). Without `-reverse`, converts `CR` (`13`) to `LF` (`10`). | `0` (CR $\to$ LF) |
| `-v` | Enable verbose byte inspection: prints every non-newline character and its integer ASCII code (`%c %i`) to `stdout`. | `0` |
| `-pitch`, `-roll`, `-depth <m>` | Legacy template flags parsed by the CLI loop (retained from `drawCustom.c`; unused by the byte translator). | Unused |

---

## Byte Translation Logic

1. **Forward Translation (`reverse == 0`):**
   Iterates while `(i = getc(infile)) != -1`:
   * If `i == 13` (`\r`): sets `i = 10` (`\n`) and writes `putc(10, outfile)`.
   * Otherwise: writes `putc(i, outfile)` (and prints `" %c %i\n"` if `-v` is enabled).
   * Echoes `putc(i, stdout)`.
   *(Note: If the input file already contains DOS `CR+LF` (`13 10`), replacing `13` with `10` produces double newlines `10 10`; this mode is primarily intended for classic Mac OS or instrument serial logs that terminate lines solely with `CR` `0x0D`).*
2. **Reverse Translation (`-reverse`, `reverse > 0`):**
   Iterates while `(i = getc(infile)) != -1`:
   * If `i == 10` (`\n`): writes both `putc(13, outfile)` and `putc(10, outfile)` (`\r\n`).
   * Otherwise: writes `putc(i, outfile)`.

---

## Example Usage

```bash
# Convert a serial-logged tide gauge file with Carriage Returns (0x0D) to Unix newlines (0x0A)
getCR raw_mac_tide.txt unix_tide.txt

# Convert a Unix ASCII table to DOS CR+LF format for PC import
getCR -reverse unix_tide.txt pc_tide.txt
```
