---
layout: default
title: makefile (seabed)
parent: Seabed Tools
grand_parent: Sidescan Tools
nav_order: 10
tool_name: makefile
source_path: code/sidescan/seabed/makefile
category: Build Configuration
input_formats: ["profile.c"]
output_formats: ["Executable binary (profile)"]
related_tools: ["profile", "bpick"]
---

# makefile (`sidescan/seabed`)

## Overview
The `makefile` in `code/sidescan/seabed/` compiles the [`profile`](profile.md) seabed depth and near-nadir return profiling utility.

## Build Target

* **`profile`** (from [`profile.c`](profile.md)): Compiles with `cc` and links against `-llocal -ljhc -lm`, installing the binary to `$(HOME)/bin/profile`.

## Usage
```bash
cd code/sidescan/seabed
make profile
```
