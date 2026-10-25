---
layout: default
title: Convert Tools
parent: Sidescan Tools
nav_order: 4
has_children: true
---

# Format Conversion Tools (`sidescan/convert`)

The `convert` directory (`code/sidescan/convert/`) provides format-conversion utilities that translate external agency and commercial sidescan sonar formats into the Ocean Mapping Group's unified 1024-byte JCU GLORIA scanline structure (`gloria_rec`, defined in `jcu_glo.h`). Once converted to `.ss` format, sidescan lines from any sonar can be processed through the standard OMG editing (`azibat/`, `edit/`), slant-range correction (`slant/`), beam removal (`beammap/`), destriping (`destripe/`), and mosaicking (`mapmos/`) pipeline.

## Available Converters

* **[`ios2glo`](ios2glo.md)** — Converts Institute of Oceanographic Sciences (IOS) raw GLORIA format files into JCU GLORIA `.ss` records.
* **[`usgs2glo`](usgs2glo.md)** — Converts United States Geological Survey (USGS) GLORIA sidescan files into JCU GLORIA `.ss` format.
* **[`xsonar2glo`](xsonar2glo.md)** — Converts USGS `xsonar` / `showimage` sidescan files into JCU GLORIA `.ss` records.
* **[`ssi2glo`](ssi2glo.md)** — Converts Soundings / SeaMARC / SSI sidescan records into JCU GLORIA `.ss` format.
* **[`jwn2glo`](jwn2glo.md)** — Converts JWN-formatted sidescan sonar files into JCU GLORIA `.ss` format.
* **[`restructure_glo`](restructure_glo.md)** — Restructures or updates legacy JCU GLORIA header fields and byte alignments to match current `jcu_glo.h` specifications.
* **[`Q-Mips/qmips2glo`](Q-Mips/qmips2glo.md)** — Converts Isis / Q-MIPS digital sidescan sonar files into JCU GLORIA `.ss` records (see [Q-Mips Tools](Q-Mips/index.md)).
* **[`makefile`](makefile.md)** — Build configuration for all format converters in `code/sidescan/convert/`.

## Related Conversion Suites
* For Triton eXtended Triton Format (`.xtf`) sidescan files, see [`xtf/xtf2glo`](../xtf/xtf2glo.md).
