---
layout: default
title: snippet
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/snippet.c
category: Sonar Format Parsers & Hardware Drivers
related_tools:
- reson
- unr8101
- xtf2omg
- makess
- jb_endian
module_name: snippet
header_path: code/subr/snippet.h
---

# snippet

## Overview
`snippet` (`snippet.c` / `snippet.h`) is the Ocean Mapping Group's parser and radiometric correction module for **Reson 81-P (8101 / 8111 / 8125 / 8150 / 8160) snippet backscatter packets** (`SNP0` ping headers and `SNP1` beam fragment packets). Introduced with Reson 81-P firmware `8111-2.07-996C` (March 2001) on UDP port `UDP_Base + 6`, snippet packets record a windowed time series of unsigned 16-bit magnitude samples (`<= 1024` samples per beam) centered on each beam's bottom detection.

Because the Reson 81-P processor packs variable-length beam snippets into Ethernet UDP packets without IP fragmentation, a single beam snippet may be split across multiple `SNP1` fragments (`FragOffset`, `FragSamples`). `readRESON_SNIPPET()` reassembles these fragments into a contiguous 2D array (`BeamCnt x MAX_SNIPPET_LENGTH`), handles Hypack `.81x` inter-record padding via `seek_next_8K_sync()`, and converts raw 16-bit amplitudes into TVG/gain-corrected 8-bit backscatter via `corrRESON_SNIPPET()`.

---

## Key Constants & Data Structures

### Constants

| Constant | Value | Description |
|---|---|---|
| `SNIPPET_ID_SNP0` | `0x534E5030` (`'SNP0'`) | Big-endian magic identifier for a Reson snippet ping header. |
| `SNIPPET_ID_SNP1` | `0x534E5031` (`'SNP1'`) | Big-endian magic identifier for a Reson beam snippet fragment header. |
| `MAX_SNIPPET_LENGTH` | `1024` | Maximum snippet length per beam in samples. |
| `SNP0_SIZE` | `74` | Size in bytes of the packed `SNP0` ping header on disk. |
| `SNP1_SIZE` | `24` | Size in bytes of the packed `SNP1` fragment header on disk. |
| `SNIPPET_PEEKER_SIZE` | `14` | Size in bytes of the `SNIPPET_PEEKER` lookahead header. |

### `SNP0` (74-byte Ping Header)
Stores per-ping sonar acquisition metadata in big-endian byte order:
- `ID` (`0x534E5030`), `HeaderSize`, `DataSize`, `PingNumber`
- `Seconds` (Unix epoch), `Millisec`, `Latency` (ms from ping to output)
- `SonarID[2]` (least significant 4 bytes of Ethernet MAC), `SonarModel`, `Frequency` (kHz)
- `SSpeed` (m/s), `SampleRate` (samples/s), `PingRate` (0.001 Hz steps), `Range` (m)
- `Power` (`b7..0`), `Gain` (`b15=auto`, `b14=TVG`, `b6..0=gain`), `PulseWidth` ($\mu\text{s}$)
- `Spread` ($n \log R$ in 0.25 dB steps), `Absorp` (dB/km), `Proj` (steering/projector type), `ProjWidth` (0.1° steps)
- `SpacingNum` / `SpacingDen` (receiver beam spacing in degrees), `ProjAngle`
- `MinRange`, `MaxRange`, `MinDepth`, `MaxDepth`, `Filters`, `bFlags` (`RollStab`, `SnipMode`), `HeadTemp` (0.1°C), `BeamCnt`

### `SNP1` (24-byte Beam Fragment Header)
Describes a single snippet fragment for beam `Beam` (`0..BeamCnt-1`):
- `ID` (`0x534E5031`), `HeaderSize`, `DataSize`, `PingNumber`, `Beam`
- `SnipSamples` (total snippet length in samples for this beam)
- `GainStart`, `GainEnd` (gain at start/end of snippet in 0.01 dB steps)
- `FragOffset` (sample offset from ping start), `FragSamples` (samples in this fragment)

### `RESON_SNIPPET` (In-Memory Ping Container)

```c
typedef struct {
    SNP0 header;                  /* 74-byte ping header */
    SNP1 *beams;                  /* Array of BeamCnt SNP1 headers */
    unsigned short *samples;      /* Raw 16-bit magnitude samples (BeamCnt * sampLength) */
    unsigned char *samples8bit;   /* Radiometrically corrected 8-bit samples */
    unsigned int sampLength;      /* Row stride (MAX_SNIPPET_LENGTH = 1024) */
    unsigned char *fragCounts;    /* Number of fragments merged per beam */
    int numValidSnippets;         /* Beams where FragSamples == SnipSamples */
    unsigned int bytesOnDisk;     /* Total packet footprint on disk */
} RESON_SNIPPET;
```

---

## Public Functions

| Function | Signature | Description |
|---|---|---|
| `initRESON_SNIPPET` | `void initRESON_SNIPPET(RESON_SNIPPET *snippet)` | Zeroes pointers (`beams`, `samples`, `samples8bit`, `fragCounts`) and counters (`bytesOnDisk`, `numValidSnippets`). |
| `readRESON_SNIPPET` | `void readRESON_SNIPPET(RESON_SNIPPET *snippet, FILE *infile)` | Reads an `SNP0` header and loops over all subsequent `SNP1` fragments belonging to the same `PingNumber`, reassembling multi-fragment beams and reading big-endian 16-bit sample arrays via `fread_BE_short()`. |
| `corrRESON_SNIPPET` | `void corrRESON_SNIPPET(RESON_SNIPPET *snippet)` | Allocates `samples8bit` and invokes `jb_fix_RESON_16bit()` (`reson.c`) on each beam's valid samples using `header.Power & 0x00FF` and `header.Gain & 0x3FFF` in `JB_8101_LOG` / `JB_8101_TRACE` mode. |
| `printRESON_SNIPPET` | `void printRESON_SNIPPET(RESON_SNIPPET *snippet)` | Dumps the `SNP0` ping header and all populated `SNP1` beam headers to `stdout`. |
| `freeRESON_SNIPPET` | `void freeRESON_SNIPPET(RESON_SNIPPET *snippet)` | Frees `beams`, `samples`, `samples8bit`, and `fragCounts`. |
| `readSNP0` / `printSNP0` | `void readSNP0(SNP0 *hdr, FILE *in)` / `void printSNP0(SNP0 *hdr)` | Reads and byte-swaps (big-endian) or prints a 74-byte `SNP0` ping header. |
| `readSNP1` / `printSNP1` | `void readSNP1(SNP1 *hdr, FILE *in)` / `void printSNP1(SNP1 *hdr)` | Reads and byte-swaps (big-endian) or prints a 24-byte `SNP1` fragment header. |
| `peekSnippet` | `void peekSnippet(SNIPPET_PEEKER *peeker, FILE *infile)` | Reads 14 bytes (`ID`, `HeaderSize`, `DataSize`, `PingNumber`, `Beam`) and rewinds `infile` via `fseek(..., -14, SEEK_CUR)` so `readRESON_SNIPPET` can detect packet boundaries non-destructively. |

---

## Architectural Role
`snippet` bridges raw Reson 81-P Ethernet/XTF/Hypack streams (`reson.c`, `xtf2omg`, `unr8101`) and OMG's sidescan/backscatter pipeline (`makess`, `mos2`). By reassembling fragmented `SNP1` UDP payloads and normalizing 16-bit linear magnitudes into 8-bit dB traces (`samples8bit`), it enables `makess` to project high-resolution seabed snippets across the swath.
