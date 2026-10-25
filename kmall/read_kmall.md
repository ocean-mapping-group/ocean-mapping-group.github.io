---
layout: default
title: read_kmall
parent: Kongsberg .kmall & .kmwcd (kmall)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 1
tool_name: read_kmall
source_path: code/kmall/read_kmall.c
category: Raw Data Unraveling
input_formats:
- .kmall
- .kmwcd
output_formats:
- .merged
- .merged.ss_data
- .merged.16_data
- .sectors
- .nav_1
- .nav_2
- .nav_3
- .orientation_1
- .orientation_2
- .net_att_1
- .net_att_2
- .NMEA
- .watercol
- .WC_Phase1
- .WC_Phase2
- .param
- .param_km
- .svp_NNN
- .ssp
- .IOP
- .svTS
related_tools:
- moveOverWCinfo
- mergeAtt
- newMergeAtt
- mergeNav
- getBounds
- makess
- makeWC
- dumpFlags
- RTlite
---

# read_kmall

## Description
`read_kmall` is the primary command-line utility for unpacking ("unraveling") modern Kongsberg Maritime `.kmall` and `.kmwcd` (water column) multibeam sonar files into the OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System) Version 4 format. Originally authored by John Hughes Clarke in May 2018, it replaces `RTlite` (which handles legacy Kongsberg `.all` and `.wcd` telegrams) for newer Kongsberg systems such as the **EM2040 / EM2040C / EM2040P / EM2042**, **EM712**, **EM304**, and **EM124**.

During execution, `read_kmall` scans the raw binary file for `#` datagram headers (`#IIP`, `#IOP`, `#SPO`, `#SKM`, `#SVP`, `#SVT`, `#SHI`, `#SCL`, `#SDE`, `#FCF`, `#MRZ`, `#MWC`, `#CHE`), validates datagram sizes and versions (supporting KMALL Revisions D through H+ automatically via `dgmVersion`), and writes synchronized ping headers, beam records, sidescan snippets, transmit sector metadata, multi-source navigation, serial/network attitude, and water column amplitude/phase structures to up to 21 distinct OMG files.

> [!IMPORTANT]
> When processing a survey line that has a separate `.kmwcd` water column file alongside the `.kmall` file, you **must** run `read_kmall` on the `.kmwcd` file **first**, rename the resulting `.merged` file (e.g., to `justWC_<line>.merged`), run `read_kmall` on the `.kmall` file **second**, and then combine the water column byte offsets into the bathymetric `.merged` file using [`moveOverWCinfo`](../omg/moveOverWCinfo.html). If you run `.kmall` first and `.kmwcd` second on the same `-out` prefix without moving `.merged`, the `.kmwcd` pass will overwrite the bathymetric `.merged` file with empty stub beams!

---

## Usage

```bash
read_kmall [OPTIONS] -in <infile.kmall | infile.kmwcd> -out <outfile_prefix>
```

### Standard Unraveling Examples

**1. Unpacking a single `.kmall` file (with embedded or no water column):**

```bash
read_kmall \
    -doWC \
    -doPhase \
    -in raw/JD100/0001_20240409_120000_Ship.kmall \
    -out merged/JD100/0001_20240409_120000_Ship
```

**2. Unpacking paired `.kmwcd` and `.kmall` files:**

