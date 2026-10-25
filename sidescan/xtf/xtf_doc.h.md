---
layout: default
title: xtf_doc.h
parent: XTF Tools
grand_parent: Sidescan Tools
nav_order: 10
tool_name: xtf_doc.h
source_path: code/sidescan/xtf/xtf_doc.h
category: XTF Sidescan Conversion
input_formats: ["C Header File (Triton XTF Rev 3 Specification)"]
output_formats: ["Included by xtf2glo.c, xtf_funcs.c, chxtfhdr.c"]
related_tools: ["xtf2glo", "chxtfhdr.h", "xtf_funcs.h", "new_xtf.h"]
---

# xtf_doc.h

## Description
`xtf_doc.h` is the official Triton Elics International eXtended Triton Format (`.XTF`, Revision 3, September 18, 1998, by Markespflug) C header specification included in `code/sidescan/xtf/`. It documents the binary structure of `.XTF` files and defines all packet type IDs, sonar family enumerations, and C data structures used by [`xtf2glo`](xtf2glo.md).

## Packet Header Type IDs (`HeaderType`)
Every packet in an `.XTF` data stream begins with magic number `0xFACE` (`64206`) followed by a `HeaderType` byte:
* `XTF_HEADER_SONAR` (`0`) — Sidescan and subbottom ping data (`XTFPINGHEADER` + `XTFPINGCHANHEADER`s).
* `XTF_HEADER_NOTES` (`1`) — Annotation text (`XTFNOTESHEADER`).
* `XTF_HEADER_BATHY` (`2`) — Multibeam bathymetry (`Seabat`, `Odom`).
* `XTF_HEADER_ATTITUDE` (`3`) — TSS or MRU high-rate pitch/roll/heave/yaw (`XTFATTITUDEDATA`).
* `XTF_HEADER_FORWARD` (`4`) — Forward-look sonar packet.
* `XTF_HEADER_ELAC` (`5`) — Elac multibeam packet.
* `XTF_HEADER_RAW_SERIAL` (`6`) — Raw ASCII serial string (`XTFRAWSERIALHEADER`).
* `XTF_HEADER_EMBED_HEAD` (`7`) — Embedded 1024-byte file header inside a mid-stream file split.

## Core Data Structures Defined
1. **`XTFFILEHEADER` (1024 bytes)**: File-level metadata (`FileFormat = 123`, `SystemType = 1`, `RecordingProgramName`, `NumberOfSonarChannels`, `NumberOfBathymetryChannels`, projection parameters, and up to six 128-byte `CHANINFO` descriptors).
2. **`CHANINFO` (128 bytes)**: Per-channel configuration (`TypeOfChannel`: `0=SUBBOTTOM`, `1=PORT`, `2=STBD`, `3=BATHYMETRY`; `BytesPerSample`: `1` or `2`; `SamplesPerChannel`; `VoltScale`; beamwidth and tilt angles).
3. **`XTFPINGHEADER` (256 bytes)**: Per-ping navigation, timestamp (`Year..HSeconds`), `EventNumber`, `PingNumber`, `SoundVelocity`, towfish (`SensorXcoordinate`, `SensorYcoordinate`, `SensorDepth`, `SensorPrimaryAltitude`, `SensorPitch`, `SensorRoll`, `SensorHeading`) and ship (`ShipXcoordinate`, `ShipYcoordinate`, `ShipGyro`, `ShipSpeed`, `Layback`, `CableOut`) telemetry.
4. **`XTFPINGCHANHEADER` (64 bytes)**: Per-channel ping header (`ChannelNumber`, `DownsampleMethod`, `SlantRange`, `TimeDelay`, `TimeDuration`, `SecondsPerPing`, `NumSamples`, `Weight`), immediately followed by the raw `NumSamples × BytesPerSample` acoustic trace.
