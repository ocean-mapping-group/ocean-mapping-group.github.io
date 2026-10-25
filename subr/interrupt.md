---
layout: default
title: interrupt
parent: Core Shared Libraries (subr)
module_name: interrupt
source_path: code/subr/interrupt.c
header_path: code/subr/interrupt.h
category: "System Utilities, Memory & File I/O"
related_tools:
  - mos2
  - weigh_grid
  - swathed
  - RT
---

# `interrupt` — Graceful POSIX Signal Trapping for Long-Running Processes

## Overview & Purpose
The `interrupt` module (`code/subr/interrupt.c` and `code/subr/interrupt.h`) provides a lightweight POSIX signal-trapping mechanism originally written by Guy Carpenter at James Cook University of North Queensland (`JCUNQ`) on February 9, 1990. In the Ocean Mapping Group (`OMG`) architecture, batch gridding and sidescan mosaicking programs maintain large in-memory LRU tile caches (`code/subr/cache.c`) backed by temporary disk files. If a user presses `Ctrl-C` (`SIGINT`) or disconnects a terminal session (`SIGHUP`) during a multi-hour run, immediate process termination would leave cached grid tiles unflushed and output `.r4` files corrupted. `interrupt` traps these signals and sets a pollable global flag (`interrupt_flag`) so processing loops can finish the current ping or cleanly flush and close output files before exiting.

---

## Global State Variables (`interrupt.h` / `interrupt.c`)

```c
extern int interrupt_flag;
```
- **`interrupt_flag`:** Initialized to `0` (`false`) when `interrupt_trap()` is called. Asynchronously set to `1` (`true`) by `interrupt_handler()` whenever `SIGINT` or `SIGHUP` is delivered to the process.
- **`oldHUPhandler`, `oldINThandler`:** Internal `void *` pointers in `interrupt.c` that preserve the previous signal dispositions returned by `signal(SIGHUP, ...)` and `signal(SIGINT, ...)` so they can be restored when critical sections complete.

---

## Public Functions & Signatures

### 1. Enable Signal Trapping
```c
void interrupt_trap(void);
```
- **Purpose:** Installs `interrupt_handler` as the active signal handler for both `SIGHUP` (terminal hangup) and `SIGINT` (keyboard interrupt `Ctrl-C`), saves the previous handlers in `oldHUPhandler` and `oldINThandler`, and resets `interrupt_flag = 0`.
- **Error Handling:** If `signal()` returns `-1` (`SIG_ERR`), calls `error("interrupt_trap: failed to trap signal ...")` via `code/subr/error.c`.

### 2. Restore Original Signal Handlers
```c
void interrupt_untrap(void);
```
- **Purpose:** Restores the saved signal handlers (`oldHUPhandler` and `oldINThandler`) for `SIGHUP` and `SIGINT`. Typically called once a batch ping loop finishes and the program is ready to flush its cache and exit normally.

### 3. Asynchronous Signal Callback
```c
void interrupt_handler(int sig, int code, int scp);
```
- **Purpose:** Invoked by the OS kernel when `SIGINT` or `SIGHUP` arrives. Sets `interrupt_flag = true` and emits a non-fatal diagnostic message (`warning("Interrupt (%d) trapped", sig)`) to `stderr` so the user knows the interrupt was acknowledged and graceful shutdown is underway.

---

## How It Fits Into the OMG Architecture
`interrupt` is used in batch processing engines and interactive X11/Motif viewers that perform heavy disk or graphics operations:
- **Sidescan Mosaicking (`mos2`):** Calls `interrupt_trap()` before iterating over survey lines; checks `if (interrupt_flag)` after each ping so an interrupted mosaic still flushes all modified cache blocks (`cache_flush()`) and writes a valid `.r4` / `.b` mosaic file.
- **Weighted Bathymetric Gridding (`weigh_grid`):** Traps `SIGINT`/`SIGHUP` during multi-file swath accumulation so partial grids can be normalized and written to disk if the user aborts early.
- **Interactive Swath & Real-Time Viewers (`swathed`, `RT`):** Used in `SE_WaterColumn.c` and `RT_unravel.c` to allow users to cancel long water-column stacking or real-time playback loops cleanly without crashing the GUI session.