```bash
# Step 1: Unpack the .kmwcd file first to generate .watercol, .WC_Phase1/2, and WC profile offsets
read_kmall -doWC -doPhase \
    -in raw/JD100/0001_line.kmwcd \
    -out merged/JD100/0001_line

# Step 2: Save the temporary WC-only .merged file
mv merged/JD100/0001_line.merged merged/JD100/justWC_0001_line.merged

# Step 3: Unpack the .kmall file to generate bathymetry, snippets, nav, and attitude
read_kmall \
    -in raw/JD100/0001_line.kmall \
    -out merged/JD100/0001_line

# Step 4: Transfer water column byte offsets into the primary .merged file
moveOverWCinfo merged/JD100/0001_line.merged merged/JD100/justWC_0001_line.merged
rm merged/JD100/justWC_0001_line.merged
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <filepath>` | **Required.** Path to the input `.kmall` or `.kmwcd` file. | None |
| `-out <prefix>` | **Required.** Output file path prefix (e.g., `merged/subdir/line_number`). `read_kmall` appends extensions (`.merged`, `.nav_1`, `.net_att_2`, etc.) to this prefix. | None |
| `-doWC` | Unpack `#MWC` (Multibeam Water Column) datagrams and write `<prefix>.watercol`. Output files are only created if `#MWC` datagrams are actually encountered in the input file. | Disabled (`0`) |
| `-doPhase` | Used alongside `-doWC`. Unpacks 8-bit (`phaseFlag == 1`) or 16-bit (`phaseFlag == 2`) water column split-beam phase data into `<prefix>.WC_Phase1` and `<prefix>.WC_Phase2`. | Disabled (`0`) |
| `-betterR0` | Compute profile `range_to_normal_incidence` ($R_0$) using `min_twtt * seabedImageSampleRate` instead of `min_sample_range / 2.0`. | Disabled (`0`) |
| `-hunt_corrupt_MWC` | If a corrupted beam trace is detected inside an `#MWC` datagram, scan forward byte-by-byte within the datagram to recover plausible subsequent beam headers rather than dropping the rest of the ping. | Disabled (`0`) |
| `-isRevH` | **Deprecated / No-op.** Previously used to add byte offsets for Kongsberg KMALL Rev H datagrams. Now prints `-- Yo -isRevH is retired no longer needed` because `read_kmall` automatically inspects `header.dgmVersion >= 1`. Safe to leave in existing scripts. | `0` |
| `-v` | Enable verbose diagnostic output for every datagram, sector, and beam unpacked. | Disabled (`0`) |
| `-notquiet` | Disable quiet mode; prints 2-character datagram progress codes (`IN-`, `RT-`, `PO-`, `BN-`, `VP-`, `VT-`, `DE-`, `WC-`) to stdout. | Quiet (`1`) |
| `-check` | Print a validation line (`VALID DGM --#MRZ-- numBytes ...`) for every recognized datagram header. | Disabled (`0`) |
| `-sector_debug` | Print detailed transmit sector parameters (`centreFreq_Hz`, `signalBandWidth_Hz`, `totalSignalLength_sec`, `effectiveSignalLength_sec`, `tiltAngleReTx_deg`) for every `#MRZ` ping. | Disabled (`0`) |
| `-debug_Cnt` | Print ping counter, swath index, and file byte offset for every `#MRZ` datagram, and warn on backward ping number jumps (`BACK ping jump of N pings`). | Disabled (`0`) |
| `-debug_PNSWRX` | Write ping number, Rx fan index, swath along-position, and file percentage to `debug_MWC.txt` and `debug_MRZ.txt` in the current working directory to diagnose dropped or out-of-order pings/swaths. | Disabled (`0`) |
| `-debug_TAGS64` | Detect network transfer corruption (large blocks of contiguous null `0x00` bytes in `.kmwcd` files, first observed on USNS Heezen TAGS-64). If 10 MB (`10,000,000` contiguous 20-byte reads) of zeroes are encountered, writes `<infile>.ABORT` and exits with `-1`. | Disabled (`0`) |

---

## Supported Echo Sounders & Tool Types

`read_kmall` validates `emdgmhead->echoSounderID` in every datagram header and maps it to the internal OMG-HDCS `toolType` and maximum beam slots (`summary.numDepths`):

| Kongsberg `echoSounderID` | Sonar System | Internal OMG `toolType` | Initial `numDepths` (MWC / MRZ) |
|---|---|---|---|
| `2040` | EM2040 / EM2040P | `EM2040` | 400 (or `rxInfo.numSoundingsMaxMain`) |
| `2042` | EM2042 | `EM2040` | 400 (or `rxInfo.numSoundingsMaxMain`) |
| `2045` | EM2040C | `EM2040` | 400 (or `rxInfo.numSoundingsMaxMain`) |
| `712` | EM712 | `EM710` | 400 (or `rxInfo.numSoundingsMaxMain`) |
| `304` | EM304 | `EM302` | 800 (or `rxInfo.numSoundingsMaxMain`) |
| `124` | EM124 | `EM122` | 800 (or `rxInfo.numSoundingsMaxMain`) |

