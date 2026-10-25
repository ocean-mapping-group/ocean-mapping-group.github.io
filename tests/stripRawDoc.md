---
layout: default
title: stripRawDoc
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 16
tool_name: stripRawDoc
source_path: code/tests/stripRawDoc.c
category: Binary Format & Forensic File Recovery (tests)
input_formats:
- Raw binary disk image, corrupted document, or binary stream
output_formats:
- Extracted ASCII text file (default string search mode)
- <outname>_0000.doc / <outname>_0000.ppt (carved Microsoft Office OLE2 documents in -grab_microsoft mode)
related_tools:
- getCR
- read4bit
---

# stripRawDoc

## Overview
`stripRawDoc` (`code/tests/stripRawDoc.c`, authored by John Hughes Clarke in December 2005) is a binary stream searcher and forensic file-carving utility originally written to recover text and embedded Microsoft Office documents (`.doc` Word 97–2003 and `.ppt` PowerPoint) from raw disk images, corrupted files, or unallocated byte streams.

It operates in two distinct modes:
1. **ASCII String Search & Text Extraction Mode (Default):** Scans `<infile>` starting at byte offset `-skip` until it locates an exact match for `-string <target>`, then extracts the next `-nobytes` of printable ASCII characters (`ASCII 40` to `177`, plus spaces and `CR` $\to$ `LF` newlines) into `<outfile>`.
2. **Microsoft OLE2 Compound Document Carver (`-grab_microsoft`):** Scans `<infile>` byte-by-byte from `-skip` for the 32-byte Microsoft OLE2 Compound Document magic header (`D0 CF 11 E0 A1 B1 1A E1 ...`), carves each embedded document into sequential files `<outname>_0000`, `<outname>_0001`, ..., inspects internal stream signatures (`"Microsoft Word"` or `"Microsoft PowerPoint"` and the 80-byte `END_MSWord8Doc` trailer), automatically renames recognized files to `.doc` or `.ppt`, and deletes unrecognized fragments.

---

## Syntax & CLI Options

```bash
stripRawDoc [-v] [-grab_microsoft] [-string "<search_text>"] \
            [-nobytes <N>] [-skip <byte_offset>] <infile> <outfile>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `<infile>` | **Required.** Input binary file or raw disk image to scan. | None |
| `<outfile>` | **Required.** Output ASCII file (in default mode) or output filename prefix `<outname>_XXXX` (in `-grab_microsoft` mode). | None |
| `-grab_microsoft` | Enable Microsoft OLE2 Compound Document carving mode (`grab_microsoft++`). | `0` (Disabled) |
| `-string "<text>"` | Target ASCII substring to search for in default mode (`string_to_search`). | None |
| `-nobytes <int>` | Maximum number of bytes to extract after finding `-string` or after an OLE2 `START_Microsoft` signature. | `1000000` (1 MB) |
| `-skip <int>` | Initial byte offset passed to `fseek(infile, Skip, 0)` before starting the search. | `0` |
| `-v` | Increment verbose flag (`verbose_flag++`). | `0` |

---

## Binary Signatures & Recovery Logic

### Mode 1: Target String Search & Printable ASCII Filtering
1. Seeks to `Skip` (`fseek(infile, Skip, 0)`) and slides a window of length `strlen(string_to_search)` forward 1 byte at a time until `strncmp(random_string, string_to_search, string_length) == 0` or EOF is reached.
2. Prints `YAHOO found string at <byte_offset> bytes off` and the matched characters.
3. Reads the subsequent `Nobytes` bytes from `byte_offset`:
   * Converts Carriage Return (`ibyte == 13`) to Line Feed (`putc(10, outfile)`).
   * Preserves single spaces (`ibyte == 32`) only when the preceding byte was printable ASCII (`lastbyte_was_ascii == 1`), collapsing binary runs of spaces/nulls.
   * Writes printable bytes in the range `40 <= ibyte <= 177` (`'('` through `'~'`).

### Mode 2: Microsoft Office OLE2 Carving (`-grab_microsoft`)
Slides an 80-byte buffer (`random_string`) byte-by-byte through `<infile>`:
1. **Header Match (`START_Microsoft`, 32 bytes):**
   Matches the standard OLE2 Compound Binary File header:

   ```text
   D0 CF 11 E0 A1 B1 1A E1 00 00 00 00 00 00 00 00
   00 00 00 00 00 00 00 00 3E 00 03 00 FE FF 09 00
   ```
   Opens `<outname>_<MSfile_count>` (e.g., `recovered_0000`) and begins streaming bytes into `micfile` up to `Nobytes`.
2. **Document Type Identification:**
   * If `"Microsoft PowerPoint"` (20 bytes) is encountered inside the carved stream, executes `mv <dumpname> <dumpname>.ppt` and tags `MS_file_type = MS_POWERPT`.
   * If `"Microsoft Word"` (14 bytes) is encountered, executes `mv <dumpname> <dumpname>.doc` and tags `MS_file_type = MS_WORD`.
3. **Trailer Match (`END_MSWord8Doc`, 80 bytes):**
   Matches the 80-byte Word 8.0 (`Word.Document.8`) directory trailer, flushes the final 80 bytes to `micfile`, and stops writing (`MS_write_out = 0`). If a carved fragment reaches the next `START_Microsoft` header without ever matching a Word or PowerPoint signature (`MS_file_type == MS_UNKNOWN`), it is automatically removed (`/bin/rm <dumpname>*`).

---

## Example Usage

```bash
# 1. Search a corrupted Word file or raw binary dump for a known phrase and extract 50 KB of text
stripRawDoc -string "Ocean Mapping Group" -nobytes 50000 corrupted.doc recovered_text.txt

# 2. Carve embedded .doc and .ppt files starting at byte offset 10,000,000
stripRawDoc -grab_microsoft -skip 10000000 -nobytes 5000000 raw_disk.img carved_ms
```
