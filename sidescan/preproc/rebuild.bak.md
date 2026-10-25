---
layout: default
title: rebuild.bak
parent: Preprocessing Tools
grand_parent: Sidescan Tools
nav_order: 4
tool_name: rebuild.bak
source_path: code/sidescan/preproc/rebuild.bak
category: Sidescan Preprocessing
input_formats: ["C-shell Script Template"]
output_formats: ["N/A"]
related_tools: ["rebuild_neaust", "rebuild_neaust.bak", "neaust_fixazi"]
---

# rebuild.bak

## Description
`rebuild.bak` is the initial C-shell header stub (`#!/bin/csh`, written by Guy Carpenter, November 7, 1990) in `code/sidescan/preproc/` that served as the starting template for [`rebuild_neaust`](rebuild_neaust.md).

## Script Contents
```csh
#!/bin/csh
#
# rebuild - Nov 7, 1990 - Guy Carpenter
```
For the complete 6-stage GLORIA batch preprocessing implementation, see **[`rebuild_neaust`](rebuild_neaust.md)**.
