---
layout: default
title: mboneTool
parent: MB-System .mb1 Format (mb1)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 2
tool_name: mboneTool
source_path: code/mb1/mboneTool.c
category: Raw Data Unraveling & Format Conversion
input_formats:
- .tdy (Teledyne MB1)
output_formats:
- STDOUT packet inventory & header dump
related_tools:
- mbone2omg
---

# mboneTool

## Overview

`mboneTool` (`code/mb1/mboneTool.c`) is a command-line diagnostic and packet-inspection utility for **Teledyne `.tdy` (MB1 / RTA1)** binary sonar files.

Before unpacking a `.tdy` file with [`mbone2omg`](mbone2omg.html), operators can run `mboneTool` to verify file integrity, inspect the total packet count by record type (`FILE_HEADER`, `TDYMB01`, and `TDYRTA1` sub-types), and selectively dump the parsed header fields of specific packet IDs using `-vid <ID>` or `-v`.

---

## Usage

```bash
mboneTool [-v] [-vid <ID>] -in <inputfile.tdy>
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-in` | `<inputfile.tdy>` | **Required.** Path to the input Teledyne `.tdy` binary file. |
| `-v` | *(none)* | Enables full verbose mode: prints every packet ID as it is encountered (`Got ID: <id> --> <name>`) and pretty-prints the full header contents of all `FILE_HEADER`, `TDYMB01`, and `TDYRTA1` records. |
| `-vid` | `<ID>` | Enables selective header pretty-printing (`verbose_id[ID]++`) for a specific integer packet ID (`1` through `6`, repeatable) without printing every other packet type. |

---

## Supported Packet IDs & Structures (`omg_mb1.h`)

`mboneTool` allocates tracking arrays (`verbose_id`, `count`, `corrupt`, `sizes`) of length `MB1_ID_MAX_ID` (`7`) and dispatches each record returned by `get_next_MB1_rec_type(infile)` across the following IDs defined in `/home/iwc/local/include/omg_mb1.h`:

| Packet ID (`-vid`) | Macro Name | Parser & Printer Functions | Description |
| :--- | :--- | :--- | :--- |
| `1` | `MB1_ID_FILE_HEADER` | `parse_MB1_File_Header()` / `print_MB1_File_Header()` | 61-byte `MB1_File_Header` containing the 48-byte ASCII file signature and UTC start timestamp (`year`, `month`, `day`, `hour`, `minute`, `second`, `milliseconds`). |
| `2` | `MB1_ID_TDYMB01` | `parse_MB1_MB01_Header()` / `print_MB1_MB01_Header()` | `MB1_MB01_Header` multibeam ping record containing sonar model/serial/firmware metadata, ping number, segment offset directory (`TIME`, `RAW`, `PROC`, `AR`, `QUAL`, `SNIPPET`, `SS`, `WC`), and parsed sub-segments. |
| `3` | `MB1_ID_TDYRTA1_0` | `parse_MB1_RTA1_Header()` / `print_MB1_RTA1_Header()` | Teledyne Real-Time Appliance (`TDYRTA1`) packet with `sub_id == 0`. |
| `4` | `MB1_ID_TDYRTA1_1` | `parse_MB1_RTA1_Header()` / `print_MB1_RTA1_Header()` | Teledyne Real-Time Appliance (`TDYRTA1`) packet with `sub_id == 1`. |
| `5` | `MB1_ID_TDYRTA1_2` | `parse_MB1_RTA1_Header()` / `print_MB1_RTA1_Header()` | Teledyne Real-Time Appliance (`TDYRTA1`) packet with `sub_id == 2`. |
| `6` | `MB1_ID_TDYRTA1_4` | `parse_MB1_RTA1_Header()` / `print_MB1_RTA1_Header()` | Teledyne Real-Time Appliance (`TDYRTA1`) packet with `sub_id == 4`. |

---

## Example Output

When run without `-v` or `-vid`, `mboneTool` scans the entire `.tdy` file and prints a summary table at completion:

```text
Got file size 104857600
(1)             MB1_ID_FILE_HEADER                       00001 (0 corrupt) 0 bytes
(2)             MB1_ID_TDYMB01                           01420 (0 corrupt) 0 bytes
(3)             MB1_ID_TDYRTA1_0                         00355 (0 corrupt) 0 bytes
```

---

## Architectural Fit

`mboneTool` serves the same diagnostic role for Teledyne `.tdy` files that `kmall_index` / `read_kmall -v` serves for Kongsberg `.kmall` files, enabling rapid verification of packet counts, sonar firmware headers, and segment presence before running [`mbone2omg`](mbone2omg.html).
