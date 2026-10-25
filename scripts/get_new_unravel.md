---
layout: default
title: get_new_unravel
parent: Helper Scripts
tool_name: get_new_unravel
source_path: code/scripts/get_new_unravel
category: Batch Processing & File Management Scripts
related_tools: ["bunravel", "unravel_KMALL_2500m_RevHplus_netatt2_parallel", "get_prefix", "rename"]
---

# get_new_unravel

## Overview
`get_new_unravel` (`code/scripts/get_new_unravel`) is a `tcsh` bootstrap utility script written by Jonathan Beaudoin to fetch and unpack the `new_unravel` batch multibeam unraveling script into a working survey directory.

---

## Usage

```bash
get_new_unravel
```

---

## Script Behavior

1. **Existence Check:** Checks whether a `new_unravel` script already exists in the current working directory (`if (-e new_unravel)`). If present, it prints:
   ```text
   Hey...you've already got a new_unravel script!
   ```
   and exits cleanly (`exit(0)`) to avoid overwriting local survey-specific customizations (such as vessel lever arms, SVP paths, or mapsheet bounds).
2. **Download & Extraction:** If `new_unravel` is not present, it downloads the compressed template from the UNB Ocean Mapping Group server (`wget http://www.omg.unb.ca/~jonnyb/processing/new_unravel.gz`), decompresses it via `gunzip new_unravel.gz`, and marks it executable (`chmod +x new_unravel`).

---

## Source Code (`code/scripts/get_new_unravel`)

```tcsh
#!/bin/tcsh

if (-e new_unravel) then
	echo "Hey...you've already got a new_unravel script!"
	exit(0)
endif

wget http://www.omg.unb.ca/~jonnyb/processing/new_unravel.gz
gunzip new_unravel.gz
chmod +x new_unravel

exit(0)
```
