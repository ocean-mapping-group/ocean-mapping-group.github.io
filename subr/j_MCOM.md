---
layout: default
title: j_MCOM
parent: Core Shared Libraries (subr)
module_name: j_MCOM
source_path: code/subr/j_MCOM.c
header_path: code/subr/j_MCOM.h
category: "Navigation, Attitude & Sensor Telegram Parsers"
related_tools:
  - readDelHeave
  - j_SUB2K
  - readEA600
  - ek80_parse_proc
---

# `j_MCOM` — CodaOctopus F180 (`MCOM`) Inertial Attitude & Positioning Parser

## Overview & Purpose
The `j_MCOM` module (`code/subr/j_MCOM.c` and `code/subr/j_MCOM.h`) decodes binary `MCOM` real-time motion, attitude, heave, and positioning packets output by the **CodaOctopus F180** series aided inertial navigation systems. Originally written by John Hughes Clarke in February 2003 inside `readDelHeave.c` and refactored into `subr/` in November 2007, this module unpacks 84-byte binary `MCOM` frames—including packed 24-bit signed integer sensor fields and multiplexed status channels—into physical engineering units. It also exports general-purpose 24-to-32-bit sign-extension and binary bit-printing diagnostic utilities used by other binary sonar parsers.

---

## Key Data Structures (`j_MCOM.h`)

### `MCOM_packet` Structure
Represents a fully decoded 84-byte CodaOctopus `MCOM` inertial navigation and attitude frame:
```c
typedef struct {
    char sync[5];                          /* "MCOM\0" header identifier */
    unsigned short millisecs_inMinute;     /* 0..59999 ms within current UTC minute */
    float accelX, accelY, accelZ;          /* 3-axis accelerations (m/s^2) */
    float angrateX, angrateY, angrateZ;    /* 3-axis angular rates (rad/s) */
    unsigned char navstatus;               /* Navigation status byte */
    double latitude, longitude;            /* WGS84 position (decimal degrees) */
    float altitude;                        /* Altitude (m, 1 mm resolution) */
    float NorthVelocity, EastVelocity, DownVelocity; /* 3D velocities (m/s) */
    float heading;                         /* True heading (0..360 deg) */
    float pitch, roll;                     /* Pitch and roll (deg) */
    float onlineHeave;                     /* Real-time online heave (m, 2 mm res) */
    float longperiodHeave;                 /* Delayed/long-period heave (m, 2 mm res) */
    unsigned char cyclicPacketCounter;     /* 0..63 cyclic multiplexer index */
    unsigned char GPSstatusSummary;
    unsigned char StatusChannel[10];       /* 10-byte multiplexed status block */
    char checksum;
    char termCR, termLF;

    /* Derived & Multiplexed Channel 0 / Channel 40 Diagnostics */
    float total_accel, horizontal_accel;
    float vel_SOG, vel_COG;
    int primaryGPSmode, num_Sats;
    char MCOM_version[5];
    unsigned char outputDelay;
    unsigned short longperiodHeaveLatency;
    unsigned short longperiodHeave_filterPeriod;
} MCOM_packet;
```

---

## Public Functions & Signatures

### 1. `MCOM` Packet Decoder
```c
int interpret_MCOM_packet(char *MCOMrawpacket, MCOM_packet *packet);
```
- **Purpose:** Unpacks an 84-byte raw binary `MCOM` buffer (`MCOMrawpacket`) into `packet`.
- **Decoding Details:**
  1. **24-Bit Signed Integer Unpacking:** Body-frame accelerations (`accelX/Y/Z`, scaled by $2 \times 10^{-4}\text{ m/s}^2$), angular rates (`angrateX/Y/Z`, scaled by $10^{-5}\text{ rad/s}$), and 3D velocities (`North/East/DownVelocity`, scaled by $10^{-4}\text{ m/s}$) are stored on wire as 3-byte (24-bit) signed integers. Each 3-byte field is copied into a 32-bit `int` and sign-extended via `switch_24_to32_bit()`.
  2. **64-Bit Radian Position:** Reads 8-byte IEEE doubles for latitude and longitude in radians (byte-swapping via `swap_double()` on big-endian `MOTOROLA` hosts) and converts to decimal degrees via `RAD_TO_DEG`.
  3. **16-Bit Attitude & Heave:** Unpacks 16-bit unsigned heading ($0..2\pi\text{ rad} \to 0..360^\circ$), signed pitch/roll ($10^{-4}\text{ rad}$), and signed `onlineHeave` and `longperiodHeave` ($0.002\text{ m}$ per LSB).
  4. **Multiplexed Status Channels:** Inspects `cyclicPacketCounter`:
     - When `cyclicPacketCounter == 0`, extracts `primaryGPSmode` and `num_Sats` from `StatusChannel`.
     - When `cyclicPacketCounter == 40`, extracts the 4-character `MCOM_version`, `outputDelay`, `longperiodHeaveLatency`, and `longperiodHeave_filterPeriod`.

### 2. 24-Bit Sign Extension & Bit-Printing Utilities
```c
signed int switch_24_to32_bit(signed int anint, int show);
int print8bits(char achar);
int print16bits(short ashort);
int print32bits(int anint);
```
- **`switch_24_to32_bit()`:** Sign-extends a 24-bit two's-complement integer occupying the lower 24 bits of `anint` into a 32-bit signed integer by left-shifting 8 bits and arithmetic-dividing by `256` (`(anint << 8) / 256`).
- **`print8bits()`, `print16bits()`, `print32bits()`:** Print the binary bit representation (`0`/`1`) of 8-, 16-, and 32-bit integers to `stdout` for low-level telemetry debugging.

---

## How It Fits Into the OMG Architecture
- **Delayed Heave & Motion Ingestion (`readDelHeave`, `j_SUB2K`):** Parses logged CodaOctopus F180 `MCOM` files so long-period delayed heave (`longperiodHeave`) and high-rate attitude can be merged into OMG HDCS bathymetry files.
- **Bit-Level Telemetry Diagnostics (`ek80_parse_proc`, `readEA600`):** Reuses `print8bits()`, `print16bits()`, and `print32bits()` when inspecting Simrad transceiver bitmasks.
