---
layout: default
title: bunravel
parent: Automated Processing Scripts (scripts)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 2
tool_name: bunravel
source_path: code/jonnyb/scripts/bunravel
category: Raw Data Unraveling
input_formats:
- .all
- .wcd
output_formats:
- .merged
- .rawfilesize
- .flag_bk
- .ss
- .ss_detvg
- .watercol
related_tools:
- RTlite
- dumpFlags
- mergeAtt
- mergeNav
- getBounds
- swathed
- makess
- deTVG
- moveOverWCinfo
---

# bunravel

## Description
`bunravel` (Bash Unravel, authored by Jonathan Beaudoin) is the standard automated batch-processing script for legacy Kongsberg Maritime `.all` and `.wcd` multibeam files. It orchestrates [`RTlite`](../RTLite/RTlite.html), [`dumpFlags`](../omg/dumpFlags.html), [`mergeAtt`](../omg/mergeAtt.html), [`mergeNav`](../nav/mergeNav.html), [`getBounds`](../omg/getBounds.html), [`makess`](../omg/makess.html), [`deTVG`](../omg/deTVG.html), and [`moveOverWCinfo`](../omg/moveOverWCinfo.html) across local `raw/` subdirectories or via incremental `rsync` from a shipboard logging directory.

 A key feature of `bunravel` is its `.rawfilesize` tracking mechanism: for every `.all` file converted, it records the byte size of the `.all` file in `merged/<subdir>/<prefix>.rawfilesize`. On subsequent runs, if a `.merged` file already exists and its `.rawfilesize` matches the current `.all` file size, `bunravel` automatically skips the file (unless `-F` is passed). If the `.all` file was still being logged by SIS during the previous run and has since grown in size, `bunravel` detects the size mismatch and automatically re-unravels it while preserving any `swathed` cleaning flags via `dumpFlags`!

---

## Usage

```bash
bunravel [OPTIONS] -f "raw/subdir/*.all"
# OR rsync from a remote/mounted logging directory:
bunravel [OPTIONS] -r /mnt/sis_logging/ -l raw/
```

### Common Examples

**1. Unravel all `.all` files in `raw/JD100/` with `deTVG` backscatter (`-d -s 4`) and water column (`-w`):**

```bash
bunravel -v -w -d -s 4 -f "raw/JD100/*.all"
```

**2. Force re-unraveling of specific files (`-F`) and open each line in `swathed` (`-i`):**

```bash
bunravel -F -i -f "raw/JD100/0001_*.all"
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-f "<files>"` | Specify local `.all` file(s) to process (quote wildcards so `bunravel` or the shell expands them properly). | Required (unless `-r` is used) |
| `-r <remote_dir>` | Rsync new `.all` files (excluding `9999.all` active logging file) from `<remote_dir>` into `<local_dir>` (`raw/` by default) and unravel any new or grown files. | Disabled |
| `-l <local_dir>` | Local directory to `rsync` into when `-r` is used. | `raw/` |
| `-F` | Force re-conversion of all specified `.all` files even if `<prefix>.merged` already exists and `.rawfilesize` has not changed. | Skip already-unravelled files (`0`) |
| `-w` | Unpack water column data (`-unpack_watercol` in `RTlite`). Also checks for a companion `.wcd` file, unpacks it to `WCD_<prefix>.merged`, transfers water column pointers via `moveOverWCinfo -tol 0.002`, and renames `WCD_<prefix>.watercol` to `<prefix>.watercol`. | Disabled (`0`) |
| `-d` | Run [`deTVG`](../omg/deTVG.html) on `<prefix>.merged` and generate a second un-normalized sidescan file `ss/<subdir>/<prefix>.ss_detvg` via `makess -use_deTVG`. | Disabled (`0`) |
| `-s <shift>` | Digitizer sample shift (`-digitizer_sample_shift <shift>`) passed to `deTVG` when `-d` is active. | `0` |
| `-i` | Interactive inspection mode: launches [`swathed`](../SE/swathed.html) on `<prefix>.merged` right after `getBounds` and waits for the user to close `swathed` before generating sidescan and moving to the next file. | Disabled (`0`) |
| `-v` | Verbose mode: prints parsed `RAWDIR`, `SUBDIRS`, `OUTFILE_PREFIX`, and `SUFFIX` for each file. | Disabled (`0`) |
| `-h` | Show usage help message. | |

