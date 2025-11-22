---
layout: default
title: bytes2func
parent: XTF Tools
grand_parent: sidescan
nav_order: 1
---
# bytes2func

## Description
`bytes2func` is a C utility library providing functions to convert sequences of bytes (raw binary data) into standard C data types: `short`, `int`, `float`, and `double`. A key feature of these functions is their ability to handle endianness differences, allowing for correct interpretation of binary data regardless of whether it originated from a little-endian or big-endian system. This library is crucial for parsing proprietary binary file formats like XTF, which may have specific byte ordering.

## Functions

### `short bytes2short(char *data, int SWAP)`
Converts two bytes from the `data` pointer into a `short` integer.
*   `data`: Pointer to the two bytes to convert.
*   `SWAP`: If non-zero, performs a byte swap (reverses byte order) during conversion.

### `int bytes2int(char *data, int SWAP)`
Converts four bytes from the `data` pointer into an `int` integer.
*   `data`: Pointer to the four bytes to convert.
*   `SWAP`: If non-zero, performs a byte swap.

### `float bytes2float(char *data, int SWAP)`
Converts four bytes from the `data` pointer into a `float` floating-point number.
*   `data`: Pointer to the four bytes to convert.
*   `SWAP`: If non-zero, performs a byte swap.

### `double bytes2double(char *data, int SWAP)`
Converts eight bytes from the `data` pointer into a `double` floating-point number.
*   `data`: Pointer to the eight bytes to convert.
*   `SWAP`: If non-zero, performs a byte swap.

## How It Works
Each function uses a `union` to overlay a data type (e.g., `short`, `int`, `float`, `double`) with an array of `unsigned char`. This allows direct manipulation of the underlying bytes.
*   **No Swap (`!SWAP`):** If `SWAP` is 0, bytes are copied directly from the input `data` pointer to the `unsigned char` array of the `union` in their natural order. The `val` member of the `union` then holds the correctly interpreted value for the current system's endianness.
*   **Byte Swap (`SWAP`):** If `SWAP` is non-zero, the bytes are copied in reverse order (e.g., for a 4-byte `int`, `data[0]` goes to `equiv.one[3]`, `data[1]` to `equiv.one[2]`, and so on). This effectively reverses the endianness of the incoming data to match the current system's, ensuring correct interpretation.
