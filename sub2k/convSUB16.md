---
layout: default
title: convSUB16
parent: SUB2K Tools
grand_parent: code
nav_order: 1
---
# convSUB16

## Description
`convSUB16` is a utility designed to convert 16-bit intensity sidescan data from Submetrix 2000 into an 8-bit GLORIA format (typically a `.sst` file). It processes OMG_HDCS merged files, extracting profile and beam information, and then reads associated 16-bit sidescan data (`.ss_data`). The tool offers various scaling options (linear, square root, TVG, or logarithmic) to effectively compress the high-resolution 16-bit data into an 8-bit dynamic range suitable for display or further processing.

## Usage
```bash
convSUB16 [-v] [-linss | -sqrtss | -tvgss] [-dump_ping <ping_num>] [-dump_sample <sample_num>] [-min16 <value>] [-max16 <value>] <mergedfile>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-v` | Enable verbose output, providing more detailed processing messages. | (None) |
| `-linss` | Apply linear scaling to the 16-bit data. | (None, mutually exclusive) |
| `-sqrtss` | Apply square root scaling to the 16-bit data. | (None, mutually exclusive) |
| `-tvgss` | This option is present but its functionality for TVG-based scaling is not explicitly implemented in the provided code snippet (falls through to logarithmic by default). | (None, mutually exclusive) |
| `-dump_ping <ping_num>` | Debugging option: Prints all samples for a specific ping and exits. | (None) |
| `-dump_sample <sample_num>` | Debugging option: Prints the value of a specific sample for every other ping. | (None) |
| `-min16 <value>` | Sets the minimum 16-bit value for the scaling range. | `0` |
| `-max16 <value>` | Sets the maximum 16-bit value for the scaling range. | `64000` |
| `<mergedfile>` | **Required.** The input OMG_HDCS merged file. The tool will also look for `<mergedfile>.ss_data` (for 16-bit sidescan) and will create `<mergedfile>.sst` (for 8-bit output). |

## How It Works
1.  **Argument Parsing & Initialization:** The tool parses command-line arguments to set scaling parameters (`min16`, `max16`) and flags for different scaling methods (`linear_ss`, `sqrtss`, `tvgss`).
2.  **Min/Max Range Setup:** It calls `set_Min_Max_Range` to initialize internal min/max values for different scaling types.
3.  **File Handling:**
    *   Opens the input OMG_HDCS merged file.
    *   Opens an associated `.sst` file for writing the 8-bit GLORIA output.
    *   Opens an associated `.ss_data` file for reading the raw 16-bit sidescan data.
4.  **Process Pings:** It iterates through each ping (record) in the merged file:
    *   **Read Profile:** Reads the `OMG_HDCS_profile_header` for the current ping.
    *   **Read GLORIA Header:** Reads the corresponding GLORIA record header from the `.sst` file (to get byte offset and number of samples from `cb_offset[0]` and `cb_depth[0]`).
    *   **Seek 16-bit Data:** Uses the `byteoffset` and `nosams` from the GLORIA header to seek to the correct location in the `.ss_data` file and reads `nosams` 16-bit samples into `dat16`.
    *   **Debug Options:** If `-dump_ping` or `-dump_sample` are used, specific debugging information is printed.
    *   **Scaling and Compression:** For each 16-bit sample (`fval`) in `dat16`:
        *   **Linear Scaling (`-linss`):** `fval = (fval - min16) / (max16 - min16);`
        *   **Square Root Scaling (`-sqrtss`):** `fval = sqrt(fval); fval = (fval - minsqrt) / (maxsqrt - minsqrt);`
        *   **Logarithmic Scaling (Default or if `-tvgss`):** `fval = log(fval); fval = (fval - minlog) / (maxlog - minlog);`
        *   The scaled `fval` is then multiplied by 255.0 and clamped to the 0-255 range to create an 8-bit value (`dat8`).
    *   **Collapse into 512 (`collapse_into_512`):** The `dat8` array (containing `nosams` 8-bit samples) is collapsed into a 512-sample GLORIA record. This involves averaging `ipack` (where `ipack = rxsamps / 512`) samples into one GLORIA pixel. The processed 8-bit data is then assigned to the port or starboard side of `grec` based on `current_side`.
    *   **Write GLORIA Record:** The resulting 8-bit `grec` is written to the `.sst` file.
5.  **File Closing:** All opened files are closed.
