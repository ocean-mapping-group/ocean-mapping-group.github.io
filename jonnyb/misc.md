---
layout: default
title: misc
parent: Jonathan Beaudoin (jonnyb) Tools
nav_order: 8
tool_name: misc
source_path: code/jonnyb/misc.c
category: Developer Templates & Utilities (jonnyb)
input_formats: ["Any file (-in)"]
output_formats: ["Any file (-out)"]
related_tools: ["misc_omg"]
---

# misc

## Description
`misc` (`code/jonnyb/misc.c`) is Jonathan Beaudoin's boilerplate C command-line skeleton used as a starting point when writing new OMG command-line utilities. It initializes the global `ARGC` and `ARGV` variables required by `support.h` (`usage()`, `error()`, `warning()`), parses `-in <infile>` and `-out <outfile>` arguments, validates that both files can be opened for reading and writing respectively, and cleanly closes both file handles.

---

## Usage

```bash
misc -in <infile> -out <outfile>
```

### Example

```bash
# Copy misc.c as a starting template for a new OMG utility:
cp code/jonnyb/misc.c code/jonnyb/gom_stuff/my_new_tool.c
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <infile>` | Input file path (opened with `fopen(inname, "r")`). | Required |
| `-out <outfile>` | Output file path (opened with `fopen(outname, "w")`). | Required |

---

## Code Structure (`code/jonnyb/misc.c`)

1. **Global Error-Reporting Setup:**
   Assigns `ARGC = argc; ARGV = argv;` so that `usage()` and `error()` from `support.h` print the program name and `USAGE` string on invalid arguments.
2. **Argument Loop:**
   Iterates over `while (*(++argv))` matching `-in` and `-out`.
3. **File Handle Validation:**
   Verifies `if (!inname || !outname) usage("Must specify input/output file");`, opens both files, checks for `NULL` pointers via `error()`, and closes both streams before returning `0`.
