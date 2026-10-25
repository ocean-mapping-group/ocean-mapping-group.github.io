---
layout: default
title: labs (Teaching & Coursework Labs)
has_children: true
nav_order: 28
---

# Teaching & Coursework Labs (`labs`)

The `labs/` (`code/labs/`) directory contains educational C programs and student laboratory templates written by John Hughes Clarke (2000–2001) for Ocean Mapping Group (OMG) graduate and undergraduate hydrographic acoustic courses (such as GEOD/GGE 5042 / 3353 at the University of New Brunswick). These standalone programs introduce students to three foundational pillars of multibeam and sidescan sonar engineering:

1. **Binary Sonar Telegram Unpacking & Byte-Order Handling (`EM_unpack`):** Scanning raw Kongsberg Simrad EM3000 `.all` byte streams for Start-of-Transmission (`STX = 0x02`) markers, validating 32-bit length prefixes, swapping little-endian/big-endian fields (`swap_short`, `swap_int`), and decoding common datagram headers (`model_no`, `ymd`, `mdnt_time`).
2. **Time-Domain Pulse Convolution (`example`):** Reading ASCII transmit pulse waveforms and seabed/target impulse response time series, applying discrete time-domain convolution (`doconv`), and exporting the convolved echo trace for visualization.
3. **Transducer Array Beam Pattern Synthesis (`mkbp` & `mkbp_skeleton`):** Computing far-field acoustic pressure, intensity, and logarithmic directivity ($10\log_{10}I$) across $\theta \in [-90^\circ, +90^\circ]$ in $0.1^\circ$ increments for circular planar pistons (first-order Bessel function $J_1$), continuous line arrays ($\text{sinc}$ function), and shaded discrete multi-element line arrays using complex phasor summation and the Array Product Theorem.

---

## Tool Index

| Tool | Source File | Description |
| :--- | :--- | :--- |
| **[`EM_unpack`](EM_unpack.md)** | `code/labs/EM_unpack.c` | Educational parser for Kongsberg Simrad EM3000 binary `.all` telegram files; scans for `EM_STX` (`0x02`), validates record lengths, performs optional 16/32-bit endian swapping (`-swap`), and decodes Nav (`0x50`), Image (`0x53`), Raw Time & Angle (`0x46`), and Depth (`0x44`) telegram headers. |
| **[`example`](example.md)** | `code/labs/example.c` | Laboratory template for discrete time-domain acoustic convolution; reads two-column ASCII transmit pulse (`-pulse`) and target impulse response (`-impul`) files and provides the `doconv()` framework for convolving sonar waveforms. |
| **[`mkbp`](mkbp.md)** | `code/labs/mkbp.c` | Reference solution for interactive acoustic transducer beam pattern modeling; computes normalized far-field pressure, intensity, and directivity across 1,800 angular bins ($-90^\circ$ to $+90^\circ$) for circular planar pistons, continuous line arrays, and shaded discrete line arrays. |
| **[`mkbp_skeleton`](mkbp_skeleton.md)** | `code/labs/mkbp_skeleton.c` | Student assignment skeleton for `mkbp`; provides the complete CLI argument parser, interactive array geometry prompts, normalization loop, and ASCII file output while leaving the analytical circular piston, continuous line, and discrete phasor summation formulas as student exercises. |

---

## Pedagogical & Architectural Context

Within the broader OMG software ecosystem, the programs in `code/labs/` serve as simplified, self-contained counterparts to production libraries and utilities:

* **`EM_unpack.c`** introduces the exact Kongsberg Simrad `.all` binary framing and endianness logic used in production unravelers such as [`unravel`](../omg/unravel.md) and [`read_kmall`](../kmall/read_kmall.md), without requiring students to link against the full `liblocal.a` or `swapio.h` infrastructure (`cc EM_unpack.c -o EM_unpack -lm`).
* **`example.c`** pairs directly with [`testChirp`](../tests/testChirp.md) (`code/tests/testChirp.c`), which generates synthetic `pulse.ascii` and `impulse.ascii` files for students to convolve and inspect.
* **`mkbp.c`** and **`mkbp_skeleton.c`** provide the command-line mathematical foundation for the interactive X11/Motif beam-forming and array shading demonstration tool [`bpdemo`](../bpdemo/bpdemo.md) (`code/bpdemo/bpdemo.c`).
