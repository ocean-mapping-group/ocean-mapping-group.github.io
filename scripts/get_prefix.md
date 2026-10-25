---
layout: default
title: get_prefix
parent: Helper Scripts
tool_name: get_prefix
source_path: code/scripts/get_prefix
category: Batch Processing & File Management Scripts
related_tools: ["tomos", "tor4", "bunravel", "rename"]
---

# get_prefix

## Overview
`get_prefix` (`code/scripts/get_prefix`) is a lightweight `tcsh` and `awk` helper script used by OMG shell pipelines (such as [`tomos`](tomos.md) and [`tor4`](tor4.md)) to strip the trailing file extension (e.g., `.blank`, `.merged`, `.ss`, `.all`) from one or more filenames and print the base prefix.

---

## Usage

```bash
get_prefix <filename(s) ...>
```

---

## How It Works
For each filename argument passed on the command line, `get_prefix` splits the string on `.` (`awk -F.`) and prints all dot-separated fields except the final extension field (`for (i=1; i<NF; i++) print $i`):

```tcsh
#!/bin/tcsh

if ($# == 0) then
	exit(0)
endif

foreach FILE ($*)
	echo $FILE | awk -F. '{for (i=1;i<NF;i++) print $i }'
end

exit
```

### Example
```bash
$ get_prefix bay_of_fundy.blank
bay_of_fundy
```
