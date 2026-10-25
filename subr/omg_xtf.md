---
layout: default
title: omg_xtf
parent: Core Shared Libraries (subr)
module_name: omg_xtf
source_path: code/subr/omg_xtf.c
header_path: code/subr/omg_xtf.h
category: File Formats & Vendor Parsers
related_tools:
  - xtfTool
  - xtf2omg_reson
  - xtf2omg_r2sonic
  - xtf2omg_simrad
  - klein2omg
  - elac2omg
  - xtf2nav
  - xtf2orientation
  - xtf2param
  - extractSnippet
  - extractRI
  - stripSS
---

# omg_xtf

## Overview & Purpose

`omg_xtf` implements reading, writing, peeking, and random-access packet indexing for the Triton Elics International eXtended Triton Format (XTF). Because XTF serves as a multi-vendor container for sidescan, sub-bottom, and multibeam bathymetry (housing native packets from Reson 8100/7125, R2Sonic, Simrad, Elac, Klein, and iXBlue), `omg_xtf` provides both standard XTF packet parsers (file headers, channel descriptors, ping/bathymetry headers, attitude packets, raw serial packets, POS MV raw navigation, Reson navigation, Qinsy multibeam entries, and R2Sonic FTS snippets) and a full-file packet indexer (`XTFFileIndex`) for synchronizing asynchronous sonar and ancillary data streams.

## Key Data Structures, Constants & Macros

### Packet Header Types & Constants
- `FMT_XTF` (`123`), Magic Number `0xFACE` on all data packets.
- Packet Type Identifiers (`MAX_XTF_PACKET_ID` = `255`):
  - `XTF_HEADER_SONAR` (`0`), `XTF_HEADER_NOTES` (`1`), `XTF_HEADER_BATHY` (`2`), `XTF_HEADER_ATTITUDE` (`3`), `XTF_HEADER_FORWARD` (`4`), `XTF_HEADER_ELAC` (`5`), `XTF_HEADER_RAW_SERIAL` (`6`), `XTF_HEADER_EMBED_HEAD` (`7`), `XTF_HEADER_HIDDEN_SONAR` (`8`), `XTF_HEADER_PHASE_RAW_BATHY` (`9`), `XTF_HEADER_PHASE_PROCESSED_BATHY` (`10`), `XTF_HEADER_HIGHSPEED_SENSOR` (`11`), `XTF_HEADER_ECHOSTRENGTH` (`12`), `XTF_HEADER_GEOREC` (`13`), `XTF_HEADER_HYDROSTAR_BATHY` (`16`), `XTF_HEADER_RESON_SNIPPET` (`19`), `XTF_HEADER_Q_MULTIBEAM` (`28`), Reson 7125 bathy/snippets (`61`/`62`), R2Sonic bathy/FTS (`65`/`66`), `XTF_HEADER_RESON_NAVIGATION` (`100`), `XTF_HEADER_POS_RAW_NAVIGATION` (`107`).
- Fixed Structure Sizes: `CHANINFO_SIZE` (`128`), `XTFFILEHEADER_SIZE` (`256` base + $6 \times 128 = 1024$ bytes), `PACKETPEEKER_SIZE` (`14`), `XTFATTITUDEDATA_SIZE` (`64`), `XTFPINGHEADER_SIZE` / `XTFBATHHEADER_SIZE` (`256`), `XTFNOTESHEADER_SIZE` (`256`), `XTFRAWSERIALHEADER_SIZE` (`30`), `XTFPINGCHANHEADER_SIZE` (`64`), `XTFPOSRAWNAVIGATION_SIZE` (`64`), `XTFRESONNAVIGATION_SIZE` (`64`), `XTFHEADERQMBEENTRY_SIZE` (`64`).

