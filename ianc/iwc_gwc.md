---
layout: default
title: iwc_gwc
parent: Ian Church — Hydrodynamic & 3D Ray-Trace Suite (ianc)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 11
tool_name: iwc_gwc
source_path: code/ianc/subr/iwc_gwc.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats:
- Generic Water Column Binary Format (.gwc)
output_formats:
- In-memory GWC packet structs (GWC_FileHeader, GWC_WaterColumnPacket, etc.)
related_tools:
- iwc_water
- iwc_support
- oceanReader
---

# iwc_gwc

## Description

`iwc_gwc` (`code/ianc/subr/iwc_gwc.c` and `code/ianc/subr/iwc_gwc.h`) is a binary parser library written by Ian Church in April 2016 for reading **Generic Water Column (`.gwc`)** acoustic water-column files (used by QPS FMMidwater / Qimera and CARIS water-column workflows). The module defines the complete set of binary packet structures, packet type identifiers (`110`–`115`), sample data type enumerations (`INT8` through `FLOAT64`), and file-stream reader functions required to decode `.gwc` headers, multibeam water-column acoustic backscatter packets, beam geometry arrays, transmit sector metadata, vessel installation lever arms, sound speed profiles, tidal records, and source/navigation file descriptors.

## Public API & Usage

### Header Include

```c
#include "j_watercolumn.h"
#include "iwc_gwc.h"
```

### Example C Usage

```c
FILE *gwcFile = fopen("survey_line01.gwc", "rb");
GWC_FileHeader fHeader;
GWC_PacketHeader pHeader;

getGWCHeader(gwcFile, &fHeader);

while (!feof(gwcFile)) {
    getGWCPacketHeader(gwcFile, &pHeader);
    if (pHeader.packetID == GWC_WatercolumnPacket) {
        GWC_WaterColumnPacket wcPacket;
        wcPacket.packHeader = pHeader;
        getGWCWaterColumnPacket(gwcFile, &wcPacket, fHeader.sampleType);
        /* Process wcPacket.wcHeader, wcPacket.beamInfo, and wcPacket.sampleData */
    } else if (pHeader.packetID == GWC_SoundSpeedProfile) {
        GWC_SoundSpeed ssp;
        getGWCSoundSpeed(gwcFile, &ssp);
    }
}
```

## Constants & Macros

### Header & Block Byte Sizes
* `GWC_FILE_HEADER_SIZE` (`128`), `GWC_NAV_FILE_INFO` (`644`), `GWC_PACKET_SIZE` (`24`), `GWC_WC_SIZE` (`260`), `GWC_CAL_SIZE` (`64`), `GWC_INSTALL_SIZE` (`260`).

### Packet Type Identifiers (`packetID`)
* `GWC_WatercolumnPacket` (`110`): Multibeam acoustic water-column ping data.
* `GWC_InstallationParameters` (`111`): Transducer, motion sensor, and GNSS lever-arm offsets and time delays.
* `GWC_SourceFileInfo` (`112`): Original raw sonar filename and source ID (`sourceFile[512]`).
* `GWC_SoundSpeedProfile` (`113`): Embedded water-column sound velocity profile (`depth`, `speed` arrays).
* `GWC_TideInfo` (`114`): Embedded tidal height time series (`time`, `tide` in centimeters).
* `GWC_NavFileInfo` (`115`): Associated navigation file path (`navFilePath[512]`).

### Sample Data Types (`sampleType`)
* `GWC_INVALID_TYPE` (`0`), `GWC_INT8_TYPE` (`2`, 1B), `GWC_INT16_TYPE` (`3`, 2B), `GWC_INT32_TYPE` (`4`, 4B), `GWC_INT64_TYPE` (`5`, 8B), `GWC_UINT8_TYPE` (`6`, 1B), `GWC_UINT16_TYPE` (`7`, 2B), `GWC_UINT32_TYPE` (`8`, 4B), `GWC_UINT64_TYPE` (`9`, 8B), `GWC_FLOAT32_TYPE` (`10`, 4B), `GWC_FLOAT64_TYPE` (`11`, 8B).

## Data Structures & Public Functions

### Key Structures (`iwc_gwc.h`)

