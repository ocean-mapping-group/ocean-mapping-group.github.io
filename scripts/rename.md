---
layout: default
title: rename
parent: Helper Scripts
tool_name: rename
source_path: code/scripts/rename
category: Batch Processing & File Management Scripts
related_tools: ["get_prefix", "tomos", "tor4"]
---

# rename

## Overview
`rename` (`code/scripts/rename`) is the classic Perl regular-expression batch file-renaming utility (originally written by Larry Wall and enhanced with `Getopt::Long` safety checks by Robin Barker) bundled in `code/scripts/` for batch renaming survey lines, Kongsberg `.all`/`.kmall` files, and OMG-HDCS `.merged`/`.ss` derivatives.

---

## Usage

```bash
rename [-v] [-n] [-f] '<perlexpr>' [filenames ...]
```

If no `filenames` are provided on the command line, `rename` reads target filenames from `stdin` (one per line), making it easy to pipe output from `find` or `ls`.

---

## Command-Line Options

| Option | Description |
|---|---|
| `-v`, `--verbose` | Verbose: print each file successfully renamed (`<old> renamed as <new>`). |
| `-n`, `--no-act` | Dry-run mode: show what files *would* be renamed without modifying the filesystem (automatically enables `-v`). |
| `-f`, `--force` | Overwrite existing target files if the destination filename already exists (by default, `rename` skips and warns if the destination exists). |
| `<perlexpr>` | **Required.** A Perl expression (such as `s/old/new/` or `y/A-Z/a-z/`) that modifies `$_` for each input filename. |

---

## Examples in Hydrographic Processing Workflows

```bash
# Preview (-n) stripping .bak extensions from backed-up .merged files
rename -n 's/\.bak$//' *.merged.bak

# Rename .all.merged files to .merged
rename -v 's/\.all\.merged$/.merged/' *.all.merged

# Convert uppercase filenames to lowercase
rename 'y/A-Z/a-z/' *
```
