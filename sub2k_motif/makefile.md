---
layout: default
title: makefile (sub2k_motif)
parent: Submetrix Motif GUI (sub2k_motif)
nav_order: 21
tool_name: makefile
source_path: sub2k_motif/makefile
category: sub2k_motif
input_formats:
  - C source files (.c, .h)
output_formats:
  - Shared library (libsubx.so)
  - Executable (RTsubx)
related_tools:
  - RTsubx
  - makefile.test_shared
---

# `makefile` (`sub2k_motif/makefile`) — Build Configuration for `RTsubx` and `libsubx.so`

## Overview

`sub2k_motif/makefile` compiles the 19 GUI and interferometric processing modules in `sub2k_motif/` into a shared library (`$(LIB_PATH)/libsubx.so`) and links the main program [`RTsubx.c`](RTsubx.html) against `libsubx.so`, OSF/Motif (or LessTif), X11, and the OMG `liblocal_graphics` and `liblocal` libraries to produce the `RTsubx` executable.

---

## Usage

```bash
# Build libsubx.so and the RTsubx executable
make -f makefile

# Remove intermediate .o object files
make -f makefile clean
```

---

## Build Targets & Configuration

| Target | Dependencies | Action |
| :--- | :--- | :--- |
| `all` | `$(LIB_PATH)/libsubx.so`, `RTsubx` | Builds both the shared library and the `RTsubx` binary |
| `$(LIB_PATH)/libsubx.so` | 19 object files (`$(OBJS)`) | Links `$(OBJS)` into a shared library using `cc $(CFLAGS) -shared -o $(LIB_PATH)/libsubx.so $(OBJS)` |
| `RTsubx` | `RTsubx.c`, `$(LIB_PATH)/libsubx.so`, `$(LIB_PATH)/liblocal.a` | Compiles `RTsubx.c` and links with `-lsubx -llocal_graphics -llocal -lXm -lXt -lX11 -lm`, then copies `RTsubx` to `$(BIN_DIR)` |
| `clean` | None | Executes `rm -f *.o` |

---

## Object Modules Linked into `libsubx.so`

`OBJS` comprises all GUI window, event, callback, and drawing modules:
- `init_windows.o`, `callbacks.o`, `file.o`, `file_selection.o`, `error.o`, `cantsave.o`, `about.o`
- `Str2XmString.o`, `draw_view.o`, `da_all_events.o`, `work_proc.o`, `do_parse.o`, `warning.o`
- `bathy_window.o`, `bathy_events.o`, `draw_bathy.o`, `spacing_select.o`, `threshold_select.o`, `set_values.o`

---

## Multi-Platform Support

The top of `sub2k_motif/makefile` includes platform-specific blocks for:
- **RedHat / Fedora Linux (x86):** `CFLAGS = -g -DLINUX -I/usr/X11R6/include -I/usr/local/LessTif/Motif1.2/include -I$(INC_PATH)`
- **SGI IRIX:** `CFLAGS = -g -cckr -DSGI -I$(INC_PATH)`
- **Sun Solaris / SunOS:** `CFLAGS = -g -DSUN -I/usr/openwin/include ...`
- **HP-UX:** `CFLAGS = -Ae +Z -g -DHP ...`
- **DEC OSF/1 (Tru64):** `CFLAGS = -g -DDIGITAL -I$(INC_PATH)`
