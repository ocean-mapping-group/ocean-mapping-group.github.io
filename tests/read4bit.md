---
layout: default
title: read4bit
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 12
tool_name: read4bit
source_path: code/tests/read4bit.c
category: Binary Format & Bit-Level Diagnostics (tests)
input_formats:
- Binary file containing 4-bit nibble-packed bytes
output_formats:
- Binary file with high-nibble masked bytes (onebyte & 0xF0)
- Optional verbose bit-level ASCII trace on stdout (-v)
related_tools:
- getCR
- stripRawDoc
- test64
---

# read4bit

## Overview
`read4bit` (`code/tests/read4bit.c`, authored by John Hughes Clarke) is a bit-manipulation and nibble-unpacking diagnostic utility created to inspect binary sonar or raster files where two 4-bit unsigned samples (nibbles, values $0\text{–}15$) are packed into a single 8-bit `unsigned char` byte.

For every byte read from `<infile>`, `read4bit` extracts both the lower 4 bits shifted into the upper nibble (`lowval = onebyte << 4`) and the upper 4 bits masked in place (`highval = onebyte & 240`, i.e., `0xF0`), writes `highval` to `<outfile>`, and—when `-v` is enabled—prints the 32-bit and 8-bit binary bit patterns (`0` and `1` characters grouped by bytes) of the input integer, raw byte, `lowval`, and `highval` using `print32bits()` and `print8bits()`.

---

## Syntax & CLI Options

```bash
read4bit [-v] [-pitch] [-roll] [-depth <m>] <infile> <outfile>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `<infile>` | **Required.** Input binary file to inspect and mask. | None |
| `<outfile>` | **Required.** Output binary file receiving the upper-nibble masked bytes (`onebyte & 240`). | None |
| `-v` | Enable verbose bit-dumping: calls `print32bits(i)`, `print8bits(onebyte)`, `print8bits(lowval)`, and `print8bits(highval)` for every byte read. | `0` (Disabled) |
| `-pitch`, `-roll`, `-depth <m>` | Template CLI flags parsed into `convert_flag` and `depth` (unused by the bit-unpacking loop). | Unused |

---

## Bit-Level Unpacking & Inspection Functions

### 1. High and Low Nibble Extraction
Inside the main byte loop (`while ((i = getc(infile)) != -1)`):
1. `onebyte = (unsigned char)i;`
2. **Low Nibble Shifted to Upper 4 Bits (`lowval`):**
   $$\text{lowval} = (\text{onebyte} \ll 4) \pmod{256}$$
   which moves bits `[3:0]` into bit positions `[7:4]` and zeroes bits `[3:0]`, scaling a 4-bit value $v_{\text{low}} \in [0, 15]$ to $16 \cdot v_{\text{low}} \in [0, 240]$ (8-bit dynamic range).
3. **High Nibble Masked in Upper 4 Bits (`highval`):**
   $$\text{highval} = \text{onebyte} \ \& \ 240 \quad (\text{binary } 11110000_2 = \text{0xF0})$$
   which preserves bits `[7:4]` and zeroes bits `[3:0]`, scaling $v_{\text{high}} \in [0, 15]$ to $16 \cdot v_{\text{high}} \in [0, 240]$.
4. Writes `putc(highval, outfile);` *(note: `putc(lowval, outfile)` or a second `putc(highval, outfile)` is commented out on line 145).*

### 2. Bit-Pattern Diagnostic Printers (`print8bits` and `print32bits`)
* **`print8bits(unsigned char anint)`:** Loops from bit $b = 0$ to $7$ (LSB-first), testing `anint & (int)pow(2, b)` and printing a leading `-` followed by eight `1`/`0` characters.
* **`print32bits(int anint)`:** Loops from bit $b = 0$ to $31$ (LSB-first), printing a `-` separator every 8 bits (`b % 8 == 0`) to visualize all four bytes of a 32-bit `int`.

---

## Example Usage

```bash
# Unpack upper 4-bit nibbles and inspect bit patterns on stdout
read4bit -v packed_4bit.bin unpacked_high_nibble.bin | head -n 20
```
Sample `-v` output for byte `0xA5` (`165`, binary `10100101`, LSB-first `-10100101`):

```text
-10100101-00000000-00000000-00000000
-10100101
-00001010
-00000101
```