> [!WARNING]
> If a `.kmall` file contains any other `echoSounderID`, `read_kmall` will print `invalid datagram echosSounder_ID!! -- <ID>` or terminate with `HeyA - never head of this echosounder ID`.

---

## Output Files & File Handle Mapping

`read_kmall` opens an array of 21 file pointers (`omgfile[0..20]`) using `<outfile_prefix>` as the base name:

| Internal Handle | Output Filename | Source Datagram | Description |
|---|---|---|---|
| `omgfile[0]` | `<prefix>.merged` | `#MRZ` / `#MWC` | Primary OMG-HDCS v4 bathymetry & profile header file. |
| `omgfile[1]` | `<prefix>.merged.ss_data` | `#MRZ` | 8-bit seabed image (snippet) trace amplitudes compressed to 0.5 dB resolution (`SIsample_desidB / 5`). |
| `omgfile[2]` | `<prefix>.merged.16_data` | `#MRZ` | 16-bit seabed image (snippet) trace amplitudes in 0.1 dB resolution (`SIsample_desidB`). |
| `omgfile[3]` | `<prefix>.sectors` | `#MRZ` | Binary transmit sector records (24 bytes per sector: tilt angle, focus range, signal length, delay, frequency, bandwidth, waveform). |
| `omgfile[4]` | `<prefix>.nav_1` | `#SPO` (`sensorSystem == 0`) | Primary binary navigation file (`jcu_nav_rec`, 48 bytes/record). |
| `omgfile[19]` | `<prefix>.nav_2` | `#SPO` (`sensorSystem == 1`) | Secondary binary navigation file. |
| `omgfile[20]` | `<prefix>.nav_3` | `#SPO` (`sensorSystem == 2`) | Tertiary binary navigation file. |
| `omgfile[5]` | `<prefix>.orientation_1` | `#SKM` (`sensorInputFormat == 2`) | Serial EM3000-format attitude file (`OMG_HDCS_attitude`). |
| `omgfile[8]` | `<prefix>.orientation_2` | `#SKM` | Reserved secondary serial orientation file. |
| `omgfile[9]` | `<prefix>.net_att_1` | `#SKM` (`sensorInputFormat == 7`) | Network attitude from POS M/V GRP 102/103 (`OMG_HDCS_attitude`). |
| `omgfile[10]` | `<prefix>.net_att_2` | `#SKM` (`sensorInputFormat == 1`) | Network attitude from KM Binary Sensor Input (`OMG_HDCS_attitude`). |
| `omgfile[6]` | `<prefix>.NMEA` | `#SPO` | Raw ASCII NMEA strings extracted from position datagrams. |
| `omgfile[7]` | `<prefix>.watercol` | `#MWC` | Binary water column amplitude data (created only if `-doWC` is set and `#MWC` is present). |
| `omgfile[11]` | `<prefix>.WC_Phase1` | `#MWC` | 8-bit water column phase data (created only if `-doPhase` is set and `#MWC` is present). |
| `omgfile[12]` | `<prefix>.WC_Phase2` | `#MWC` | Secondary water column phase file handle. |
| `omgfile[13]` | `<prefix>.param` | `#IIP` | Parsed OMG lever-arm and installation parameter file (`WLZ`, `S1X..S1R`, `S2X..S2R`, `S3X..S3R`). |
| `omgfile[14]` | `<prefix>.param_km` | `#IIP` | Verbatim ASCII dump of the Kongsberg `#IIP` installation parameter text. |
| `omgfile[15]` | `<prefix>.svp_001`, `.svp_002`... | `#SVP` | Sound Velocity Profiles written in OMG `watercolumn` format as each `#SVP` datagram arrives. |
| `omgfile[16]` | `<prefix>.ssp` | `#SVT` + `#SPO` | ASCII surface sound speed track (`lat lon soundVelocity_mPerSec`). |
| `omgfile[17]` | `<prefix>.IOP` | `#IOP` | Verbatim ASCII dump of the Kongsberg `#IOP` runtime parameter datagram. |
| `omgfile[18]` | `<prefix>.svTS` | `#SVT` + `#SPO` | ASCII surface sound velocity time series (`datestring dtime lat lon SV temp_C salinity`). Note: If salinity is missing (`<0` or `>50`) but SV and Temperature are valid, `read_kmall` inverts the Chen & Millero equation via bisection to estimate salinity! |

