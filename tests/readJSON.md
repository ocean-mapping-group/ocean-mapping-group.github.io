---
layout: default
title: readJSON
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 13
tool_name: readJSON
source_path: code/tests/readJSON.c
category: Binary/JSON Format Inspection (tests)
input_formats:
  - .json (CRIMAC / Kongsberg Simrad EK80 processing metadata & filter JSON files)
output_formats:
  - Recursive typed key-value and array dump on stdout
related_tools:
  - testNormConv
  - EKlook
  - BatchProcEK
---

# readJSON

## Overview
`readJSON` (`code/tests/readJSON.c`, authored by John Hughes Clarke in March 2025) is a recursive JSON parser and schema inspector built using the `json-c` library (`<json.h>`, linked with `-ljson-c`). It was developed to inspect JSON parameter, calibration, decimation filter (`FIL1`), and raw complex $I/Q$ quadrant (`RAW3` `Q1`–`Q4`) files exported by the **CRIMAC** (Centre for Research-based Innovation in Marine Acoustic Abundance Estimation and Coastal Zone Management) Simrad EK80 broadband processing pipeline.

It loads a JSON document from disk (`json_object_from_file`), traverses every nested JSON object (`json_parse`) and JSON array (`json_parse_array`), and prints the `json_type` enumeration, key name, array length, and typed scalar values (`boolean`, `double`, `int`, `string`) to `stdout`.

---

## Syntax & CLI Options

```bash
readJSON [-v] [-savearray <keyname> ...] [-depth <m>] -in <input.json> -out <outfile>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-in <file.json>` | **Required.** Input JSON file path (e.g., CRIMAC EK80 configuration or ping data JSON). | None |
| `-out <outfile>` | **Required on CLI.** Output filename string (`outname` is validated on the command line; all parsed JSON output is currently printed to `stdout`). | None |
| `-savearray <key>` | Repeatable option (up to 10 keys) to register target JSON array keys (`savearray[nosavearray]`) for extraction. | `0` keys |
| `-depth <m>` | Optional numeric depth parameter parsed via `strtodbl()`. | Unused |
| `-v` | Increment verbose flag (`verbose_flag++`). | `0` |

---

## Recursive JSON Traversal Architecture

`readJSON` implements three mutually recursive traversal functions over `json_object *` trees from `json-c`:

### 1. Object Key-Value Iterator (`json_parse(json_object *jobj)`)
Uses the `json_object_object_foreach(jobj, key, val)` macro to inspect each property in a JSON object and dispatches on `json_object_get_type(val)`:
* `json_type_null` (`0`): Prints `json_type_null`.
* `json_type_boolean` (`1`): Prints `\t 1 - <key> b value: <0|1>`.
* `json_type_double` (`2`): Prints `\t 2 - <key> d value: <double>`.
* `json_type_int` (`3`): Prints `\t 3 - <key> i value: <int>`.
* `json_type_object` (`4`): Prints `descending into lower object : <key>` and recursively calls `json_parse(json_object_object_get(jobj, key))`.
* `json_type_array` (`5`): Retrieves the array via `json_object_object_get(jobj, key)`, prints its length via `json_object_array_length()`, and invokes `json_parse_array(jobj, key)`.
* `json_type_string` (`6`): Prints `\t 6 - <key> s value: <string>`.

### 2. Recursive Array Unpacker (`json_parse_array(json_object *jobj, char *key)`)
Iterates from `i = 0` to `arraylen - 1` using `json_object_array_get_idx(jarray, i)`:
* If element `i` is itself a nested `json_type_array`, recursively calls `json_parse_array(jvalue, NULL)`.
* If element `i` is a `json_type_object`, calls `json_parse(jvalue)`.
* Otherwise, prints `value[i]: ` followed by `print_json_value(jvalue)`.

### 3. EK80 / CRIMAC Schema Targets
In `main()`, `readJSON` declares `json_object` pointers corresponding to standard Kongsberg EK80 / CRIMAC structures:
* **Transducer & Environment Parameters:** `FrequencyPar`, `frequencies`, `gain`, `angle_offset_athwartship`, `angle_offset_alongship`, `beam_width_athwartship`, `beam_width_alongship`, `Environment`, `Parameter`.
* **Filter & Raw Sample Blocks:** `FIL1` (`f1`, `f2` stage-1 and stage-2 FIR decimation filters) and `RAW3` (`Q1`, `Q2`, `Q3`, `Q4` split-beam complex $I/Q$ quadrants).

---

## Example Usage

```bash
# Inspect the full hierarchy of a CRIMAC EK80 JSON dump
readJSON -in crimac_ek80_ping.json -out dump.txt | less
```
To test matched-filter complex convolution on extracted EK80 $I/Q$ filter and trace arrays, see [`testNormConv`](testNormConv.md).
