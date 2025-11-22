---
layout: default
title: targethunt.h
parent: OMG Tools
nav_order: 71
---
# targethunt.h

## Description
`targethunt.h` is a header file that serves as an interface for the `targethunt` functionality, defining constants and including other necessary headers. It is designed to be used in conjunction with `targethunt.c` and `c_wcpick.h` to provide tools for detecting and managing targets within water column data.

The file primarily sets up the environment for the target hunting process within the broader OMG toolkit.

## Macros
```c
#define _C_TARGETHUNT
#define MAXSLOTSIZE 1000
```
*   `_C_TARGETHUNT`: A preprocessor macro to prevent multiple inclusions of this header file.
*   `MAXSLOTSIZE`: Defines the maximum number of water column pings/swaths that can be processed in one "slot" or chunk by the `targethunt` application.

## Includes
```c
#include "c_wcpick.h"
```
This header file includes `c_wcpick.h`, which suggests that the core target detection logic (e.g., `c_hunt_for_detections`, `c_mark_targets`) is defined and implemented in `c_wcpick.c` or a related module.

## Comment Codes
The header file also includes a detailed section of "Some comment codes used" which are conventions for developers working on this project. These codes indicate:
*   **Future work:** `TODO`, `TASK`
*   **Debug stuff:** `HACK`, `FIXME`, `TESTING`, `CHECK_ME`
*   **Other useful comments:** `TEST`, `UNUSED`, `DEPRECATED`, `DANGER`, `WARNING`, `BUG`

## Purpose
The `targethunt.h` header defines the foundational elements needed for the `targethunt` program to operate. It makes available the `MAXSLOTSIZE` constant and integrates the `c_wcpick` module, which is central to its target detection capabilities. It also indicates the typical structure of variables that would be associated with a target hunting widget or GUI, even though these variables themselves are commented out.
