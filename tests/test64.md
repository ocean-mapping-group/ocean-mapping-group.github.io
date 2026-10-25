---
layout: default
title: test64
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 17
tool_name: test64
source_path: code/tests/test64.c
category: System Architecture & Endianness Diagnostics (tests)
input_formats:
  - Optional binary/ASCII file (<inname>) to test fseek/ftell
output_formats:
  - Console diagnostic report (endianness macros, C data type byte sizes, file byte length)
related_tools:
  - read4bit
  - EM_unpack
---

# test64

## Overview
`test64` (`code/tests/test64.c`, authored by John Hughes Clarke in August 1992) is a system-architecture and compiler-portability diagnostic utility created when migrating the OMG software suite across 32-bit and 64-bit Unix/Linux platforms (such as SGI IRIX MIPS, Sun SPARC, DEC Alpha, and x86/x86_64 Linux).

When executed, `test64` reports three critical platform properties:
1. **Compile-Time Endianness Macros (`INTEL` vs. `MOTOROLA`):** Prints the integer values of `INTEL` and `MOTOROLA` defined in `swapio.h` to verify whether byte-swapping routines (`jswap_short`, `jswap_int`, `jswap_float`) are configured for little-endian or big-endian host order.
2. **C Primitive Type Sizes (`sizeof`):** Prints the byte widths (`%ld`) of `long int`, `int`, `short`, `float`, and `double`—specifically checking whether `long int` is 4 bytes (`ILP32`) or 8 bytes (`LP64` on 64-bit Unix/Linux), which directly impacts binary header structs in OMG formats.
3. **File Seeking & `ftell` Offset Width:** If an optional `<inname>` file is provided on the command line, opens the file, seeks to `SEEK_END` (`fseek(infile, 0, SEEK_END)`), and prints the resulting byte offset (`ftell(infile)`) as a `long int` (`%ld`) to verify large-file support.

---

## Syntax & CLI Options

```bash
test64 [-v] [-depth <val>] [<infile> [<outfile>]]
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `<infile>` | Optional input file path used to test `fopen`, `fseek(infile, 0, SEEK_END)`, and `ftell(infile)`. | None |
| `<outfile>` | Optional second positional argument stored in `outname` (commented out in source). | Unused |
| `-v` | Parsed on command line (no-op). | Unused |
| `-depth <val>` | Consumes one following argument on the command line (no-op). | Unused |

---

## Diagnostic Output Interpretation

Running `test64` on a 64-bit Linux (`LP64`, little-endian x86_64) system produces:

```text
 INTEL 1 MOTOROLA 0
 8 4 2 4 8 
```
where the five `sizeof` integers correspond to:

| Position | Expression | 32-bit (`ILP32`) | 64-bit (`LP64`) |
| :--- | :--- | :--- | :--- |
| 1 | `sizeof(long int)` | `4` bytes | **`8` bytes** |
| 2 | `sizeof(int)` | `4` bytes | `4` bytes |
| 3 | `sizeof(short)` | `2` bytes | `2` bytes |
| 4 | `sizeof(float)` | `4` bytes | `4` bytes |
| 5 | `sizeof(double)` | `8` bytes | `8` bytes |

> [!IMPORTANT]
> Because `sizeof(long int)` changes from 4 bytes on 32-bit architectures to 8 bytes on 64-bit Linux (`LP64`), all fixed-width 32-bit integer fields in OMG binary file headers (`.merged`, `.r4`, `.mos`) must be declared as `int` (4 bytes) rather than `long`. `test64` was written specifically to verify these type sizes during compiler transitions.

---

## Example Usage

```bash
# Check host endianness, data type byte widths, and file size of a .merged file
test64 survey_line_001.merged
```
Sample output:
```text
 INTEL 1 MOTOROLA 0
 8 4 2 4 8 
 going to open survey_line_001.merged
opened  going to seek 2
where I am 0
seeked 
length 14582400
```
