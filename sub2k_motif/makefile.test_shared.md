---
layout: default
title: makefile.test_shared (sub2k_motif)
parent: Submetrix Motif GUI (sub2k_motif)
nav_order: 22
tool_name: makefile.test_shared
source_path: sub2k_motif/makefile.test_shared
category: sub2k_motif
input_formats:
  - C source files (.c, .h)
output_formats:
  - Shared library (libsubx.so)
  - Executable (RTsubx)
related_tools:
  - makefile
  - RTsubx
---

# `makefile.test_shared` (`sub2k_motif/makefile.test_shared`) — Shared Library Test Makefile

## Overview

`sub2k_motif/makefile.test_shared` is an alternate build configuration used to test dynamic linking of `libsubx.so` with `RTsubx` without requiring `-llocal_graphics` at link time.

---

## Usage

```bash
make -f makefile.test_shared
```

---

## Differences from `sub2k_motif/makefile`

| Feature | `sub2k_motif/makefile.test_shared` | `sub2k_motif/makefile` |
| :--- | :--- | :--- |
| Link Libraries (`RTsubx`) | `-lsubx -llocal $(XLIBS) -lm` | `-lsubx -llocal_graphics -llocal $(XLIBS) -lm` |
| Shared Library Target | `$(LIB_PATH)/libsubx.so` built with `cc $(CFLAGS) -shared` | Identical (`$(LIB_PATH)/libsubx.so`) |

---

## How It Works

When testing `libsubx.so` on systems where all X11/Motif drawing routines are self-contained inside `sub2k_motif/` (`draw_view.o`, `draw_bathy.o`, `init_windows.o`) rather than calling external `liblocal_graphics` primitives, `makefile.test_shared` links `RTsubx` directly against `-lsubx -llocal -lXm -lXt -lX11 -lm`.
