---
layout: default
title: support
parent: Shared Core Libraries (subr)
module_name: support
source_path: code/subr/support.c
header_path: code/subr/support.h
category: Core System, I/O & Time Utilities
related_tools: ["omg_buffer", "array", "mos2", "weigh_grid", "swathed"]
---

# support

## Overview
`support` (`support.c` / `support.h`), originally created by Guy Carpenter (Oct 1989) and expanded by John Hughes Clarke and Jonathan Beaudoin, is the **foundational C utility library** included by nearly every source file in the Ocean Mapping Group codebase. It provides:
1. Standardized CLI usage/warning/fatal error reporting (`usage`, `warning`, `error`) and exit cleanup hooks (`cleanup_register`).
2. Dynamic path and filename manipulation (`mem_strcpy`, `mem_strappend`, `mem_justpath`, `mem_strippath`, `mem_stripprefix`, `mem_stripext`, `mem_replace`).
3. Numeric and geographic angle string parsing (`strtoint`, `strtodbl`, `strtoangle`, `fieldtoint`, `fieldtodbl`) with error checking (`check_error`).
4. Grid boundary rounding helpers (`rounddown`, `roundup`, `roundupforce`).
5. Line-oriented file readers (`getc_line`, `getc_line_jb`, `getc_line_vlength`) and batch file-list loaders (`load_inputfiles_from_list`, powering `-xyzlist` in `mos2`, `weigh_grid`, and `swathed`).

---

## Global Variables, Macros & Types

### CLI Globals
Every OMG `main()` function initializes these globals at startup:
```c
extern int ARGC;      /* Set to argc in main() */
extern char **ARGV;   /* Set to argv in main() */
extern char *USAGE;   /* Defined per-program to describe CLI syntax */
```

### Standard Macros & Types
- `MIN(a,b)`, `MAX(a,b)`, `SQUARE(a)`, `SWAP(A,B,C)`, `TOLOWER(C)`, `PI` (`3.1415926535`)
- `CREATE(T)` — Type-safe allocation macro `((T *)malloc(sizeof(T)))`.
- `boolean` (`unsigned char`), `true` (`0xff`), `false` (`0x00`).
- `error_type` — Enum `{error_val_no_error, error_val_str_not_used}` returned by `check_error()` after string-to-number conversions.

---

## Public Functions

### 1. Diagnostics, Usage & Cleanup Hooks
| Function | Signature | Description |
|---|---|---|
| `usage` | `void usage(char *msg, ...)` | Prints `Usage : <ARGV[0]> <USAGE>` followed by the formatted `(<msg>)` to `stderr`, runs `cleanup()`, and exits with status `1`. |
| `error` | `void error(char *msg, ...)` | Prints `Error : <msg>` to `stderr`, runs `cleanup()`, and exits with status `1`. |
| `warning` | `void warning(char *msg, ...)` | Prints `Warning : <msg>` to `stderr` and continues execution. |
| `cleanup_register` | `void cleanup_register(cleanup_fn *fn)` | Pushes a callback onto a linked list (`cleanup_list`) executed automatically on `cleanup()`, `error()`, or `usage()`. |
| `cleanup` | `void cleanup(void)` | Invokes and frees all registered cleanup callbacks. |

### 2. String & Path Manipulation (Heap-Allocated)
| Function | Signature | Description |
|---|---|---|
| `mem_strcpy` | `char *mem_strcpy(char *str)` | `malloc`s and returns a duplicate of `str` (NULL-safe). |
| `mem_strappend` | `char *mem_strappend(char *str1, char *str2)` | `malloc`s and returns the concatenation `str1 + str2` (tolerates either argument being `NULL`). |
| `mem_justpath` | `char *mem_justpath(char *filename)` | Returns a newly allocated string containing only the directory path up to and including the final `/` (or `NULL` if no `/` is present). |
| `mem_strippath` | `char *mem_strippath(char *filename)` | Returns a newly allocated string containing the basename after the last `/`. |
| `mem_stripprefix` | `char *mem_stripprefix(char *filename)` | Returns a newly allocated string containing only the file extension after the last `.`. |
| `mem_stripext` | `char *mem_stripext(char *filename)` | Returns a newly allocated string with the final `.ext` stripped off. |
| `mem_replace` | `char *mem_replace(char *filename, char *search, char *replace)` | Replaces the first occurrence of `search` in `filename` with `replace` (or deletes `search` if `replace == NULL`). Powers `-swap_dirs` in `mos2`. |
| `word_tolower` | `char *word_tolower(char *str)` | Converts `str` to lowercase in-place and returns `str`. |

### 3. Numeric, Angle & File-List Parsing
| Function | Signature | Description |
|---|---|---|
| `strtoint` / `strtodbl` | `int strtoint(char *s)` / `double strtodbl(char *s)` | Parses an integer or double from `s`; sets `error_val = error_val_str_not_used` if trailing non-numeric characters remain. |
| `fieldtoint` / `fieldtodbl` | `int fieldtoint(char *s, int len)` / `double fieldtodbl(char *s, int len)` | Parses a fixed-width ASCII column of length `len` into an `int` or `double`. |
| `strtoangle` | `double strtoangle(char *s)` | Parses geographic angles into signed decimal degrees; accepts whole degrees (`nnn`), decimal degrees (`nnn.ddd`), degrees/minutes (`nnn'mm.mm` or `nnn^mm.mm`), and trailing hemisphere suffixes (`N`/`E` positive, `S`/`W` negative). |
| `check_error` | `error_type check_error(void)` | Returns and clears `error_val` after `strtoint`/`strtodbl`/`strtoangle`. |
| `rounddown` / `roundup` / `roundupforce` | `double rounddown(double n, double mod)` | Rounds `n` down or up to an exact multiple of `mod`. |
| `getc_line` / `getc_line_jb` / `getc_line_vlength` | `int getc_line(FILE *file, char *string, int printit)` | Reads a newline-terminated line from `file` (with dynamic `OMG_Buffer` growth in `getc_line_vlength`). |
| `load_inputfiles_from_list` | `int load_inputfiles_from_list(char *name, char *allnames[], int *totin)` | Reads a text file list (`-xyzlist`), skips blank lines and `#` comments, prepends the list file's directory path to relative entries, and appends valid file paths into `allnames[]`. |
