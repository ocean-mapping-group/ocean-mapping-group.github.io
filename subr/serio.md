---
layout: default
title: serio
parent: Core Shared Libraries (subr)
module_name: serio
source_path: code/subr/serio.c
header_path: code/subr/serio.h
category: System, File I/O & String Utilities
related_tools:
  - serio
---

# `serio` — UNIX Terminal / RS-232 Serial Port I/O Wrapper Library

## Overview & Purpose

The `serio` module (`code/subr/serio.c` and `code/subr/serio.h`) provides a low-level UNIX System V `termio` / `ioctl` wrapper library for opening, configuring, reading, writing, and closing RS-232 serial port devices (e.g., `/dev/ttyS*` or `/dev/ttyd*` on SGI IRIX and Linux workstations) used for real-time shipboard sensor and navigation acquisition.

In addition to managing serial line discipline and baud rate configuration (`4800`, `9600`, `19200`, and `38400` baud, 8 data bits, raw non-canonical mode), `serio.h` defines symbolic constants for the complete set of ASCII control characters (`NUL` through `US` and `DEL`) used in NMEA-0183 and binary serial sensor framing protocols.

---

## Key Constants & Global State

### Error & Boolean Constants (`serio.h`)

| Macro | Value | Description |
| :--- | :--- | :--- |
| `NOERROR` | `0` | Operation completed without error |
| `OPENERROR` / `RWERROR` | `-1` | Error opening device or reading/writing byte |
| `IOCTLERROR` | `-2` | Error executing `ioctl(TCSETA)` terminal control call |
| `BOOLEAN`, `FALSE`, `TRUE` | `int`, `0`, `1` | Boolean type and truth constants |
| `DEBUG` | `FALSE` (`0`) | Compile-time diagnostic logging toggle |

### ASCII Control Character Macros (`serio.h`)

Defines standard control codes `0x00`–`0x20` and `DEL`:
- Framing & Handshaking: `NUL` (`0x00`), `SOH` (`0x01`), `STX` (`0x02`), `ETX` (`0x03`), `EOT` (`0x04`), `ENQ` (`0x05`), `ACK` (`0x06`), `NAK` (`0x15`), `SYN` (`0x16`), `ETB` (`0x17`), `CAN` (`0x18`), `ESC` (`0x1B`).
- Separators & Formatting: `BEL` (`0x07`), `BS` (`0x08`), `HT` (`0x09`), `NL` (`0x0A`), `VT` (`0x0B`), `NP` (`0x0C`), `CR` (`0x0D`), `SO` (`0x0E`), `SI` (`0x0F`), `DLE` (`0x10`), `DC1`–`DC4` (`0x11`–`0x14`), `EM` (`0x19`), `SUB` (`0x1A`), `FS` (`0x1C`), `GS` (`0x1D`), `RS` (`0x1E`), `US` (`0x1F`), `SP` (`0x20`), `DEL` (`0x255`).

### Module-Scope State (`serio.c`)

- **`struct termio SPctrl, *SPctrlptr`**: Terminal I/O control structure passed to `ioctl(..., TCSETA, SPctrlptr)`.
- **`FILE *spin, *spout`**: Buffered read (`"r+"`) and write (`"w"`) streams attached to the active serial device.
- **`char *portname`**: Dynamically duplicated string storing the currently open serial device path.
- **`int openstatus`**: Boolean flag preventing multiple simultaneous `ser_open()` calls without an intervening `ser_close()`.

---

## Public Functions & Signatures

### `ser_open`
```c
int ser_open(char *devicename, int baudrate);
```
- **Purpose**: Opens and initializes the serial port device `devicename` at the specified `baudrate` (`4800`, `9600`, `19200`, or `38400`).
- **Configuration**:
  - Sets `c_iflag = 0`, `c_oflag = 0`, `c_lflag = 0`, `c_cc[VMIN] = 0`, and `c_cc[VTIME] = 0` (raw, non-blocking, non-canonical mode).
  - Configures 8-bit characters (`CS8`), receiver enabled (`CREAD`), and local line mode (`CLOCAL`, or `CSTOPB` two stop bits at `4800` baud).
  - Opens `spin` (`fopen(devicename, "r+")`) and `spout` (`fopen(devicename, "w")`) and applies the `termio` settings via `ioctl(fileno(...), TCSETA, SPctrlptr)`.
- **Returns**: `1` on success, `-1` on error (unsupported baud rate, port already open, `fopen` failure, or `ioctl` failure).

### `ser_close`
```c
int ser_close(void);
```
- **Purpose**: Resets the serial line parameters (setting input/output speeds to `0` to trigger hangup, ignoring breaks/parity/carriage returns via `IGNBRK | IGNPAR | IGNCR`), applies `ioctl(..., TCSETA, ...)`, closes `spin` and `spout`, frees `portname`, and resets `openstatus = FALSE`.
- **Returns**: `1` on success, `-1` on `ioctl` error.

### `ser_write`
```c
int ser_write(int c);
```
- **Purpose**: Writes a single byte `c` to the open serial output stream `spout` via `fputc(c, spout)`.

### `ser_read`
```c
int ser_read(void);
```
- **Purpose**: Reads and returns a single byte (`>= 0`) from the open serial input stream `spin` via `fgetc(spin)`, or `-1` (`EOF`) if no data is available.

---

## How It Fits Into the OMG Architecture

- **Real-Time Serial Sensor Acquisition (`subr/serio.c`, `subr/serio.h`)**: Provides the foundational RS-232 serial port interface and ASCII control character definitions (`STX`, `ETX`, `CR`, `NL`, etc.) for legacy real-time shipboard navigation and sensor logging utilities in the OMG software suite.
