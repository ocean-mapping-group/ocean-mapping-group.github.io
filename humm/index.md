---
layout: default
title: Humminbird Side-Imaging Sonar (humm)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 11
has_children: true
---

# Humminbird 6-Beam Sonar Converter (`humm`)

The `humm` directory contains the ingestion utility for converting serial ASCII logs from 6-beam Humminbird recreational/coastal swath echosounders into the Ocean Mapping Group's binary HDCS format.

---

## Tools in `humm/`

* [`humm2omg`](humm2omg.html) — Parses interleaved ASCII `$GPGGA` NMEA navigation, Trimcube pitch/roll attitude telegrams, and Humminbird 6-beam depth strings ($\pm 25^\circ, \pm 15^\circ, \pm 5^\circ$) into OMG-HDCS `.merged` and `.nav` files.