---

## Crucial Downstream Workflow Requirements

Because `read_kmall` separates multi-sensor navigation and attitude streams into numbered files, **downstream OMG tools (`mergeAtt`, `mergeNav`) will fail or use empty files unless you copy your chosen source to `.nav` and `.orientation`**:

1. **Navigation Selection:**
   `read_kmall` writes position fixes to `.nav_1`, `.nav_2`, and `.nav_3` (corresponding to `#SPO` `sensorSystem` 0, 1, and 2), but does **not** create `<prefix>.nav`. Before running `mergeNav` or `appendNav`, copy the active navigation source to `.nav`:

   ```bash
   cp merged/JD100/line.nav_1 merged/JD100/line.nav
   ```

2. **Attitude Selection (`orientation_1` vs `net_att_1` vs `net_att_2`):**
   `read_kmall` routes `#SKM` attitude records based on `infoPart.sensorInputFormat`:
   * Format `1` (KM Binary Sensor Input) $\rightarrow$ `.net_att_2`
   * Format `2` (EM3000 Serial) $\rightarrow$ `.orientation_1`
   * Format `7` (POS M/V GRP 102/103 Network) $\rightarrow$ `.net_att_1`
   
   Before running `mergeAtt`, check which file is non-empty (`ls -l <prefix>.*att* <prefix>.orientation*`) and copy it to `<prefix>.orientation`:

   ```bash
   cp merged/JD100/line.net_att_2 merged/JD100/line.orientation
   mergeAtt merged/JD100/line
   ```

---

## Troubleshooting & Diagnostic Messages

| Message / Symptom | Cause | Resolution |
|---|---|---|
| `whoa.... unsupported SKM input sensor format <N>` | The `#SKM` datagram uses a `sensorInputFormat` other than `1` (KM binary), `2` (EM3000), or `7` (POS MV GRP 102/103), such as `3` (Sagem) or `4/5/6` (Seapath binary 11/23/26). | Update `write_out_KMall_SKM()` in `code/kmall/read_kmall.c` (around line 736) to map format `<N>` to an output file handle, or re-export with KM Binary format. |
| `CAREFUL!!!! - more than one Datagram per MWC (X of Y) -- Aborting....` | An `#MWC` water column ping was partitioned across multiple datagrams (`numOfDgms > 1`). | Currently `unpack_KMALL_MWC()` only unpacks single-partition `#MWC` datagrams and skips partitioned ones. |
| `Yo- bad MWC trace ping ... dodgy value#` | Corrupted beam header inside an `#MWC` water column datagram (sector $>9$, pointing angle outside $\pm 90^\circ$, or sample count out of bounds). | Re-run `read_kmall` with `-hunt_corrupt_MWC` to scan byte-by-byte for valid subsequent beam traces. |
| `invalid KMWCD datagram size!! -- <N> (max allowed 6000000)` | A water column datagram exceeded `MAX_KMWCD` (6 MB) or header alignment was lost. | `read_kmall` automatically seeks back 19 bytes and scans for the next `#` header. If `.kmwcd` is padded with zeroes from a network drop, run with `-debug_TAGS64`. |
| `.merged` file has 0 bathymetry soundings after unraveling `.kmall` and `.kmwcd` | `read_kmall` was run on `.kmall` first and `.kmwcd` second using the same `-out` prefix, overwriting `.merged` with water-column-only profile headers. | Always unravel `.kmwcd` first, move `<prefix>.merged` to `justWC_<prefix>.merged`, unravel `.kmall` second, and run `moveOverWCinfo`. |