### Core Structs
- `CHANINFO`: 128-byte channel descriptor (`TypeOfChannel`, `SubChannelNumber`, `CorrectionFlags`, `UniPolar`, `BytesPerSample`, `ChannelName[16]`, `VoltScale`, `Frequency`, `HorizBeamAngle`, `TiltAngle`, `BeamWidth`, lever arms `OffsetX/Y/Z`, mounting angles `OffsetYaw/Pitch/Roll`, `BeamsPerArray`).
- `XTFFILEHEADER`: 1024-byte file header (`FileFormat`, `SystemType`, `RecordingProgramName`, `RecordingProgramVersion`, `SonarName`, `SonarType`, `NoteString`, `ThisFileName`, `NavUnits`, channel counts, `NavigationLatency`, `NavOffsetY/X/Z/Yaw`, `MRUOffsetY/X/Z/Yaw/Pitch/Roll`, and `CHANINFO ChanInfo[6]`).
- `PACKETPEEKER`: 14-byte lookahead struct (`MagicNumber`, `HeaderType`, `packetSpecificInfoBuffer[7]`, `NumBytesThisRecord`).
- `XTFATTITUDEDATA`: 64-byte high-rate motion packet (`Pitch`, `Roll`, `Heave`, `Yaw`, `TimeTag`, `Heading`).
- `XTFPINGHEADER` / `XTFBATHHEADER`: 256-byte sonar/bathymetry ping header containing timestamp, `PingNumber`, `SoundVelocity`, `OceanTide`, raw/computed CTD fields, 3-axis magnetometer, 6 auxiliary channels, ship speed/gyro/position, towfish speed/KP/position/layback/cable out, sensor depth/altitude/pitch/roll/heading/heave/yaw, and Trackpoint deltas (`FishPositionDeltaX/Y`).
- `XTFPINGCHANHEADER`: 64-byte per-channel header (`ChannelNumber`, `DownsampleMethod`, `SlantRange`, `GroundRange`, `TimeDelay`, `TimeDuration`, `SecondsPerPing`, `ProcessingFlags`, `Frequency`, `InitialGainCode`, `GainCode`, `BandWidth`, contact fields, `NumSamples`, `FixedVSOP`).
- `XTFRAWSERIALHEADER`, `XTFPOSRAWNAVIGATION`, `XTFRESONNAVIGATION`, `XTFHEADERQMBEENTRY`, and `XTFHEADERR2SONICSFTS` (`_H0`, `_SNIPPET`).
- `XTFFileIndex`: Random-access packet index containing `long *frameIndices[MAX_XTF_PACKET_ID]`, where `frameIndices[id][0]` stores the count of packets of type `id` and `frameIndices[id][1..N]` store their byte offsets in the XTF file.

## Public Functions & Signatures

- **Header & Packet I/O (`read*`, `write*`, `print*`)**:
  - `readCHANINFO`, `writeCHANINFO`, `printCHANINFO`
  - `readXTFFILEHEADER`, `writeXTFFILEHEADER`, `printXTFFILEHEADER`
  - `peekPACKETPEEKER`, `printPACKETPEEKER`: Reads 14 bytes to inspect `MagicNumber`, `HeaderType`, and `NumBytesThisRecord`, then rewinds `infile` by 14 bytes.
  - `readXTFATTITUDEDATA`, `printXTFATTITUDEDATA`
  - `readXTFPINGHEADER`, `writeXTFPINGHEADER`, `printXTFPINGHEADER`, `readXTFBATHHEADER`, `printXTFBATHHEADER`
  - `readXTFRAWSERIALHEADER`, `printXTFRAWSERIALHEADER`
  - `readXTFPINGCHANHEADER`, `writeXTFPINGCHANHEADER`, `printXTFPINGCHANHEADER`
  - `readXTFPOSRAWNAVIGATION`, `printXTFPOSRAWNAVIGATION`, `readXTFRESONNAVIGATION`, `printXTFRESONNAVIGATION`, `readXTFHEADERQMBEENTRY`, `printXTFHEADERQMBEENTRY`
  - `initXTFHEADERR2SONICSFTS`, `readXTFHEADERR2SONICSFTS`, `printXTFHEADERR2SONICSFTS`, `readXTFHEADERR2SONICSFTS_H0`, `readXTFHEADERR2SONICSFTS_SNIPPET`
- **File Indexing & Stream Matching**:
  - `XTFFileIndex *buildXTFIndex(FILE *infile)` / `void printXTFIndex(XTFFileIndex *theIndex)` / `void freeXTFIndex(XTFFileIndex *index)`
  - `int writeXTFIndex(XTFFileIndex *index, FILE *outfile)` / `XTFFileIndex *readXTFIndex(FILE *infile)`
  - `unsigned long *matchXTFPackets(XTFFileIndex *theIndex, unsigned long fileSize, int id1, int id2)` & `unsigned int gimme_matching_ss(XTFFileIndex *theIndex, unsigned int bathyCounter, unsigned int lastSS)`
    - Matches packets of type `id1` and `id2` (e.g., bathymetry pings and sidescan/snippet packets) by file offset proximity.

## How It Fits Into the OMG Architecture

`omg_xtf` is the foundation of the entire `code/xtf/` suite (`xtfTool`, `xtf2omg_reson`, `xtf2omg_r2sonic`, `xtf2omg_simrad`, `klein2omg`, `elac2omg`, `xtf2gloria`, `xtf2nav`, `xtf2orientation`, `xtf2param`, `extractSnippet`, `extractRI`, `stripSS`, `getTVG`), as well as `readixBlueXTF` (`code/knudsen/`), `ss2xtf`, `getRESONlatency`, `reson.h`, and `xtf_utils.c`.