| Structure | Key Members | Description |
| :--- | :--- | :--- |
| `GWC_FileHeader` | `marker`, `revision`, `sampleType`, `minVal`, `maxVal`, `maxSamples`, `sourceFile`, `maxRange`, `maxNadirRange`, `minTXDepth`, `maxTXDepth`, `reserved[76]` | 128-byte master file header at byte offset `0`. |
| `GWC_PacketHeader` | `marker`, `numBytes`, `revision`, `packetID`, `timeTag` | 24-byte header prefixing every packet in the `.gwc` stream. |
| `GWC_WaterColumnHeader` | `sonarHints`, `navType`, `utmZone`, `posX`, `posY`, `posZ`, `txDepth`, `pitch`, `roll`, `heading`, `heave`, `CMG`, `numBeams`, `numSamples`, `downSampleFactor`, `sampleInterval`, `soundVel`, `timeDelay`, `nadirDepth`, `pingNum`, `transID`, `tvg`, `tvgOffset` | Ping-level navigation, attitude, sampling geometry, and TVG metadata (`236` bytes following `GWC_PacketHeader`). |
| `GWC_CalibrationData` & `GWC_calBlock` | `numBeams`, `size`, `txPower`, `absCoeff`, `txGain`, `freq`, `pulseLen`, `equivBeamAngle`, `saCorr`, `spreading`, `beamWidthVert`, `beamWidthHori` | Per-beam radiometric and acoustic calibration parameters. |
| `GWC_BeamInformation` | `BeamSize`, `*sampleCount`, `*beamElev`, `*beamAzi`, `*beamWidth`, `*bottomTime`, `*sector` | Dynamically allocated arrays of length `numBeams` describing beam pointing angles and bottom detection two-way travel times. |
| `GWC_SectorInformation` & `GWC_Sector` | `numSect`, `size`, `sectNum`, `sigWave`, `tiltAngle`, `txTimeOffset`, `centerFreq`, `bandwidth`, `focusRange`, `sigLength`, `absCoeff` | Transmit sector waveform and steering geometry. |
| `GWC_WaterColumnPacket` | `packHeader`, `wcHeader`, `calData`, `beamInfo`, `sectInfo`, `*sampleData` | Composite structure holding an entire decoded water-column ping (`110`) and its raw backscatter amplitude array. |
| `GWC_Installation` | `validityMask`, `transOneLinearOffset[3]`, `transOneAngularOffset[3]`, `transTwo*`, `positionLinearOffset[3]`, `motionLinearOffset[3]`, `motionAngularOffset[3]`, `positionTimeDelay`, `motionTimeDelay`, `gyroOffset`, `waterLineOffset`, `sonarID` | Vessel survey configuration and sensor lever-arm offsets (`111`). |
| `GWC_SourceFile`, `GWC_SoundSpeed`, `GWC_Tide`, `GWC_NavInfo` | Packet-specific fields and dynamic arrays (`*depth`, `*speed`, `*time`, `*tide`) | Auxiliary metadata packets (`112`, `113`, `114`, `115`). |

### Reader Functions (`iwc_gwc.c`)

| Function | Signature | Description |
| :--- | :--- | :--- |
| `getGWCHeader` | `void getGWCHeader(FILE *infile, GWC_FileHeader *fHeader)` | Reads the 128-byte `GWC_FileHeader` and advances the file pointer by `GWC_FILE_HEADER_SIZE`. |
| `getGWCPacketHeader` | `void getGWCPacketHeader(FILE *infile, GWC_PacketHeader *pHeader)` | Reads the 24-byte `GWC_PacketHeader` (`marker`, `numBytes`, `revision`, `packetID`, `timeTag`). |
| `getGWCWaterColumnHeader` | `void getGWCWaterColumnHeader(FILE *infile, GWC_WaterColumnHeader *wcHeader)` | Reads the ping navigation, attitude, and acoustic sampling parameters. |
| `getGWCCalibrationData` | `void getGWCCalibrationData(FILE *infile, GWC_CalibrationData *calData)` | Allocates and reads `numBeams` `GWC_calBlock` records. |
| `getGWCBeamInfo` | `void getGWCBeamInfo(FILE *infile, GWC_BeamInformation *beamData, unsigned short numBeams)` | Allocates and populates per-beam `sampleCount`, `beamElev`, `beamAzi`, `beamWidth`, `bottomTime`, and `sector` arrays. |
| `getGWCSectorInformation` | `void getGWCSectorInformation(FILE *infile, GWC_SectorInformation *sectInfo)` | Allocates and reads transmit sector records (`GWC_Sector`). |
| `getGWCWaterColumnPacket` | `void getGWCWaterColumnPacket(FILE *infile, GWC_WaterColumnPacket *wcPacket, unsigned int sampleType)` | Orchestrates reading the full water-column packet (`wcHeader`, `calData`, `beamInfo`, `sectInfo`) and allocates/reads `numBeams * numSamples * byteCount` bytes into `wcPacket->sampleData`. |
| `getGWCInstallation` | `void getGWCInstallation(FILE *infile, GWC_Installation *install)` | Reads packet `111` installation offsets and time delays. |
| `getGWCSourceFile` | `void getGWCSourceFile(FILE *infile, GWC_SourceFile *sourceData)` | Reads packet `112` source ID and 512-byte filename string. |
| `getGWCSoundSpeed` | `void getGWCSoundSpeed(FILE *infile, GWC_SoundSpeed *sspData)` | Reads packet `113` header and dynamically allocates/reads `sampleCount` pairs of `(depth[i], speed[i])`. |
| `getGWCTide` | `void getGWCTide(FILE *infile, GWC_Tide *tideData)` | Reads packet `114` header and dynamically allocates/reads `sampleCount` pairs of `(time[i], tide[i])`. |
| `getGWCNavInfo` | `void getGWCNavInfo(FILE *infile, GWC_NavInfo *navInfo)` | Reads packet `115` navigation ID and 512-byte `navFilePath`. |

## How It Works

1. **Sequential Packet Framing**: A `.gwc` file begins with a fixed 128-byte `GWC_FileHeader` read via `getGWCHeader()`, followed by a sequence of self-describing packets. Each packet starts with a 24-byte `GWC_PacketHeader` containing `packetID` (`110`–`115`), `numBytes`, and UTC `timeTag`.
2. **Dynamic Sub-Block Allocation**: For variable-length packets (`GWC_WatercolumnPacket`, `GWC_SoundSpeedProfile`, `GWC_TideInfo`), the reader functions inspect the count fields (`numBeams`, `numSamples`, `numSect`, `sampleCount`), dynamically `malloc()` the exact array sizes required, and read the binary arrays sequentially using `fread()`.
3. **Sample Width Resolution**: In `getGWCWaterColumnPacket()`, a `switch(sampleType)` block maps the GWC data type (`GWC_INT8_TYPE` through `GWC_FLOAT64_TYPE`) to its byte width (`byteCount = 1, 2, 4, or 8`) to allocate and read the 2D beam-by-sample acoustic amplitude matrix.
