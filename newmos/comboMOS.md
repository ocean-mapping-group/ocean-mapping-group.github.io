---
layout: default
title: comboMOS
parent: Sidescan Mosaicking (newmos)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 2
tool_name: comboMOS
source_path: code/newmos/comboMOS.c
category: Backscatter & Sidescan Mosaicking
input_formats:
- .mos
- .ran
- wts_*.mos
- .shifts
output_formats:
- .mos
- .ran
related_tools:
- mos2
- make_blank
- tomos
- jview
- makeWts
---

# comboMOS

## Description
`comboMOS` (`code/newmos/comboMOS.c`, written by John Hughes Clarke, May 2004) merges multiple co-registered 8-bit backscatter mosaics (`<line_or_block>.mos`) and their companion priority-weight/range arrays (`<line_or_block>.ran`) into a single composite mosaic (`<comboprefix>.mos` and `<comboprefix>.ran`) using **pixel-by-pixel weight autoseaming**.

When a large survey is mosaicked in separate sub-blocks, days, or individual survey lines onto identical mapsheet bounds (`header.dx x header.dy`), `comboMOS` iterates through up to 5,000 input `.mos` files and compares the priority weight of each valid pixel (`ran != 255`) against the composite `.ran` buffer. Following the JCU/OMG range-weight convention where **smaller numbers in `.ran` represent higher priority** (`0` = highest weight, `254` = lowest weight, `255` = unpainted/background), `comboMOS` retains whichever pixel has the smaller `.ran` value:

```c
if (in_ranbuf[idx] != 255 && in_ranbuf[idx] < out_ranbuf[idx]) {
    out_mosbuf[idx] = in_mosbuf[idx];
    out_ranbuf[idx] = in_ranbuf[idx];
}
```
It also supports applying per-mosaic Digital Number (`.shifts`) radiometric offsets (`-use_shifts`) or generating a color-coded seam-index map (`-paint_frame`) showing which input mosaic won at every pixel.

---

## Usage

```bash
comboMOS [-v] [-brad_custom] [-use_shifts] [-paint_frame] -out <comboprefix> <input1.mos> [input2.mos ...]
```

### Example Workflow

```bash
# Combine daily sub-mosaics (day100.mos/day100.ran, day101.mos/day101.ran) into a master mosaic
comboMOS -v -out master_bay day100.mos day101.mos day102.mos

# Combine per-line mosaics while applying radiometric DN offsets from <line>.shifts files
comboMOS -use_shifts -out calibrated_bay line_*.mos

# Generate a color-coded seam ownership map (pixels painted with colors 8..13)
comboMOS -paint_frame -out master_bay_seams day100.mos day101.mos day102.mos
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-out <comboprefix>` | **Required.** Output prefix for the combined `<comboprefix>.mos` and `<comboprefix>.ran` files. Unlike `mos2`, `comboMOS` creates and initializes `<comboprefix>.mos` and `<comboprefix>.ran` (primed to `255`) directly using the 1024-byte `JHC_header` of the first input `.mos` file. | None |
| `<input.mos ...>` | **Required.** One to 5,000 input `.mos` files. All input files **must** share identical grid dimensions (`header.dx` and `header.dy`). | None |
| `-use_shifts` | For each `<name>.mos`, opens `<name>.shifts` and reads an integer Digital Number offset (`dB_shifts`). Adds this shift to all valid pixels (`!= 255`) of `<name>.mos` (clamped to `[0, 254]`) before compositing. If `<name>.shifts` is absent, a shift of `0` is used. | Disabled |
| `-brad_custom` | Instead of opening `<prefix>.ran` for each `<prefix>.mos`, opens `wts_<prefix>.mos` as the companion weight grid. | Standard `<prefix>.ran` |
| `-paint_frame` | Diagnostic seam-visualization mode: instead of writing the backscatter amplitude from `in_mosbuf`, writes `8 + (current_file % 6)` into `<comboprefix>.mos` so each contributing input mosaic is rendered in a distinct primary color (`COL_OFFSET = 8` in `jview`). | Disabled |
| `-v` | Enable verbose output. | Disabled |

---

## Architectural Notes
- **Progressive Disk Flushing**: After compositing each input `.mos` file in memory, `comboMOS` immediately flushes `out_mosbuf` and `out_ranbuf` to `<comboprefix>.mos` and `<comboprefix>.ran` so the user can inspect intermediate progress in [`jview`](../JV/jview.html).
- **Strict Mapsheet Alignment**: Every input `.mos` file must have been initialized from the exact same `.blank` mapsheet (`header.dx == thehead.dx && header.dy == thehead.dy`); otherwise `comboMOS` exits with `"YO dude, an input file that hasn't got the same dimensions !"`.
