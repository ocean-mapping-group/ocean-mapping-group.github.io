---
layout: default
title: unb_huffproc
parent: Shared Core Libraries (subr)
module_name: unb_huffproc
source_path: code/subr/unb_huffproc.c
header_path: code/subr/unb_huffproc.h
category: Sonar Format Parsers & Hardware Drivers
related_tools: ["j_knud", "knud2r4"]
---

# unb_huffproc

## Overview
`unb_huffproc` (`unb_huffproc.c` / `unb_huffproc.h`, alongside `unb_huffstruct.h`) implements **Huffman lossless compression and decompression** for **Knudsen 320 / 320B / 320M / 3260** echosounder binary `.keb` and `.kea` envelope/trace records.

Adapted to plain ANSI C by John Hughes Clarke (January 2008) from Knudsen Engineering's C++ `CHuffmanProcessing` class (itself derived from Mark Nelson and Jean-Loup Gailly's *The Data Compression Book, 2nd Edition*), `unb_huffproc` decompresses Huffman-encoded acoustic echogram trace blocks in [`j_knud`](j_knud.md) and `knud2r4`.

---

## Constants & Data Structures

Defined in `unb_huffproc.h` and `unb_huffstruct.h`:

| Constant / Type | Value / Fields | Description |
|---|---|---|
| `MAX_HUFFMAN_SIZE` | `80000` | Maximum byte size for Huffman compression/decompression buffers. |
| `END_OF_STREAM` | `256` | Special 9-bit sentinel symbol (`256`, immediately above byte symbols `0..255`) marking the end of a compressed bit stream. |
| `NODE` | `unsigned int count`<br>`unsigned int saved_count`<br>`int child_0`<br>`int child_1` | Node in the 514-entry Huffman decoding tree (`m_pNodes[0..513]`). Leaf nodes `0..256` represent byte values plus `END_OF_STREAM`; internal nodes `257..512` link `child_0` and `child_1`; node `513` holds `0xffff` as a sentinel maximum weight during `BuildTree()`. |
| `CODE` | `unsigned int code`<br>`int code_bits` | Lookup table entry (`m_pCodes[0..256]`) holding the variable-length Huffman bit string and bit length for each symbol during compression. |

### Global Buffers & State Variables
- `unsigned char *m_pDataBuffer` — Uncompressed raw byte buffer (output of `ExpandDataBlock()`, or input to `CompressDataBuffer()`).
- `unsigned char *m_pHuffmanBuffer` — Compressed bit-stream buffer (input to `ExpandDataBlock()`, or output of `CompressDataBuffer()`).
- `short m_nOutputBytes`, `short m_nInputBytes` — Byte counters tracking decompressed/compressed block lengths.
- `int m_MaxDataLimit`, `int m_CompressionOn`, `int m_RootNode`, `unsigned char m_Mask`, `int m_Rack`.

---

## Public Functions

| Function | Signature | Description |
|---|---|---|
| `init_CHuffmanProcessing` | `int init_CHuffmanProcessing(int compression_flag, int DataSize)` | Allocates internal buffers for up to `DataSize` bytes: `m_pNodes` (`514 * sizeof(NODE)`), `m_pHuffmanBuffer` (`DataSize`), and either `m_pCounts`/`m_pCodes` (when `compression_flag != 0`) or `m_pDataBuffer` (when `compression_flag == 0` for decompression). |
| `cleanup_CHuffmanProcessing` | `int cleanup_CHuffmanProcessing(void)` | Frees `m_pCounts`, `m_pCodes`, `m_pDataBuffer`, `m_pNodes`, and `m_pHuffmanBuffer`. |
| `ExpandDataBlock` | `void ExpandDataBlock(void)` | Decompresses the Huffman bit stream in `m_pHuffmanBuffer` into `m_pDataBuffer` and sets `m_nOutputBytes`: calls `InputCounts()`, `BuildTree()`, and `DoTheExpansion()`. |
| `CompressDataBuffer` | `void CompressDataBuffer(char *pBuf, short nBytes)` | Compresses `nBytes` from `pBuf` into `m_pHuffmanBuffer` and sets `m_nOutputBytes`: calls `CountBytes()`, `ScaleCounts()`, `OutputCounts()`, `BuildTree()`, `ConvertTreeToCode()`, and `DoTheCompression()`. |
| `BuildTree` | `int BuildTree(void)` | Iteratively pairs the two active nodes with minimum `count` weights into parent nodes (`257..512`) until a single root node remains, returning `m_RootNode`. |
| `InputCounts` / `OutputCounts` | `void InputCounts(void)` / `void OutputCounts(void)` | Reads or writes run-length encoded `[first, last, counts..., 0]` symbol frequency tables at the start of `m_pHuffmanBuffer`. |
| `DoTheExpansion` / `InputBit` | `void DoTheExpansion(void)` / `int InputBit(void)` | Traverses `m_pNodes` from `m_RootNode` bit-by-bit (`child_1` on `1`, `child_0` on `0`) until reaching a leaf symbol `<= END_OF_STREAM`. |
| `DoTheCompression` / `OutputBits` | `void DoTheCompression(void)` / `void OutputBits(unsigned long code, int count)` | Emits variable-length Huffman codes from `m_pCodes[]` followed by `m_pCodes[END_OF_STREAM]`. |
| `CountBytes` / `ScaleCounts` / `ConvertTreeToCode` | `void CountBytes(void)` / `void ScaleCounts(void)` / `void ConvertTreeToCode(...)` | Tallies input byte frequencies, scales counts into `1..255` so code lengths never exceed 16 bits, and recursively extracts bit codes from the decoding tree. |

---

## Architectural Role
`unb_huffproc` is invoked by [`j_knud`](j_knud.md) whenever a Knudsen `.keb` packet header indicates Huffman-compressed sample traces. The caller copies the compressed payload into `m_pHuffmanBuffer`, calls `ExpandDataBlock()`, and reads `m_nOutputBytes` of uncompressed echogram samples from `m_pDataBuffer`.