---

## Step-by-Step Pipeline Executed by `bunravel`

For each `<FILE>` (`raw/<SUBDIRS>/<OUTFILE_PREFIX>.all`):

1. **Incremental Check:** Compares `stat -f '%z' $FILE` against `merged/$SUBDIRS/$OUTFILE_PREFIX.rawfilesize`. Skips if `.merged` exists, size is unchanged, and `-F` is not set.
2. **Save Existing Flags:** If `.merged` already exists, runs `dumpFlags merged/$SUBDIRS/$OUTFILE_PREFIX` to back up manual `swathed` edits to `.flag_bk`.
3. **Unpack `.all` via `RTlite`:**

   ```bash
   RTlite [-unpack_watercol] -v4 -float_twtt \
       -auto_write_primary_nav -auto_write_primary_orientation -rescale_BSN \
       -infile $FILE -outprefix merged/$SUBDIRS/$OUTFILE_PREFIX
   ```
   *(Note: `-auto_write_primary_nav` and `-auto_write_primary_orientation` automatically create `.nav` and `.orientation` for `.all` files, unlike `read_kmall` which requires manual `cp` of `.nav_1` and `.net_att_2`.)*
4. **Restore Flags:** If `.flag_bk` exists, runs `dumpFlags -load merged/$SUBDIRS/$OUTFILE_PREFIX`.
5. **Merge Attitude & Navigation:**

   ```bash
   mergeAtt merged/$SUBDIRS/$OUTFILE_PREFIX
   mergeNav merged/$SUBDIRS/$OUTFILE_PREFIX.merged
   ```
6. **Build Spatial Index:** Runs `getBounds merged/$SUBDIRS/$OUTFILE_PREFIX.merged`.
7. **Optional Interactive Editing (`-i`):** Runs `swathed merged/$SUBDIRS/$OUTFILE_PREFIX.merged`.
8. **Generate Sidescan (`.ss` and optional `.ss_detvg`):**

   ```bash
   makess merged/$SUBDIRS/$OUTFILE_PREFIX.merged ss/$SUBDIRS/$OUTFILE_PREFIX.ss
   # If -d is specified:
   deTVG -digitizer_sample_shift $DETVG_SHIFT -in merged/$SUBDIRS/$OUTFILE_PREFIX.merged
   makess -use_deTVG merged/$SUBDIRS/$OUTFILE_PREFIX.merged ss/$SUBDIRS/$OUTFILE_PREFIX.ss_detvg
   ```
9. **Optional Companion `.wcd` Processing (`-w`):**
   If `raw/$SUBDIRS/$OUTFILE_PREFIX.wcd` exists:

   ```bash
   RTlite -v4 -rescale_BSN -fix_wc_time -unpack_watercol \
       -prefix $RAWDIR/$SUBDIRS/ -suffix .wcd -line $OUTFILE_PREFIX -out merged/$SUBDIRS/WCD_
   moveOverWCinfo -tol 0.002 merged/$SUBDIRS/$OUTFILE_PREFIX.merged merged/$SUBDIRS/WCD_$OUTFILE_PREFIX.merged
   mv merged/$SUBDIRS/WCD_$OUTFILE_PREFIX.watercol merged/$SUBDIRS/$OUTFILE_PREFIX.watercol
   rm merged/$SUBDIRS/WCD_$OUTFILE_PREFIX.*
   ```

> [!WARNING]
> **Linux vs. macOS `stat` Compatibility:**
> Line 145 of `bunravel` uses `stat -f '%z' $FILE` (BSD/macOS `stat` syntax for file size in bytes). On Linux (GNU coreutils), `stat -f` reports filesystem status rather than file size (`stat -c '%s' $FILE` is the GNU equivalent). When running `bunravel` on Linux, replace `stat -f '%z'` with `stat -c '%s'` so `.rawfilesize` comparison works properly.
